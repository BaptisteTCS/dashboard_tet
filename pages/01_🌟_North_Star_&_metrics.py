import streamlit as st
import pandas as pd

from utils.data import (
    load_df_pap,
    load_df_pap_statut_semaine,
    load_df_pap_notes_summed,
    load_df_typologie_fiche,
    load_df_airtable_pipeline_semaine,
    load_df_pap_statut_semaine_12_mois,
)
from utils.analytics import (
    compute_totals_by_period,
    date_to_month,
    display_totals_table,
)
from utils.plots import plot_area_with_totals


st.set_page_config(page_title="North Star & Metrics", page_icon="🌟", layout="wide")
st.markdown(
    """
    <div style=\"padding: 10px 14px; margin-bottom: 18px;\">
      <h2 style=\"margin: 0; font-size: 40px;\">🌟 North Star & metrics</h2>
    </div>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)  
def _load_sources():
    # mappe un nom lisible vers (DataFrame, params par défaut)
    df_pap = load_df_pap()
    df_pap_statut_semaine = load_df_pap_statut_semaine()
    df_pap_notes_summed = load_df_pap_notes_summed()
    df_typologie_fiche = load_df_typologie_fiche()
    df_airtable_pipeline_semaine = load_df_airtable_pipeline_semaine()
    df_pap_statut_semaine_12_mois = load_df_pap_statut_semaine_12_mois()

    sources = {
        "🌟 North Star 1 - Activation": (
            df_pap_statut_semaine,
            {
                "date_col": "semaine",
                "group_col": "statut",
                "force_granularite": 'W',
                "force_cumulatif": False,
                "objectif": 500,
            },
        ),
        "🌟 North Star 1 - Activation (12 mois)": (
            df_pap_statut_semaine_12_mois,
            {
                "date_col": "semaine",
                "group_col": "statut",
                "force_granularite": 'W',
                "force_cumulatif": False,
                "objectif": 500,
            },
        ),
        "🌟 North Star 2 - Rétention : Somme des scores": (
            df_pap_notes_summed,
            {
                "date_col": "semaine",
                "group_col": "type_score",
                "force_granularite": 'W',
                "force_cumulatif": False,
                "objectif": None,
                "use_values_col": "somme",
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
        "Evolution des plans par type": (
            df_pap,
            {
                "date_col": "passage_pap",
                "group_col": "nom_plan",
                "force_granularite": None,
                "force_cumulatif": None,
                "objectif": None,
            },
        ),
        "Evolution des fiches actions par type": (
            df_typologie_fiche,
            {
                "date_col": "modified_at",
                "group_col": "type",
                "force_granularite": None,
                "force_cumulatif": None,
                "objectif": None,
            },
        ),
        "Evolution du nombre de CT par pipeline (bizdev)": (
            df_airtable_pipeline_semaine[df_airtable_pipeline_semaine['pipeline'] != 'A acquérir'],
            {
                "date_col": "semaine",
                "group_col": "pipeline",
                "force_granularite": 'W',
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
        st.text(f"Granularité: forcée")
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
        st.text(f"Type: forcé")
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

    # Debug expander
    with st.expander("🐛 Debug - Voir les données brutes"):
        st.write(f"**Source sélectionnée :** {selection}")
        st.write(f"**Shape du DataFrame :** {df.shape}")
        st.write(f"**Colonnes :** {list(df.columns)}")
        st.write(f"**Types de données :**")
        st.write(df.dtypes)
        st.write("**Aperçu des données (20 premières lignes) :**")
        st.dataframe(df.head(20), width='stretch')

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
            use_values_col=params.get("use_values_col") if params.get("use_values_col") else None,
        )
        with st.container(border=True):
            st.subheader("Résultat", divider="blue")
            st.plotly_chart(fig, width='stretch')
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
        with st.container(border=True):
            st.subheader("Résultat", divider="blue")
            st.info("Astuce: vous pouvez trier le tableau en cliquant sur les en-têtes de colonnes.")
            st.dataframe(df_totals, width='stretch')
