import streamlit as st
import pandas as pd
from streamlit_elements import elements, nivo, mui
from datetime import datetime

from utils.data import load_df_pap, load_df_typologie_fiche

# Configuration de la page
st.set_page_config(page_title="Expérimentation Nivo", page_icon="🪐", layout="wide")

st.title("🪐 Expérimentation Nivo :blue-badge[:material/experiment: Beta]")
st.markdown("Cette page permet d'expérimenter avec les différents graphiques Nivo.")

st.markdown("---")

# ==========================
# Chargement des données
# ==========================

@st.cache_data(ttl=3600)
def charger_donnees_pap():
    """Charge les données PAP."""
    return load_df_pap()

@st.cache_data(ttl=3600)
def charger_donnees_fiches():
    """Charge les données de typologie des fiches."""
    return load_df_typologie_fiche()

df_pap = charger_donnees_pap()
df_fiches = charger_donnees_fiches()

if df_pap.empty:
    st.warning("⚠️ Aucune donnée PAP disponible")
    st.stop()

if df_fiches.empty:
    st.warning("⚠️ Aucune donnée de fiches disponible")
    st.stop()

# ==========================
# TreeMap des plans
# ==========================

st.header("📖 Les PAP sur Territoire en Transition")

# Préparer les données pour le TreeMap
plan_counts = df_pap['nom_plan'].value_counts().reset_index()
plan_counts.columns = ['nom_plan', 'count']

# Convertir au format TreeMap Nivo
# Le format attendu est : { name, children: [{ name, value }, ...] }
treemap_data = {
    "name": "Plans",
    "children": [
        {
            "name": row['nom_plan'],
            "value": int(row['count'])
        }
        for _, row in plan_counts.iterrows()
    ]
}

# Afficher le TreeMap
with elements("treemap_plans"):
    with mui.Box(sx={"height": 500}):
        nivo.TreeMap(
            data=treemap_data,
            identity="name",
            value="value",
            valueFormat=".0f",
            margin={"top": 10, "right": 10, "bottom": 10, "left": 10},
            labelSkipSize=12,
            labelTextColor={"from": "color", "modifiers": [["darker", 1.8]]},
            parentLabelPosition="left",
            parentLabelTextColor={"from": "color", "modifiers": [["darker", 2]]},   
            borderColor={"from": "color", "modifiers": [["darker", 0.3]]},
            enableParentLabel=True,
            animate=True,
            motionConfig="gentle",
            theme={
                "text": {
                    "fontFamily": "Source Sans Pro, sans-serif",
                    "fontSize": 13,
                    "fill": "#31333F"
                },
                "labels": {
                    "text": {
                        "fontFamily": "Source Sans Pro, sans-serif",
                        "fontSize": 13,
                        "fill": "#ffffff"
                    }
                },
                "tooltip": {
                    "container": {
                        "background": "rgba(30, 30, 30, 0.95)",
                        "color": "#ffffff",
                        "fontSize": "13px",
                        "fontFamily": "Source Sans Pro, sans-serif",
                        "borderRadius": "4px",
                        "boxShadow": "0 2px 8px rgba(0,0,0,0.3)",
                        "padding": "8px 12px",
                        "border": "1px solid rgba(255, 255, 255, 0.1)"
                    }
                }
            }
        )

st.markdown("---")

# ==========================
# Calendar des fiches actions
# ==========================

st.header("📅 Création de fiches actions")

# Préparer les données pour le Calendar
# Convertir modified_at en datetime et extraire la date
df_fiches_calendar = df_fiches.copy()
df_fiches_calendar['modified_at'] = pd.to_datetime(df_fiches_calendar['modified_at'], errors='coerce')
df_fiches_calendar = df_fiches_calendar.dropna(subset=['modified_at'])
df_fiches_calendar['date'] = df_fiches_calendar['modified_at'].dt.date

# Compter le nombre de modifications par jour
daily_counts = df_fiches_calendar.groupby('date').size().reset_index()
daily_counts.columns = ['date', 'value']

# Convertir au format Calendar Nivo : [{ day: "2025-01-15", value: 42 }, ...]
calendar_data = [
    {
        "day": str(row['date']),
        "value": int(row['value'])
    }
    for _, row in daily_counts.iterrows()
]

# Déterminer la plage de dates
if not daily_counts.empty:
    min_date = '2024-01-01'
    max_date = daily_counts['date'].max()
    
    # Afficher le Calendar
    with elements("calendar_fiches"):
        with mui.Box(sx={"height": 600}):
            nivo.Calendar(
                data=calendar_data,
                from_=str(min_date),
                maxValue=100,
                to=str(max_date),
                emptyColor="#eeeeee",
                margin={"top": 40, "right": 40, "bottom": 40, "left": 40},
                yearSpacing=40,
                monthBorderColor="#ffffff",
                dayBorderWidth=2,
                dayBorderColor="#ffffff",
                theme={
                    "text": {
                        "fontFamily": "Source Sans Pro, sans-serif",
                        "fontSize": 12,
                        "fill": "#808495"
                    },
                    "tooltip": {
                        "container": {
                            "background": "rgba(30, 30, 30, 0.95)",
                            "color": "#ffffff",
                            "fontSize": "13px",
                            "fontFamily": "Source Sans Pro, sans-serif",
                            "borderRadius": "4px",
                            "boxShadow": "0 2px 8px rgba(0,0,0,0.3)",
                            "padding": "8px 12px",
                            "border": "1px solid rgba(255, 255, 255, 0.1)"
                        }
                    }
                }
            )
else:
    st.warning("⚠️ Aucune donnée de date disponible pour le calendrier")
