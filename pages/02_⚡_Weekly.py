import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from streamlit_elements import elements, nivo, mui

from utils.data import load_df_pap_notes
from utils.plots import prepare_radar_data_nivo

from utils.data import (
    load_df_pap, 
    load_df_collectivite,
    load_df_pap_notes
)

from utils.db import (
    read_table
)

# Solution compatible avec pandas.read_sql_query et SQL natif PostgreSQL (pas de :param dans la requête, on place directement la valeur formatée)
fa = read_table('fa_last_week')

df_notes = load_df_pap_notes()

st.set_page_config(layout="wide")

# === TOGGLE THEME SOMBRE ===
col_title, col_toggle = st.columns([8, 1])

with col_title:
    st.title("⚡ Weekly")
    st.markdown("Les info clés de la semaine.")
with col_toggle:
    st.space("medium")
    dark_mode = st.toggle("🌙", value=False)

# Définition des thèmes Nivo
theme_clair = {
    "text": {
        "fontFamily": "Source Sans Pro, sans-serif",
        "fontSize": 13,
        "fill": "#31333F"
    },
    "labels": {
        "text": {
            "fontFamily": "Source Sans Pro, sans-serif",
            "fontSize": 13,
            "fill": "#000000"
        }
    },
    "tooltip": {
        "container": {
            "background": "rgba(255, 255, 255, 0.95)",
            "color": "#31333F",
            "fontSize": "13px",
            "fontFamily": "Source Sans Pro, sans-serif",
            "borderRadius": "4px",
            "boxShadow": "0 2px 8px rgba(0,0,0,0.15)",
            "padding": "8px 12px",
            "border": "1px solid rgba(0, 0, 0, 0.1)"
        }
    }
}

theme_sombre = {
    "text": {
        "fontFamily": "Source Sans Pro, sans-serif",
        "fontSize": 13,
        "fill": "#FFFFFF"
    },
    "labels": {
        "text": {
            "fontFamily": "Source Sans Pro, sans-serif",
            "fontSize": 13,
            "fill": "#FFFFFF"
        }
    },
    "tooltip": {
        "container": {
            "background": "rgba(30, 30, 30, 0.95)",
            "color": "#FFFFFF",
            "fontSize": "13px",
            "fontFamily": "Source Sans Pro, sans-serif",
            "borderRadius": "4px",
            "boxShadow": "0 2px 8px rgba(0,0,0,0.3)",
            "padding": "8px 12px",
            "border": "1px solid rgba(255, 255, 255, 0.1)"
        }
    }
}

# Sélection du thème actif
theme_actif = theme_sombre if dark_mode else theme_clair

# Définition des thèmes Radar Nivo
theme_radar_clair = {
    "text": {
        "fontFamily": "Source Sans Pro, sans-serif",
        "fontSize": 13,
        "fill": "#31333F"
    },
    "labels": {
        "text": {
            "fontFamily": "Source Sans Pro, sans-serif",
            "fontSize": 16,
            "fill": "#31333F"
        }
    },
    "grid": {
        "line": {
            "stroke": "#e0e0e0",
            "strokeWidth": 1,
            "strokeOpacity": 0.8
        }
    },
    "legends": {
        "text": {
            "fontFamily": "Source Sans Pro, sans-serif",
            "fontSize": 12,
            "fill": "#31333F"
        }
    },
    "tooltip": {
        "container": {
            "background": "rgba(255, 255, 255, 0.95)",
            "color": "#31333F",
            "fontSize": "13px",
            "fontFamily": "Source Sans Pro, sans-serif",
            "borderRadius": "4px",
            "boxShadow": "0 2px 8px rgba(0,0,0,0.15)",
            "padding": "8px 12px",
            "border": "1px solid rgba(0, 0, 0, 0.1)"
        }
    }
}

