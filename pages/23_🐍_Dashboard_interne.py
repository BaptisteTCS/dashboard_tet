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
    read_table
)

# On cache toutes les données pour optimiser les performances
@st.cache_resource(ttl="3d")
def load_data():
    df_ct_actives = read_table('ct_actives')
    df_ct_niveau = read_table('ct_niveau')
    df_ct_users_actifs = read_table('user_actifs_ct_mois')
    df_fap_et_no_fap = read_table('fap_et_no_fap')  
    df_pap_statut_region = read_table('pap_statut_region')
    df_pap_note_region = read_table('pap_note_region')  
    return df_ct_actives, df_ct_niveau, df_ct_users_actifs, df_fap_et_no_fap, df_pap_statut_region, df_pap_note_region

#Chargement des données
df_ct_actives, df_ct_niveau, df_ct_users_actifs, df_fap_et_no_fap, df_pap_statut_region, df_pap_note_region = load_data() 

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

# ===============================================
# === SELECTEUR DE REGION ET DEPARTEMENT ========
# ===============================================

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

st.markdown("*La sélection d'un territoire s'applique à tous les onglets. Les deltas sont calculés par rapport au mois précédent.*")


tabs = st.tabs(["🌀 Vue d'ensemble", "🌟 North Star"])

# ===============================================
# === Nombre de collectivités par catégorie =====
# ===============================================

with tabs[0]:

    if selected_region != "Toutes" and selected_departement == "Tous":
        st.badge(f'Activation : **{selected_region}**', icon=":material/trending_up:", color="green")
    elif selected_region != "Toutes" and selected_departement != "Tous":
        st.badge(f'Activation : **{selected_departement}**', icon=":material/trending_up:", color="green")
    else:
        st.badge(f'Activation : **Territoire national**', icon=":material/trending_up:", color="green")

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

    if selected_region != "Toutes" and selected_departement == "Tous":
        st.badge(f'Suivi de l\'activité : **{selected_region}**', icon=":material/browse_activity:", color="blue")
    elif selected_region != "Toutes" and selected_departement != "Tous":
        st.badge(f'Suivi de l\'activité : **{selected_departement}**', icon=":material/browse_activity:", color="blue")
    else:
        st.badge(f'Suivi de l\'activité : **Territoire national**', icon=":material/browse_activity:", color="blue")

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
    if selected_region != "Toutes" and selected_departement == "Tous":
        st.badge(f'Suivi des plans et FA : **{selected_region}**', icon=":material/modeling:", color="violet")
    elif selected_region != "Toutes" and selected_departement != "Tous":
        st.badge(f'Suivi des plans et FA : **{selected_departement}**', icon=":material/modeling:", color="violet")
    else:
        st.badge(f'Suivi des plans et FA : **Territoire national**', icon=":material/modeling:", color="violet")

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

