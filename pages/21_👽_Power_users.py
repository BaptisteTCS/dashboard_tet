import streamlit as st
import pandas as pd
from streamlit_elements import elements, nivo, mui

from utils.db import read_table

# Configuration de la page
st.set_page_config(page_title="Power users", page_icon="👽", layout="wide")

st.title("👽 Power users :blue-badge[:material/experiment: Beta]")

@st.cache_data(ttl=3600)
def load_data():
    return read_table('calendar_power_user')

@st.cache_data(ttl=3600)
def load_data_pap():
    return read_table('pap_date_passage')

df_calendar_power_user = load_data()
df_pap_date_passage = load_data_pap()

df_calendar_power_user.rename(columns={'page_clean': 'page'}, inplace=True)

# Filtre par collectivité
if 'nom' in df_calendar_power_user.columns:
    collectivites = sorted(df_calendar_power_user['nom'].dropna().unique())
    
    # Ajouter l'option "Toutes"
    options = ["Toutes"] + [c for c in collectivites]
    
    selected_collectivite = st.selectbox(
        "🏛️ Filtrer par collectivité",
        options=options,
        index=0
    )
    
    # Filtrer les données si une collectivité spécifique est sélectionnée
    if selected_collectivite != "Toutes":
        df_calendar = df_calendar_power_user[
            df_calendar_power_user['nom'] == selected_collectivite
        ].copy()
    else:
        df_calendar = df_calendar_power_user.copy()
else:
    df_calendar = df_calendar_power_user.copy()
    st.warning("⚠️ La colonne 'nom' n'existe pas dans les données")

st.markdown("---")

# Vérifier si la colonne 'page' existe
if 'page' not in df_calendar.columns:
    st.error("⚠️ La colonne 'page' n'existe pas dans les données")
    st.stop()

# Récupérer les valeurs uniques de la colonne 'page'
pages = sorted(df_calendar['page'].dropna().unique())

if len(pages) == 0:
    st.warning("⚠️ Aucune page trouvée dans les données")
    st.stop()

# Préparer les données communes
# S'assurer que 'jour' est au format datetime
df_calendar['jour'] = pd.to_datetime(df_calendar['jour'], errors='coerce')
df_calendar = df_calendar.dropna(subset=['jour'])

# Supprimer le timezone si présent
if df_calendar['jour'].dt.tz is not None:
    df_calendar['jour'] = df_calendar['jour'].dt.tz_localize(None)

# Extraire uniquement la date (format YYYY-MM-DD)
df_calendar['date_str'] = df_calendar['jour'].dt.strftime('%Y-%m-%d')

# Afficher d'abord le calendrier "All" avec toutes les données
st.header("📅 Activité sur l'app")

# Compter le nombre de lignes par jour pour toutes les pages
daily_counts_all = df_calendar.groupby('date_str')['email'].nunique().reset_index()
daily_counts_all.columns = ['date', 'value']

# Convertir au format Calendar Nivo
calendar_data_all = [
    {
        "day": (pd.to_datetime(row['date']) + pd.Timedelta(days=1)).strftime('%Y-%m-%d'),
        "value": int(row['value'])
    }
    for _, row in daily_counts_all.iterrows()
]