theme_radar_sombre = {
    "text": {
        "fontFamily": "Source Sans Pro, sans-serif",
        "fontSize": 13,
        "fill": "#FFFFFF"
    },
    "labels": {
        "text": {
            "fontFamily": "Source Sans Pro, sans-serif",
            "fontSize": 16,
            "fill": "#FFFFFF"
        }
    },
    "grid": {
        "line": {
            "stroke": "#4a4a4a",
            "strokeWidth": 1,
            "strokeOpacity": 0.3
        }
    },
    "legends": {
        "text": {
            "fontFamily": "Source Sans Pro, sans-serif",
            "fontSize": 12,
            "fill": "#FFFFFF"
        }
    },
    "tooltip": {
        "container": {
            "background": "rgba(30, 30, 30, 0.95)",
            "color": "#FFFFFF",
            "fontSize": "13px",
            "fontFamily": "Source Sans Pro, sans-serif",
            "borderRadius": "4px",
            "boxShadow": "0 2px 8px rgba(0,0,0,0.3)",
            "padding": "8px 12px",
            "border": "1px solid rgba(255, 255, 255, 0.1)"
        }
    }
}

# Sélection du thème radar actif
theme_radar_actif = theme_radar_sombre if dark_mode else theme_radar_clair

# === CHARGEMENT DES DONNÉES ===
df_pap = load_df_pap()
df_ct = load_df_collectivite()

if df_pap.empty:
    st.info("Aucune donnée. Branchez vos sources dans `utils/data.py`.")
    st.stop()

# Jointure avec les collectivités
df_pap_enrichi = pd.merge(df_pap, df_ct, on='collectivite_id', how='left')

# Préparation des dates
df_pap_enrichi['passage_pap'] = pd.to_datetime(df_pap_enrichi['passage_pap'], errors='coerce').dt.tz_localize(None)
df_pap_enrichi['semaine_pap'] = df_pap_enrichi['passage_pap'].dt.to_period('W').dt.to_timestamp()

# === IDENTIFICATION DES SEMAINES S-1 ET S-2 ===
semaines_disponibles = sorted(df_pap_enrichi['semaine_pap'].dropna().unique(), reverse=True)

if len(semaines_disponibles) < 2:
    st.warning("⚠️ Pas assez de données pour comparer S-1 et S-2.")
    st.stop()

# S-1 = dernière semaine, S-2 = avant-dernière semaine
s1 = semaines_disponibles[0]
s2 = semaines_disponibles[1]

s1_str = pd.to_datetime(s1).strftime("%d/%m/%Y")
s2_str = pd.to_datetime(s2).strftime("%d/%m/%Y")

st.markdown("---")

# === DONNÉES S-1 ET S-2 ===
df_s1 = df_pap_enrichi[df_pap_enrichi['semaine_pap'] == s1].copy()
df_s2 = df_pap_enrichi[df_pap_enrichi['semaine_pap'] == s2].copy()

# Nouveaux PAP en S-1
nouveaux_pap_s1 = len(df_s1)
nouveaux_pap_s2 = len(df_s2)
diff_pap = nouveaux_pap_s1 - nouveaux_pap_s2

# Nouvelles collectivités PAP en S-1 (qui n'avaient jamais eu de PAP avant)
# Pour S-1 : collectivités ayant un PAP avant S-1
ct_avant_s1 = df_pap_enrichi[df_pap_enrichi['semaine_pap'] < s1]['collectivite_id'].unique()
ct_s1 = df_s1['collectivite_id'].unique()
nouvelles_ct_s1 = len([ct for ct in ct_s1 if ct not in ct_avant_s1])

# Pour S-2 : collectivités ayant un PAP avant S-2
ct_avant_s2 = df_pap_enrichi[df_pap_enrichi['semaine_pap'] < s2]['collectivite_id'].unique()
ct_s2 = df_s2['collectivite_id'].unique()
nouvelles_ct_s2 = len([ct for ct in ct_s2 if ct not in ct_avant_s2])

