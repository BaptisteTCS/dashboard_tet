import streamlit as st

# Configuration de la page en premier
st.set_page_config(
    page_title="Dashboard OKRs",
    page_icon="🌠",
    layout="wide"
)

import pandas as pd
from streamlit_elements import elements, nivo, mui
from utils.db import read_table

# ==========================
# Chargement des données
# ==========================

@st.cache_resource(ttl="2d")
def load_data():
    df_nb_fap_13 = read_table('nb_fap_13')
    df_nb_fap_52 = read_table('nb_fap_52')
    df_nb_fap_pilote_13 = read_table('nb_fap_pilote_13')
    df_nb_fap_pilote_52 = read_table('nb_fap_pilote_52')
    df_pap_13 = read_table('okr_plan_actif_13')
    df_pap_52 = read_table('okr_plan_actif_52')
    df_pap_date_passage = read_table('pap_date_passage')
    df_pap_note = read_table('pap_note')
    return df_nb_fap_13, df_nb_fap_52, df_nb_fap_pilote_13, df_nb_fap_pilote_52, df_pap_13, df_pap_52, df_pap_date_passage, df_pap_note


df_nb_fap_13, df_nb_fap_52, df_nb_fap_pilote_13, df_nb_fap_pilote_52, df_pap_13, df_pap_52, df_pap_date_passage, df_pap_note = load_data()

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


st.title("🌠 Dashboard OKRs")
tabs =st.tabs(["1 - Activation", "2 - Rétention", "3 - Qualité"])