# Déterminer la plage de dates
if not daily_counts_all.empty:
    min_date_all = (pd.to_datetime(daily_counts_all['date'].min()) + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
    max_date_all = (pd.to_datetime(daily_counts_all['date'].max()) + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Afficher le Calendar All
    with elements("calendar_all"):
        with mui.Box(sx={"height": 300}):
            nivo.Calendar(
                data=calendar_data_all,
                from_=min_date_all,
                to=max_date_all,
                emptyColor="#eeeeee",
                colors=['#FFFFCC', '#FEEA9A','#FECD69','#FDA245','#FC6831','#EA2920','#C10324','#800026'],
                margin={"top": 40, "right": 40, "bottom": 40, "left": 40},
                yearSpacing=40,
                monthBorderColor="#ffffff",
                dayBorderWidth=2,
                dayBorderColor="#ffffff",
                legends=[
                    {
                        "anchor": "bottom-right",
                        "direction": "row",
                        "translateY": 36,
                        "itemCount": 4,
                        "itemWidth": 42,
                        "itemHeight": 36,
                        "itemsSpacing": 14,
                        "itemDirection": "right-to-left"
                    }
                ],
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
    st.info("Aucune donnée disponible")

st.markdown("---")

# Afficher un calendrier pour chaque page (pages sélectionnées avec emojis personnalisés)
page_emojis = {
    'plans': '📋',
    'referentiel': '📚',
    'indicateurs': '🔍'
}

for page, emoji in page_emojis.items():
    st.header(f"{emoji} {page}")
    
    # Filtrer les données pour cette page
    df_page = df_calendar[df_calendar['page'] == page].copy()
    
    if df_page.empty:
        st.info(f"Aucune donnée pour la page {page}")
        continue
    
    # Compter le nombre de lignes par jour pour cette page
    daily_counts = df_page.groupby('date_str').size().reset_index()
    daily_counts.columns = ['date', 'value']
    
    # Convertir au format Calendar Nivo : [{ day: "2025-01-15", value: 42 }, ...]
    # Ajouter +1 jour pour corriger le décalage de timezone
    calendar_data = [
        {
            "day": (pd.to_datetime(row['date']) + pd.Timedelta(days=1)).strftime('%Y-%m-%d'),
            "value": int(row['value'])
        }
        for _, row in daily_counts.iterrows()
    ]
    
    # Déterminer la plage de dates (avec le même décalage +1)
    if not daily_counts.empty:
        min_date = (pd.to_datetime(daily_counts['date'].min()) + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
        max_date = (pd.to_datetime(daily_counts['date'].max()) + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
        
        # Afficher le Calendar
        with elements(f"calendar_{page.replace(' ', '_')}"):
            with mui.Box(sx={"height": 300}):
                nivo.Calendar(
                    data=calendar_data,
                    from_=min_date,
                    to=max_date,
                    emptyColor="#eeeeee",
                    colors=['#FFFFCC', '#FEEA9A','#FECD69','#FDA245','#FC6831','#EA2920','#C10324','#800026'],
                    margin={"top": 40, "right": 40, "bottom": 40, "left": 40},
                    yearSpacing=40,
                    monthBorderColor="#ffffff",
                    dayBorderWidth=2,
                    dayBorderColor="#ffffff",
                    legends=[
                        {
                            "anchor": "bottom-right",
                            "direction": "row",
                            "translateY": 36,
                            "itemCount": 4,
                            "itemWidth": 42,
                            "itemHeight": 36,
                            "itemsSpacing": 14,
                            "itemDirection": "right-to-left"
                        }
                    ],
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
        st.info(f"Aucune donnée de date disponible pour la page {page}")
    
    st.markdown("---")

# === SECTION PAP : Pie Charts par type d'import ===
st.header("📊 Plans d'action (PAP) - Passages après 2025-01-01")

# Filtrer les données PAP après le 1er janvier 2025
df_pap_date_passage['passage_pap'] = pd.to_datetime(df_pap_date_passage['passage_pap'], errors='coerce')
df_pap_filtered = df_pap_date_passage[df_pap_date_passage['passage_pap'] > '2025-01-01'].copy()

if df_pap_filtered.empty:
    st.warning("⚠️ Aucune donnée PAP après le 2025-01-01")
else:
    # Vérifier que les colonnes nécessaires existent
    if 'import' not in df_pap_filtered.columns or 'nom_plan' not in df_pap_filtered.columns:
        st.error("⚠️ Les colonnes 'import' ou 'nom_plan' n'existent pas dans les données")
    else:
        # Créer deux colonnes pour afficher les charts côte à côt
        
        # === PIE CHART 1 : Import = Autonome ===
        st.subheader("🟢 Import Autonome")
        df_autonome = df_pap_filtered[df_pap_filtered['import'] == 'Autonome']
        
        if df_autonome.empty:
            st.info("Aucune donnée pour Import = Autonome")
        else:
            # Compter par nom_plan
            counts_autonome = df_autonome.groupby('nom_plan').size().reset_index(name='count')
            
            # Convertir au format Nivo Pie
            pie_data_autonome = [
                {
                    "id": row['nom_plan'] if pd.notna(row['nom_plan']) else 'Sans nom',
                    "label": row['nom_plan'] if pd.notna(row['nom_plan']) else 'Sans nom',
                    "value": int(row['count'])
                }
                for _, row in counts_autonome.iterrows()
            ]
            
            # Afficher le total
            total_autonome = df_autonome.shape[0]
            st.caption(f"Total : {total_autonome} passages")
            
            # Afficher le Pie Chart
            with elements("pie_autonome"):
                with mui.Box(sx={"height": 400}):
                    nivo.Pie(
                        data=pie_data_autonome,
                        margin={"top": 40, "right": 80, "bottom": 80, "left": 80},
                        innerRadius=0.5,
                        padAngle=0.7,
                        cornerRadius=3,
                        activeOuterRadiusOffset=8,
                        borderWidth=1,
                        borderColor={"from": "color", "modifiers": [["darker", 0.2]]},
                        arcLinkLabelsSkipAngle=10,
                        arcLinkLabelsTextColor="#333333",
                        arcLinkLabelsThickness=2,
                        arcLinkLabelsColor={"from": "color"},
                        arcLabelsSkipAngle=10,
                        arcLabelsTextColor={"from": "color", "modifiers": [["darker", 2]]},
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
        
        # === PIE CHART 2 : Import = Importé ===
        st.subheader("🔵 Import Importé")
        df_importe = df_pap_filtered[df_pap_filtered['import'] == 'Importé']
        
        if df_importe.empty:
            st.info("Aucune donnée pour Import = Importé")
        else:
            # Compter par nom_plan
            counts_importe = df_importe.groupby('nom_plan').size().reset_index(name='count')
            
            # Convertir au format Nivo Pie
            pie_data_importe = [
                {
                    "id": row['nom_plan'] if pd.notna(row['nom_plan']) else 'Sans nom',
                    "label": row['nom_plan'] if pd.notna(row['nom_plan']) else 'Sans nom',
                    "value": int(row['count'])
                }
                for _, row in counts_importe.iterrows()
            ]
            
            # Afficher le total
            total_importe = df_importe.shape[0]
            st.caption(f"Total : {total_importe} passages")
            
            # Afficher le Pie Chart
            with elements("pie_importe"):
                with mui.Box(sx={"height": 400}):
                    nivo.Pie(
                        data=pie_data_importe,
                        margin={"top": 40, "right": 80, "bottom": 80, "left": 80},
                        innerRadius=0.5,
                        padAngle=0.7,
                        cornerRadius=3,
                        activeOuterRadiusOffset=8,
                        borderWidth=1,
                        borderColor={"from": "color", "modifiers": [["darker", 0.2]]},
                        arcLinkLabelsSkipAngle=10,
                        arcLinkLabelsTextColor="#333333",
                        arcLinkLabelsThickness=2,
                        arcLinkLabelsColor={"from": "color"},
                        arcLabelsSkipAngle=10,
                        arcLabelsTextColor={"from": "color", "modifiers": [["darker", 2]]},
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

