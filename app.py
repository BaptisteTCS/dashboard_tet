import streamlit as st
from utils.plots import (
    radar_spider_graph_plotly_with_comparison,
    radar_spider_graph_plotly,
    plot_area_with_totals,
    indicator
)
from utils.data import (
    load_df_pap,
    load_df_ct,
    load_df_pap_notes,
    load_df_plan_pilote,
    load_df_plan_referent,
    load_df_sharing,
    load_df_score_indicateur
)


st.set_page_config(
    page_title="Dashboard PAP",
    page_icon="📊",
    layout="wide"
)


st.title("Dashboard PAP – Migration Datalore → Streamlit")
st.write("""
Cette application reprend les principales visualisations du notebook Datalore et les expose en pages Streamlit.
Utilisez le menu de gauche pour naviguer. Les données sont chargées via `utils/data.py` – adaptez ces fonctions à votre source (SQL, CSV, API).
""")

st.sidebar.success("Choisissez une page dans le menu Pages")

st.caption("Astuce: appuyez sur R pour recharger la page après modifications de code.")


