import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import text
from streamlit_elements import elements, nivo, mui
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta

from utils.db import (
    get_engine_prod, read_table
)

# On cache toutes les données pour optimiser les performances
@st.cache_resource(ttl="2d")
def load_data():
    df_ct_actives = read_table('ct_actives')
    df_ct_niveau = read_table('ct_niveau')
    df_ct_users_actifs = read_table('user_actifs_ct_mois')
    df_fap_et_no_fap = read_table('fap_et_no_fap')  
    return df_ct_actives, df_ct_niveau, df_ct_users_actifs, df_fap_et_no_fap

#Chargement des données
df_ct_actives, df_ct_niveau, df_ct_users_actifs, df_fap_et_no_fap = load_data() 

#Thème Nivo
theme_actif = {
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

#Config page
st.set_page_config(layout="wide")
st.title("🐍 Dashboard interne")
st.markdown('---')

# ===============================================
# === SELECTEUR DE REGION ET DEPARTEMENT ========
# ===============================================

st.badge("Vue d'ensemble", icon=":material/home:", color="green")

selects = st.columns(2)
with selects[0]:
    regions = ["Toutes"] + sorted(df_ct_actives["region_name"].dropna().unique().tolist())
    selected_region = st.selectbox("Région", options=regions, index=0)

with selects[1]:
    # Filtrer les départements selon la région sélectionnée
    if selected_region == "Toutes":
        departements = ["Tous"] + sorted(df_ct_actives["departement_name"].dropna().unique().tolist())
    else:
        departements = ["Tous"] + sorted(df_ct_actives[df_ct_actives["region_name"] == selected_region]["departement_name"].dropna().unique().tolist())
    selected_departement = st.selectbox("Département", options=departements, index=0)

st.markdown("*La sélection d'un territoire s'appliquera à toute la page. Les deltas ci-dessous sont les collectivités activées au cours du dernier mois.*")

# ===============================================
# === Nombre de collectivités par catégorie =====
# ===============================================

df_ct_actives_selected = df_ct_actives.copy()
if selected_region != "Toutes":
    df_ct_actives_selected = df_ct_actives_selected[df_ct_actives_selected["region_name"] == selected_region]
if selected_departement != "Tous":
    df_ct_actives_selected = df_ct_actives_selected[df_ct_actives_selected["departement_name"] == selected_departement]

ordre_prioritaire = ["EPCI", "Syndicats", "PETR", "Communes"]

cats = sorted(
    df_ct_actives_selected["categorie"].dropna().unique(),
    key=lambda c: ordre_prioritaire.index(c)
    if c in ordre_prioritaire
    else len(ordre_prioritaire)
)

df_ct_actives_selected["date_activation"] = pd.to_datetime(df_ct_actives_selected["date_activation"])


max_cols = 6
for row_start in range(0, len(cats), max_cols):
    row_cats = cats[row_start:row_start + max_cols]
    cols = st.columns(len(row_cats))

    for col, cat in zip(cols, row_cats):
        with col:
            df_cat = df_ct_actives_selected[df_ct_actives_selected["categorie"] == cat]
            st.metric(
                cat,
                int(df_cat.shape[0]),
                delta=df_cat[df_cat.date_activation > (datetime.now(timezone.utc) - timedelta(days=30))].shape[0]
            )

# ===================================================
# === Evolution des collectivités par catégorie =====
# ===================================================


# Calculer le nombre cumulé par mois et catégorie
df_ct_actives_selected['mois'] = df_ct_actives_selected['date_activation'].dt.to_period('M')
df_evolution = df_ct_actives_selected.groupby(['mois', 'categorie']).size().reset_index(name='nb_ct')
df_evolution['nb_ct_cumule'] = df_evolution.groupby('categorie')['nb_ct'].cumsum()

all_mois = sorted(df_ct_actives_selected['mois'].dropna().unique())
all_categories = df_ct_actives_selected['categorie'].dropna().unique()

# Vérifier si des données sont disponibles
if len(all_mois) == 0:
    st.info("Aucune donnée disponible pour les filtres sélectionnés.")
else:
    # Calculer le total au dernier mois pour chaque catégorie (pour le tri)
    dernier_mois = max(all_mois)
    totaux_dernier_mois = {}
    for cat in all_categories:
        df_cat = df_evolution[df_evolution['categorie'] == cat]
        if not df_cat.empty:
            # Prendre la valeur cumulative au dernier mois disponible pour cette catégorie
            totaux_dernier_mois[cat] = df_cat['nb_ct_cumule'].iloc[-1]
        else:
            totaux_dernier_mois[cat] = 0

    # Trier les catégories par ordre décroissant (le plus grand en bas du stack = premier dans la liste)
    categories_triees = sorted(all_categories, key=lambda c: totaux_dernier_mois.get(c, 0), reverse=True)

    # Préparer les données pour le graphique Nivo (une série par catégorie, avec les trous bouchés)
    area_data_ct_evolution = []
    for cat in categories_triees:
        df_filtered = df_evolution[df_evolution['categorie'] == cat].copy()
        if not df_filtered.empty:
            # Créer un dataframe avec tous les mois
            df_all_mois = pd.DataFrame({'mois': all_mois})
            # Merger avec les données existantes
            df_complete = df_all_mois.merge(df_filtered[['mois', 'nb_ct_cumule']], on='mois', how='left')
            # Remplir les trous avec la valeur précédente (forward fill), puis 0 pour les premiers mois sans données
            df_complete['nb_ct_cumule'] = df_complete['nb_ct_cumule'].ffill().fillna(0).astype(int)
            
            area_data_ct_evolution.append({
                "id": cat,
                "data": [
                    {"x": str(row['mois']), "y": row['nb_ct_cumule']}
                    for _, row in df_complete.iterrows()
                ]
            })

    with elements("area_ct_evolution"):
        with mui.Box(sx={"height": 500}):
            nivo.Line(
                data=area_data_ct_evolution,
                margin={"top": 20, "right": 110, "bottom": 50, "left": 60},
                xScale={"type": "point"},
                yScale={"type": "linear", "min": 0, "max": "auto", "stacked": True, "reverse": False},
                curve="monotoneX",
                axisTop=None,
                axisRight=None,
                axisBottom={
                    "tickSize": 5,
                    "tickPadding": 5,
                    "tickRotation": -45,
                    "legend": "Mois",
                    "legendOffset": 45,
                    "legendPosition": "middle"
                },
                axisLeft={
                    "tickSize": 5,
                    "tickPadding": 5,
                    "tickRotation": 0,
                    "legend": "Nombre cumulé",
                    "legendOffset": -50,
                    "legendPosition": "middle"
                },
                enableArea=True,
                areaOpacity=0.7,
                enablePoints=False,
                useMesh=True,
                enableSlices="x",
                legends=[
                    {
                        "anchor": "bottom-right",
                        "direction": "column",
                        "justify": False,
                        "translateX": 100,
                        "translateY": 0,
                        "itemsSpacing": 2,
                        "itemWidth": 80,
                        "itemHeight": 20,
                        "itemDirection": "left-to-right",
                        "itemOpacity": 0.85,
                        "symbolSize": 12,
                        "symbolShape": "circle",
                    }
                ],
                colors={"scheme": "pastel2"},
                theme=theme_actif,
            )

# ===============================================
# === Waffle Chart - Répartition par niveau =====
# ===============================================

st.markdown('---')

if selected_region != "Toutes" and selected_departement == "Tous":
    st.badge(f'EPCI tracker : **{selected_region}**', icon=":material/track_changes:", color="orange")
elif selected_region != "Toutes" and selected_departement != "Tous":
    st.badge(f'EPCI tracker : **{selected_departement}**', icon=":material/track_changes:", color="orange")
else:
    st.badge(f'EPCI tracker : **Territoire national**', icon=":material/track_changes:", color="orange")

# Filtrer df_ct_niveau selon la sélection
df_ct_niveau_selected = df_ct_niveau.copy()
if selected_region != "Toutes":
    df_ct_niveau_selected = df_ct_niveau_selected[df_ct_niveau_selected["region_name"] == selected_region]
if selected_departement != "Tous":
    df_ct_niveau_selected = df_ct_niveau_selected[df_ct_niveau_selected["departement_name"] == selected_departement]

# Compter les collectivités par niveau
niveau_counts = df_ct_niveau_selected.groupby("niveau")["collectivite_id"].count().reset_index()
niveau_counts.columns = ["niveau", "count"]

# Ordre obligatoire des niveaux (de haut en bas)
ordre_niveaux = ['Inactives', 'Activées', 'PAP', 'PAP actif', 'PAP actif >2.5']
niveau_counts["niveau"] = pd.Categorical(niveau_counts["niveau"], categories=ordre_niveaux, ordered=True)
niveau_counts = niveau_counts.sort_values("niveau")

# Préparer les données pour le waffle chart Nivo
waffle_data = [
    {"id": str(row["niveau"]), "label": f"{row['niveau']}", "value": int(row["count"])}
    for _, row in niveau_counts.iterrows()
    if pd.notna(row["niveau"])  # Exclure les niveaux non reconnus
]

total_ct_niveau = niveau_counts["count"].sum()


cols_wafffle = st.columns(2)
with cols_wafffle[0]:
    # Bar chart vertical du nombre de CT par niveau

    niveau_counts_actives = niveau_counts[niveau_counts["niveau"] != "Inactives"]

    bar_data_niveau = [
        {"niveau": str(row["niveau"]), "count": int(row["count"])}
        for _, row in niveau_counts_actives.iterrows()
        if pd.notna(row["niveau"])
    ]
    
    # Couleurs pour les barres (même palette que le waffle)
    bar_colors = ["#ffcc99", "#a1d99b", "#74c476", "#31a354"]
    
    if len(bar_data_niveau) > 0:
        with elements("bar_niveau"):
            with mui.Box(sx={"height": 400}):
                nivo.Bar(
                    data=bar_data_niveau,
                    keys=["count"],
                    indexBy="niveau",
                    margin={"top": 20, "right": 20, "bottom": 25, "left": 60},
                    padding=0.3,
                    layout="vertical",
                    colors=bar_colors[:len(bar_data_niveau)],
                    colorBy="indexValue",
                    borderRadius=4,
                    axisBottom={
                        "tickSize": 5,
                        "tickPadding": 5,
                        "tickRotation": 0,
                    },
                    axisLeft={
                        "tickSize": 5,
                        "tickPadding": 5,
                        "tickRotation": 0,
                        "legend": "Nombre de CT",
                        "legendPosition": "middle",
                        "legendOffset": -50,
                    },
                    enableLabel=True,
                    labelSkipWidth=12,
                    labelSkipHeight=12,
                    labelTextColor="#ffffff",
                    theme=theme_actif,
                )

    
with cols_wafffle[1]:
    # Couleurs pour les niveaux : rouge/orange pastel pour Inactives/Activées, puis vert
    waffle_colors = ["#f4a5a5", "#ffcc99", "#a1d99b", "#74c476", "#31a354"]

    if len(waffle_data) > 0:
        with elements("waffle_niveau"):
            with mui.Box(sx={"height": 380}):
                nivo.Waffle(
                    data=waffle_data,
                    total=int(total_ct_niveau),
                    rows=10,
                    columns=10,
                    borderRadius=4,
                    padding=1.5,
                    fillDirection="top",
                    margin={"top": 10, "right": 10, "bottom": 0, "left": 10},
                    colors=waffle_colors,
                    borderColor={"from": "color", "modifiers": [["darker", 0.3]]},
                    animate=True,
                    motionStaggering=2,
                    theme=theme_actif,
                )
    else:
        st.info("Aucune donnée de niveau disponible pour les filtres sélectionnés.")


# ===============================================
# === Suivi du nombre d'utilisateurs ============
# ===============================================

st.markdown('---')
st.badge(f'Suivi de l\'activité', icon=":material/browse_activity:", color="blue")

segmentation = st.segmented_control(
    "Segmentation",
    options=["Utilisateurs", "Collectivités"],
    default="Utilisateurs"
)

# Mapping des options du slider vers le nombre de mois et la fréquence pandas
activite_options = ["2 ans", "1 an", "6 mois", "3 mois", "1 mois"]
activite_mois = {
    "2 ans": 24,
    "1 an": 12,
    "6 mois": 6,
    "3 mois": 3,
    "1 mois": 1
}
activite_freq = {
    "2 ans": "2YE",
    "1 an": "YE",
    "6 mois": "6ME",
    "3 mois": "QE",
    "1 mois": "ME"
}

selected_activite = st.select_slider(
    "Granularité",
    options=activite_options,
    value="3 mois"
)
nb_mois_activite = activite_mois[selected_activite]

# Filtrer df_ct_users_actifs selon la sélection géographique
df_users_selected = df_ct_users_actifs.copy()
if selected_region != "Toutes":
    df_users_selected = df_users_selected[df_users_selected["region_name"] == selected_region]
if selected_departement != "Tous":
    df_users_selected = df_users_selected[df_users_selected["departement_name"] == selected_departement]

# Convertir la colonne mois en datetime pour le filtrage temporel
df_users_selected['mois_dt'] = pd.to_datetime(df_users_selected['mois'].astype(str))
mois_max = df_users_selected['mois_dt'].max()
mois_cutoff = mois_max - pd.DateOffset(months=nb_mois_activite - 1)

# Filtrer pour ne garder que les X derniers mois
df_users_periode = df_users_selected[df_users_selected['mois_dt'] >= mois_cutoff]

if segmentation == "Utilisateurs":

    # Calculer les métriques sur la période sélectionnée
    nb_users = df_users_periode['email'].nunique()
    users_par_ct = df_users_periode.groupby('collectivite_id')['email'].nunique()
    moyenne_users = round(users_par_ct.mean(), 1) if len(users_par_ct) > 0 else 0
    max_users = int(users_par_ct.max()) if len(users_par_ct) > 0 else 0
    
    # Afficher les métriques
    cols_metrics = st.columns(3)
    with cols_metrics[0]:
        st.metric(f"Utilisateurs actifs ({selected_activite})", nb_users)
    with cols_metrics[1]:
        st.metric("Moyenne par collectivité", moyenne_users)
    with cols_metrics[2]:
        st.metric("Max par collectivité", max_users)

    # Compter le nombre d'utilisateurs uniques par période sélectionnée
    freq = activite_freq[selected_activite]
    df_users_par_periode = df_users_selected.set_index('mois_dt').groupby(pd.Grouper(freq=freq))['email'].nunique().reset_index(name='nb_utilisateurs')
    df_users_par_periode = df_users_par_periode.sort_values('mois_dt')
    df_users_par_periode = df_users_par_periode[df_users_par_periode['nb_utilisateurs'] > 0]

    # Formater les labels selon la période
    if nb_mois_activite == 1:
        df_users_par_periode['periode_label'] = df_users_par_periode['mois_dt'].dt.strftime('%b %Y').str.lower()
    elif nb_mois_activite == 3:
        df_users_par_periode['periode_label'] = df_users_par_periode['mois_dt'].dt.to_period('Q').astype(str)
    elif nb_mois_activite == 6:
        df_users_par_periode['periode_label'] = df_users_par_periode['mois_dt'].apply(lambda x: f"S{1 if x.month <= 6 else 2} {x.year}")
    else:  # 12 ou 24 mois
        df_users_par_periode['periode_label'] = df_users_par_periode['mois_dt'].dt.strftime('%Y')

    # Préparer les données pour le graphique Nivo Line avec Area
    if len(df_users_par_periode) > 0:
        area_data_users = [{
            "id": "Utilisateurs actifs",
            "data": [
                {"x": row['periode_label'], "y": int(row['nb_utilisateurs'])}
                for _, row in df_users_par_periode.iterrows()
            ]
        }]

        with elements("area_users_evolution"):
            with mui.Box(sx={"height": 500}):
                nivo.Line(
                    data=area_data_users,
                    margin={"top": 20, "right": 30, "bottom": 50, "left": 60},
                    xScale={"type": "point"},
                    yScale={"type": "linear", "min": 0, "max": "auto", "stacked": False, "reverse": False},
                    curve="monotoneX",
                    axisTop=None,
                    axisRight=None,
                    axisBottom={
                        "tickSize": 5,
                        "tickPadding": 5,
                        "tickRotation": -45,
                        "legend": "Période",
                        "legendOffset": 45,
                        "legendPosition": "middle"
                    },
                    axisLeft={
                        "tickSize": 5,
                        "tickPadding": 5,
                        "tickRotation": 0,
                        "legend": "Nombre d'utilisateurs",
                        "legendOffset": -50,
                        "legendPosition": "middle"
                    },
                    enableArea=True,
                    areaOpacity=0.3,
                    enablePoints=True,
                    pointSize=8,
                    pointColor={"theme": "background"},
                    pointBorderWidth=2,
                    pointBorderColor={"from": "serieColor"},
                    useMesh=True,
                    enableSlices="x",
                    colors=["#3b82f6"],
                    theme=theme_actif,
                )
    else:
        st.info("Aucune donnée d'utilisateurs disponible pour les filtres sélectionnés.")

else:
    # Calculer les métriques sur la période sélectionnée
    nb_collectivites = df_users_periode['collectivite_id'].nunique()
    
    # Afficher les métriques
    st.metric(f"Collectivités actives ({selected_activite})", nb_collectivites)

    # Compter le nombre de collectivités uniques par période sélectionnée
    freq = activite_freq[selected_activite]
    df_ct_par_periode = df_users_selected.set_index('mois_dt').groupby(pd.Grouper(freq=freq))['collectivite_id'].nunique().reset_index(name='nb_collectivites')
    df_ct_par_periode = df_ct_par_periode.sort_values('mois_dt')
    df_ct_par_periode = df_ct_par_periode[df_ct_par_periode['nb_collectivites'] > 0]

    # Formater les labels selon la période
    if nb_mois_activite == 1:
        df_ct_par_periode['periode_label'] = df_ct_par_periode['mois_dt'].dt.strftime('%b %Y').str.lower()
    elif nb_mois_activite == 3:
        df_ct_par_periode['periode_label'] = df_ct_par_periode['mois_dt'].dt.to_period('Q').astype(str)
    elif nb_mois_activite == 6:
        df_ct_par_periode['periode_label'] = df_ct_par_periode['mois_dt'].apply(lambda x: f"S{1 if x.month <= 6 else 2} {x.year}")
    else:  # 12 ou 24 mois
        df_ct_par_periode['periode_label'] = df_ct_par_periode['mois_dt'].dt.strftime('%Y')

    # Préparer les données pour le graphique Nivo Line avec Area
    if len(df_ct_par_periode) > 0:
        area_data_ct = [{
            "id": "Collectivités actives",
            "data": [
                {"x": row['periode_label'], "y": int(row['nb_collectivites'])}
                for _, row in df_ct_par_periode.iterrows()
            ]
        }]

        with elements("area_collectivites_evolution"):
            with mui.Box(sx={"height": 500}):
                nivo.Line(
                    data=area_data_ct,
                    margin={"top": 20, "right": 30, "bottom": 50, "left": 60},
                    xScale={"type": "point"},
                    yScale={"type": "linear", "min": 0, "max": "auto", "stacked": False, "reverse": False},
                    curve="monotoneX",
                    axisTop=None,
                    axisRight=None,
                    axisBottom={
                        "tickSize": 5,
                        "tickPadding": 5,
                        "tickRotation": -45,
                        "legend": "Période",
                        "legendOffset": 45,
                        "legendPosition": "middle"
                    },
                    axisLeft={
                        "tickSize": 5,
                        "tickPadding": 5,
                        "tickRotation": 0,
                        "legend": "Nombre de collectivités",
                        "legendOffset": -50,
                        "legendPosition": "middle"
                    },
                    enableArea=True,
                    areaOpacity=0.3,
                    enablePoints=True,
                    pointSize=8,
                    pointColor={"theme": "background"},
                    pointBorderWidth=2,
                    pointBorderColor={"from": "serieColor"},
                    useMesh=True,
                    enableSlices="x",
                    colors=["#ff6b6b"],
                    theme=theme_actif,
                )
    else:
        st.info("Aucune donnée de collectivités disponible pour les filtres sélectionnés.")


# ===============================================
# === Suivi des plans et FA =====================
# ===============================================

st.markdown('---')
st.badge(f'Suivi des plans et FA', icon=":material/modeling:", color="violet")

# Filtrer df_fap_et_no_fap selon la sélection
df_fap_selected = df_fap_et_no_fap.copy()
if selected_region != "Toutes":
    df_fap_selected = df_fap_selected[df_fap_selected["region_name"] == selected_region]
if selected_departement != "Tous":
    df_fap_selected = df_fap_selected[df_fap_selected["departement_name"] == selected_departement]

cols_pie = st.columns(2)

with cols_pie[0]:
    st.markdown("**Répartition par type de plan**")
    
    # Compter le nombre de plans par type et trier du plus grand au plus petit
    type_counts = df_fap_selected.groupby('type').size().reset_index(name='count')
    type_counts = type_counts.sort_values('count', ascending=False)
    
    if len(type_counts) > 0:
        pie_data_type = [
            {"id": str(row['type']), "label": str(row['type']), "value": int(row['count'])}
            for _, row in type_counts.iterrows()
        ]
        
        with elements("pie_type_plans"):
            with mui.Box(sx={"height": 400}):
                nivo.Pie(
                    data=pie_data_type,
                    margin={"top": 80, "right": 80, "bottom": 80, "left": 80},
                    innerRadius=0.5,
                    padAngle=0.7,
                    cornerRadius=3,
                    activeOuterRadiusOffset=8,
                    colors={"scheme": "pastel2"},
                    borderWidth=1,
                    borderColor={"from": "color", "modifiers": [["darker", 0.2]]},
                    arcLinkLabelsStraightLength=5,
                    arcLinkLabelsSkipAngle=10,
                    arcLinkLabelsTextColor="#333333",
                    arcLinkLabelsThickness=2,
                    arcLinkLabelsColor={"from": "color"},
                    arcLabelsSkipAngle=10,
                    arcLabelsTextColor={"from": "color", "modifiers": [["darker", 2]]},
                    theme=theme_actif,
                )
    else:
        st.info("Aucune donnée de type disponible.")

with cols_pie[1]:
    st.markdown("**Fiches actions pilotables et non-pilotables**")
    
    # Calculer les sommes de nb_fap et nb_no_fap
    total_fap = int(df_fap_selected['nb_fap'].sum())
    total_no_fap = int(df_fap_selected['nb_no_fap'].sum())
    
    if total_fap + total_no_fap > 0:
        pie_data_fap = [
            {"id": "Pilotables", "label": "Pilotables", "value": total_fap},
            {"id": "Non-pilotables", "label": "Non-pilotables", "value": total_no_fap}
        ]
        
        with elements("pie_fap_distribution"):
            with mui.Box(sx={"height": 400}):
                nivo.Pie(
                    data=pie_data_fap,
                    margin={"top": 80, "right": 80, "bottom": 80, "left": 80},
                    innerRadius=0.5,
                    padAngle=0.7,
                    cornerRadius=3,
                    activeOuterRadiusOffset=8,
                    colors={"scheme": "pastel2"},
                    borderWidth=1,
                    borderColor={"from": "color", "modifiers": [["darker", 0.2]]},
                    arcLinkLabelsSkipAngle=10,
                    arcLinkLabelsTextColor="#333333",
                    arcLinkLabelsThickness=2,
                    arcLinkLabelsColor={"from": "color"},
                    arcLabelsSkipAngle=10,
                    arcLabelsTextColor={"from": "color", "modifiers": [["darker", 2]]},
                    theme=theme_actif,
                )
    else:
        st.info("Aucune donnée FA disponible.")
