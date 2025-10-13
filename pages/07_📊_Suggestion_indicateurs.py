import streamlit as st
from openai import OpenAI
# Import de la liste d'indicateurs
try:
    from utils.list_ind import indicateurs_possibles
except ImportError:
    # Fallback si l'import ne fonctionne pas
    indicateurs_possibles = []
import json

st.set_page_config(layout="wide", page_title="Suggestion d'indicateurs", page_icon="📊")

# En-tête
st.markdown("""
<div style='text-align: center; padding: 1rem 0 2rem 0;'>
    <h1 style='font-size: 2.5rem; margin-bottom: 0.5rem;'>📊 Suggestion d'indicateurs</h1>
    <p style='color: #666; font-size: 1rem;'>Prototype : Saisissez le titre d'une action pour obtenir des suggestions d'indicateurs de suivi</p>
</div>
""", unsafe_allow_html=True)

# Sidebar avec configuration
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    model_choice = st.selectbox(
        "Modèle",
        ["gpt-5", "gpt-5-mini", "gpt-5-nano"],
        index=1,  # gpt-5-mini par défaut
        help="Par défaut gpt-5-mini, gpt-5 est plus performant"
    )
    
    st.markdown("---")
    
    st.info("💡 **Conseil :** Soyez précis dans le titre de votre action. Plus le contexte est clair, meilleures seront les suggestions d'indicateurs.")
    
    st.markdown("---")
    
    st.markdown("### 📝 Exemples d'actions")
    st.markdown("""
    - Développement du photovoltaïque sur les toitures publiques
    - Mise en place d'un plan de déplacements doux
    - Rénovation énergétique du patrimoine bâti
    - Déploiement de bornes de recharge électrique
    - Création d'un réseau de chaleur urbain
    """)

# Zone de saisie principale
st.markdown("### 🎯 Saisissez le titre de votre action")

# Zone de texte pour le titre de l'action
action_title = st.text_area(
    "Titre de l'action",
    placeholder="Ex: Développement du photovoltaïque sur les toitures publiques de la collectivité",
    height=100,
    help="Décrivez clairement l'action que vous souhaitez suivre"
)

