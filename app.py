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
        st.Page("pages/06_✨_AI_Stats_assistant.py", title="IA Transitos", icon="🧠"),
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
        st.Page("pages/37_🌿_Dashboard_biodiv.py", title="Biodiv", icon="🌿"),
        st.Page("pages/38_usser_path.py", title="User Path", icon="🛤️"),
    ],
    "Indicateurs Open Data": [
        st.Page("pages/09_🌀_Import_indicateurs.py", title="Import Indicateurs", icon="🌀"),
        st.Page("pages/10_🚚_Livraison_pre_prod.py", title="Livraison Pre-Prod", icon="🚚"),
        st.Page("pages/11_🚢🚨_Livraison_Prod.py", title="Livraison Prod", icon="🚨"),
    ],
    "Analyses": [
        st.Page("pages/26_run_impact.py", title="Analyse des actions par CT", icon="🌀"),
        st.Page("pages/31_priorisation_perimetre.py", title="Optionnel - Périmètre d'action", icon="🔧"),
    ],
    "Priorisation": [
        st.Page("pages/39_priorisation_faisabilite_new.py", title="Priorisation des actions", icon="🥇", default=True),
        st.Page("pages/40_priorisation_action.py", title="Actions de référence", icon="🏅"),
        st.Page("pages/41_priorisation_synthese_new.py", title="Synthèse - Tableau de bord", icon="🏆"),
    ],
}

pg = st.navigation(pages)
pg.run()

