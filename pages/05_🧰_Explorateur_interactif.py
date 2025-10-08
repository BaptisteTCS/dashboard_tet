import streamlit as st
import pandas as pd

from utils.data import (
    load_df_pap,
    load_df_pap_statut_semaine,
)
from utils.analytics import (
    compute_totals_by_period,
    date_to_month,
    display_totals_table,
)
from utils.plots import plot_area_with_totals


st.set_page_config(page_title="Explorateur interactif", page_icon="🧰", layout="wide")
st.markdown(
    """
    <div style=\"padding: 10px 14px; background: #F6F8FB; border: 1px solid #E5E7EB; border-radius: 12px; margin-bottom: 18px;\">
      <h2 style=\"margin: 0; font-size: 28px; color: #0F172A;\">🧰 Explorateur interactif</h2>
      <p style=\"margin: 6px 0 0; color: #374151;\">Sélectionnez une source, une granularité et le type d'affichage.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)
def _load_sources():
    # mappe un nom lisible vers (DataFrame, params par défaut)
    df_pap = load_df_pap()
    df_pap_statut_semaine = load_df_pap_statut_semaine()
    
    sources = {
        "🌟 North Star": (
            df_pap_statut_semaine,
            {
                "date_col": "semaine",
                "group_col": "statut",
                "force_granularite": 'W',
                "force_cumulatif": False,
                "objectif": 500,
            },
        ),
        "PAP importés/autonomes": (
            df_pap,
            {
                "date_col": "passage_pap",
                "group_col": "import",
                "force_granularite": None,
                "force_cumulatif": None,
                "objectif": None,
            },
        ),
    }
    return sources


sources = _load_sources()
col_left, col_right = st.columns([1, 3], gap="large")
with col_left:
    with st.container(border=True):
        st.subheader("Données", divider="blue")
        selection = st.selectbox("Sélection", options=list(sources.keys()))
    df, params = sources[selection]

    with st.container(border=True):
        st.subheader("Paramètres", divider="blue")
        min_date = st.date_input("Date de début", value=pd.to_datetime("2025-01-01").date())

    if params["force_granularite"] is not None:
        time_granularity = params["force_granularite"]
        st.text(f"Granularité: {time_granularity} (forcée)")
    else:
        gran_label = st.segmented_control(
            "Granularité",
            options=["Semaine", "Mois"],
            default="Mois",
        )
        gran_map = {"Semaine": "W", "Mois": "M"}
        time_granularity = gran_map.get(gran_label, "M")

    if params["force_cumulatif"] is not None:
        cumulatif = params["force_cumulatif"]
        st.text(f"Type: {'Cumulé' if cumulatif else 'Brut'} (forcé)")
    else:
        type_label = st.segmented_control(
            "Type",
            options=["Brut", "Cumulé"],
            default="Brut",
        )
        cumulatif = True if type_label == "Cumulé" else False

    with st.container(border=True):
        st.subheader("Affichage", divider="blue")
        view_label = st.segmented_control(
            "Mode",
            options=["Graphe", "Tableau"],
            default="Graphe",
        )
        view = "graph" if view_label == "Graphe" else "table"

with col_right:
    # Affichage
    if view == "graph":
        fig = plot_area_with_totals(
            df=df,
            date_col=params["date_col"],
            group_col=params["group_col"],
            time_granularity=time_granularity,
            cumulatif=cumulatif,
            min_date=pd.to_datetime(min_date).strftime('%Y-%m-%d'),
            values_graph=True,
            objectif=params.get("objectif"),
        )
        with st.container(border=True):
            st.subheader("Résultat", divider="blue")
            st.plotly_chart(fig, use_container_width=True)
    else:
        df_totals = compute_totals_by_period(
            df=df,
            date_col=params["date_col"],
            group_col=params["group_col"],
            time_granularity=time_granularity,
            cumulatif=cumulatif,
            min_date=pd.to_datetime(min_date).strftime('%Y-%m-%d'),
        )
        df_totals = date_to_month(df_totals)
        table_fig = display_totals_table(df_totals)
        with st.container(border=True):
            st.subheader("Résultat", divider="blue")
            st.plotly_chart(table_fig, use_container_width=True)


