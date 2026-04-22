import streamlit as st
from openai import OpenAI
from utils.db_text import tables_text, relations_text
from utils.db import get_engine_prod
import pandas as pd
from sqlalchemy import text
import re

st.set_page_config(layout="wide", page_title="SQL AI Assistant", page_icon="✨")


# === FONCTIONS HELPER ===
def build_conversation_history(messages, max_exchanges=10):
    """
    Construit l'historique de conversation formaté pour le prompt.
    
    Args:
        messages: Liste des messages de la session
        max_exchanges: Nombre maximum d'échanges à inclure (par défaut 10)
    
    Returns:
        String formaté avec l'historique de conversation
    """
    if len(messages) == 0:
        return ""
    
    # Limiter aux N derniers échanges pour éviter des prompts trop longs
    # On prend les messages 2 par 2 (user + assistant)
    relevant_messages = messages[-(max_exchanges * 2):] if len(messages) > max_exchanges * 2 else messages
    
    if len(relevant_messages) == 0:
        return ""
    
    history_text = "\n### Historique de la conversation :\n"
    
    for msg in relevant_messages:
        if msg["role"] == "user":
            history_text += f"\nUtilisateur : {msg['content']}\n"
        elif msg["role"] == "assistant" and "sql_query" in msg:
            history_text += f"Assistant (SQL généré) : {msg['sql_query']}\n"
    
    return history_text


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

# Bouton de réinitialisation et compteur
col1, col2 = st.columns([3, 1])
with col1:
    num_messages = len(st.session_state.messages)
    if num_messages > 0:
        st.caption(f"💬 {num_messages} message(s) dans la conversation")    
with col2:
    if st.button("🔄 Nouvelle conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Avertissement si le contexte devient trop long
if len(st.session_state.messages) >= 20:
    st.warning(
        "⚠️ **Attention** : Le contexte s'allonge à chaque requête, ce qui augmente les coûts et peut ralentir les réponses. "
        "Il est recommandé de lancer une nouvelle conversation.",
        icon="⚠️"
    )

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
                
                # Construire l'historique de conversation
                conversation_history = build_conversation_history(st.session_state.messages[:-1])
                
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
                - Dans notre langage courant, on appelle souvent "mesure" ou "mesure du référentiel" ce qui est une action dans notre base de données.
                - Une fiche action liée à une fiche action se trouve dans la table fiche_action_lien et une fiche action lié à une mesure se trouve dans la table fiche_action_action
                - Le droit des utilisateurs se trouve dans la table private_utilisateur_droit, dans la colonne niveau_acces.
                - On appelle souvent FA ou action ce qui est en fait une fiche_action dans notre base de données.
                - Retire systématiquement les collectivités test de tes requêtes. Il suffit pour ça de mettre une clause where public.collectivite.type != 'test'
                - Une sous-action est une action (fiche_action) dont le parent_id est non null.

                ### Historique de la conversation :
                {conversation_history}

                ### Question utilisateur actuelle :
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
                        else:
                            st.caption(f"{len(df)} ligne(s)")
                            st.dataframe(df, width='stretch')
                            assistant_message["row_count"] = len(df)
                            assistant_message["dataframe"] = df
                            
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