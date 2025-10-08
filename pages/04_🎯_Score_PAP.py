import streamlit as st
import pandas as pd

from utils.data import load_df_pap_notes
from utils.plots import radar_spider_graph_plotly


st.title("🎯 Score des PAP")

df_notes = load_df_pap_notes().copy()

if df_notes.empty:
    st.info("Aucune note disponible. Renseignez `load_df_pap_notes()`.")
    st.stop()

# Conserver la dernière note par plan
pap_note = df_notes.sort_values(by='semaine', ascending=False).drop_duplicates(subset=['plan_id'], keep='first').copy()

st.write("Sélectionnez un plan pour afficher le radar des scores.")
plans = pap_note['plan_id'].unique().tolist()
plan_id = st.selectbox("Plan", options=plans)

row = pap_note[pap_note['plan_id'] == plan_id].iloc[0]
fig = radar_spider_graph_plotly(row)
st.plotly_chart(fig, use_container_width=False)