diff_ct = nouvelles_ct_s1 - nouvelles_ct_s2

# Répartition Import/Autonome
if 'import' in df_s1.columns and 'import' in df_s2.columns:
    nb_importes_s1 = len(df_s1[df_s1['import'] == 'Importé'])
    nb_importes_s2 = len(df_s2[df_s2['import'] == 'Importé'])
    diff_importes = nb_importes_s1 - nb_importes_s2
    
    nb_autonomes_s1 = len(df_s1[df_s1['import'] == 'Autonome'])
    nb_autonomes_s2 = len(df_s2[df_s2['import'] == 'Autonome'])
    diff_autonomes = nb_autonomes_s1 - nb_autonomes_s2
else:
    nb_importes_s1 = 0
    nb_autonomes_s1 = 0
    diff_importes = 0
    diff_autonomes = 0

# === CALCUL DES ÉVOLUTIONS SUR 2 MOIS ===
# Prendre les 8 dernières semaines (environ 2 mois)
nb_semaines_evolution = min(8, len(semaines_disponibles))
semaines_evolution = semaines_disponibles[:nb_semaines_evolution][::-1]  # Ordre chronologique

# Initialisation des listes d'évolution
evolution_pap = []
evolution_ct = []
evolution_importes = []
evolution_autonomes = []

# Calcul pour chaque semaine
for semaine in semaines_evolution:
    df_semaine = df_pap_enrichi[df_pap_enrichi['semaine_pap'] == semaine]
    
    # Nouveaux PAP
    evolution_pap.append(len(df_semaine))
    
    # Nouvelles collectivités (jamais vu avant)
    ct_avant_semaine = df_pap_enrichi[df_pap_enrichi['semaine_pap'] < semaine]['collectivite_id'].unique()
    ct_semaine = df_semaine['collectivite_id'].unique()
    nouvelles_ct_semaine = len([ct for ct in ct_semaine if ct not in ct_avant_semaine])
    evolution_ct.append(nouvelles_ct_semaine)
    
    # PAP Importés et Autonomes
    if 'import' in df_semaine.columns:
        evolution_importes.append(len(df_semaine[df_semaine['import'] == 'Importé']))
        evolution_autonomes.append(len(df_semaine[df_semaine['import'] == 'Autonome']))
    else:
        evolution_importes.append(0)
        evolution_autonomes.append(0)

st.badge("Clés", icon=":material/key:", color="green")

# === INDICATEURS CLÉS ===
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Nouveaux PAP",
        nouveaux_pap_s1,
        delta=f"{diff_pap:+d}",
        delta_color="normal",
        border = True,
        chart_type="line",
        chart_data=evolution_pap
    )

with col2:
    st.metric(
        "Nouvelles collectivités PAP",
        nouvelles_ct_s1,
        delta=f"{diff_ct:+d}",
        delta_color="normal",
        border = True,
        chart_type="line",
        chart_data=evolution_ct
    )

with col3:
    if 'import' in df_s1.columns:
        st.metric(
            "PAP Importés",
            nb_importes_s1,
            delta=f"{diff_importes:+d}",
            delta_color="normal",
            border = True,
            chart_type="line",
            chart_data=evolution_importes
        )
    else:
        st.metric("PAP Importés", "N/A")

with col4:
    if 'import' in df_s1.columns:
        st.metric(
            "PAP Autonomes",
            nb_autonomes_s1,
            delta=f"{diff_autonomes:+d}",
            delta_color="normal",
            border = True,
            chart_type="line",
            chart_data=evolution_autonomes
        )
    else:
        st.metric("PAP Autonomes", "N/A")

# === GRAPHIQUES DE RÉPARTITION ===
tab1, tab2, tab3, tab4 = st.tabs(["🆕 Plans", "🎉 Nouvelles collectivités", "💪 Champions", "📢 Fiches actions"])

