import streamlit as st
import pandas as pd

from utils.data import (
    load_df_plan_pilote,
    load_df_plan_referent,
    load_df_sharing,
)
from utils.plots import plot_area_with_totals, indicator


st.title("🚀 MEP / Cycle – Indicateurs d'usage")

st.header("Ajouter une personne pilote / élu·e référent·e")

df_5 = load_df_plan_pilote().copy()
if df_5.empty:
    st.info("Aucune donnée pour les pilotes. Voir `load_df_plan_pilote()`.")
else:
    df_5['type_user'] = df_5.user_id.fillna(0).apply(lambda x: 'tag' if x == 0 else 'user')
    fig5 = plot_area_with_totals(
        df=df_5,
        date_col='created_at',
        group_col='type_user',
        time_granularity='W',
        cumulatif=True,
        min_date='2025-01-01',
        values_graph=True,
        objectif=None,
        title='Plans avec pilote'
    )
    st.plotly_chart(fig5, width='stretch')
    st.plotly_chart(indicator(df_5.nom.nunique(), 'Collectivités utilisant la feature'))

df_6 = load_df_plan_referent().copy()
if df_6.empty:
    st.info("Aucune donnée pour les référents. Voir `load_df_plan_referent()`.")
else:
    df_6['type_user'] = df_6.user_id.fillna(0).apply(lambda x: 'tag' if x == 0 else 'user')
    fig6 = plot_area_with_totals(
        df=df_6,
        date_col='created_at',
        group_col='type_user',
        time_granularity='W',
        cumulatif=True,
        min_date='2025-01-01',
        values_graph=True,
        objectif=None,
        title='Plans avec référent'
    )
    st.plotly_chart(fig6, width='stretch')
    st.plotly_chart(indicator(df_6.nom.nunique(), 'Collectivités utilisant la feature'))

st.header("Partages de fiches")
df_7 = load_df_sharing().copy()
if df_7.empty:
    st.info("Aucune donnée de partage. Voir `load_df_sharing()`.")
else:
    fig7 = plot_area_with_totals(
        df=df_7,
        date_col='created_at',
        group_col=False,
        time_granularity='W',
        cumulatif=True,
        min_date='2025-01-01',
        values_graph=True,
        objectif=None,
        title='Partages de fiches (1 valeur = 1 partage)'
    )
    st.plotly_chart(fig7, width='stretch')
    st.plotly_chart(indicator(df_7.collectivite_id.nunique(), 'Collectivités utilisant la feature'))