with tabs[0]:

    st.markdown("## Objectif 1 : ACTIVATION")
    st.markdown("Permettre à chaque collectivité territoriale française de piloter ses plans & actions.")

    # ======================
    st.markdown("### A-1 (⭐ NS1 - externe)  : Nombre de collectivités avec ≥1 Plan d’Action Pilotable (PAP) dont actifs ≤1 an (12 mois | 52 semaines)")

    # Compter les collectivités distinctes par mois et statut
    df_evolution_statut = df_pap_52.copy()
    df_evolution_statut['semaine'] = pd.to_datetime(df_evolution_statut['semaine'])
    df_evolution_statut['mois'] = df_evolution_statut['semaine'].dt.to_period('M').dt.to_timestamp()

    df_evolution_statut = df_evolution_statut.sort_values('statut').drop_duplicates(subset=['collectivite_id', 'mois'], keep='first')
    df_evolution_statut = df_evolution_statut[df_evolution_statut['mois'] >= '2023-01-01']
    df_evolution_statut = df_evolution_statut.groupby(['mois', 'statut'])['collectivite_id'].nunique().reset_index(name='nb_collectivites')
    df_evolution_statut = df_evolution_statut.sort_values('mois')
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].dt.strftime('%Y-%m')

    # Métriques pour décembre de chaque année (collectivités actives)
    df_actif = df_evolution_statut[df_evolution_statut['statut'] == 'actif']
    
    jan_2024 = df_actif[df_actif['mois_label'] == '2023-12']['nb_collectivites'].values
    jan_2025 = df_actif[df_actif['mois_label'] == '2024-12']['nb_collectivites'].values
    jan_2026 = df_actif[df_actif['mois_label'] == '2025-12']['nb_collectivites'].values
    
    val_2024 = int(jan_2024[0]) if len(jan_2024) > 0 else 0
    val_2025 = int(jan_2025[0]) if len(jan_2025) > 0 else 0
    val_2026 = int(jan_2026[0]) if len(jan_2026) > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Actifs - Décembre 2023", val_2024)
    with col2:
        st.metric("Actifs - Décembre 2024", val_2025, delta=val_2025 - val_2024 if val_2024 > 0 else None)
    with col3:
        st.metric("Actifs - Décembre 2025", val_2026, delta=val_2026 - val_2025 if val_2025 > 0 else None)

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
            with elements("line_evolution_statuts_pap_52"):
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




    # ======================
    st.markdown("### A-2 (🌟 NS1 - interne)  : Nombre de collectivités avec ≥1 Plan d'Action Pilotable (PAP) actif ≤3 mois")

    df_evolution_statut = df_pap_13.copy()
    df_evolution_statut['semaine'] = pd.to_datetime(df_evolution_statut['semaine'])
    df_evolution_statut['mois'] = df_evolution_statut['semaine'].dt.to_period('M').dt.to_timestamp()

    df_evolution_statut = df_evolution_statut.sort_values('statut').drop_duplicates(subset=['collectivite_id', 'mois'], keep='first')
    df_evolution_statut = df_evolution_statut[df_evolution_statut['mois'] >= '2023-01-01']
    df_evolution_statut = df_evolution_statut.groupby(['mois', 'statut'])['collectivite_id'].nunique().reset_index(name='nb_collectivites')
    df_evolution_statut = df_evolution_statut.sort_values('mois')
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].dt.strftime('%Y-%m')

    # Métriques pour décembre de chaque année (collectivités actives)
    df_actif = df_evolution_statut[df_evolution_statut['statut'] == 'actif']
    
    jan_2024 = df_actif[df_actif['mois_label'] == '2023-12']['nb_collectivites'].values
    jan_2025 = df_actif[df_actif['mois_label'] == '2024-12']['nb_collectivites'].values
    jan_2026 = df_actif[df_actif['mois_label'] == '2025-12']['nb_collectivites'].values
    
    val_2024 = int(jan_2024[0]) if len(jan_2024) > 0 else 0
    val_2025 = int(jan_2025[0]) if len(jan_2025) > 0 else 0
    val_2026 = int(jan_2026[0]) if len(jan_2026) > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Actifs - Décembre 2023", val_2024)
    with col2:
        st.metric("Actifs - Décembre 2024", val_2025, delta=val_2025 - val_2024 if val_2024 > 0 else None)
    with col3:
        st.metric("Actifs - Décembre 2025", val_2026, delta=val_2026 - val_2025 if val_2025 > 0 else None)

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
            with elements("line_evolution_statuts_pap_13"):
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


    # ======================
    st.markdown("### A-3 (💫 - Activité) Nombre d’Actions pilotables actives ≤3 mois")

    df_evolution_statut = df_nb_fap_13.copy()

    df_evolution_statut['mois'] = pd.to_datetime(df_evolution_statut['mois'])
    df_evolution_statut = df_evolution_statut[df_evolution_statut['mois'] >= '2023-12-01']
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].dt.strftime('%Y-%m')

    # Métriques pour décembre de chaque année (collectivités actives)
    df_actif = df_evolution_statut[df_evolution_statut['statut'] == 'actif']

    df_evolution_statut = df_evolution_statut.sort_values('mois')
    
    jan_2024 = df_actif[df_actif['mois_label'] == '2023-12']['fiche_id'].values
    jan_2025 = df_actif[df_actif['mois_label'] == '2024-12']['fiche_id'].values
    jan_2026 = df_actif[df_actif['mois_label'] == '2025-12']['fiche_id'].values
    
    val_2024 = int(jan_2024[0]) if len(jan_2024) > 0 else 0
    val_2025 = int(jan_2025[0]) if len(jan_2025) > 0 else 0
    val_2026 = int(jan_2026[0]) if len(jan_2026) > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Actifs - Décembre 2023", val_2024)
    with col2:
        st.metric("Actifs - Décembre 2024", val_2025, delta=val_2025 - val_2024 if val_2024 > 0 else None)
    with col3:
        st.metric("Actifs - Décembre 2025", val_2026, delta=val_2026 - val_2025 if val_2025 > 0 else None)

    if len(df_evolution_statut) > 0:
        # Ordre : actif en premier (en bas du stack), inactif en second (au-dessus)
        line_data_statuts = []
        for statut in ["actif", "inactif"]:
            df_statut = df_evolution_statut[df_evolution_statut['statut'] == statut].copy()
            if not df_statut.empty:
                line_data_statuts.append({
                    "id": statut.capitalize(),
                    "data": [
                        {"x": row['mois_label'], "y": int(row['fiche_id'])}
                        for _, row in df_statut.iterrows()
                    ]
                })
        
        if len(line_data_statuts) > 0:
            with elements("line_evolution_statuts_fap_13"):
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
                            "legend": "Nombre d'actions pilotables actives",
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


    # ======================
    st.markdown("### A-4 (🎇 - Exploration) : Nombre de PAP initialisés de façon autonome")

    df_evolution_statut = df_pap_date_passage.copy()

    df_evolution_statut['passage_pap'] = pd.to_datetime(df_evolution_statut['passage_pap'])
    df_evolution_statut['mois'] = df_evolution_statut['passage_pap'].dt.to_period('M').dt.to_timestamp()
    df_evolution_statut = df_evolution_statut[df_evolution_statut['mois'] >= '2023-01-01']
    df_evolution_statut = df_evolution_statut.sort_values('mois')
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].dt.strftime('%Y-%m')

    df_evolution_statut = df_evolution_statut[df_evolution_statut['import'] == 'Autonome'].groupby(['mois'])['plan'].nunique().reset_index(name='nb_plans_autonomes')
    df_evolution_statut = df_evolution_statut.sort_values('mois')
    df_evolution_statut['nb_plans_autonomes_cumul'] = df_evolution_statut['nb_plans_autonomes'].cumsum()
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].dt.strftime('%Y-%m')

    # Métriques pour décembre de chaque année
    jan_2024 = df_evolution_statut[df_evolution_statut['mois_label'] == '2023-12']['nb_plans_autonomes_cumul'].values
    jan_2025 = df_evolution_statut[df_evolution_statut['mois_label'] == '2024-12']['nb_plans_autonomes_cumul'].values
    jan_2026 = df_evolution_statut[df_evolution_statut['mois_label'] == '2025-12']['nb_plans_autonomes_cumul'].values
    
    val_2024 = int(jan_2024[0]) if len(jan_2024) > 0 else 0
    val_2025 = int(jan_2025[0]) if len(jan_2025) > 0 else 0
    val_2026 = int(jan_2026[0]) if len(jan_2026) > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("PAP Autonomes - Décembre 2023", val_2024)
    with col2:
        st.metric("PAP Autonomes - Décembre 2024", val_2025, delta=val_2025 - val_2024 if val_2024 > 0 else None)
    with col3:
        st.metric("PAP Autonomes - Décembre 2025", val_2026, delta=val_2026 - val_2025 if val_2025 > 0 else None)

    if len(df_evolution_statut) > 0:
        line_data_statuts = [{
            "id": "PAP Autonomes (cumulé)",
            "data": [
                {"x": row['mois_label'], "y": int(row['nb_plans_autonomes_cumul'])}
                for _, row in df_evolution_statut.iterrows()
            ]
        }]
        
        with elements("line_evolution_autonome"):
            with mui.Box(sx={"height": 450}):
                nivo.Line(
                    data=line_data_statuts,
                    margin={"top": 20, "right": 110, "bottom": 60, "left": 60},
                    xScale={"type": "point"},
                    yScale={"type": "linear", "min": 0, "max": "auto", "stacked": False, "reverse": False},
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
                        "legend": "Nombre de PAP autonomes (cumulé)",
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

# ======================

with tabs[1]:

    st.markdown('## Objectif 2 : RÉTENTION')
    st.markdown('Faciliter la transversalité entre Plans & Actions & Contributeurs')

    st.markdown('### R-1 (⭐ NS2 - externe) : Nombre de CT avec ≥ 2 PAP avec contribution active 12 mois')

    # Compter les collectivités distinctes par mois et statut
    df_evolution_statut = df_pap_52.copy()
    df_evolution_statut['semaine'] = pd.to_datetime(df_evolution_statut['semaine'])
    df_evolution_statut['mois'] = df_evolution_statut['semaine'].dt.to_period('M').dt.to_timestamp()

    count_pap = df_evolution_statut.groupby(['mois', 'statut', 'collectivite_id'])['plan_id'].nunique().reset_index(name='nb_paps')
    count_pap = count_pap[(count_pap['nb_paps'] >= 2) & (count_pap['statut'] == 'actif')]

    df_evolution_statut = df_evolution_statut[df_evolution_statut['mois'] >= '2023-01-01']

    df_evolution_statut = df_evolution_statut.merge(count_pap, on=['mois', 'statut', 'collectivite_id'], how='inner')


    df_evolution_statut = df_evolution_statut.groupby(['mois', 'statut'])['collectivite_id'].nunique().reset_index(name='nb_collectivites')
    df_evolution_statut = df_evolution_statut.sort_values('mois')
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].dt.strftime('%Y-%m')

    # Métriques pour décembre de chaque année (collectivités actives)
    df_actif = df_evolution_statut[df_evolution_statut['statut'] == 'actif']
    
    jan_2024 = df_actif[df_actif['mois_label'] == '2023-12']['nb_collectivites'].values
    jan_2025 = df_actif[df_actif['mois_label'] == '2024-12']['nb_collectivites'].values
    jan_2026 = df_actif[df_actif['mois_label'] == '2025-12']['nb_collectivites'].values
    
    val_2024 = int(jan_2024[0]) if len(jan_2024) > 0 else 0
    val_2025 = int(jan_2025[0]) if len(jan_2025) > 0 else 0
    val_2026 = int(jan_2026[0]) if len(jan_2026) > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Décembre 2023", val_2024)
    with col2:
        st.metric("Décembre 2024", val_2025, delta=val_2025 - val_2024 if val_2024 > 0 else None)
    with col3:
        st.metric("Décembre 2025", val_2026, delta=val_2026 - val_2025 if val_2025 > 0 else None)

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
            with elements("line_evolution_statuts_pap_52_fois_2"):
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


    # ======================

    st.markdown("---")

    st.markdown('### R-2 (🌟 NS2 - interne) : Nombre de CT avec ≥ 2 PAP avec contribution active 3 mois (dont avec/sans ≥2 pilotes de plans différents)')

    # Compter les collectivités distinctes par mois et statut
    df_evolution_statut = df_pap_13.copy()
    df_evolution_statut['semaine'] = pd.to_datetime(df_evolution_statut['semaine'])
    df_evolution_statut['mois'] = df_evolution_statut['semaine'].dt.to_period('M').dt.to_timestamp()

    count_pap = df_evolution_statut.groupby(['mois', 'statut', 'collectivite_id'])['plan_id'].nunique().reset_index(name='nb_paps')
    count_pap = count_pap[(count_pap['nb_paps'] >= 2) & (count_pap['statut'] == 'actif')]

    df_evolution_statut = df_evolution_statut[df_evolution_statut['mois'] >= '2023-01-01']
    df_evolution_statut = df_evolution_statut.merge(count_pap, on=['mois', 'statut', 'collectivite_id'], how='inner')
    df_evolution_statut['multi_pilotes'] = df_evolution_statut['nb_pilotes'].apply(lambda x: '>= 2 pilotes' if x>1 else '1 pilote ou moins')


    df_evolution_statut = df_evolution_statut.groupby(['mois', 'statut', 'multi_pilotes'])['collectivite_id'].nunique().reset_index(name='nb_collectivites')
    df_evolution_statut = df_evolution_statut.sort_values('mois')
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].dt.strftime('%Y-%m')

    # Métriques pour décembre de chaque année (collectivités actives)
    df_actif = df_evolution_statut[df_evolution_statut['statut'] == 'actif']
    
    jan_2024 = df_actif[df_actif['mois_label'] == '2023-12']['nb_collectivites'].values
    jan_2025 = df_actif[df_actif['mois_label'] == '2024-12']['nb_collectivites'].values
    jan_2026 = df_actif[df_actif['mois_label'] == '2025-12']['nb_collectivites'].values
    
    val_2024 = int(jan_2024[0]) if len(jan_2024) > 0 else 0
    val_2025 = int(jan_2025[0]) if len(jan_2025) > 0 else 0
    val_2026 = int(jan_2026[0]) if len(jan_2026) > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Décembre 2023", val_2024)
    with col2:
        st.metric("Décembre 2024", val_2025, delta=val_2025 - val_2024 if val_2024 > 0 else None)
    with col3:
        st.metric("Décembre 2025", val_2026, delta=val_2026 - val_2025 if val_2025 > 0 else None)

    if len(df_evolution_statut) > 0:
        # Créer la liste de tous les mois triés chronologiquement
        tous_les_mois = df_evolution_statut.sort_values('mois')['mois_label'].unique().tolist()
        
        line_data_statuts = []
        for statut in [">= 2 pilotes", "1 pilote ou moins"]:
            df_statut = df_evolution_statut[df_evolution_statut['multi_pilotes'] == statut].copy()
            if not df_statut.empty:
                # Créer un dictionnaire pour lookup rapide
                valeurs_par_mois = dict(zip(df_statut['mois_label'], df_statut['nb_collectivites']))
                # Construire les données dans l'ordre chronologique
                line_data_statuts.append({
                    "id": statut.capitalize(),
                    "data": [
                        {"x": mois, "y": int(valeurs_par_mois.get(mois, 0))}
                        for mois in tous_les_mois
                    ]
                })
        


        if len(line_data_statuts) > 0:
            with elements("line_evolution_statuts_pap_13_fois_2"):
                with mui.Box(sx={"height": 450}):
                    nivo.Line(
                        data=line_data_statuts,
                        margin={"top": 20, "right": 160, "bottom": 60, "left": 100},
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
    st.markdown('### R-3 (💫 - Activité) : Nombre d’Actions pilotables actives avec pilote de l’action actif ≤ 12 mois')

    df_evolution_statut = df_nb_fap_pilote_13.copy()

    df_evolution_statut['mois'] = pd.to_datetime(df_evolution_statut['mois'])
    df_evolution_statut = df_evolution_statut[df_evolution_statut['mois'] >= '2023-12-01']
    df_evolution_statut = df_evolution_statut.sort_values('mois')
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].dt.strftime('%Y-%m')

    # Métriques pour décembre de chaque année (collectivités actives)
    df_actif = df_evolution_statut[df_evolution_statut['statut'] == 'actif']
    
    jan_2024 = df_actif[df_actif['mois_label'] == '2023-12']['fiche_id'].values
    jan_2025 = df_actif[df_actif['mois_label'] == '2024-12']['fiche_id'].values
    jan_2026 = df_actif[df_actif['mois_label'] == '2025-12']['fiche_id'].values
    
    val_2024 = int(jan_2024[0]) if len(jan_2024) > 0 else 0
    val_2025 = int(jan_2025[0]) if len(jan_2025) > 0 else 0
    val_2026 = int(jan_2026[0]) if len(jan_2026) > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Actifs - Décembre 2023", val_2024)
    with col2:
        st.metric("Actifs - Décembre 2024", val_2025, delta=val_2025 - val_2024 if val_2024 > 0 else None)
    with col3:
        st.metric("Actifs - Décembre 2025", val_2026, delta=val_2026 - val_2025 if val_2025 > 0 else None)

    if len(df_evolution_statut) > 0:
        # Ordre : actif en premier (en bas du stack), inactif en second (au-dessus)
        line_data_statuts = []
        for statut in ["actif", "inactif"]:
            df_statut = df_evolution_statut[df_evolution_statut['statut'] == statut].copy()
            if not df_statut.empty:
                line_data_statuts.append({
                    "id": statut.capitalize(),
                    "data": [
                        {"x": row['mois_label'], "y": int(row['fiche_id'])}
                        for _, row in df_statut.iterrows()
                    ]
                })
        
        if len(line_data_statuts) > 0:
            with elements("line_evolution_statuts_fap_pilote_13"):
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
                            "legend": "Nombre d'actions pilotables actives",
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


