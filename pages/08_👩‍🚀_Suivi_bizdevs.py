import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import text

from utils.data import (
    load_df_calendly_events,
    load_df_calendly_invitees,
    load_df_bizdev_contact_collectivite,
    load_df_evenements_airtable,
    load_df_pipeline_semaine
)

from utils.db import (
    get_engine_prod, read_table
)

from utils.plots import plot_area_with_totals


st.set_page_config(layout="wide")
st.title("👩‍🚀 Suivi des actions bizdevs")

# === CHARGEMENT ===
df_calendly_events = load_df_calendly_events()
df_calendly_invitees = load_df_calendly_invitees()
df_bizdev_contact_collectivite = load_df_bizdev_contact_collectivite()
df_evenements_airtable = load_df_evenements_airtable()
df_pipeline_semaine = load_df_pipeline_semaine()

# Lire la table collectivite directement depuis la prod
engine_prod = get_engine_prod()
with engine_prod.connect() as conn:
    df_collectivite = pd.read_sql_query(
        text('SELECT * FROM collectivite'),
        conn
    )

mapping_events = {
    # 'https://api.calendly.com/event_types/01a671ef-0151-423b-b8fc-875562ebb4b7': '🆘 Support - 15min pour vous débloquer',
    # 'https://api.calendly.com/event_types/0759411f-17c3-4528-85ea-a50d91c8306d': '🆘 Support - 15min pour vous débloquer',
    'https://api.calendly.com/event_types/0d8512ff-e307-4434-9900-7be0b0541c6c': '🎬 Les RDV Territoires en Transitions',
    'https://api.calendly.com/event_types/2859f624-013e-4560-be2c-5f10ace7f022': '⏏️ Démo - Commencez votre état des lieux (T.E.T.E)',
    'https://api.calendly.com/event_types/60033b52-21d5-47e3-8c39-dcd00024568c': '⏩ Démo Pilotage - Fonctionnalités expertes (2/2)',
    # 'https://api.calendly.com/event_types/61757879-a6d4-4e90-87e8-f97d516a9ea9': '🌟 Suivi Super-Utilisateurs',
    'https://api.calendly.com/event_types/cd9b2d14-85bf-46d3-8839-21bd8d7e64ba': '⏩ Démo Pilotage - Fonctionnalités expertes (2/2)',
    # 'https://api.calendly.com/event_types/d6ab7313-ef74-4f26-8d87-90c68d0204b2': '🌟 Suivi Super-Utilisateurs ( > 3 mois de pilotage)',
    'https://api.calendly.com/event_types/e065aec8-0a0a-4683-97ea-d79c76ea321f': '⏏️ Démo - Commencez votre état des lieux (T.E.T.E)',
    'https://api.calendly.com/event_types/f7554b84-1bab-40c5-ae0a-c1493b2c0d42': '▶️ Démo Pilotage - Découverte & prise en main (1/2)',
    'https://api.calendly.com/event_types/97394a2f-ecd9-47f4-9ff5-38f63918f9e9': '🎬 Démo - Nouveautés plateforme',
    'https://api.calendly.com/event_types/67efc46c-a6f8-4cff-b9fe-c70de314dd06': '▶️ Démo Pilotage - Découverte & prise en main (1/2)'
}

df_calendly_events = df_calendly_events.copy()
df_calendly_events['type'] = df_calendly_events['event_type'].map(mapping_events)
df_calendly_events['start_time'] = pd.to_datetime(df_calendly_events['start_time']).dt.tz_localize(None)

# Participants actifs uniquement
df_invitees_active = df_calendly_invitees.copy()
df_invitees_active = df_invitees_active[df_invitees_active['status'].str.lower() == 'active']
df_invitees_active = df_invitees_active.merge(
    df_calendly_events[['uri', 'type', 'start_time']], left_on='uri_event', right_on='uri', how='left'
)

# Démos uniquement
df_calendly_events = df_calendly_events[df_calendly_events['type'].notna()].copy()
df_invitees_active = df_invitees_active[df_invitees_active['type'].notna()].copy()

