import streamlit as st
import pandas as pd

from utils.data import load_df_pap_notes
from utils.plots import radar_spider_graph_plotly_with_comparison


st.title("🫡 Les champions de la semaine")

df_notes = load_df_pap_notes()

if df_notes.empty:
    st.info("Aucune donnée de notes. Alimentez `load_df_pap_notes()`.")
    st.stop()

# Conserver les deux dernières semaines disponibles
semaines = sorted(df_notes['semaine'].dropna().unique(), reverse=True)[:2]
df_2 = df_notes[df_notes['semaine'].isin(semaines)].copy()

if len(semaines) < 2:
    st.warning("Pas assez d'historique pour comparaison semaine N / N-1.")

df_pivot = df_2.pivot(index=['collectivite_id', 'plan_id'], columns='semaine', values='score')
if df_pivot.shape[1] >= 2:
    df_pivot['difference_score'] = df_pivot.iloc[:, 1] - df_pivot.iloc[:, 0]
    df_diff = df_pivot[['difference_score']].reset_index()
    top_rows = df_diff.sort_values(by='difference_score', ascending=False).head(5)

    for _, top_row in top_rows.iterrows():
        plan_id = top_row['plan_id']
        diff = top_row['difference_score']

        df_plan = df_2[df_2['plan_id'] == plan_id].sort_values(by='semaine', ascending=False)
        if len(df_plan) < 2:
            continue
        row = df_plan.iloc[0]
        row_precedente = df_plan.iloc[1]

        fig = radar_spider_graph_plotly_with_comparison(row, row_precedente, diff)
        st.plotly_chart(fig, use_container_width=False)
else:
    st.info("Données insuffisantes pour calculer la différence de score.")