with tabs[1]:

    
    if selected_region != "Toutes" and selected_departement == "Tous":
        st.badge(f"NS 1 : **{selected_region}**", icon=":material/star_shine:", color="yellow")
    elif selected_region != "Toutes" and selected_departement != "Tous":
        st.badge(f"NS 1 : **{selected_departement}**", icon=":material/star_shine:", color="yellow")
    else:
        st.badge(f"NS 1 : **Territoire national**", icon=":material/star_shine:", color="yellow")


    df_ct_pap_statut_selected = df_pap_statut_region.copy()
    if selected_region != "Toutes":
        df_ct_pap_statut_selected = df_ct_pap_statut_selected[df_ct_pap_statut_selected["region_name"] == selected_region]
    if selected_departement != "Tous":
        df_ct_pap_statut_selected = df_ct_pap_statut_selected[df_ct_pap_statut_selected["departement_name"] == selected_departement]

    # Identifier les deux dernièrs mois
    mois_uniques = sorted(df_ct_pap_statut_selected['mois'].dropna().unique(), reverse=True)

    metrics_ns = st.columns(4)
    
    if len(mois_uniques) >= 1:
        derniere_mois = mois_uniques[0]
        df_derniere_mois = df_ct_pap_statut_selected[df_ct_pap_statut_selected['mois'] == derniere_mois]
        
        total = df_derniere_mois['collectivite_id'].nunique()
        actifs = df_derniere_mois[df_derniere_mois["statut"] == "actif"]['collectivite_id'].nunique()
        inactifs = df_derniere_mois[df_derniere_mois["statut"] == "inactif"]['collectivite_id'].nunique()
        
        if total > 0:
            ratio_activite = actifs / total * 100
        else:
            ratio_activite = 0
        
        # Calculer le delta par rapport au mois précédent
        delta_activite = None
        delta_total = None
        delta_actifs = None
        delta_inactifs = None
        if len(mois_uniques) >= 2:
            mois_precedent = mois_uniques[1]
            df_mois_precedent = df_ct_pap_statut_selected[df_ct_pap_statut_selected['mois'] == mois_precedent]
            
            total_prec = df_mois_precedent['collectivite_id'].nunique()
            actifs_prec = df_mois_precedent[df_mois_precedent["statut"] == "actif"]['collectivite_id'].nunique()
            inactifs_prec = df_mois_precedent[df_mois_precedent["statut"] == "inactif"]['collectivite_id'].nunique()
            
            if total_prec > 0:
                ratio_activite_prec = actifs_prec / total_prec * 100
                delta_activite = ratio_activite - ratio_activite_prec

            delta_total = total - total_prec
            delta_actifs = actifs - actifs_prec
            delta_inactifs = inactifs - inactifs_prec

        with metrics_ns[0]:
            st.metric("Collectivités PAP", total, delta=delta_total)
        with metrics_ns[1]:
            st.metric("PAP actifs", actifs, delta=delta_actifs)
        with metrics_ns[2]:
            st.metric("PAP inactifs", inactifs, delta=delta_inactifs, delta_color="inverse")
        with metrics_ns[3]:
            st.metric(
                "Activité", 
                f"{ratio_activite:.0f}%",
                delta=f"{delta_activite:.1f}%" if delta_activite is not None else None,
                delta_color="normal"
            )

    else:
        with metrics_ns[0]:
            st.metric("Collectivités PAP", "N/A")
        with metrics_ns[1]:
            st.metric("PAP actifs", "N/A")
        with metrics_ns[2]:
            st.metric("PAP inactifs", "N/A")
        with metrics_ns[3]:
            st.metric("Activité", "N/A")

    # ===============================================
    # === Graphique évolution mensuelle ==========
    # ===============================================
    
    # Compter les collectivités distinctes par mois et statut
    df_evolution_statut = df_ct_pap_statut_selected.copy()
    df_evolution_statut['mois'] = pd.to_datetime(df_evolution_statut['mois'])
    df_evolution_statut = df_evolution_statut[df_evolution_statut['mois'] >= '2024-06-01']
    df_evolution_statut = df_evolution_statut.groupby(['mois', 'statut'])['collectivite_id'].nunique().reset_index(name='nb_collectivites')
    df_evolution_statut = df_evolution_statut.sort_values('mois')
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].dt.strftime('%Y-%m')
    
    if len(df_evolution_statut) > 0:
        # Ordre : actif en premier (en bas du stack), inactif en second (au-dessus)
        line_data_statuts = []
        for statut in ["actif", "inactif"]:
            df_statut = df_evolution_statut[df_evolution_statut['statut'] == statut].copy()
            if not df_statut.empty:
                line_data_statuts.append({
                    "id": statut.capitalize(),
                    "data": [
                        {"x": row['mois_label'], "y": int(row['nb_collectivites'])}
                        for _, row in df_statut.iterrows()
                    ]
                })
        
        if len(line_data_statuts) > 0:
            with elements("line_evolution_statuts_pap"):
                with mui.Box(sx={"height": 450}):
                    nivo.Line(
                        data=line_data_statuts,
                        margin={"top": 20, "right": 110, "bottom": 60, "left": 60},
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
                            "legendOffset": 50,
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
    else:
        st.info("Aucune donnée disponible pour le graphique d'évolution.")

    
    st.markdown("---")

    if selected_region != "Toutes" and selected_departement == "Tous":
        st.badge(f'NS 2 : **{selected_region}**', icon=':material/stars_2:', color='orange')
    elif selected_region != "Toutes" and selected_departement != "Tous":
        st.badge(f'NS 2 : **{selected_departement}**', icon=':material/stars_2:', color='orange')
    else:
        st.badge(f'NS 2 : **Territoire national**', icon=':material/stars_2:', color='orange')

    df_pap_note_selected = df_pap_note_region.copy()
    if selected_region != "Toutes":
        df_pap_note_selected = df_pap_note_selected[df_pap_note_selected["region_name"] == selected_region]
    if selected_departement != "Tous":
        df_pap_note_selected = df_pap_note_selected[df_pap_note_selected["departement_name"] == selected_departement]

    # Contrôles de sélection
    segmentation_ns2 = st.segmented_control(
        "Granularité",
        options=["Collectivités", "Plans"],
        default="Collectivités",
        key="segmentation_ns2"
    )

    periode_options_ns2 = ["1 an", "6 mois", "3 mois", "1 mois"]
    periode_mois_ns2 = {"1 an": 12, "6 mois": 6, "3 mois": 3, "1 mois": 1}
    selected_periode_ns2 = st.select_slider(
        "Période de comparaison",
        options=periode_options_ns2,
        value="3 mois",
        key="periode_ns2"
    )
    nb_mois_ns2 = periode_mois_ns2[selected_periode_ns2]

    # Convertir semaine en datetime
    df_pap_note_selected['semaine'] = pd.to_datetime(df_pap_note_selected['semaine'])
    
    if len(df_pap_note_selected) > 0:
        # Dernière semaine disponible
        derniere_semaine = df_pap_note_selected['semaine'].max()
        
        # Calculer la date de référence (aujourd'hui - X mois, premier lundi après)
        date_reference = datetime.now() - relativedelta(months=nb_mois_ns2)
        # Trouver le premier lundi après cette date
        jours_jusqu_lundi = (7 - date_reference.weekday()) % 7
        if jours_jusqu_lundi == 0:
            jours_jusqu_lundi = 7
        premier_lundi = date_reference + timedelta(days=jours_jusqu_lundi)
        
        # Trouver la semaine de référence la plus proche dans les données
        semaines_disponibles = sorted(df_pap_note_selected['semaine'].unique())
        semaine_reference = None
        for s in semaines_disponibles:
            if s >= pd.Timestamp(premier_lundi):
                semaine_reference = s
                break
        
        # Si pas de semaine trouvée après, prendre la première disponible
        if semaine_reference is None and len(semaines_disponibles) > 0:
            semaine_reference = semaines_disponibles[0]
        
        # Préparer les données selon la segmentation
        if segmentation_ns2 == "Collectivités":
            # Regrouper par collectivité et prendre le score max par semaine
            df_derniere_raw = df_pap_note_selected[df_pap_note_selected['semaine'] == derniere_semaine]
            # Pour chaque collectivité, prendre la ligne avec le score max (pour avoir le plan_id correspondant)
            idx_max = df_derniere_raw.groupby('collectivite_id')['score'].idxmax()
            df_derniere = df_derniere_raw.loc[idx_max, ['collectivite_id', 'plan_id', 'score', 'nom', 'region_name']].copy()
            df_derniere.columns = ['id', 'plan_id', 'score_actuel', 'nom', 'region']
            
            if semaine_reference is not None:
                df_reference = df_pap_note_selected[df_pap_note_selected['semaine'] == semaine_reference].groupby('collectivite_id')['score'].max().reset_index()
                df_reference.columns = ['id', 'score_reference']
            else:
                df_reference = pd.DataFrame(columns=['id', 'score_reference'])
        else:
            # Mode Plans : utiliser plan_id comme identifiant
            df_derniere_raw = df_pap_note_selected[df_pap_note_selected['semaine'] == derniere_semaine]
            df_derniere = df_derniere_raw[['plan_id', 'collectivite_id', 'score', 'nom', 'nom_plan']].copy()
            df_derniere.columns = ['id', 'collectivite_id', 'score_actuel', 'nom', 'nom_plan']
            
            if semaine_reference is not None:
                df_reference = df_pap_note_selected[df_pap_note_selected['semaine'] == semaine_reference][['plan_id', 'score']].copy()
                df_reference.columns = ['id', 'score_reference']
            else:
                df_reference = pd.DataFrame(columns=['id', 'score_reference'])
        
        # Merger les deux pour comparer
        df_comparaison = df_derniere.merge(df_reference, on='id', how='left')
        df_comparaison['est_nouveau'] = df_comparaison['score_reference'].isna()
        df_comparaison['evolution'] = df_comparaison['score_actuel'] - df_comparaison['score_reference'].fillna(0)
        df_comparaison['a_evolue'] = (~df_comparaison['est_nouveau']) & (df_comparaison['evolution'].abs() > 0.01)  # Exclure les nouveaux
        
        # Calculer les métriques
        nb_nouveau = df_comparaison['est_nouveau'].sum()
        nb_evolue = df_comparaison['a_evolue'].sum()
        evolution_moyenne = df_comparaison[df_comparaison['a_evolue']]['evolution'].mean() if nb_evolue > 0 else 0
        evolution_max = df_comparaison['evolution'].max() if len(df_comparaison) > 0 else 0
        note_max = df_comparaison['score_actuel'].max() if len(df_comparaison) > 0 else 0

        # Afficher les métriques
        label_entity = "collectivités" if segmentation_ns2 == "Collectivités" else "plans"
        metrics_ns2 = st.columns(4)
        with metrics_ns2[0]:
            st.metric(f"{label_entity.capitalize()} ayant progressé", int(nb_evolue))
        with metrics_ns2[1]:
            st.metric("Progression moyenne", f"+{evolution_moyenne:.1f}" if not pd.isna(evolution_moyenne) else "N/A")
        with metrics_ns2[2]:
            st.metric("Progression max", f"+{evolution_max:.1f}" if evolution_max >= 0 else f"{evolution_max:.2f}")
        with metrics_ns2[3]:
            st.metric("Score max", f"{note_max:.1f}")
        
        # ===============================================
        # === Leaderboards stylisés =====================
        # ===============================================
        
        # Fonction pour générer le lien vers le plan
        def get_plan_url(collectivite_id, plan_id):
            return f"https://app.territoiresentransitions.fr/collectivite/{int(collectivite_id)}/plans/{int(plan_id)}"
        
        # Style CSS pour les cartes
        st.markdown("""
        <style>
        .leaderboard-card {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 12px;
            border-left: 4px solid #6c757d;
            transition: transform 0.2s, box-shadow 0.2s;
            text-decoration: none !important;
            display: block;
            color: inherit;
        }
        .leaderboard-card * {
            text-decoration: none !important;
        }
        .leaderboard-card:hover {
            transform: translateX(8px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .leaderboard-card.gold { border-left-color: #ffd700; background: linear-gradient(135deg, #fffef0 0%, #fff9e6 100%); }
        .leaderboard-card.progress { border-left-color: #28a745; background: linear-gradient(135deg, #f0fff4 0%, #e6f7ed 100%); }
        .card-rank { font-size: 24px; font-weight: bold; color: #6c757d; margin-right: 16px; }
        .card-rank.gold { color: #d4a800; }
        .card-rank.progress { color: #28a745; }
        .card-content { flex: 1; }
        .card-title { font-size: 16px; font-weight: 600; color: #212529; margin-bottom: 4px; }
        .card-subtitle { font-size: 13px; color: #6c757d; }
        .card-score { font-size: 20px; font-weight: bold; color: #495057; text-align: right; }
        .card-delta { font-size: 14px; color: #28a745; font-weight: 600; }
        .card-row { display: flex; align-items: center; }
        </style>
        """, unsafe_allow_html=True)

        cols_leaderboards = st.columns(2)
        with cols_leaderboards[0]:
        
            # === Top scores ===

            st.badge("Meilleurs scores", icon=':material/trophy:', color='orange')
            
            if segmentation_ns2 == "Collectivités":
                df_top_scores = df_comparaison.nlargest(5, 'score_actuel')
            else:
                df_top_scores = df_comparaison.nlargest(5, 'score_actuel')
            
            for idx, (_, row) in enumerate(df_top_scores.iterrows()):
                rank = idx + 1
                rank_class = "gold" if rank <= 3 else "progress"
                
                if segmentation_ns2 == "Collectivités":
                    url = get_plan_url(row['id'], row['plan_id'])
                    subtitle = row['region'] if pd.notna(row.get('region')) else ""
                    title = row['nom']
                else:
                    url = get_plan_url(row['collectivite_id'], row['id'])
                    subtitle = row['nom_plan'] if pd.notna(row.get('nom_plan')) else ""
                    title = row['nom']
                
                score = row['score_actuel']
                
                card_html = f"""
                <a href="{url}" target="_blank" class="leaderboard-card {rank_class}">
                    <div class="card-row">
                        <div class="card-rank {rank_class}">#{rank}</div>
                        <div class="card-content">
                            <div class="card-title">{title}</div>
                            <div class="card-subtitle">{subtitle}</div>
                        </div>
                        <div style="text-align: right;">
                                <div class="card-score">{score:.2f}</div>
                                <div class="card-delta" style="visibility:hidden;">A</div>
                            </div>
                    </div>
                </a>
                """
                st.markdown(card_html, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
        
        # === Meilleures progressions ===
        with cols_leaderboards[1]:

            st.badge("Meilleures progressions", icon=':material/trending_up:', color='orange')
        
            df_progressions = df_comparaison[df_comparaison['evolution'] > 0.01].copy()
            
            if len(df_progressions) > 0:
                df_top_progressions = df_progressions.nlargest(5, 'evolution')
                
                for idx, (_, row) in enumerate(df_top_progressions.iterrows()):
                    rank = idx + 1
                    rank_class = "gold" if rank <= 3 else "progress"
                    
                    if segmentation_ns2 == "Collectivités":
                        url = get_plan_url(row['id'], row['plan_id'])
                        subtitle = row['region'] if pd.notna(row.get('region')) else ""
                        title = row['nom']
                    else:
                        url = get_plan_url(row['collectivite_id'], row['id'])
                        subtitle = row['nom_plan'] if pd.notna(row.get('nom_plan')) else ""
                        title = row['nom']
                    
                    score = row['score_actuel']
                    delta = row['evolution']
                    
                    card_html = f"""
                    <a href="{url}" target="_blank" class="leaderboard-card {rank_class}">
                        <div class="card-row">
                            <div class="card-rank {rank_class}">#{rank}</div>
                            <div class="card-content">
                                <div class="card-title">{title}</div>
                                <div class="card-subtitle">{subtitle}</div>
                            </div>
                            <div style="text-align: right;">
                                <div class="card-score">{score:.2f}</div>
                                <div class="card-delta">+{delta:.2f}</div>
                            </div>
                        </div>
                    </a>
                    """
                    st.markdown(card_html, unsafe_allow_html=True)
            else:
                st.info("Aucune progression sur la période.")

        # ==================
        # === Graphe ===
        # ==================

        st.badge("Distribution des scores", icon=':material/bar_chart:', color='orange')
        
        
        # Créer des bins pour la distribution (0-0.5, 0.5-1, 1-1.5, ..., 4.5-5)
        bins = [i * 0.5 for i in range(11)]
        labels_bins = [f"{bins[i]:.1f}-{bins[i+1]:.1f}" for i in range(len(bins)-1)]
        
        df_comparaison['bin'] = pd.cut(df_comparaison['score_actuel'], bins=bins, labels=labels_bins, include_lowest=True)
        
        # Compter par bin et par statut (stable, évolution, nouveau)
        distribution_nouveau = df_comparaison[df_comparaison['est_nouveau']].groupby('bin', observed=True).size()
        distribution_evolue = df_comparaison[df_comparaison['a_evolue']].groupby('bin', observed=True).size()
        distribution_stable = df_comparaison[(~df_comparaison['a_evolue']) & (~df_comparaison['est_nouveau'])].groupby('bin', observed=True).size()
        
        # Préparer les données pour Nivo Bar (stacked)
        bar_data_distribution = []
        for label in labels_bins:
            stable_count = int(distribution_stable.get(label, 0))
            evolue_count = int(distribution_evolue.get(label, 0))
            nouveau_count = int(distribution_nouveau.get(label, 0))
            bar_data_distribution.append({
                "bin": label,
                "Sans progression": stable_count,
                "Ayant progressé": evolue_count,
                "New": nouveau_count
            })
        
        if len(bar_data_distribution) > 0:
            with elements("bar_distribution_notes_ns2"):
                with mui.Box(sx={"height": 400}):
                    nivo.Bar(
                        data=bar_data_distribution,
                        keys=["Sans progression", "Ayant progressé", "New"],
                        indexBy="bin",
                        margin={"top": 20, "right": 130, "bottom": 50, "left": 60},
                        padding=0.3,
                        groupMode="stacked",
                        colors={"scheme": "pastel2"},
                        borderRadius=2,
                        axisBottom={
                            "tickSize": 5,
                            "tickPadding": 5,
                            "tickRotation": -45,
                            "legend": "Score",
                            "legendOffset": 45,
                            "legendPosition": "middle"
                        },
                        axisLeft={
                            "tickSize": 5,
                            "tickPadding": 5,
                            "tickRotation": 0,
                            "legend": f"Nombre de {label_entity}",
                            "legendOffset": -50,
                            "legendPosition": "middle"
                        },
                        enableLabel=True,
                        labelSkipWidth=12,
                        labelSkipHeight=12,
                        labelTextColor="#ffffff",
                        legends=[
                            {
                                "dataFrom": "keys",
                                "anchor": "bottom-right",
                                "direction": "column",
                                "justify": False,
                                "translateX": 120,
                                "translateY": 0,
                                "itemsSpacing": 2,
                                "itemWidth": 100,
                                "itemHeight": 20,
                                "itemDirection": "left-to-right",
                                "itemOpacity": 0.85,
                                "symbolSize": 12,
                                "symbolShape": "circle",
                            }
                        ],
                        theme=theme_actif,
                    )
        
        # ==========================================
        # === Évolution de la moyenne par semaine ===
        # ==========================================
        
        st.badge("Évolution de la moyenne", icon=':material/show_chart:', color='orange')
        
        # Calculer la moyenne par semaine selon la segmentation
        if segmentation_ns2 == "Collectivités":
            # Pour chaque semaine, prendre le score max par collectivité, puis faire la moyenne
            df_moyenne_semaine = df_pap_note_selected.groupby(['semaine', 'collectivite_id'])['score'].max().reset_index()
            df_moyenne_semaine = df_moyenne_semaine.groupby('semaine')['score'].mean().reset_index()
        else:
            # Pour chaque semaine, moyenne de tous les plans
            df_moyenne_semaine = df_pap_note_selected.groupby('semaine')['score'].mean().reset_index()
        
        df_moyenne_semaine = df_moyenne_semaine.sort_values('semaine')
        df_moyenne_semaine['semaine_label'] = df_moyenne_semaine['semaine'].dt.strftime('%Y-%m-%d')
        
        if len(df_moyenne_semaine) > 0:
            line_data_moyenne = [{
                "id": f"Score moyen ({label_entity})",
                "data": [
                    {"x": row['semaine_label'], "y": round(row['score'], 2)}
                    for _, row in df_moyenne_semaine.iterrows()
                ]
            }]
            
            with elements("line_evolution_moyenne_ns2"):
                with mui.Box(sx={"height": 400}):
                    nivo.Line(
                        data=line_data_moyenne,
                        margin={"top": 20, "right": 30, "bottom": 60, "left": 60},
                        xScale={"type": "point"},
                        yScale={"type": "linear", "min": 0, "max": 5, "stacked": False, "reverse": False},
                        curve="monotoneX",
                        axisTop=None,
                        axisRight=None,
                        axisBottom={
                            "tickSize": 5,
                            "tickPadding": 5,
                            "tickRotation": -45,
                            "legend": "Semaine",
                            "legendOffset": 50,
                            "legendPosition": "middle"
                        },
                        axisLeft={
                            "tickSize": 5,
                            "tickPadding": 5,
                            "tickRotation": 0,
                            "legend": "Score moyen",
                            "legendOffset": -50,
                            "legendPosition": "middle"
                        },
                        enableArea=True,
                        areaOpacity=0.15,
                        enablePoints=True,
                        pointSize=8,
                        pointColor={"theme": "background"},
                        pointBorderWidth=2,
                        pointBorderColor={"from": "serieColor"},
                        useMesh=True,
                        enableSlices="x",
                        colors=["#ff7f0e"],
                        theme=theme_actif,
                    )
            
    else:
        st.info("Aucune donnée de notes disponible pour les filtres sélectionnés.")