with tabs[2]:

    st.markdown('## Objectif 3 : QUALITÉ')
    st.markdown('Augmenter la qualité des Plans & Actions')
    st.markdown('On passe les notes initialement sur 5 à 4. 2/5 équivaut maintenant à 50% (2/4) et 4/5 équivaut maintenant à 100% (4/4)')

    st.markdown('### Q-1 (⭐ NS3 - externe) : Nombre de PAP ayant un Score de complétude ≥ 2,5 (score ≥50%)')
    
    df_evolution_statut = df_pap_note.copy()

    df_evolution_statut['semaine'] = pd.to_datetime(df_evolution_statut['semaine'])
    df_evolution_statut['mois'] = df_evolution_statut['semaine'].dt.to_period('M').dt.to_timestamp()

    df_evolution_statut = df_evolution_statut.sort_values('score', ascending=False).drop_duplicates(subset=['plan_id', 'mois'], keep='first')
    df_evolution_statut = df_evolution_statut[df_evolution_statut['mois'] >= '2023-01-01']
    
    df_evolution_statut['statut'] = df_evolution_statut['score'].apply(lambda x: "Score >=50%" if x>=2 else "Score <50%")

    df_evolution_statut = df_evolution_statut.groupby(['mois', 'statut'])['plan_id'].nunique().reset_index(name='nb_plans')

    df_evolution_statut = df_evolution_statut.sort_values('mois')
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].dt.strftime('%Y-%m')

    # Métriques pour décembre de chaque année (collectivités actives)
    df_actif = df_evolution_statut[df_evolution_statut['statut'] == 'Score >=50%']
    
    may_2025 = df_actif[df_actif['mois_label'] == '2025-05']['nb_plans'].values
    jan_2026 = df_actif[df_actif['mois_label'] == '2025-12']['nb_plans'].values
    
    val_2025 = int(may_2025[0]) if len(may_2025) > 0 else 0
    val_2026 = int(jan_2026[0]) if len(jan_2026) > 0 else 0
    
    st.metric("Score >=50% - Jan 2025", val_2026, delta=val_2026 - val_2025 if val_2026 > 0 else None)

    if len(df_evolution_statut) > 0:
        # Ordre : actif en premier (en bas du stack), inactif en second (au-dessus)
        line_data_statuts = []
        for statut in ["Score >=50%", "Score <50%"]:
            df_statut = df_evolution_statut[df_evolution_statut['statut'] == statut].copy()
            if not df_statut.empty:
                line_data_statuts.append({
                    "id": statut.capitalize(),
                    "data": [
                        {"x": row['mois_label'], "y": int(row['nb_plans'])}
                        for _, row in df_statut.iterrows()
                    ]
                })
        
        if len(line_data_statuts) > 0:
            with elements("line_evolution_statuts_pap_note_13"):
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
                            "legend": "Nombre de PAP",
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


    st.markdown('---')

    st.markdown('### Q-2 (🌟 NS3 - interne) : Nombre de PAP ayant un Score de complétude ≥3.2 (score ≥80%)')

    df_evolution_statut = df_pap_note.copy()

    df_evolution_statut['semaine'] = pd.to_datetime(df_evolution_statut['semaine'])
    df_evolution_statut['mois'] = df_evolution_statut['semaine'].dt.to_period('M').dt.to_timestamp()

    df_evolution_statut = df_evolution_statut.sort_values('score', ascending=False).drop_duplicates(subset=['plan_id', 'mois'], keep='first')
    df_evolution_statut = df_evolution_statut[df_evolution_statut['mois'] >= '2023-01-01']
    
    df_evolution_statut['statut'] = df_evolution_statut['score'].apply(lambda x: "Score >=80%" if x>=3.2 else "Score <80%")

    df_evolution_statut = df_evolution_statut.groupby(['mois', 'statut'])['plan_id'].nunique().reset_index(name='nb_plans')

    df_evolution_statut = df_evolution_statut.sort_values('mois')
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].dt.strftime('%Y-%m')

    # Métriques pour décembre de chaque année (collectivités actives)
    df_actif = df_evolution_statut[df_evolution_statut['statut'] == 'Score >=80%']
    
    may_2025 = df_actif[df_actif['mois_label'] == '2025-05']['nb_plans'].values
    jan_2026 = df_actif[df_actif['mois_label'] == '2025-12']['nb_plans'].values
    
    val_2025 = int(may_2025[0]) if len(may_2025) > 0 else 0
    val_2026 = int(jan_2026[0]) if len(jan_2026) > 0 else 0
    
    st.metric("Score >=80% - Jan 2025", val_2026, delta=val_2026 - val_2025 if val_2026 > 0 else None)

    if len(df_evolution_statut) > 0:
        # Ordre : actif en premier (en bas du stack), inactif en second (au-dessus)
        line_data_statuts = []
        for statut in ["Score >=80%", "Score <80%"]:
            df_statut = df_evolution_statut[df_evolution_statut['statut'] == statut].copy()
            if not df_statut.empty:
                line_data_statuts.append({
                    "id": statut.capitalize(),
                    "data": [
                        {"x": row['mois_label'], "y": int(row['nb_plans'])}
                        for _, row in df_statut.iterrows()
                    ]
                })
        
        if len(line_data_statuts) > 0:
            with elements("line_evolution_statuts_pap_note_13_80pct"):
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
                            "legend": "Nombre de PAP",
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