# === ONGLETS ===
tab1, tab2, tab3 = st.tabs(["🔑 Vue d'ensemble", "🔍 Suivi pipeline", "🎥 Participation aux démos"])

with tab1:
    ############################
    # === INDICATEURS CLÉS === #
    ############################
    st.markdown("## 🔑 Indicateurs clés")

    st.markdown('Selectionnez la période de référence (les 31 derniers jours par défaut). Les deltas sont ensuite calculés par rapport à la période précédente de même durée. Vous pouvez filtrer les collectivités par segment du pipeline.')

    today = pd.Timestamp.today().normalize()

    cstart_reach, cend_reach = st.columns(2)
    with cstart_reach:
        d1_reach = st.date_input("Début", value=today - pd.Timedelta(days=31), key="reach_debut")
    with cend_reach:
        d2_reach = st.date_input("Fin", value=today.date(), key="reach_fin")

    cur_start = pd.to_datetime(d1_reach)
    cur_end = pd.to_datetime(d2_reach)
    prev_start = cur_start - (cur_end - cur_start)
    prev_end = cur_start - pd.Timedelta(seconds=1)

    # Segmented control pour filtrer les collectivités
    filtre_collectivites = st.segmented_control(
        "Filtre par segment du pipeline ",
        options=["Toutes les CT", "Activation & Conversion", "Retention"],
        default="Toutes les CT",
        key="filtre_collectivites_tab1"
    )

    st.markdown("---")

    st.markdown("### Actions de contact et échanges utilisateurs :blue-badge[:material/edit_note: Notes de suivi]")

    # Préparation des dates pour le reach
    df_biz = df_bizdev_contact_collectivite.copy()
    if not df_biz.empty:
        df_biz['date_contact'] = pd.to_datetime(df_biz['date_contact'], errors='coerce').dt.tz_localize(None)

    # Filtrage des collectivités selon le segmented control
    if filtre_collectivites != "Toutes les CT":
        liste_pipelines = ['En activation', 'A acquérir', 'En test (+6 mois)', 'En test (-6 mois)', 'En conversion']
        
        df_pipeline_semaine_filtered = df_pipeline_semaine[
            pd.to_datetime(df_pipeline_semaine.semaine) >= cur_start
        ]
        
        if filtre_collectivites == "Activation & Conversion":
            # Filtrer les collectivités dans la liste des pipelines
            df_pipeline_semaine_filtered = df_pipeline_semaine_filtered[
                df_pipeline_semaine_filtered.pipeline.isin(liste_pipelines)
            ]
        else:  # Retention
            # Filtrer les collectivités NOT in la liste des pipelines
            df_pipeline_semaine_filtered = df_pipeline_semaine_filtered[
                ~df_pipeline_semaine_filtered.pipeline.isin(liste_pipelines)
            ]
        
        df_biz = df_biz[df_biz.collectivite_id.isin(df_pipeline_semaine_filtered.collectivite_id)].copy()

    reach_cur = df_biz[(df_biz['date_contact'] >= cur_start) & (df_biz['date_contact'] <= today)] if not df_biz.empty else df_biz
    reach_prev = df_biz[(df_biz['date_contact'] >= prev_start) & (df_biz['date_contact'] <= prev_end)] if not df_biz.empty else df_biz

    total_reach_cur = int(len(reach_cur))
    total_reach_prev = int(len(reach_prev))
    delta_reach = ("+∞%" if total_reach_prev == 0 and total_reach_cur > 0 else
                "0%" if total_reach_prev == 0 else
                f"{((total_reach_cur - total_reach_prev) / total_reach_prev * 100):+.0f}%")

    ct_reach_cur = int(reach_cur['collectivite_id'].nunique()) if not reach_cur.empty else 0
    ct_reach_prev = int(reach_prev['collectivite_id'].nunique()) if not reach_prev.empty else 0
    delta_ct = ("+∞%" if ct_reach_prev == 0 and ct_reach_cur > 0 else
                "0%" if ct_reach_prev == 0 else
                f"{((ct_reach_cur - ct_reach_prev) / ct_reach_prev * 100):+.0f}%")

    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.metric(
            label="Actions de contact",
            value=total_reach_cur,
            delta=delta_reach,
            delta_color="normal"
        )
    with col_r2:
        st.metric(
            label="Collectivités uniques contactés",
            value=ct_reach_cur,
            delta=delta_ct,
            delta_color="normal"
        )

    cols_buttons = st.columns([1, 2, 2])
    with cols_buttons[0]:
        affichage_type = st.segmented_control(
        "Type d'affichage",
        options=["Graphe", "Tableau"],
        default="Graphe",
        key="reach_affichage",
    )
    with cols_buttons[1]:
        niveau_agregation = st.segmented_control(
        "Niveau d'agrégation (graphe)",
        options=["Actions de contact", "Collectivités uniques contactées"],
        default="Actions de contact",
        key="reach_niveau",
        )

    start_date_reach = pd.to_datetime(d1_reach)
    end_date_reach = pd.to_datetime(d2_reach) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
        

    # Filtrage des données bizdev
    df_biz_reach = df_bizdev_contact_collectivite.copy()
    if not df_biz_reach.empty:
        df_biz_reach['date_contact'] = pd.to_datetime(df_biz_reach['date_contact'], errors='coerce').dt.tz_localize(None)
        df_biz_reach_filtre = df_biz_reach[(df_biz_reach['date_contact'] >= start_date_reach) & (df_biz_reach['date_contact'] <= end_date_reach)]
    else:
        df_biz_reach_filtre = df_biz_reach

    if not df_biz_reach_filtre.empty:
        # Agrégation par mois
        df_reach_mois = df_biz_reach_filtre.copy()
        df_reach_mois['mois'] = df_reach_mois['date_contact'].dt.to_period('W').dt.to_timestamp()
        
        # Calcul du reach brut et des collectivités par mois
        df_agg_mois = df_reach_mois.groupby('mois').agg({
            'date_contact': 'count',  # Reach brut
            'collectivite_id': 'nunique'  # Collectivités uniques
        }).reset_index()
        df_agg_mois.columns = ['Semaine', 'Contacts', 'Collectivités uniques']
        df_agg_mois['Semaine'] = df_agg_mois['Semaine'].dt.strftime('%Y-%m-%d')
        
        # Calcul du nombre de collectivités uniques sur la période
        nb_collectivites_uniques = int(df_biz_reach_filtre['collectivite_id'].nunique())

        if affichage_type == "Graphe":
            # Graphe selon le niveau d'agrégation
            if niveau_agregation == "Actions de contact":
                fig_reach = px.line(
                    df_agg_mois, 
                    x='Semaine', 
                    y='Contacts', 
                    title="", 
                    height=500)
                fig_reach.update_layout(xaxis_title="Semaine", yaxis_title="Actions de contacts")
            else:
                fig_reach = px.line(
                    df_agg_mois, 
                    x='Semaine', 
                    y='Collectivités uniques', 
                    title="",
                    height=500)
                fig_reach.update_layout(xaxis_title="Semaine", yaxis_title="Collectivités uniques")
            
            st.plotly_chart(fig_reach, use_container_width=True)
        else:
            # Affichage tableau avec les deux colonnes
            st.dataframe(df_agg_mois, use_container_width=True)
    else:
        st.info("Aucune donnée de contacts sur la période sélectionnée.")

    st.markdown("---")
    st.markdown("### Echanges enregistrés :orange-badge[:material/checklist_rtl: Activités & Feedbacks  ]")



    # Préparation des dates pour les événements Airtable
    df_evt = df_evenements_airtable.copy()
    if not df_evt.empty:
        df_evt['Date'] = pd.to_datetime(df_evt['Date'], errors='coerce').dt.tz_localize(None)
        
        evt_cur = df_evt[(df_evt['Date'] >= cur_start) & (df_evt['Date'] <= today)]
        evt_prev = df_evt[(df_evt['Date'] >= prev_start) & (df_evt['Date'] <= prev_end)]
        
        # Comptages par type d'événement
        evt_cur_g = evt_cur.groupby('evenements').size().rename('evt_30j')
        evt_prev_g = evt_prev.groupby('evenements').size().rename('evt_prev')
        
        kpis_evt = pd.concat([evt_cur_g, evt_prev_g], axis=1).fillna(0).astype(int).reset_index().rename(columns={'index': 'evenements'})
        
        def pct_delta_evt(cur: int, prev: int) -> str:
            if prev == 0:
                return "+∞%" if cur > 0 else "0%"
            return f"{((cur - prev) / prev * 100):+.0f}%"
        
        kpis_evt['Δ événements'] = kpis_evt.apply(lambda r: pct_delta_evt(r['evt_30j'], r['evt_prev']), axis=1)
        kpis_evt = kpis_evt[['evenements', 'evt_30j', 'Δ événements']].sort_values('evt_30j', ascending=False)
        
        # Affichage par type d'événement
        nb_types_evt = len(kpis_evt)
        if nb_types_evt == 0:
            st.info("Pas de données sur les 30 derniers jours.")
        else:
            cols_per_row = min(len(kpis_evt), 4)
            cols = st.columns(cols_per_row)
            for i, row in kpis_evt.reset_index(drop=True).iterrows():
                with cols[i % cols_per_row]:
                    st.metric(
                        label=row['evenements'],
                        value=int(row['evt_30j']),
                        delta=row['Δ événements'],
                        delta_color="normal"
                    )
    else:
        st.info("Aucune donnée d'événements disponible.")

