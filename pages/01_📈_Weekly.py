import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from utils.data import load_df_pap


st.title("🌈 Nouveaux PAP – Hebdo")

df_pap = load_df_pap()

if df_pap.empty:
    st.info("Aucune donnée. Branchez vos sources dans `utils/data.py`.")
    st.stop()

df_pap['passage_pap'] = pd.to_datetime(df_pap['passage_pap'], errors='coerce').dt.tz_localize(None)
df_pap['semaine_pap'] = df_pap['passage_pap'].dt.to_period('W').dt.to_timestamp()

pap_par_semaine = df_pap.groupby('semaine_pap').size().sort_index()
pap_cumule = pap_par_semaine.cumsum()

if pap_cumule.empty:
    st.info("Pas de dates valides pour calculer l'indicateur.")
    st.stop()

semaine_actuelle = pap_cumule.index.max()
semaine_precedente = semaine_actuelle - pd.Timedelta(weeks=1)

total_actuel = int(pap_cumule.loc[semaine_actuelle])
total_precedent = int(pap_cumule.get(semaine_precedente, 0))

fig = go.Figure()
fig.add_trace(go.Indicator(
    mode="number+delta",
    value=total_actuel,
    delta={'reference': total_precedent, 'relative': False, 'position': "top", 'font': {'size': 20}},
    number={'valueformat': 'd', 'font': {'size': 40}}
))
fig.update_layout(width=200, height=140, margin=dict(l=0, r=0, t=0, b=0))

st.plotly_chart(fig, use_container_width=False)

# Stack bar des nouveaux PAP par plan sur la dernière semaine
df_bar = (
    df_pap[df_pap["passage_pap"] > semaine_actuelle]
    .groupby("nom_plan")["plan"].count()
    .sort_values(ascending=False)
    .reset_index()
    .rename(columns={"plan": "count"})
)

if not df_bar.empty:
    fig_bar = go.Figure()
    fig_bar.add_bar(x=["Nouveaux PAP"], y=[df_bar.loc[0, "count"]], name=str(df_bar.loc[0, "nom_plan"]))
    for i in range(1, len(df_bar)):
        fig_bar.add_bar(x=["Nouveaux PAP"], y=[df_bar.loc[i, "count"]], name=str(df_bar.loc[i, "nom_plan"]))
    fig_bar.update_layout(barmode="stack", height=300, width=500, showlegend=True, xaxis_showticklabels=False)
    st.plotly_chart(fig_bar, use_container_width=False)
else:
    st.write("Aucune donnée pour la période sélectionnée")


