import streamlit as st
import pandas as pd
from openai import OpenAI
import io

st.set_page_config(layout="wide", page_title="Suggestions d'indicateurs", page_icon="🤖")

# En-tête minimaliste
st.markdown("""
<div style='text-align: center; padding: 1rem 0 2rem 0;'>
    <h1 style='font-size: 2.5rem; margin-bottom: 0.5rem;'>🤖  Suggestions d'indicateurs</h1>
    <p style='color: #666; font-size: 1rem;'>Saisissez une action pour obtenir des suggestions d'indicateurs</p>
</div>
""", unsafe_allow_html=True)

# Initialisation des session states
if 'last_action' not in st.session_state:
    st.session_state.last_action = ""
if 'should_generate' not in st.session_state:
    st.session_state.should_generate = False

# Chargement de la liste d'indicateurs
@st.cache_data
def load_indicators():
    """Charge la liste des indicateurs depuis le CSV"""
    try:
        df = pd.read_csv('utils/indicateurs_v2.csv')
        return df['indicateur'].tolist()
    except Exception as e:
        st.error(f"Erreur lors du chargement des indicateurs : {e}")
        return []

# Zone de saisie avec layout amélioré
col1, col2 = st.columns([4, 1])

with col1:
    action = st.text_input(
        "Action à analyser",
        placeholder="Ex: Développement du photovoltaïque sur les toitures publiques",
        help="Saisissez votre action et appuyez sur Entrée ou cliquez sur le bouton",
        key="action_input"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)  # Espacement pour aligner avec le text_input
    generate_button = st.button("🚀 Générer", type="secondary", use_container_width=True, help="Ou appuyez sur Entrée dans le champ de saisie")

# Détection si une nouvelle action a été saisie (Enter pressé)
action_changed = action != st.session_state.last_action and action.strip()

# Gestion de la génération (bouton ou Enter)
if generate_button or action_changed:
    if not action.strip():
        st.error("⚠️ Veuillez saisir une action")
    else:
        with st.spinner("Génération des suggestions..."):
            try:
                # Chargement des indicateurs
                indicateurs_list = load_indicators()
                
                if not indicateurs_list:
                    st.error("❌ Impossible de charger la liste des indicateurs")
                else:
                    # Création du DataFrame pour le prompt
                    df = pd.DataFrame({'indicateur': indicateurs_list})
                    
                    # Construction du prompt
                    user_prompt = f"""
                        Vous êtes un expert en politiques publiques locales et en suivi des plans d'actions climat-air-énergie (PCAET).
                        Votre rôle est de suggérer des indicateurs pertinents à une collectivité pour suivre la mise en œuvre d'une action donnée.

                        ### Données disponibles
                        Voici la liste complète des indicateurs possibles :
                        <<<
                        {list(df.indicateur)}
                        >>>

                        ### Tâche
                        À partir du titre de l'action ci-dessous, propose entre **0 et 5** indicateurs **parmi ceux de la liste**, qui seraient les plus pertinents pour évaluer l'avancement ou les résultats de cette action.

                        ### Contraintes :
                        - Retournez uniquement les libellés exacts des indicateurs issus de la liste.
                        - Séparez les indicateurs par des ";".
                        - Ne proposez rien si aucun indicateur ne correspond clairement.
                        - Ne reformulez pas les indicateurs.

                        ### Exemple de sortie attendue :
                        "Consommation d'énergie du patrimoine communal; Part de la surface agricole utile en agriculture biologique"

                        ### Action à analyser :
                        <<<
                        {action}
                        >>>
                        """
                    
                    # Appel à l'API OpenAI
                    client = OpenAI(
                        api_key=st.secrets.get("OPENAI_API_KEY", "")
                    )
                    
                    response = client.responses.create(
                        model="gpt-5-mini",
                        input=user_prompt,
                        max_output_tokens=10000,
                        reasoning={"effort":"low"}
                    )
                    
                    # Extraction de la réponse
                    suggestions = response.output_text.strip()
                    
                    # Affichage des résultats
                    st.markdown("---")
                    
                    if suggestions:
                        # Séparation des indicateurs
                        indicateurs_suggérés = [ind.strip() for ind in suggestions.split(';') if ind.strip()]
                        
                        if indicateurs_suggérés:
                            if len(indicateurs_suggérés)>1:
                                st.markdown(f"### ✅ {len(indicateurs_suggérés)} indicateurs suggérés")
                            else:
                                st.markdown(f"### ✅ {len(indicateurs_suggérés)} indicateur suggéré")
                            
                            # Affichage des indicateurs dans des boxes attractives
                            for i, indicateur in enumerate(indicateurs_suggérés, 1):
                                st.markdown(f"""
                                <div style="
                                    background: #f0f9ff;
                                    border: 1px solid #bae6fd;
                                    padding: 1rem 1.5rem;
                                    border-radius: 8px;
                                    margin: 0.5rem 0;
                                    color: #0f172a;
                                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                                    border-left: 4px solid #22c55e;
                                    width: fit-content;
                                    max-width: 80%;
                                ">
                                    <div style="display: flex; align-items: center; gap: 10px;">
                                        <span style="
                                            background: #22c55e;
                                            color: white;
                                            border-radius: 50%;
                                            width: 28px;
                                            height: 28px;
                                            display: flex;
                                            align-items: center;
                                            justify-content: center;
                                            font-weight: bold;
                                            font-size: 0.8rem;
                                        ">{i}</span>
                                        <span style="font-size: 0.95rem; line-height: 1.4;">{indicateur}</span>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
    
                        else:
                            st.info("ℹ️ Aucun indicateur spécifique trouvé pour cette action")
                    else:
                        st.info("ℹ️ Aucune suggestion générée")
                        
            except Exception as e:
                st.error(f"❌ Erreur de génération : {str(e)}")
        
        # Mise à jour du session state
        st.session_state.last_action = action