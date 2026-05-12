import streamlit as st

st.set_page_config(
    page_title="Dashboard TET",
    page_icon="🏄‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration de la navigation avec des sections (groupes)
pages = {
    "Favoris": [
        st.Page("pages/26_Dashboard_okrs.py", title="Dashboard OKRs", icon="🌠"),
        st.Page("pages/02_⚡_Weekly.py", title="Weekly", icon="⚡", default=True),
        st.Page("pages/22_🪄_Import_Tool.py", title="Import Tool", icon="🪄"),
        st.Page("pages/06_✨_AI_Stats_assistant.py", title="AI Stats Assistant", icon="✨"),
    ],
    "Tableaux de Bord": [
        st.Page("pages/27_Dashboard_produit.py", title="Dashboard Produit", icon="🚀"),
        st.Page("pages/08_👩‍🚀_Suivi_bizdevs.py", title="Dashboard Bizdevs", icon="👩‍🚀"),
        st.Page("pages/04_🥐_TDB_collectivite.py", title="Dashbaord Collectivité", icon="🥐"),
        st.Page("pages/16_👥_Implication_Conseillers.py", title="Dashboard Conseillers", icon="👥"),
        
    ],
    "Livraison": [
        st.Page("pages/09_🌀_Import_indicateurs.py", title="Import Indicateurs", icon="🌀"),
        st.Page("pages/10_🚚_Livraison_pre_prod.py", title="Livraison Pre-Prod", icon="🚚"),
        st.Page("pages/11_🚢🚨_Livraison_Prod.py", title="Livraison Prod", icon="🚨"),
    ],
    "Bac à sable": [
        st.Page("pages/26_run_impact.py", title="Calcul impact", icon="🎯"),
        st.Page("pages/12_⛱️_North_Star_Bac_a_sable.py", title="North Star Bac à sable", icon="⛱️"),
        st.Page("pages/21_👽_Power_users.py", title="Power users", icon="👽"),
        st.Page("pages/07_💡_Suggestion_indicateurs.py", title="Suggestion Indicateurs", icon="🤖"),
        st.Page("pages/25_Impact.py", title="Modélisation d'impact GES", icon="🎯"),
        st.Page("pages/24_🗺️_Carte_de_france.py", title="Dashboard Carte de France", icon="🗺️"),
        st.Page("pages/28_Agent_IA_Benchmark.py", title="Agent IA Benchmark", icon="🥸"),
        st.Page("pages/29_Matrice_dimpact.py", title="Matrice d'impact", icon="🎯"),
    ],
}

pg = st.navigation(pages)
pg.run()