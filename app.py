import streamlit as st

st.set_page_config(
    page_title="Dashboard TET",
    page_icon="🏄‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration de la navigation avec des sections (groupes)
pages = {
    "Accueil": [
        st.Page("app_home.py", title="Accueil", icon="🏠", default=True),
    ],
    "📊 Métriques & Suivi": [
        st.Page("pages/01_🌟_North_Star_&_metrics.py", title="North Star & Metrics", icon="🌟"),
        st.Page("pages/02_⚡_Weekly.py", title="Weekly", icon="⚡"),
        st.Page("pages/03_🏆_Champions.py", title="Champions", icon="🏆"),
    ],
    "🏛️ Tableaux de Bord": [
        st.Page("pages/04_🥐_TDB_collectivite.py", title="TDB Collectivité", icon="🥐"),
        st.Page("pages/16_👥_Implication_Conseillers.py", title="Implication Conseillers", icon="👥"),
        st.Page("pages/17_🌍_Suivi_Campagne_Regions.py", title="Suivi Campagne Régions", icon="🌍"),
        st.Page("pages/08_👩‍🚀_Suivi_bizdevs.py", title="Suivi Bizdevs", icon="👩‍🚀"),
    ],
    "🔓 Open Data": [
        st.Page("pages/14_📊_Dashboard_Open_Data.py", title="Dashboard Open Data", icon="📊"),
        st.Page("pages/15_🏛️_Open_Data_Collectivité.py", title="Open Data par Collectivité", icon="🏛️"),
    ],
    "🤖 Intelligence Artificielle": [
        st.Page("pages/06_✨_AI_Stats_assistant.py", title="AI Stats Assistant", icon="✨"),
        st.Page("pages/07_💡_Suggestion_indicateurs.py", title="Suggestion Indicateurs", icon="🤖"),
        st.Page("pages/18_✨_Import_des_plans.py", title="Import Des Plans", icon="✨"),
    ],
    "⚙️ Import & Configuration": [
        st.Page("pages/09_🌀_Import_indicateurs.py", title="Import Indicateurs", icon="🌀"),
        st.Page("pages/13_🪇_Import_groupement_indicateurs.py", title="Import Groupement Indicateurs", icon="🪇"),
    ],
    "🚀 Livraison": [
        st.Page("pages/10_🚚_Livraison_pre_prod.py", title="Livraison Pre-Prod", icon="🚚"),
        st.Page("pages/11_🚢🚨_Livraison_Prod.py", title="Livraison Prod", icon="🚨"),
    ],
    "🧪 Bac à sable": [
        st.Page("pages/12_⛱️_North_Star_Bac_a_sable.py", title="North Star Bac à sable", icon="⛱️"),
        st.Page("pages/19_🪐_Experimentation_Nivo.py", title="Expérimentation Nivo", icon="🪐"),
        st.Page("pages/20_📢_Stats_publiques.py", title="Stats Publiques", icon="📢"),
        st.Page("pages/21_👽_Power_users.py", title="Power users", icon="👽"),
    ],
}

pg = st.navigation(pages)
pg.run()


