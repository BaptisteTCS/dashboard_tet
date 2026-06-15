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
        st.Page("pages/06_✨_AI_Stats_assistant.py", title="AI Assistant", icon="✨"),
        st.Page("pages/22_🪄_Import_Tool.py", title="Import Tool", icon="🪄"),
        st.Page("pages/26_Dashboard_okrs.py", title="OKRs", icon="🌠"),
        st.Page("pages/02_⚡_Weekly.py", title="Weekly", icon="⚡"),
    ],
    "Dashboards": [
        st.Page("pages/08_👩‍🚀_Suivi_bizdevs.py", title="Bizdevs", icon="👩‍🚀"),
        st.Page("pages/35_dashboard_bug.py", title="Bug - Support", icon="🐛"),
        st.Page("pages/04_🥐_TDB_collectivite.py", title="Collectivité", icon="🥐"),
        st.Page("pages/16_👥_Implication_Conseillers.py", title="Conseillers", icon="👥"),
        st.Page("pages/27_Dashboard_produit.py", title="Produit", icon="🚀"),
        st.Page("pages/36_📈_Retro_data.py", title="Retro Data", icon="🛰️"),
    ],
    "Indicateurs Open Data": [
        st.Page("pages/09_🌀_Import_indicateurs.py", title="Import Indicateurs", icon="🌀"),
        st.Page("pages/10_🚚_Livraison_pre_prod.py", title="Livraison Pre-Prod", icon="🚚"),
        st.Page("pages/11_🚢🚨_Livraison_Prod.py", title="Livraison Prod", icon="🚨"),
    ],
    "Priorisation": [
        st.Page("pages/26_run_impact.py", title="Analyse des actions par CT", icon="🌀"),
        st.Page("pages/31_priorisation_perimetre.py", title="Optionnel - Périmètre d'action", icon="🔧"),
        st.Page("pages/30_priorisation.py", title="1 - Diagnostic", icon="🧭", default=True),
        st.Page("pages/32_priorisation_faisabilite.py", title="2 - Faisabilité politique", icon="⚖️"),
        st.Page("pages/33_priorisation_action.py", title="3 - Exploration des actions de référence", icon="🏅"),
        st.Page("pages/34_priorisation_synthese.py", title="4 - Synthèse", icon="🏆"),
    ],
}

pg = st.navigation(pages)
pg.run()

