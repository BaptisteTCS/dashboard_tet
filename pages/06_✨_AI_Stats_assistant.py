import streamlit as st
from openai import OpenAI
from utils.db_text import tables_text, relations_text
from utils.db import get_engine_prod, get_engine
import pandas as pd
from sqlalchemy import text
import re
import json
from datetime import datetime

st.set_page_config(layout="wide", page_title="SQL AI Assistant", page_icon="✨")


# === FONCTIONS DE LOGGING ===
@st.cache_resource(show_spinner=False)

def log_ai_answer(question: str, sql: str, reponse: dict):
    """Enregistre une réponse de l'IA dans la base de données"""
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(
                text("""
                    INSERT INTO ai_answers (question, sql, reponse, created_at)
                    VALUES (:question, :sql, :reponse, :created_at)
                """),
                {
                    "question": question,
                    "sql": sql,
                    "reponse": json.dumps(reponse, ensure_ascii=False, default=str),
                    "created_at": datetime.now()
                }
            )
            conn.commit()
    except Exception as e:
        # On ne veut pas bloquer l'utilisateur si le logging échoue
        st.warning(f"⚠️ Impossible d'enregistrer la requête : {e}")


# Initialisation de l'historique de session
if "messages" not in st.session_state:
    st.session_state.messages = []

# En-tête minimaliste
st.markdown("""
<div style='text-align: center; padding: 1rem 0 2rem 0;'>
    <h1 style='font-size: 2.5rem; margin-bottom: 0.5rem;'>✨ SQL AI Assistant</h1>
    <p style='color: #666; font-size: 1rem;'>Posez votre question en langage naturel</p>
</div>
""", unsafe_allow_html=True)

# Affichage de l'historique des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.markdown(message["content"])
        else:
            # Affichage de la requête SQL
            st.markdown("**📝 Requête SQL**")
            st.code(message["sql_query"], language="sql")
            
            # Affichage des résultats
            if "error" in message:
                st.error(message["error"])
            elif "warning" in message:
                st.warning(message["warning"])
            else:
                st.markdown("**✅ Résultats**")
                if message["row_count"] == 0:
                    st.info("Aucun résultat trouvé")
                else:
                    st.caption(f"{message['row_count']} ligne(s)")
                    st.dataframe(message["dataframe"], width='stretch')

# Zone de saisie en bas (style chat)
user_request = st.chat_input("Ex: Affiche-moi toutes les collectivités qui ont crée un PCAET en 2024")