with tab1:
    if not df_s1.empty and 'nom_plan' in df_s1.columns:
        # Préparer les données pour le Pie Chart Nivo
        pap_par_plan_s1 = df_s1['nom_plan'].value_counts().reset_index()
        pap_par_plan_s1.columns = ['Type de plan', 'Nombre']
        
        # Convertir au format Nivo Pie : [{ "id": "label", "value": number }, ...]
        pie_data = [
            {
                "id": row['Type de plan'],
                "label": row['Type de plan'],
                "value": int(row['Nombre'])
            }
            for _, row in pap_par_plan_s1.iterrows()
        ]
        
        # Afficher le Pie Chart Nivo avec thème par défaut
        with elements("pie_plans"):
            with mui.Box(sx={"height": 450}):
                nivo.Pie(
                    data=pie_data,
                    margin={"top": 40, "right": 80, "bottom": 80, "left": 80},
                    innerRadius=0.5,
                    padAngle=0.7,
                    cornerRadius=3,
                    activeOuterRadiusOffset=8,
                    borderWidth=1,
                    borderColor={"from": "color", "modifiers": [["darker", 0.2]]},
                    arcLinkLabelsSkipAngle=10,
                    arcLinkLabelsTextColor=theme_actif["text"]["fill"],
                    arcLinkLabelsThickness=2,
                    arcLinkLabelsColor={"from": "color"},
                    arcLabelsSkipAngle=10,
                    arcLabelsTextColor={"from": "color", "modifiers": [["darker", 2]]},
                    enableArcLabels=True,
                    enableArcLinkLabels=True,
                    theme=theme_actif
                )
    else:
        st.info("Pas de données pour S-1")

    st.dataframe(df_s1[['nom', 'nom_plan', 'type_collectivite', 'population_totale', 'import']].sort_values(by='population_totale', ascending=False), hide_index=True)
        
with tab2: 
    # Ne garder que les collectivités qui n'avaient jamais eu de PAP avant S-1
    df_s1_nouvelles = df_s1[df_s1['collectivite_id'].isin([ct for ct in ct_s1 if ct not in ct_avant_s1])].copy()

    # Collectivités uniques de S-1 (seulement les nouvelles)
    collectivites_s1 = df_s1_nouvelles.groupby('collectivite_id').agg({
        'nom': 'first',
        'type_collectivite': 'first',
        'population_totale': 'first',
        'import': 'first' if 'import' in df_s1_nouvelles.columns else lambda x: 'N/A',
        'nom_plan': lambda x: ', '.join(x.unique())  # Liste des plans
    }).reset_index()

    collectivites_s1.columns = [
        'ID Collectivité', 'Nom', 'Type', 'Population', 'Statut Import', 'Plans'
    ]

    # Tri par population décroissante
    collectivites_s1 = collectivites_s1.sort_values(by='Population', ascending=False)
    collectivites_s1['Population'] = collectivites_s1['Population'].fillna(0).astype(int)

    # Affichage du tableau
    st.dataframe(
        collectivites_s1[['Nom', 'Plans', 'Statut Import', 'Type', 'Population']],
        hide_index=True
    )