with tab2:
    
    # Mapping des couleurs par pipeline
    pipe_color_mapping = {
        "A acquérir": "#C8C8C8",            # gris clair
        "En activation": "#E6B0FF",         # rose/violet clair
        "En test (+6 mois)": "#D7D6FF",     # lavande
        "En test (-6 mois)": "#BCA6FF",     # violet moyen
        "En conversion": "#FFD966",         # jaune
        "En rétention": "#A6ECA5",          # vert clair
        "En pilotage": "#8FD9A8",           # vert menthe
        "En rétention (à surveiller)": "#F7B896",   # orange clair
        "En pilotage (à surveiller)": "#F7C8A0",    # beige orangé
        "En rétention (à réactiver)": "#FF9966",    # orange soutenu
        "En pilotage (à réactiver)": "#FFB399"      # saumon clair
    }
    
    # Chargement et préparation des données
    df_pipe = df_pipeline_semaine.copy()
    df_ct = df_collectivite.copy()
    
    # Filtrer les collectivités de test
    df_ct = df_ct[df_ct['type'] != 'test'].copy()
    
    # Prendre uniquement id et type
    df_ct = df_ct[['id', 'type']].copy()
    
    # Jointure avec collectivités
    df_pipe = df_pipe.merge(df_ct, left_on='collectivite_id', right_on='id', how='inner')
    
    # Prendre la semaine la plus récente
    if not df_pipe.empty:
        semaine_recente = df_pipe['semaine'].max()
        
        # Filtre par type de collectivité
        st.markdown("### Filtres")
        types_disponibles = sorted(df_pipe['type'].dropna().unique().tolist())
        types_selection = st.multiselect(
            "Type de collectivité",
            options=types_disponibles,
            default=types_disponibles,
            key="type_collectivite_filter"
        )
        
        semaine_selection = st.selectbox(
            "Sélectionner une semaine",
            options=df_pipe['semaine'].sort_values(ascending=False).unique().tolist(),
            key="semaine_selection"
        )
        
        # Appliquer le filtre
        df_pipe = df_pipe[df_pipe['pipeline'] != 'A acquérir'].copy()
        df_pipe_filtre = df_pipe[df_pipe['type'].isin(types_selection) & (df_pipe['semaine'] == semaine_selection)].copy()
        
        if not df_pipe_filtre.empty:
            # Calcul des comptes par pipeline
            pipeline_counts = df_pipe_filtre['pipeline'].value_counts().reset_index()
            pipeline_counts.columns = ['Pipeline', 'Nombre de collectivités']
            
            # Trouver la semaine S-4
            semaines_triees = sorted(df_pipe['semaine'].unique())
            idx_semaine_actuelle = semaines_triees.index(semaine_selection) if semaine_selection in semaines_triees else -1
            
            if idx_semaine_actuelle >= 4:
                semaine_s4 = semaines_triees[idx_semaine_actuelle - 4]
                
                # Calculer les counts pour S-4 avec les mêmes filtres de type
                df_pipe_s4 = df_pipe[df_pipe['type'].isin(types_selection) & (df_pipe['semaine'] == semaine_s4)].copy()
                
                if not df_pipe_s4.empty:
                    pipeline_counts_s4 = df_pipe_s4['pipeline'].value_counts().reset_index()
                    pipeline_counts_s4.columns = ['Pipeline', 'Nombre S-4']
                    
                    # Joindre avec les counts actuels
                    pipeline_counts = pipeline_counts.merge(pipeline_counts_s4, on='Pipeline', how='left')
                    pipeline_counts['Nombre S-4'] = pipeline_counts['Nombre S-4'].fillna(0).astype(int)
                    
                    # Calculer le delta
                    pipeline_counts['delta'] = pipeline_counts['Nombre de collectivités'] - pipeline_counts['Nombre S-4']
                    
                    # Créer le texte d'affichage
                    pipeline_counts['text_display'] = pipeline_counts.apply(
                        lambda row: f"{int(row['Nombre de collectivités'])} ({row['delta']:+d})" 
                        if row['delta'] != 0 
                        else f"{int(row['Nombre de collectivités'])}",
                        axis=1
                    )
                else:
                    # Pas de données S-4, afficher juste le nombre
                    pipeline_counts['text_display'] = pipeline_counts['Nombre de collectivités'].astype(str)
            else:
                # Pas assez de semaines historiques, afficher juste le nombre
                pipeline_counts['text_display'] = pipeline_counts['Nombre de collectivités'].astype(str)
            
            # Affichage de la date de la semaine

            st.markdown("---")
            st.markdown("### 📊 Répartition")
            st.markdown("Les deltas sont calculés par rapport à l'état des pipes 4 semaines plus tôt.")

            # Histogramme
            fig = px.bar(
                pipeline_counts,
                x='Pipeline',
                y='Nombre de collectivités',
                color='Pipeline',
                color_discrete_map=pipe_color_mapping,
                text='text_display',
                height=500
            )
            fig.update_traces(textposition='outside')
            fig.update_layout(
                xaxis_title="",
                yaxis_title="",
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # === ÉVOLUTION D'UN PIPELINE ===
            st.markdown("---")
            st.markdown("### 📈 Évolution")
            
            # Sélection du pipeline à analyser
            pipelines_disponibles = sorted(df_pipe_filtre['pipeline'].unique().tolist())
            pipeline_selection = st.selectbox(
                "Sélectionner un pipeline",
                options=pipelines_disponibles,
                key="pipeline_evolution"
            )
            
            if pipeline_selection:
                # Filtrer les données historiques pour ce pipeline et ces types de collectivités
                df_pipe_evolution = df_pipe[
                    (df_pipe['pipeline'] == pipeline_selection) & 
                    (df_pipe['type'].isin(types_selection))
                ].copy()
                
                if not df_pipe_evolution.empty:
                    # Convertir la colonne semaine en datetime
                    df_pipe_evolution['semaine'] = pd.to_datetime(df_pipe_evolution['semaine'])
                    
                    # Grouper par semaine et compter les collectivités
                    evolution = df_pipe_evolution.groupby('semaine')['collectivite_id'].nunique().reset_index()
                    evolution.columns = ['Semaine', 'Nombre de collectivités']
                    evolution = evolution.sort_values('Semaine')
                    
                    # Graphique d'évolution
                    fig_evolution = px.line(
                        evolution,
                        x='Semaine',
                        y='Nombre de collectivités',
                        title=f"Évolution du nombre de collectivités - {pipeline_selection}",
                        markers=True
                    )
                    
                    # Appliquer la couleur du pipeline
                    pipeline_color = pipe_color_mapping.get(pipeline_selection, "#3366CC")
                    fig_evolution.update_traces(
                        line_color=pipeline_color,
                        marker=dict(size=8, color=pipeline_color)
                    )
                    
                    fig_evolution.update_layout(
                        xaxis_title="Semaine",
                        yaxis_title="Nombre de collectivités",
                        height=500
                    )
                    
                    st.plotly_chart(fig_evolution, use_container_width=True)
                    
                else:
                    st.info(f"Aucune donnée historique disponible pour le pipeline '{pipeline_selection}' avec les types sélectionnés.")

        else:
            st.info("Aucune donnée disponible pour les types de collectivités sélectionnés.")
    else:
        st.info("Aucune donnée de pipeline disponible.")

with tab3:
    st.markdown("## 🎥 Participation aux démos")
    st.markdown('Selectionnez la période de référence (les 31 derniers jours par défaut). Les deltas sont ensuite calculés par rapport à la période précédente de même durée.')

    today = pd.Timestamp.today().normalize()    

    cstart_reach, cend_reach = st.columns(2)
    with cstart_reach:
        d1_reach = st.date_input("Début", value=today - pd.Timedelta(days=31), key="reach_debut_2")
    with cend_reach:
        d2_reach = st.date_input("Fin", value=today.date(), key="reach_fin_2")

    cur_start = pd.to_datetime(d1_reach)
    cur_end = pd.to_datetime(d2_reach)
    prev_start = cur_start - (cur_end - cur_start)
    prev_end = cur_start - pd.Timedelta(seconds=1)

    st.markdown("---")

    st.markdown("### Evenements et taux de remplissage")


    # Filtrages
    events_cur = df_calendly_events[(df_calendly_events['start_time'] >= cur_start) & (df_calendly_events['start_time'] <= today)]
    events_prev = df_calendly_events[(df_calendly_events['start_time'] >= prev_start) & (df_calendly_events['start_time'] <= prev_end)]
    inv_cur = df_invitees_active[(df_invitees_active['start_time'] >= cur_start) & (df_invitees_active['start_time'] <= today)]
    inv_prev = df_invitees_active[(df_invitees_active['start_time'] >= prev_start) & (df_invitees_active['start_time'] <= prev_end)]


    type_selection = ['▶️ Démo Pilotage - Découverte & prise en main (1/2)', '▶️ Démo Pilotage - Fonctionnalités expertes (2/2)', '⏏️ Démo - Commencez votre état des lieux (T.E.T.E)']

    # Calcul du taux de remplissage global
    # Total participants = somme de nb_participants_reel sur tous les événements
    # Total inscrits = nombre d'inscrits (lignes dans invitees)
    total_participants_cur = int(events_cur[events_cur['type'].isin(type_selection)]['nb_participants_reel'].sum())
    total_inscrits_cur = len(inv_cur[inv_cur['type'].isin(type_selection)])
    taux_remplissage_cur = (total_participants_cur / total_inscrits_cur * 100) if total_inscrits_cur > 0 else 0

    # Calcul période précédente
    total_participants_prev = int(events_prev['nb_participants_reel'].sum())
    total_inscrits_prev = len(inv_prev)
    taux_remplissage_prev = (total_participants_prev / total_inscrits_prev * 100) if total_inscrits_prev > 0 else 0

    delta_taux = taux_remplissage_cur - taux_remplissage_prev

    # Affichage du taux de remplissage global
    st.metric(
        label="Taux de remplissage global (seulement démos)",
        value=f"{taux_remplissage_cur:.0f}%",
        delta=f"{delta_taux:+.0f}%",
        delta_color="normal"
    )

    # Comptages par type
    events_cur_g = events_cur.groupby('type').size().rename('events_30j')
    inv_cur_g = inv_cur.groupby('type').size().rename('inscrits_30j')

    # Participants réels (nouvelle colonne nb_participants_reel)
    if 'nb_participants_reel' in events_cur.columns:
        part_cur_g = events_cur.groupby('type')['nb_participants_reel'].sum().rename('participants_30j')
    else:
        part_cur_g = pd.Series(dtype=int, name='participants_30j')

    kpis = pd.concat([events_cur_g, inv_cur_g, part_cur_g], axis=1).fillna(0).astype(int).reset_index().rename(columns={'index': 'type'})
    kpis = kpis[['type', 'events_30j', 'inscrits_30j', 'participants_30j']].sort_values('events_30j', ascending=False)

    # Affichage "sexy" façon Weekly: cartes de métriques par type
    nb_types = len(kpis)
    if nb_types == 0:
        st.info("Pas de données sur les 30 derniers jours.")
    else:
        cols_per_row = 3
        cols = st.columns(cols_per_row)
        for i, row in kpis.reset_index(drop=True).iterrows():
            with cols[i % cols_per_row]:
                st.markdown(
                    f"""
                    <div style="background: linear-gradient(90deg,#EEF6FF,#F8FAFF); border:1px solid #E5EAF2; border-radius: 12px; padding: 14px 14px 6px 14px; margin-bottom: 12px;">
                    <div style="font-weight:600; font-size:14px; color:#334155; margin-bottom:8px;">{row['type']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                c_ev, c_in, c_pa = st.columns(3)
                with c_ev:
                    st.metric(
                        label="Événements",
                        value=int(row['events_30j'])
                    )
                with c_in:
                    st.metric(
                        label="Inscrits",
                        value=int(row['inscrits_30j'])
                    )
                with c_pa:
                    st.metric(
                        label="Participants",
                        value=int(row['participants_30j'])
                    )

    st.markdown("## Calendly")

    start_date = cur_start
    end_date = cur_end

    # Sélection du type d'événement (centré et plus étroit)
    types_disponibles = df_calendly_events['type'].dropna().sort_values().unique().tolist()
    type_defaut = '▶️ Démo Pilotage - Découverte & prise en main (1/2)'
    type_selection = st.selectbox(
        "Type d'événement",
        options=types_disponibles,
        index=types_disponibles.index(type_defaut) if type_defaut in types_disponibles else 0,
        key="type_focus",
    )

    # Filtres focus
    events_filtres = df_calendly_events[(df_calendly_events['start_time'] >= start_date) & (df_calendly_events['start_time'] <= end_date) & (df_calendly_events['type'] == type_selection)]
    invitees_filtres = df_invitees_active[(df_invitees_active['start_time'] >= start_date) & (df_invitees_active['start_time'] <= end_date) & (df_invitees_active['type'] == type_selection)]

    # Préparation des données pour les participants réels
    if 'nb_participants_reel' in events_filtres.columns:
        # Créer un dataframe avec les participants réels par événement
        participants_reel_filtres = events_filtres[['start_time', 'type', 'nb_participants_reel']].copy()
        participants_reel_filtres = participants_reel_filtres[participants_reel_filtres['nb_participants_reel'] > 0]
    else:
        # Fallback sur les inscrits actifs si la colonne n'existe pas
        participants_reel_filtres = invitees_filtres.copy()

    # === TABLEAUX MENSUELS ===

    def monthly_single_table(events_df: pd.DataFrame, invitees_df: pd.DataFrame, participants_df: pd.DataFrame, date_col: str) -> pd.DataFrame:
        # Table unique quand un seul type est sélectionné
        e = events_df.copy()
        i = invitees_df.copy()
        p = participants_df.copy()
        if e.empty and i.empty and p.empty:
            return pd.DataFrame()
        for df in (e, i, p):
            if not df.empty:
                df[date_col] = pd.to_datetime(df[date_col]).dt.tz_localize(None)
                df['mois'] = df[date_col].dt.to_period('M').dt.to_timestamp()
        
        ev = e.groupby('mois').size().rename('Événements') if not e.empty else pd.Series(dtype=int, name='Événements')
        inscr = i.groupby('mois').size().rename('Inscrits') if not i.empty else pd.Series(dtype=int, name='Inscrits')
        
        # Utiliser nb_participants_reel si disponible, sinon compter les lignes
        if 'nb_participants_reel' in p.columns and not p.empty:
            pa = p.groupby('mois')['nb_participants_reel'].sum().rename('Participants')
        else:
            pa = p.groupby('mois').size().rename('Participants') if not p.empty else pd.Series(dtype=int, name='Participants')
        
        dfm = pd.concat([ev, inscr, pa], axis=1).fillna(0).astype(int).sort_index()
        
        # Calcul du taux de remplissage
        dfm['Taux de remplissage (%)'] = dfm.apply(
            lambda row: round(row['Participants'] / row['Inscrits'] * 100) if row['Inscrits'] > 0 else 0,
            axis=1
        )
        
        dfm.index = dfm.index.strftime('%Y-%m')
        return dfm

    # Rendu du tableau
    table_single = monthly_single_table(events_filtres, invitees_filtres, participants_reel_filtres, 'start_time')
    if not table_single.empty:
        st.dataframe(table_single, use_container_width=True)
    else:
        st.info("Aucune donnée disponible pour la période et l'événement sélectionnés.")

    ############################################
    # === COMMENT ONT-ILS TROUVÉ LA DÉMO 1/2 ?
    ############################################
    st.markdown("---")
    st.markdown("### 🔍 Comment ont-ils trouvé la démo 1/2 ?")

    min_dt = df_calendly_events['start_time'].min()
    max_dt = df_calendly_events['start_time'].max()

    pie_c1, pie_c2 = st.columns(2)
    with pie_c1:
        d1_pie = st.date_input("Début (démo)", value=max(min_dt.date(), (today - pd.Timedelta(days=30)).date()))
    with pie_c2:
        d2_pie = st.date_input("Fin (démo)", value=today.date())

    pie_start = pd.to_datetime(d1_pie)
    pie_end = pd.to_datetime(d2_pie) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

    demo12 = df_invitees_active[(df_invitees_active['type'] == '▶️ Démo Pilotage - Découverte & prise en main (1/2)') & (df_invitees_active['start_time'] >= pie_start) & (df_invitees_active['start_time'] <= pie_end)][['reponse']].copy()

    def parse_reponse(value: str) -> list[str]:
        if pd.isna(value):
            return []
        txt = str(value).strip()
        txt = ' '.join(txt.split())
        try:
            import json
            parsed = json.loads(txt)
            if isinstance(parsed, list):
                return [str(x).strip() for x in parsed if str(x).strip()]
            if isinstance(parsed, dict):
                return [f"{k}: {v}" for k, v in parsed.items()]
        except Exception:
            pass
        import re
        matches = re.findall(r'"([^"]+)"', txt)
        if matches:
            return [m.strip() for m in matches if m.strip()]
        sep = ';' if ';' in txt else ','
        items = [item.strip() for item in txt.strip('{} ').split(sep) if item.strip()]
        items = [' '.join(i.split()) for i in items]
        return items

    demo12['items'] = demo12['reponse'].apply(parse_reponse)
    pie_df = demo12.explode('items').dropna(subset=['items'])

    if pie_df.empty:
        st.info("Aucun retour disponible sur la période sélectionnée.")
    else:
        total_counts = pie_df['items'].value_counts().reset_index()
        total_counts.columns = ['items', 'nb']
        left, center, right = st.columns([1, 5, 1])
        with center:
            total_counts_filtre = total_counts[total_counts['nb'] > 3]
            fig_pie = px.pie(total_counts_filtre, values='nb', names='items', title="Répartition des retours (Démo 1/2)")
            st.plotly_chart(fig_pie, use_container_width=True)
            # Export CSV des comptes agrégés affichés
            csv_pie = total_counts.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Exporter CSV retours démo 1/2",
                data=csv_pie,
                file_name="retours_demo12_agg.csv",
                mime="text/csv"
            )