# Bouton pour générer les suggestions
if st.button("🚀 Générer les suggestions d'indicateurs", type="primary", use_container_width=True):
    if not action_title.strip():
        st.error("⚠️ Veuillez saisir un titre d'action")
    else:
        with st.spinner("Analyse de votre action et génération des suggestions..."):
            try:
                # Configuration du modèle
                model = model_choice
                
                # Préparation de la liste d'indicateurs pour le prompt
                if indicateurs_possibles:
                    indicateurs_text = "\n".join([f"- {ind}" for ind in indicateurs_possibles[:100]])  # Limite à 100 pour éviter un prompt trop long
                    st.info(f"📚 Utilisation de {len(indicateurs_possibles)} indicateurs de référence")
                else:
                    indicateurs_text = "Liste d'indicateurs non disponible"
                    st.warning("⚠️ Liste d'indicateurs de référence non disponible")
                
                # Construction du prompt
                prompt = f"""
Tu es un expert en indicateurs de suivi pour les collectivités territoriales, spécialisé dans les politiques climat-air-énergie et de transition écologique.

Ta mission est d'analyser le titre d'action fourni par l'utilisateur et de proposer 3 à 5 indicateurs de suivi pertinents et mesurables.

### Liste d'indicateurs de référence disponibles :
{indicateurs_text}

### Instructions :
1. Analyse le titre d'action fourni
2. Identifie les domaines concernés (énergie, transport, déchets, bâtiment, etc.)
3. Propose 3 à 5 indicateurs de suivi pertinents
4. Priorise les indicateurs qui sont dans la liste de référence ci-dessus
5. Si aucun indicateur de la liste ne correspond, propose des indicateurs adaptés
6. Pour chaque indicateur, indique :
   - Le nom de l'indicateur
   - L'unité de mesure
   - La fréquence de suivi recommandée
   - Une brève justification de son choix

### Format de réponse attendu :
Retourne uniquement un JSON avec cette structure :
{{
    "action_analysee": "Titre de l'action analysée",
    "domaines_identifies": ["domaine1", "domaine2"],
    "indicateurs": [
        {{
            "nom": "Nom de l'indicateur",
            "unite": "Unité de mesure",
            "frequence": "Fréquence de suivi",
            "justification": "Pourquoi cet indicateur est pertinent",
            "dans_liste_reference": true/false
        }}
    ]
}}

### Action à analyser :
{action_title}
"""

                # Appel à l'API OpenAI
                client = OpenAI(
                    api_key=st.secrets.get("OPENAI_API_KEY", "")
                )
                
                response = client.responses.create(
                    model=model,
                    input=prompt,
                    max_output_tokens=2000,
                )
                
                # Extraction de la réponse
                response_text = response.output_text.strip()
                
                # Nettoyage de la réponse (retirer les balises markdown si présentes)
                if response_text.startswith("```json"):
                    response_text = response_text.replace("```json", "").replace("```", "").strip()
                elif response_text.startswith("```"):
                    response_text = response_text.replace("```", "").strip()
                
                try:
                    # Parse de la réponse JSON
                    result = json.loads(response_text)
                    
                    # Affichage des résultats
                    st.markdown("---")
                    st.markdown("### 📋 Analyse de votre action")
                    
                    # Action analysée
                    st.markdown(f"**🎯 Action analysée :** {result.get('action_analysee', action_title)}")
                    
                    # Domaines identifiés
                    if 'domaines_identifies' in result:
                        domaines = result['domaines_identifies']
                        if domaines:
                            st.markdown(f"**🏷️ Domaines identifiés :** {', '.join(domaines)}")
                    
                    st.markdown("### 📊 Indicateurs de suivi suggérés")
                    
                    # Affichage des indicateurs
                    if 'indicateurs' in result:
                        for i, indicateur in enumerate(result['indicateurs'], 1):
                            with st.expander(f"**{i}. {indicateur.get('nom', 'Indicateur sans nom')}**", expanded=True):
                                col1, col2 = st.columns([2, 1])
                                
                                with col1:
                                    st.markdown(f"**📏 Unité :** {indicateur.get('unite', 'Non spécifiée')}")
                                    st.markdown(f"**⏰ Fréquence :** {indicateur.get('frequence', 'Non spécifiée')}")
                                    st.markdown(f"**💡 Justification :** {indicateur.get('justification', 'Non fournie')}")
                                
                                with col2:
                                    if indicateur.get('dans_liste_reference', False):
                                        st.success("✅ Dans la liste de référence")
                                    else:
                                        st.info("🆕 Indicateur personnalisé")
                    
                    # Option de téléchargement
                    st.markdown("---")
                    col1, col2, col3 = st.columns([1, 1, 1])
                    
                    with col2:
                        json_data = json.dumps(result, ensure_ascii=False, indent=2)
                        st.download_button(
                            label="💾 Télécharger les suggestions (JSON)",
                            data=json_data,
                            file_name=f"suggestions_indicateurs_{action_title[:30].replace(' ', '_')}.json",
                            mime="application/json",
                            use_container_width=True
                        )
                
                except json.JSONDecodeError as e:
                    st.error("❌ Erreur lors du parsing de la réponse JSON")
                    st.text("Réponse brute :")
                    st.code(response_text)
                    st.error(f"Erreur JSON : {str(e)}")
                
            except Exception as e:
                st.error(f"❌ Erreur de génération : {str(e)}")

# Section d'information
st.markdown("---")
with st.expander("ℹ️ À propos de cette fonctionnalité", expanded=False):
    st.markdown("""
    **📊 Suggestion d'indicateurs** est un prototype qui utilise l'intelligence artificielle pour vous aider à identifier les indicateurs de suivi pertinents pour vos actions.
    
    **🎯 Comment ça marche :**
    1. Saisissez le titre de votre action
    2. L'IA analyse le contenu et identifie les domaines concernés
    3. Elle propose des indicateurs de suivi adaptés
    4. Les indicateurs sont prioritairement choisis dans une liste de référence de plus de 500 indicateurs standards
    
    **💡 Conseils d'utilisation :**
    - Soyez précis dans le titre de votre action
    - Mentionnez les objectifs principaux
    - Indiquez le périmètre (territoire, bâtiments, etc.)
    
    **🔧 Fonctionnalités :**
    - Suggestions personnalisées selon votre action
    - Référencement à une base d'indicateurs standards
    - Export des résultats en JSON
    - Justification de chaque indicateur proposé
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem;'>
    <p>🔬 <strong>Prototype</strong> - Cette fonctionnalité est en cours de développement</p>
</div>
""", unsafe_allow_html=True)
