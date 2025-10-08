import streamlit as st
import pandas as pd

from utils.data import (
    load_df_pap,
    load_df_pap_notes,
)
from utils.analytics import (
    compute_totals_by_period,
    date_to_month,
    display_totals_table,
)
from utils.plots import plot_area_with_totals


st.set_page_config(page_title="Explorateur interactif", page_icon="🧰", layout="wide")
st.title("🧰 Explorateur interactif")
st.caption("Sélectionnez une source, une granularité et le type d'affichage.")


@st.cache_data(show_spinner=False)
def _load_sources():
    # mappe un nom lisible vers (DataFrame, params par défaut)
    df_pap = load_df_pap()
    df_pap_notes = load_df_pap_notes()
    sources = {
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
        "Évolution des plans d'actions par type": (
            df_pap,
            {
                "date_col": "passage_pap",
                "group_col": "nom_plan",
                "force_granularite": None,
                "force_cumulatif": None,
                "objectif": None,
            },
        ),
        "🌟 Évolution des scores (NS Rétention)": (
            df_pap_notes,
            {
                "date_col": "semaine",
                "group_col": "score_groupe",  # présumé présent dans df_pap_notes
                "force_granularite": "W",
                "force_cumulatif": False,
                "objectif": None,
            },
        ),
    }
    return sources


sources = _load_sources()
col_left, col_right = st.columns([1, 3])
with col_left:
    selection = st.selectbox("Donnée:", options=list(sources.keys()))
    df, params = sources[selection]

    # Widgets équivalents avec overrides possibles
    min_date = st.date_input("Date de début", value=pd.to_datetime("2025-01-01").date())

    if params["force_granularite"] is not None:
        time_granularity = params["force_granularite"]
        st.text(f"Granularité: {time_granularity} (forcée)")
    else:
        time_granularity = st.radio("Granularité:", options=[("Semaine", "W"), ("Mois", "M")], format_func=lambda x: x[0])[1]

    if params["force_cumulatif"] is not None:
        cumulatif = params["force_cumulatif"]
        st.text(f"Type: {'Cumulé' if cumulatif else 'Brut'} (forcé)")
    else:
        cumulatif = st.radio("Type:", options=[("Brut", False), ("Cumulé", True)], format_func=lambda x: x[0])[1]

    view = st.radio("Affichage:", options=[("Graphe", "graph"), ("Tableau", "table")], format_func=lambda x: x[0])[1]

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
        st.plotly_chart(table_fig, use_container_width=True)


