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
        st.Page("pages/02_⚡_Weekly.py", title="Weekly", icon="⚡", default=True),
    ],
    "Dashboards": [
        st.Page("pages/08_👩‍🚀_Suivi_bizdevs.py", title="Bizdevs", icon="👩‍🚀"),
        st.Page("pages/04_🥐_TDB_collectivite.py", title="Collectivité", icon="🥐"),
        st.Page("pages/16_👥_Implication_Conseillers.py", title="Conseillers", icon="👥"),
        st.Page("pages/27_Dashboard_produit.py", title="Produit", icon="🚀"),
    ],
    "Indicateurs Open Data": [
        st.Page("pages/09_🌀_Import_indicateurs.py", title="Import Indicateurs", icon="🌀"),
        st.Page("pages/10_🚚_Livraison_pre_prod.py", title="Livraison Pre-Prod", icon="🚚"),
        st.Page("pages/11_🚢🚨_Livraison_Prod.py", title="Livraison Prod", icon="🚨"),
    ],
}

pg = st.navigation(pages)
pg.run()