with tab3:
    semaines = sorted(df_notes['semaine'].dropna().unique(), reverse=True)[:2]
    df_2 = df_notes[df_notes['semaine'].isin(semaines)].copy()

    # Calcul des différences de scores
    df_pivot = df_2.pivot(index=['collectivite_id', 'plan_id'], columns='semaine', values='score')

    if df_pivot.shape[1] >= 2:
        df_pivot['difference_score'] = df_pivot.iloc[:, 1] - df_pivot.iloc[:, 0]
        df_diff = df_pivot[['difference_score']].reset_index()
        top_rows = df_diff.sort_values(by='difference_score', ascending=False).head(10)
        
        if top_rows.empty or top_rows['difference_score'].max() <= 0:
            st.info("ℹ️ Aucune progression significative détectée cette semaine.")
            st.stop()
        
        # Affichage en galerie (2 colonnes)
        rank = 1
        for idx in range(0, len(top_rows), 2):
            cols = st.columns(2)
            
            for col_idx, col in enumerate(cols):
                row_idx = idx + col_idx
                if row_idx < len(top_rows):
                    top_row = top_rows.iloc[row_idx]
                    plan_id = top_row['plan_id']
                    diff = top_row['difference_score']
                    
                    df_plan = df_2[df_2['plan_id'] == plan_id].sort_values(by='semaine', ascending=False)
                    if len(df_plan) < 2:
                        continue
                        
                    row = df_plan.iloc[0]
                    row_precedente = df_plan.iloc[1]
                    
                    with col:
                        
                        # Header avec badge et infos (tronqué pour éviter le décalage)
                        collectivite_nom = row['nom_ct']
                        plan_nom = row['nom']
                        
                        # Tronquer si trop long pour éviter les décalages
                        titre_complet = f"{collectivite_nom}"
                        if len(titre_complet) > 50:
                            titre_affiche = titre_complet[:40] + "..."
                        else:
                            titre_affiche = titre_complet
                        
                        st.markdown(f"#### :green-badge[{rank}] {titre_affiche}")
                        
                        # Metrics
                        col_metric1, col_metric2 = st.columns(2)
                        with col_metric1:
                            st.metric(
                                "Score actuel",
                                f"{round(row['score'], 2)}",
                                delta=f"+{round(diff, 2)}"
                            )
                        with col_metric2:
                            st.metric(
                                "Score précédent",
                                f"{round(row_precedente['score'], 2)}"
                            )
                        
                        # Infos collectivité
                        with st.expander("ℹ️ Détails", expanded=False):
                            st.write(f"**Collectivité :** {row['nom_ct']}")
                            st.write(f"**Plan :** {row['nom']}")
                            st.write(f"**Type :** {row.get('type_collectivite', 'N/A')}")
                            st.write(f"**Région :** {row.get('region_name', 'N/A')}")
                            st.write(f"**Population :** {int(row.get('population_totale', 0)):,} habitants".replace(',', ' '))
                        
                        # Graphe radar avec comparaison Nivo
                        radar_data = prepare_radar_data_nivo(row, row_precedente)
                        
                        with elements(f"radar_champion_{plan_id}_{rank}"):
                            with mui.Box(sx={"height": 500}):
                                nivo.Radar(
                                    data=radar_data,
                                    keys=["Actuelle", "Précédente"],
                                    indexBy="taste",
                                    maxValue=5,
                                    margin={"top": 70, "right": 80, "bottom": 40, "left": 80},
                                    curve="linearClosed",
                                    borderWidth=2,
                                    borderColor={"from": "color"},
                                    gridLevels=5,
                                    gridShape="circular",
                                    gridLabelOffset=20,
                                    enableDots=True,
                                    dotSize=6,
                                    dotColor={"theme": "background"},
                                    dotBorderWidth=2,
                                    dotBorderColor={"from": "color"},
                                    enableDotLabel=False,
                                    colors=["#ffc121", "#999999"],
                                    fillOpacity=0.5,
                                    blendMode="multiply",
                                    animate=True,
                                    motionConfig="wobbly",
                                    isInteractive=True,
                                    theme=theme_radar_actif,
                                    legends=[
                                        {
                                            "anchor": "top-left",
                                            "direction": "column",
                                            "translateX": -50,
                                            "translateY": -40,
                                            "itemWidth": 80,
                                            "itemHeight": 20,
                                            "itemTextColor": "#808495",
                                            "symbolSize": 12,
                                            "symbolShape": "circle",
                                        }
                                    ]
                                )
                        
                        st.markdown("---")
                        
                    rank += 1

with tab4:
    st.dataframe(fa, hide_index=True)
    