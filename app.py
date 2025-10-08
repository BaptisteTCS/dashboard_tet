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
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown(
    """
    <div style="padding: 14px 18px; background: linear-gradient(90deg,#3B82F6, #60A5FA); border-radius: 12px; color: white;">
      <h1 style="margin: 0; font-size: 28px;">Dashboard PAP</h1>
      <p style="margin: 6px 0 0; opacity: 0.95;">Migration Datalore → Streamlit • Visualisations clés et exploration interactive</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.write("")
st.info("Utilisez le menu à gauche pour naviguer entre les pages. Les données proviennent de votre base Postgres.")

st.sidebar.success("Choisissez une page dans le menu Pages")

st.caption("Astuce: appuyez sur R pour recharger la page après modifications de code.")