# === TRAITEMENT DE LA REQUÊTE ===
if user_request:
    # Ajouter le message utilisateur à l'historique
    st.session_state.messages.append({"role": "user", "content": user_request})
    
    # Afficher le message utilisateur
    with st.chat_message("user"):
        st.markdown(user_request)
    
    # Générer et afficher la réponse de l'assistant
    with st.chat_message("assistant"):
        with st.spinner("Génération de la requête..."):
            try:
                # Configuration du modèle
                model = "gpt-5"
                max_output_tokens = 50000
                
                # Construction du prompt
                prompt = f"""
                Tu es un assistant SQL expert PostgreSQL.

                Ta mission est de produire la requête SQL la plus pertinente possible
                en te basant sur le schéma de base de données et la question utilisateur ci-dessous.

                ### Contexte de la base :
                {tables_text}

                ### Relations entre les tables :
                {relations_text}

                ### Règles :
                - Retourne uniquement une requête SQL valide.
                - Utilise des jointures explicites (JOIN ... ON ...).
                - N'écris aucune explication, commentaire, ni texte additionnel.
                - Limite-toi aux tables et colonnes présentes dans le schéma.
                - Si plusieurs interprétations sont possibles, choisis la plus logique.
                - N'utilise que des commandes SELECT, jamais INSERT, UPDATE ou DELETE.

                ### Informations importantes :
                - Les plans (ou plan d'action) sont contenus dans la table axe (lorsque id=plan), le lien est fait avec les fiches actions par fiche_action_axe
                - Un indicateur est "personnalisé" lorsque que indicateur_definition.collectivite_id est non null
                - Un indicateur est "open data" lorsque indicateur_valeur.metadonnee_id est non null et indicateur_valeur.resultat est non null
                - Le budget d'investissement pour une fiche action est dans fiche_action_budget avec type='investissement'
                - Dans notre langage courant, on appelle "action" ce qui est en fait une "mesure" ou "mesure du référentiel"
                - Une fiche action liée à une fiche action se trouve dans la table fiche_action_lien et une fiche action lié à une mesure se trouve dans la table fiche_action_action
                - Le droit des utilisateurs se trouve dans la table private_utilisateur_droit, dans la colonne niveau_acces.
                - On appelle souvent FA une fiche action
                - Retire systématiquement les collectivités test de tes requêtes. Il suffit pour ça de mettre une clause where public.collectivite_id.type != 'test'

                ### Question utilisateur :
                {user_request}
                """
                
                # Appel à l'API OpenAI
                client = OpenAI(
                    api_key=st.secrets.get("OPENAI_API_KEY", "")
                )
                
                response = client.responses.create(
                    model=model,
                    input=prompt,
                    max_output_tokens=max_output_tokens,
                )
                
                # Extraction de la requête SQL
                sql_query = response.output_text.strip()
                
                # Nettoyage de la requête (retirer les balises markdown si présentes)
                if sql_query.startswith("```sql"):
                    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
                elif sql_query.startswith("```"):
                    sql_query = sql_query.replace("```", "").strip()
                
                # Afficher la requête SQL
                st.markdown("**📝 Requête SQL**")
                st.code(sql_query, language="sql")
                
                # === VÉRIFICATION DE SÉCURITÉ ===
                # Utilise des word boundaries pour éviter les faux positifs (ex: "created_at" contient "create")
                sql_query_lower = sql_query.lower()
                forbidden_keywords = ['insert', 'update', 'delete', 'drop', 'truncate', 'alter', 'create', 'grant', 'revoke']
                has_forbidden = any(re.search(r'\b' + keyword + r'\b', sql_query_lower) for keyword in forbidden_keywords)
                
                # === EXÉCUTION DE LA REQUÊTE ===
                assistant_message = {
                    "role": "assistant",
                    "sql_query": sql_query
                }
                
                if has_forbidden:
                    error_msg = "❌ Requête refusée : commandes de modification non autorisées (INSERT, UPDATE, DELETE, etc.)"
                    st.error(error_msg)
                    assistant_message["error"] = error_msg
                    
                    # Logger la réponse interdite
                    log_ai_answer(
                        question=user_request,
                        sql=sql_query,
                        reponse={
                            "status": "forbidden",
                            "error": error_msg
                        }
                    )
                else:
                    st.markdown("**✨ Résultats**")
                    try:
                        engine = get_engine_prod()
                        with engine.connect() as conn:
                            df = pd.read_sql_query(text(sql_query), conn)
                        
                        if df.empty:
                            st.info("Aucun résultat trouvé")
                            assistant_message["row_count"] = 0
                            assistant_message["dataframe"] = df
                            
                            # Logger la réponse vide
                            log_ai_answer(
                                question=user_request,
                                sql=sql_query,
                                reponse={
                                    "status": "success",
                                    "row_count": 0,
                                    "columns": list(df.columns) if not df.empty else []
                                }
                            )
                        else:
                            st.caption(f"{len(df)} ligne(s)")
                            st.dataframe(df, width='stretch')
                            assistant_message["row_count"] = len(df)
                            assistant_message["dataframe"] = df
                            
                            # Logger la réponse avec succès
                            log_ai_answer(
                                question=user_request,
                                sql=sql_query,
                                reponse={
                                    "status": "success",
                                    "row_count": len(df),
                                    "columns": list(df.columns),
                                    "sample_data": df.head(3).to_dict('records') if len(df) <= 100 else None
                                }
                            )
                            
                            # Option de téléchargement
                            csv = df.to_csv(index=False).encode('utf-8')
                            st.download_button(
                                label="💾 Télécharger (CSV)",
                                data=csv,
                                file_name="resultats_requete.csv",
                                mime="text/csv",
                            )
                    
                    except Exception as e:
                        error_msg = f"❌ Erreur d'exécution : {str(e)}"
                        st.error(error_msg)
                        assistant_message["error"] = error_msg
                        
                        # Logger l'erreur d'exécution
                        log_ai_answer(
                            question=user_request,
                            sql=sql_query,
                            reponse={
                                "status": "error",
                                "error": str(e)
                            }
                        )
                
                # Ajouter la réponse à l'historique
                st.session_state.messages.append(assistant_message)
                
            except Exception as e:
                error_msg = f"❌ Erreur de génération : {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "sql_query": "",
                    "error": error_msg
                })
                
                # Logger l'erreur de génération
                log_ai_answer(
                    question=user_request,
                    sql="",
                    reponse={
                        "status": "generation_error",
                        "error": str(e)
                    }
                )