import streamlit as st
# Configuration de la page en premier
st.set_page_config(layout="wide")

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import text
import calendar
from utils.db import get_engine_prod, read_table

# ==========================
# Chargement des données
# ==========================

@st.cache_resource(ttl="2d")
def load_data():
    df_calendly_events = read_table('calendly_events')
    df_calendly_invitees = read_table('calendly_invitees')
    df_bizdev_note_de_suivi = read_table('bizdev_note_de_suivi_contact')
    df_bizdev_af = read_table('bizdev_A_F_contact')
    df_pipeline_semaine = read_table('airtable_sync_semaine', columns=['collectivite_id', 'semaine', 'pipeline'])
    df_passage_pap = read_table('pap_date_passage')
    df_pap_13 = read_table('pap_statut_5_fiches_modifiees_13_semaines')
    df_note_plan = read_table('note_plan_historique')

    # Lire la table collectivite directement depuis la prod
    engine_prod = get_engine_prod()
    with engine_prod.connect() as conn:
        df_collectivite = pd.read_sql_query(
            text('SELECT * FROM collectivite'),
            conn
        )
    return df_calendly_events, df_calendly_invitees, df_bizdev_note_de_suivi, df_bizdev_af, df_pipeline_semaine, df_collectivite, df_passage_pap, df_pap_13, df_note_plan

df_calendly_events, df_calendly_invitees, df_bizdev_note_de_suivi, df_bizdev_af, df_pipeline_semaine, df_collectivite, df_passage_pap, df_pap_13, df_note_plan = load_data()


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
    
    # Calcul du taux de participation
    dfm['Taux de participation des inscrits (%)'] = dfm.apply(
        lambda row: round(row['Participants'] / row['Inscrits'] * 100) if row['Inscrits'] > 0 else 0,
        axis=1
    )
    
    # Calcul du taux de remplissage absolu
    dfm['Taux de participation absolu (%)'] = dfm.apply(
        lambda row: round(row['Participants'] / (row['Événements'] * 8) * 100) if row['Événements'] > 0 else 0,
        axis=1
    )
    
    dfm.index = dfm.index.strftime('%Y-%m')
    return dfm

# ==========================
# Interface
# ==========================

st.title("👩‍🚀 Dashboard Bizdevs")

st.segmented_control("Période", options=["Semaine", "Mois", "3 mois", "All Time"], default="Mois", key="view_bizdevs")

_MOIS_FR = ["", "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
            "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
if st.session_state.get("view_bizdevs", "Mois") == "Mois":
    _today_for_picker = pd.Timestamp.today().normalize()
    _month_options = []
    _y, _m = 2025, 1
    while (_y, _m) <= (_today_for_picker.year, _today_for_picker.month):
        _month_options.append(f"{_y}-{_m:02d}")
        _m += 1
        if _m > 12:
            _m = 1
            _y += 1
    _col_month, _ = st.columns([1, 3])
    with _col_month:
        st.selectbox(
            "Mois à afficher",
            options=_month_options,
            index=len(_month_options) - 1,
            format_func=lambda x: f"{_MOIS_FR[int(x.split('-')[1])]} {x.split('-')[0]}",
            key="selected_month_bizdevs"
        )

st.markdown("---")

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



############################
# === INDICATEURS CLÉS === #
############################
st.badge("🌟 North Stars", color="orange")
#st.markdown("## 🌟 North Stars")

# Préparation des données à partir de df_pap_13
df_pap_data = df_pap_13.copy()
df_pap_data['mois'] = pd.to_datetime(df_pap_data['mois']).dt.to_period('M').dt.to_timestamp()
df_pap_data = df_pap_data[df_pap_data['mois'] >= '2024-01-01']

# === CT PAP (1+ plan) : calcul actif/inactif ===
# Pour chaque CT/mois, déterminer si elle a au moins 1 plan actif
df_pap_actifs = df_pap_data[df_pap_data['statut'] == 'actif'].groupby(['mois', 'collectivite_id'])['plan'].nunique().reset_index(name='nb_plans_actifs')
ct_pap_all = df_pap_data.groupby(['mois', 'collectivite_id'])['plan'].nunique().reset_index(name='nb_plans_total')
ct_pap_all = ct_pap_all.merge(df_pap_actifs, on=['mois', 'collectivite_id'], how='left')
ct_pap_all['nb_plans_actifs'] = ct_pap_all['nb_plans_actifs'].fillna(0)
ct_pap_all['statut_pap'] = ct_pap_all['nb_plans_actifs'].apply(lambda x: 'actif' if x >= 1 else 'inactif')

# Grouper par mois/statut pour CT PAP
df_pap_statut = ct_pap_all.groupby(['mois', 'statut_pap'])['collectivite_id'].nunique().reset_index(name='nb_collectivites')
df_pap_statut.rename(columns={'statut_pap': 'statut'}, inplace=True)
df_pap_statut = df_pap_statut.sort_values('mois')

# Pour nouvelles CT PAP : première apparition d'une CT dans df_pap_data
ct_first_pap = df_pap_data.sort_values(['collectivite_id', 'mois']).drop_duplicates(subset='collectivite_id', keep='first')[['collectivite_id', 'mois']].copy()
ct_first_pap.rename(columns={'mois': 'date_premier_pap'}, inplace=True)

# === CT Multiplans (2+ plans) : calcul actif/inactif ===
# Étape 1 : Compter le nombre total de plans par CT/mois
nb_plans_total = df_pap_data.groupby(['mois', 'collectivite_id'])['plan'].nunique().reset_index(name='nb_plans_total')

# Étape 2 : Garder uniquement les CT qui ont 2+ plans
ct_multiplans = nb_plans_total[nb_plans_total['nb_plans_total'] >= 2][['mois', 'collectivite_id']]

# Étape 3 : Pour ces CT multiplans, compter le nombre de plans actifs
df_multiplans = df_pap_data.merge(ct_multiplans, on=['mois', 'collectivite_id'], how='inner')
nb_plans_actifs_mp = df_multiplans[df_multiplans['statut'] == 'actif'].groupby(['mois', 'collectivite_id'])['plan'].nunique().reset_index(name='nb_plans_actifs')

# Étape 4 : Fusionner et déterminer le statut final (actif si 2+ plans actifs, sinon inactif)
df_multiplans_final = ct_multiplans.merge(nb_plans_actifs_mp, on=['mois', 'collectivite_id'], how='left')
df_multiplans_final['nb_plans_actifs'] = df_multiplans_final['nb_plans_actifs'].fillna(0)
df_multiplans_final['statut_mp'] = df_multiplans_final['nb_plans_actifs'].apply(lambda x: 'actif' if x >= 2 else 'inactif')

# Grouper par mois/statut pour CT multiplans
df_multiplans_statut = df_multiplans_final.groupby(['mois', 'statut_mp'])['collectivite_id'].nunique().reset_index(name='nb_collectivites')
df_multiplans_statut.rename(columns={'statut_mp': 'statut'}, inplace=True)
df_multiplans_statut = df_multiplans_statut.sort_values('mois')

# Pour nouvelles CT multiplans : première apparition d'une CT avec 2+ plans
ct_first_multiplan = ct_multiplans.sort_values(['collectivite_id', 'mois']).drop_duplicates(subset='collectivite_id', keep='first')[['collectivite_id', 'mois']].copy()
ct_first_multiplan.rename(columns={'mois': 'date_premier_multiplan'}, inplace=True)

# === Note des plans PAP ===
df_evolution_note = df_note_plan.copy()
df_evolution_note['statut'] = df_evolution_note['note_plan'].apply(lambda x: '>= 8' if x>=8 else '< 8')
df_evolution_note['mois'] = pd.to_datetime(df_evolution_note['mois'])
df_evolution_note['mois'] = df_evolution_note['mois'].dt.to_period('M').dt.to_timestamp()
df_evolution_note = df_evolution_note[df_evolution_note['mois'] >= '2024-01-01']
df_evolution_note = df_evolution_note.groupby(['mois', 'statut'])['plan'].nunique().reset_index(name='nb_plans')
df_evolution_note = df_evolution_note.sort_values('mois')

# Filtrer uniquement les plans >= 8 pour les métriques
df_plans_8plus = df_evolution_note[df_evolution_note['statut'] == '>= 8'].copy()



# Calcul des périodes selon la vue sélectionnée
today = pd.Timestamp.today().normalize()
view = st.session_state.get("view_bizdevs", "Mois")
is_all_time = (view == "All Time")

if view == "Mois":
    _selected = st.session_state.get("selected_month_bizdevs", f"{today.year}-{today.month:02d}")
    sel_y, sel_m = int(_selected.split('-')[0]), int(_selected.split('-')[1])
    cur_start = pd.Timestamp(year=sel_y, month=sel_m, day=1)
    if sel_y == today.year and sel_m == today.month:
        cur_end = today
    else:
        cur_end = pd.Timestamp(year=sel_y, month=sel_m, day=calendar.monthrange(sel_y, sel_m)[1])
    # Mois précédent pour le delta
    prev_m = sel_m - 1 if sel_m > 1 else 12
    prev_y = sel_y if sel_m > 1 else sel_y - 1
    prev_start = pd.Timestamp(year=prev_y, month=prev_m, day=1)
    prev_end = pd.Timestamp(year=prev_y, month=prev_m, day=calendar.monthrange(prev_y, prev_m)[1])
elif view == "Semaine":
    nb_days = 7
    cur_start = today - pd.Timedelta(days=nb_days)
    cur_end = today
    prev_start = cur_start - pd.Timedelta(days=nb_days)
    prev_end = cur_start - pd.Timedelta(seconds=1)
elif view == "3 mois":
    nb_days = 90
    cur_start = today - pd.Timedelta(days=nb_days)
    cur_end = today
    prev_start = cur_start - pd.Timedelta(days=nb_days)
    prev_end = cur_start - pd.Timedelta(seconds=1)
else:  # All Time
    nb_days = 31
    cur_start = today - pd.Timedelta(days=nb_days)
    cur_end = today
    prev_start = cur_start - pd.Timedelta(days=nb_days)
    prev_end = cur_start - pd.Timedelta(seconds=1)

# === Métriques CT PAP et Multiplans ===
if view == "Semaine":
    st.warning("Pas de vue semaine pour les North Stars, rendez-vous sur le [dashboard Weekly](/Weekly) pour voir ces stats.")
elif is_all_time:
    # Mode All Time : afficher 5 métriques sur une ligne
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if not df_pap_statut.empty:
            latest_month = df_pap_statut['mois'].max()
            df_latest_pap = df_pap_statut[df_pap_statut['mois'] == latest_month]
            actif_pap = int(df_latest_pap.loc[df_latest_pap['statut'] == 'actif', 'nb_collectivites'].sum())
            st.metric(
                label="CT PAP actives", 
                value=actif_pap,
                help="CT avec au moins 1 PAP actif (5+ fiches modifiées sur les 3 derniers mois)"
            )
        else:
            st.metric(label="CT PAP actives", value=0, help="CCT avec au moins 1 PAP actif (5+ fiches modifiées sur les 3 derniers mois)")
    
    with col2:
        if not df_pap_statut.empty:
            latest_month = df_pap_statut['mois'].max()
            df_latest_pap = df_pap_statut[df_pap_statut['mois'] == latest_month]
            inactif_pap = int(df_latest_pap.loc[df_latest_pap['statut'] == 'inactif', 'nb_collectivites'].sum())
            st.metric(
                label="CT PAP inactives", 
                value=inactif_pap
            )
        else:
            st.metric(label="CT PAP inactives", value=0)
    
    with col3:
        if not df_multiplans_statut.empty:
            latest_month = df_multiplans_statut['mois'].max()
            df_latest_mp = df_multiplans_statut[df_multiplans_statut['mois'] == latest_month]
            actif_mp = int(df_latest_mp.loc[df_latest_mp['statut'] == 'actif', 'nb_collectivites'].sum())
            st.metric(
                label="CT multiplans actives", 
                value=actif_mp,
                help="CT avec au moins 2 PAP actifs (5+ fiches modifiées sur les 3 derniers mois)"
            )
        else:
            st.metric(label="CT multiplans actives", value=0, help="CT avec au moins 2 PAP actifs (5+ fiches modifiées sur les 3 derniers mois)")
    
    with col4:
        if not df_multiplans_statut.empty:
            latest_month = df_multiplans_statut['mois'].max()
            df_latest_mp = df_multiplans_statut[df_multiplans_statut['mois'] == latest_month]
            inactif_mp = int(df_latest_mp.loc[df_latest_mp['statut'] == 'inactif', 'nb_collectivites'].sum())
            st.metric(
                label="CT multiplans inactives", 
                value=inactif_mp
            )
        else:
            st.metric(label="CT multiplans inactives", value=0, help="Collectivités avec 2+ plans mais moins de 2 plans actifs")
    
    with col5:
        if not df_plans_8plus.empty:
            latest_month = df_plans_8plus['mois'].max()
            df_latest_8plus = df_plans_8plus[df_plans_8plus['mois'] == latest_month]
            plans_8plus = int(df_latest_8plus['nb_plans'].sum())
            st.metric(
                label="Plans >= 8/10", 
                value=plans_8plus,
                help="Plans avec une note supérieure ou égale à 8/10"
            )
        else:
            st.metric(label="Plans >= 8/10", value=0, help="Plans avec une note supérieure ou égale à 8/10")
    
    # Graphiques All Time côte à côte avec 2 lignes chacun
    col_graph1, col_graph2 = st.columns(2)
    
    with col_graph1:
        st.markdown("#### CT PAP")
        if not df_pap_statut.empty:
            all_statuts = df_pap_statut['statut'].unique()
            first_month = df_pap_statut['mois'].min()
            all_months = pd.date_range(start=first_month, end=today, freq='MS')
            full_index = pd.MultiIndex.from_product([all_months, all_statuts], names=['mois', 'statut'])
            df_pap_chart = df_pap_statut.set_index(['mois', 'statut']).reindex(full_index, fill_value=0).reset_index()
            df_pap_chart = df_pap_chart.sort_values('mois')
            df_pap_chart['mois_label'] = df_pap_chart['mois'].dt.strftime('%Y-%m')

            fig_pap = px.line(
                df_pap_chart, 
                x='mois_label', 
                y='nb_collectivites', 
                color='statut', 
                markers=True, 
                height=400,
                color_discrete_map={'actif': '#22c55e', 'inactif': '#f97316'}
            )
            fig_pap.update_layout(
                xaxis_title="Mois",
                yaxis_title="Nombre de CT PAP",
                xaxis_tickangle=-45,
                legend_title="Statut"
            )
            st.plotly_chart(fig_pap, use_container_width=True)
        else:
            st.info("Aucune donnée disponible")
    
    with col_graph2:
        st.markdown("#### CT multiplans")
        if not df_multiplans_statut.empty:
            all_statuts = df_multiplans_statut['statut'].unique()
            first_month = df_multiplans_statut['mois'].min()
            all_months = pd.date_range(start=first_month, end=today, freq='MS')
            full_index = pd.MultiIndex.from_product([all_months, all_statuts], names=['mois', 'statut'])
            df_mp_chart = df_multiplans_statut.set_index(['mois', 'statut']).reindex(full_index, fill_value=0).reset_index()
            df_mp_chart = df_mp_chart.sort_values('mois')
            df_mp_chart['mois_label'] = df_mp_chart['mois'].dt.strftime('%Y-%m')

            fig_mp = px.line(
                df_mp_chart, 
                x='mois_label', 
                y='nb_collectivites', 
                color='statut', 
                markers=True, 
                height=400,
                color_discrete_map={'actif': '#22c55e', 'inactif': '#f97316'}
            )
            fig_mp.update_layout(
                xaxis_title="Mois",
                yaxis_title="Nombre de CT multiplans",
                xaxis_tickangle=-45,
                legend_title="Statut"
            )
            st.plotly_chart(fig_mp, use_container_width=True)
        else:
            st.info("Aucune donnée disponible")
    
    # Graphique Plans >= 8 (full width)
    st.markdown("#### Plans >= 8")
    if not df_plans_8plus.empty:
        first_month = df_plans_8plus['mois'].min()
        all_months = pd.date_range(start=first_month, end=today, freq='MS')
        df_8plus_chart = df_plans_8plus.set_index('mois').reindex(all_months, fill_value=0).reset_index().rename(columns={'index': 'mois'})
        df_8plus_chart['nb_plans'] = df_8plus_chart['nb_plans'].fillna(0).astype(int)
        df_8plus_chart = df_8plus_chart.sort_values('mois')
        df_8plus_chart['mois_label'] = df_8plus_chart['mois'].dt.strftime('%Y-%m')
        
        fig_8plus = px.line(
            df_8plus_chart, 
            x='mois_label', 
            y='nb_plans', 
            markers=True, 
            height=400
        )
        fig_8plus.update_traces(line_color='#22c55e')
        fig_8plus.update_layout(
            xaxis_title="Mois",
            yaxis_title="Nombre de plans >= 8",
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_8plus, use_container_width=True)
    else:
        st.info("Aucune donnée disponible")
else:
    # Mode période : afficher 3 métriques sur une ligne
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if not ct_first_pap.empty:
            new_pap_cur = len(ct_first_pap[(ct_first_pap['date_premier_pap'] >= cur_start) & (ct_first_pap['date_premier_pap'] <= cur_end)])
            new_pap_prev = len(ct_first_pap[(ct_first_pap['date_premier_pap'] >= prev_start) & (ct_first_pap['date_premier_pap'] <= prev_end)])
            delta_pap = new_pap_cur - new_pap_prev
            st.metric(
                label="Nouvelles CT PAP",
                value=new_pap_cur,
                delta=f"{delta_pap:+d}",
                delta_color="normal",
                help="5+ fiches avec titre, pilote et statut"
            )
        else:
            st.metric(
                label="Nouvelles CT PAP", 
                value=0,
                help="5+ fiches avec titre, pilote et statut"
            )
    
    with col2:
        if not ct_first_multiplan.empty:
            new_mp_cur = len(ct_first_multiplan[(ct_first_multiplan['date_premier_multiplan'] >= cur_start) & (ct_first_multiplan['date_premier_multiplan'] <= cur_end)])
            new_mp_prev = len(ct_first_multiplan[(ct_first_multiplan['date_premier_multiplan'] >= prev_start) & (ct_first_multiplan['date_premier_multiplan'] <= prev_end)])
            delta_mp = new_mp_cur - new_mp_prev
            st.metric(
                label="Nouvelles CT multiplans",
                value=new_mp_cur,
                delta=f"{delta_mp:+d}",
                delta_color="normal",
                help="CT avec au moins 2 PAP"
            )
        else:
            st.metric(
                label="Nouvelles CT multiplans", 
                value=0,
                help="CT avec au moins 2 PAP"
            )
    
    with col3:
        if not df_plans_8plus.empty:
            # Filtrer par mois sélectionné si vue Mois
            _df_8plus_filtered = df_plans_8plus[df_plans_8plus['mois'] <= cur_end] if view == "Mois" else df_plans_8plus
            # Trier par mois décroissant pour obtenir les derniers mois
            df_sorted = _df_8plus_filtered.sort_values('mois', ascending=False)
            
            if len(df_sorted) >= 2:
                # Dernier mois et mois précédent
                last_month = df_sorted.iloc[0]
                prev_month = df_sorted.iloc[1]
                
                # Nouveaux plans >= 8 ce mois = différence entre dernier mois et mois précédent
                new_8plus_cur = int(last_month['nb_plans'] - prev_month['nb_plans'])
                
                # Pour le delta, on calcule les nouveaux plans du mois précédent
                if len(df_sorted) >= 3:
                    prev_prev_month = df_sorted.iloc[2]
                    new_8plus_prev = int(prev_month['nb_plans'] - prev_prev_month['nb_plans'])
                    delta_8plus = new_8plus_cur - new_8plus_prev
                else:
                    delta_8plus = new_8plus_cur
                
                st.metric(
                    label="Nouveaux Plans >= 8/10",
                    value=new_8plus_cur,
                    delta=f"{delta_8plus:+d}",
                    delta_color="normal",
                    help="Nouveaux plans avec note >= 8/10"
                )
            else:
                st.metric(
                    label="Nouveaux Plans >= 8/10", 
                    value=0,
                    help="Nouveaux plans avec note >= 8/10"
                )
        else:
            st.metric(
                label="Nouveaux Plans >= 8/10", 
                value=0,
                help="Nouveaux plans avec note >= 8/10"
            )

st.markdown("---")


st.badge("Effort bizdevs", icon="💪", color="green")

# Segmented control pour la vue
vue_effort = st.segmented_control(
    "Vue",
    options=["Ensemble", "Par pipe"],
    default="Ensemble",
    key="vue_effort_tab1"
)

# Préparation des données — Actions globales (notes de suivi)
df_biz_global = df_bizdev_note_de_suivi.copy()
if not df_biz_global.empty:
    df_biz_global['date'] = pd.to_datetime(df_biz_global['date'], errors='coerce').dt.tz_localize(None)

# Préparation des données — Actions qualifiées (A/F)
df_biz_qualif = df_bizdev_af.copy()
if not df_biz_qualif.empty:
    df_biz_qualif['date'] = pd.to_datetime(df_biz_qualif['date'], errors='coerce').dt.tz_localize(None)

alltime_min = pd.Timestamp('2024-01-01')
alltime_min_ensemble = pd.Timestamp('2024-11-01')
alltime_min_pipe = pd.Timestamp('2025-08-01')

_card_style_qualif = "background: linear-gradient(90deg,#F0FFF4,#F8FFF8); border:1px solid #C6F6D5; border-radius: 12px; padding: 14px; margin-bottom: 4px; display: flex; align-items: left; justify-content: left;"
_card_style_global = "background: linear-gradient(90deg,#EEF6FF,#F8FAFF); border:1px solid #E5EAF2; border-radius: 12px; padding: 14px; margin-bottom: 4px; display: flex; align-items: center; justify-content: left;"

# Palette de couleurs harmonieuse pour Actions globales et qualifiées
colors_actions = {
    'Actions globales': '#2E5090',      # Bleu foncé
    'Actions qualifiées': '#6B9BD1'     # Bleu clair
}

if vue_effort == "Ensemble":
    # ─── VUE ENSEMBLE ───
    if is_all_time:
        # Totaux sur toute la période
        df_g_at = df_biz_global[(df_biz_global['date'] >= alltime_min) & (df_biz_global['date'] <= today)] if not df_biz_global.empty else df_biz_global
        df_q_at = df_biz_qualif[(df_biz_qualif['date'] >= alltime_min) & (df_biz_qualif['date'] <= today)] if not df_biz_qualif.empty else df_biz_qualif

        col_left, col_right = st.columns(2)
        with col_left:
            st.markdown(f'<div style="{_card_style_qualif}"><div style="font-weight:600; font-size:14px; color:#334155;">🎯 Actions qualifiées</div></div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.metric(label="Actions (total)", value=f"{len(df_q_at):,}".replace(",", " "))
            with c2:
                st.metric(label="CT uniques (total)", value=f"{df_q_at['collectivite_id'].nunique() if not df_q_at.empty else 0:,}".replace(",", " "))
        with col_right:
            st.markdown(f'<div style="{_card_style_global}"><div style="font-weight:600; font-size:14px; color:#334155;">📋 Actions globales</div></div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.metric(label="Actions (total)", value=f"{len(df_g_at):,}".replace(",", " "))
            with c2:
                st.metric(label="CT uniques (total)", value=f"{df_g_at['collectivite_id'].nunique() if not df_g_at.empty else 0:,}".replace(",", " "))

        # Line charts avec 2 lignes (global / qualifié)
        def _agg_monthly(df):
            if df.empty:
                return pd.DataFrame(columns=['mois', 'Actions', 'CT_uniques'])
            d = df.copy()
            d['mois'] = d['date'].dt.to_period('M').dt.to_timestamp()
            return d.groupby('mois').agg(Actions=('date', 'count'), CT_uniques=('collectivite_id', 'nunique')).reset_index()

        agg_g = _agg_monthly(df_g_at)
        agg_g['type'] = 'Actions globales'
        agg_q = _agg_monthly(df_q_at)
        agg_q['type'] = 'Actions qualifiées'

        all_months = pd.date_range(start=alltime_min_ensemble, end=today, freq='MS')
        frames = []
        for t, sub_df in [('Actions globales', agg_g), ('Actions qualifiées', agg_q)]:
            sub = sub_df.set_index('mois')[['Actions', 'CT_uniques']].reindex(all_months, fill_value=0).reset_index().rename(columns={'index': 'mois'})
            sub['type'] = t
            frames.append(sub)
        df_agg_combined = pd.concat(frames, ignore_index=True)
        df_agg_combined = df_agg_combined[df_agg_combined['mois'] >= alltime_min_ensemble]
        df_agg_combined['mois_label'] = df_agg_combined['mois'].dt.strftime('%Y-%m')

        col1, col2 = st.columns(2)
        with col1:
            fig = px.line(df_agg_combined, x='mois_label', y='Actions', color='type', height=400, markers=True, color_discrete_map=colors_actions)
            fig.update_layout(xaxis_title="Mois", yaxis_title="Actions de contact", xaxis_tickangle=-45, legend_title="")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.line(df_agg_combined, x='mois_label', y='CT_uniques', color='type', height=400, markers=True, color_discrete_map=colors_actions)
            fig.update_layout(xaxis_title="Mois", yaxis_title="Collectivités uniques", xaxis_tickangle=-45, legend_title="")
            st.plotly_chart(fig, use_container_width=True)

    else:
        # Période : 4 métriques en cards avec deltas
        def _period_metrics(df, start, end):
            if df.empty:
                return 0, 0
            sub = df[(df['date'] >= start) & (df['date'] <= end)]
            return int(len(sub)), int(sub['collectivite_id'].nunique()) if not sub.empty else 0

        g_cur_a, g_cur_ct = _period_metrics(df_biz_global, cur_start, cur_end)
        g_prev_a, g_prev_ct = _period_metrics(df_biz_global, prev_start, prev_end)
        q_cur_a, q_cur_ct = _period_metrics(df_biz_qualif, cur_start, cur_end)
        q_prev_a, q_prev_ct = _period_metrics(df_biz_qualif, prev_start, prev_end)

        col_left, col_right = st.columns(2)
        with col_left:
            st.markdown(f'<div style="{_card_style_qualif}"><div style="font-weight:600; font-size:14px; color:#334155;">💬 Actions qualifiées : Activités & Feedbacks</div></div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.metric(label="Actions", value=q_cur_a, delta=f"{q_cur_a - q_prev_a:+d}", delta_color="normal", help="Toutes les lignes de la table Activités et Feedbacks")
            with c2:
                st.metric(label="CT uniques", value=q_cur_ct, delta=f"{q_cur_ct - q_prev_ct:+d}", delta_color="normal")
        with col_right:
            st.markdown(f'<div style="{_card_style_global}"><div style="font-weight:600; font-size:14px; color:#334155;">✏️ Actions globales : Notes de suivi</div></div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.metric(label="Actions", value=g_cur_a, delta=f"{g_cur_a - g_prev_a:+d}", delta_color="normal", help="Toutes les dates renseignées dans les notes de suivis")
            with c2:
                st.metric(label="CT uniques", value=g_cur_ct, delta=f"{g_cur_ct - g_prev_ct:+d}", delta_color="normal")

else:
    # ─── VUE PAR PIPE : ventilation par pipeline ───
    metrique_pipe = st.segmented_control(
        "Métrique",
        options=["Total", "Collectivités uniques"],
        default="Total",
        key="metrique_pipe_tab1"
    )

    df_pipe = df_pipeline_semaine.copy()
    df_pipe['semaine'] = pd.to_datetime(df_pipe['semaine'])

    # Combiner global + qualifié en un seul df avec colonne source
    _dfs_combined = []
    if not df_biz_global.empty:
        _tmp = df_biz_global[['collectivite_id', 'date']].copy()
        _tmp['source'] = 'Actions globales'
        _dfs_combined.append(_tmp)
    if not df_biz_qualif.empty:
        _tmp = df_biz_qualif[['collectivite_id', 'date']].copy()
        _tmp['source'] = 'Actions qualifiées'
        _dfs_combined.append(_tmp)
    df_biz_combined = pd.concat(_dfs_combined, ignore_index=True) if _dfs_combined else pd.DataFrame(columns=['collectivite_id', 'date', 'source'])

    if is_all_time:
        # All Time par pipe : un seul graphe selon la métrique choisie
        st.warning("Pour cette vue, les actions globales et qualifiées ont été sommées.")
        if not df_biz_combined.empty:
            df_biz_at = df_biz_combined[(df_biz_combined['date'] >= alltime_min) & (df_biz_combined['date'] <= today)].copy()
            df_biz_at['mois'] = df_biz_at['date'].dt.to_period('M').dt.to_timestamp()

            df_pipe_monthly = df_pipe[df_pipe['semaine'] >= alltime_min].copy()
            df_pipe_monthly['mois'] = df_pipe_monthly['semaine'].dt.to_period('M').dt.to_timestamp()
            df_pipe_latest = df_pipe_monthly.sort_values('semaine').drop_duplicates(
                subset=['collectivite_id', 'mois'], keep='last'
            )[['collectivite_id', 'mois', 'pipeline']]

            df_biz_pipe = df_biz_at.merge(df_pipe_latest, on=['collectivite_id', 'mois'], how='left')
            df_biz_pipe['pipeline'] = df_biz_pipe['pipeline'].fillna('Non classé')

            df_agg_pipe = df_biz_pipe.groupby(['mois', 'pipeline']).agg(
                Actions=('date', 'count'),
                CT_uniques=('collectivite_id', 'nunique')
            ).reset_index().sort_values('mois')
            df_agg_pipe = df_agg_pipe[df_agg_pipe['mois'] >= alltime_min_pipe]
            df_agg_pipe['mois_label'] = df_agg_pipe['mois'].dt.strftime('%Y-%m')

            if metrique_pipe == "Total":
                fig = px.line(df_agg_pipe, x='mois_label', y='Actions', color='pipeline', height=500, markers=True)
                fig.update_layout(xaxis_title="Mois", yaxis_title="Actions (globales + qualifiées)", xaxis_tickangle=-45, legend_title="Pipeline")
            else:
                fig = px.line(df_agg_pipe, x='mois_label', y='CT_uniques', color='pipeline', height=500, markers=True)
                fig.update_layout(xaxis_title="Mois", yaxis_title="CT uniques contactées", xaxis_tickangle=-45, legend_title="Pipeline")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée de contacts disponible.")
    else:
        # Période par pipe : stacked bar (global + qualifié) par pipeline avec deltas
        if not df_biz_combined.empty:
            df_pipe_cur = df_pipe[df_pipe['semaine'] <= cur_end].sort_values('semaine').drop_duplicates(
                subset=['collectivite_id'], keep='last'
            )[['collectivite_id', 'pipeline']]

            reach_cur = df_biz_combined[(df_biz_combined['date'] >= cur_start) & (df_biz_combined['date'] <= cur_end)].copy()
            reach_prev = df_biz_combined[(df_biz_combined['date'] >= prev_start) & (df_biz_combined['date'] <= prev_end)].copy()

            reach_cur = reach_cur.merge(df_pipe_cur, on='collectivite_id', how='left')
            reach_cur['pipeline'] = reach_cur['pipeline'].fillna('Non classé')
            reach_prev = reach_prev.merge(df_pipe_cur, on='collectivite_id', how='left')
            reach_prev['pipeline'] = reach_prev['pipeline'].fillna('Non classé')

            if metrique_pipe == "Total":
                # Stacked bar : actions par source
                agg_cur_src = reach_cur.groupby(['pipeline', 'source']).size().reset_index(name='Valeur')
                agg_cur_total = reach_cur.groupby('pipeline').size().reset_index(name='Total_cur')
                agg_prev_total = reach_prev.groupby('pipeline').size().reset_index(name='Total_prev')
                
                agg_totals = agg_cur_total.merge(agg_prev_total, on='pipeline', how='outer').fillna(0)
                agg_totals['Total_cur'] = agg_totals['Total_cur'].astype(int)
                agg_totals['Total_prev'] = agg_totals['Total_prev'].astype(int)
                agg_totals['delta'] = agg_totals['Total_cur'] - agg_totals['Total_prev']
                agg_totals['label_total'] = agg_totals.apply(lambda r: f"{r['Total_cur']} ({r['delta']:+d})", axis=1)

                pipeline_order = agg_totals.sort_values('Total_cur', ascending=True)['pipeline'].tolist()

                fig = go.Figure()
                sources_ordered = ['Actions globales', 'Actions qualifiées']
                colors_src = colors_actions

                for i, source in enumerate(sources_ordered):
                    sub = agg_cur_src[agg_cur_src['source'] == source].copy()
                    sub = sub.set_index('pipeline').reindex(pipeline_order, fill_value=0).reset_index()

                    is_last = (i == len(sources_ordered) - 1)
                    if is_last:
                        totals_map = agg_totals.set_index('pipeline')['label_total']
                        text_vals = sub['pipeline'].map(totals_map).fillna('')
                        textposition = 'outside'
                    else:
                        text_vals = sub['Valeur'].apply(lambda v: str(int(v)) if v > 0 else '')
                        textposition = 'inside'

                    fig.add_trace(go.Bar(
                        y=sub['pipeline'], x=sub['Valeur'],
                        name=source, orientation='h',
                        text=text_vals, textposition=textposition,
                        marker_color=colors_src.get(source)
                    ))

                fig.update_layout(
                    barmode='stack',
                    height=max(450, len(pipeline_order) * 70),
                    yaxis_title="Pipeline",
                    xaxis_title="Nombre d'actions",
                    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
                    margin=dict(r=120)
                )
            else:
                # Stacked bar : CT uniques par source
                agg_cur_src = reach_cur.groupby(['pipeline', 'source'])['collectivite_id'].nunique().reset_index(name='Valeur')
                agg_cur_total = reach_cur.groupby('pipeline')['collectivite_id'].nunique().reset_index(name='Total_cur')
                agg_prev_total = reach_prev.groupby('pipeline')['collectivite_id'].nunique().reset_index(name='Total_prev')
                
                agg_totals = agg_cur_total.merge(agg_prev_total, on='pipeline', how='outer').fillna(0)
                agg_totals['Total_cur'] = agg_totals['Total_cur'].astype(int)
                agg_totals['Total_prev'] = agg_totals['Total_prev'].astype(int)
                agg_totals['delta'] = agg_totals['Total_cur'] - agg_totals['Total_prev']
                agg_totals['label_total'] = agg_totals.apply(lambda r: f"{r['Total_cur']} ({r['delta']:+d})", axis=1)

                pipeline_order = agg_totals.sort_values('Total_cur', ascending=True)['pipeline'].tolist()

                fig = go.Figure()
                sources_ordered = ['Actions globales', 'Actions qualifiées']
                colors_src = colors_actions

                for i, source in enumerate(sources_ordered):
                    sub = agg_cur_src[agg_cur_src['source'] == source].copy()
                    sub = sub.set_index('pipeline').reindex(pipeline_order, fill_value=0).reset_index()

                    is_last = (i == len(sources_ordered) - 1)
                    if is_last:
                        totals_map = agg_totals.set_index('pipeline')['label_total']
                        text_vals = sub['pipeline'].map(totals_map).fillna('')
                        textposition = 'outside'
                    else:
                        text_vals = sub['Valeur'].apply(lambda v: str(int(v)) if v > 0 else '')
                        textposition = 'inside'

                    fig.add_trace(go.Bar(
                        y=sub['pipeline'], x=sub['Valeur'],
                        name=source, orientation='h',
                        text=text_vals, textposition=textposition,
                        marker_color=colors_src.get(source)
                    ))

                fig.update_layout(
                    barmode='stack',
                    height=max(450, len(pipeline_order) * 70),
                    yaxis_title="Pipeline",
                    xaxis_title="Collectivités uniques",
                    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
                    margin=dict(r=120)
                )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée de contacts disponible.")

st.markdown("---")

st.badge("Activation", icon="🐣", color="blue")

if is_all_time:
    # All Time : métriques totales + graphique mensuel d'évolution des participants par type de démo (depuis le 01/01/2024)

    time_min_activation = pd.Timestamp('2025-05-01')

    df_events_alltime = df_calendly_events[(df_calendly_events['start_time'] >= time_min_activation) & (df_calendly_events['start_time'] <= today)].copy()
    df_inv_alltime = df_invitees_active[(df_invitees_active['start_time'] >= time_min_activation) & (df_invitees_active['start_time'] <= today)].copy()

    # Métriques totales (sans delta)
    total_events_alltime = len(df_events_alltime)
    total_inscrits_alltime = len(df_inv_alltime)
    total_participants_alltime = int(df_events_alltime['nb_participants_reel'].sum()) if 'nb_participants_reel' in df_events_alltime.columns else 0
    taux_alltime = (total_participants_alltime / total_inscrits_alltime * 100) if total_inscrits_alltime > 0 else 0

    col_d1, col_d2, col_d3, col_d4 = st.columns(4)
    with col_d1:
        st.metric(label="Événements (total)", value=total_events_alltime)
    with col_d2:
        st.metric(label="Inscrits (total)", value=total_inscrits_alltime)
    with col_d3:
        st.metric(label="Participants (total)", value=total_participants_alltime)
    with col_d4:
        st.metric(label="Taux de participation", value=f"{taux_alltime:.0f}%")

    # Graphique
    df_events_alltime['mois'] = df_events_alltime['start_time'].dt.to_period('M').dt.to_timestamp()

    df_monthly = df_events_alltime.groupby(['mois', 'type']).agg(
        events=('uri', 'count'),
        participants=('nb_participants_reel', 'sum')
    ).reset_index()
    df_monthly = df_monthly.sort_values('mois')

    # Compléter avec les mois manquants pour chaque type (réindexation)
    if not df_monthly.empty:
        all_types = df_monthly['type'].unique()
        first_month = df_monthly['mois'].min()
        all_months = pd.date_range(start=first_month, end=today, freq='MS')
        full_index = pd.MultiIndex.from_product([all_months, all_types], names=['mois', 'type'])
        df_monthly = df_monthly.set_index(['mois', 'type']).reindex(full_index, fill_value=0).reset_index()
        df_monthly = df_monthly.sort_values('mois')

    df_monthly['mois_label'] = df_monthly['mois'].dt.strftime('%Y-%m')

    fig = px.bar(df_monthly, x='mois_label', y='participants', color='type', height=500, barmode='stack')
    fig.update_layout(xaxis_title="Mois", yaxis_title="Nombre de participants", xaxis_tickangle=-45, legend_title="Type")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Focus événements")

    # Sélection du type d'événement
    types_disponibles = df_calendly_events['type'].dropna().sort_values().unique().tolist()
    type_defaut = '▶️ Démo Pilotage - Découverte & prise en main (1/2)'
    type_selection = st.selectbox(
        "Type d'événement",
        options=types_disponibles,
        index=types_disponibles.index(type_defaut) if type_defaut in types_disponibles else 0,
        key="type_focus",
    )


    events_filtres = df_calendly_events[(df_calendly_events['type'] == type_selection) & (df_calendly_events['start_time'] >= time_min_activation) & (df_calendly_events['start_time'] <= today)].copy()
    invitees_filtres = df_invitees_active[(df_invitees_active['type'] == type_selection) & (df_invitees_active['start_time'] >= time_min_activation) & (df_invitees_active['start_time'] <= today)].copy()
    # Préparation des données pour les participants réels
    if 'nb_participants_reel' in events_filtres.columns:
        # Créer un dataframe avec les participants réels par événement
        participants_reel_filtres = events_filtres[['start_time', 'type', 'nb_participants_reel']].copy()
        participants_reel_filtres = participants_reel_filtres[participants_reel_filtres['nb_participants_reel'] > 0]
    else:
        # Fallback sur les inscrits actifs si la colonne n'existe pas
        participants_reel_filtres = invitees_filtres.copy()

    # Rendu du tableau
    table_single = monthly_single_table(events_filtres, invitees_filtres, participants_reel_filtres, 'start_time')
    if not table_single.empty:
        st.dataframe(table_single, use_container_width=True)
    else:
        st.info("Aucune donnée disponible pour la période et l'événement sélectionnés.")


else:
    # Vue période : métriques avec deltas
    events_cur = df_calendly_events[(df_calendly_events['start_time'] >= cur_start) & (df_calendly_events['start_time'] <= cur_end)]
    events_prev = df_calendly_events[(df_calendly_events['start_time'] >= prev_start) & (df_calendly_events['start_time'] <= prev_end)]
    inv_cur = df_invitees_active[(df_invitees_active['start_time'] >= cur_start) & (df_invitees_active['start_time'] <= cur_end)]
    inv_prev = df_invitees_active[(df_invitees_active['start_time'] >= prev_start) & (df_invitees_active['start_time'] <= prev_end)]

    events_cur_g = events_cur.groupby('type').size().rename('events_cur')
    inv_cur_g = inv_cur.groupby('type').size().rename('inscrits_cur')
    events_prev_g = events_prev.groupby('type').size().rename('events_prev')
    inv_prev_g = inv_prev.groupby('type').size().rename('inscrits_prev')

    if 'nb_participants_reel' in events_cur.columns:
        part_cur_g = events_cur.groupby('type')['nb_participants_reel'].sum().rename('participants_cur')
    else:
        part_cur_g = pd.Series(dtype=int, name='participants_cur')
    
    if 'nb_participants_reel' in events_prev.columns:
        part_prev_g = events_prev.groupby('type')['nb_participants_reel'].sum().rename('participants_prev')
    else:
        part_prev_g = pd.Series(dtype=int, name='participants_prev')

    kpis = pd.concat([events_cur_g, inv_cur_g, part_cur_g, events_prev_g, inv_prev_g, part_prev_g], axis=1).fillna(0).astype(int).reset_index().rename(columns={'index': 'type'})
    kpis['delta_events'] = kpis['events_cur'] - kpis['events_prev']
    kpis['delta_inscrits'] = kpis['inscrits_cur'] - kpis['inscrits_prev']
    
    # Calcul du taux de participation (en %)
    kpis['taux_participation_cur'] = (kpis['participants_cur'] / kpis['inscrits_cur'] * 100).where(kpis['inscrits_cur'] > 0, 0)
    kpis['taux_participation_prev'] = (kpis['participants_prev'] / kpis['inscrits_prev'] * 100).where(kpis['inscrits_prev'] > 0, 0)
    kpis['delta_taux'] = kpis['taux_participation_cur'] - kpis['taux_participation_prev']
    
    kpis = kpis[['type', 'events_cur', 'inscrits_cur', 'taux_participation_cur', 'delta_events', 'delta_inscrits', 'delta_taux']]
    
    # Filtrer et ordonner par type spécifique
    types_ordre = [
        '▶️ Démo Pilotage - Découverte & prise en main (1/2)',
        '⏩ Démo Pilotage - Fonctionnalités expertes (2/2)',
        '⏏️ Démo - Commencez votre état des lieux (T.E.T.E)'
    ]
    kpis = kpis[kpis['type'].isin(types_ordre)].copy()
    kpis['ordre'] = kpis['type'].map({t: i for i, t in enumerate(types_ordre)})
    kpis = kpis.sort_values('ordre').drop(columns=['ordre'])

    nb_types = len(kpis)
    if nb_types == 0:
        st.info("Pas de données sur la période sélectionnée.")
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
                    st.metric(label="Événements", value=int(row['events_cur']), delta=f"{int(row['delta_events']):+d}", delta_color="normal")
                with c_in:
                    st.metric(label="Inscrits", value=int(row['inscrits_cur']), delta=f"{int(row['delta_inscrits']):+d}", delta_color="normal")
                with c_pa:
                    st.metric(label="Participation", value=f"{row['taux_participation_cur']:.0f}%", delta=f"{row['delta_taux']:+.0f}%", delta_color="normal")


st.markdown("---")

st.badge("Conversion et progression", icon="🐤", color="violet")

# Fonction pour détecter les transitions entre états
def detect_transitions(df_pipe, state_from, state_to, start_date, end_date):
    """
    Détecte les CT qui sont passées de state_from à state_to pendant la période donnée.
    Retourne le nombre de CT ayant effectué cette transition.
    """
    if df_pipe.empty:
        return 0
    
    # Convertir la colonne semaine en datetime si nécessaire
    df_pipe_copy = df_pipe.copy()
    df_pipe_copy['semaine'] = pd.to_datetime(df_pipe_copy['semaine'])
    
    # Filtrer les données dans la plage de dates
    df_period = df_pipe_copy[(df_pipe_copy['semaine'] >= start_date) & (df_pipe_copy['semaine'] <= end_date)].copy()
    if df_period.empty:
        return 0
    
    # Trier par collectivite_id et semaine
    df_period = df_period.sort_values(['collectivite_id', 'semaine'])
    
    # Pour chaque CT, regarder les transitions
    transitions = []
    for ct_id, group in df_period.groupby('collectivite_id'):
        group = group.sort_values('semaine')
        pipelines = group['pipeline'].tolist()
        
        # Vérifier si la transition state_from -> state_to apparaît
        for i in range(len(pipelines) - 1):
            if pipelines[i] == state_from and pipelines[i + 1] == state_to:
                transitions.append(ct_id)
                break  # Compter une seule fois par CT
    
    return len(set(transitions))

def detect_all_transitions(df_pipe, end_date):
    """
    Détecte toutes les CT qui ont fait les transitions depuis le début jusqu'à end_date.
    """
    if df_pipe.empty:
        return 0, 0
    
    # Convertir la colonne semaine en datetime si nécessaire
    df_pipe_copy = df_pipe.copy()
    df_pipe_copy['semaine'] = pd.to_datetime(df_pipe_copy['semaine'])
    
    # Filtrer toutes les données jusqu'à end_date
    df_all = df_pipe_copy[df_pipe_copy['semaine'] <= end_date].copy()
    if df_all.empty:
        return 0, 0
    
    # Trier par collectivite_id et semaine
    df_all = df_all.sort_values(['collectivite_id', 'semaine'])
    
    # Pour chaque CT, regarder les transitions
    transition_activation_conversion = []
    transition_conversion_retention = []
    
    for ct_id, group in df_all.groupby('collectivite_id'):
        group = group.sort_values('semaine')
        pipelines = group['pipeline'].tolist()
        
        # Vérifier transition activation -> conversion
        for i in range(len(pipelines) - 1):
            if pipelines[i] == "En activation" and pipelines[i + 1] == "En conversion":
                transition_activation_conversion.append(ct_id)
                break
        
        # Vérifier transition conversion -> rétention
        for i in range(len(pipelines) - 1):
            if pipelines[i] == "En conversion" and pipelines[i + 1] == "En rétention":
                transition_conversion_retention.append(ct_id)
                break
    
    return len(set(transition_activation_conversion)), len(set(transition_conversion_retention))

# Calcul des transitions
if is_all_time:
    # Mode All Time : afficher les totaux depuis le début
    total_activ_to_conv, total_conv_to_ret = detect_all_transitions(df_pipeline_semaine, today)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label="En activation → En conversion",
            value=total_activ_to_conv,
            help="Nombre total de CT ayant effectué cette transition"
        )
    with col2:
        st.metric(
            label="En conversion → En rétention",
            value=total_conv_to_ret,
            help="Nombre total de CT ayant effectué cette transition"
        )
else:
    # Mode période : afficher avec deltas
    trans_activ_conv_cur = detect_transitions(df_pipeline_semaine, "En activation", "En conversion", cur_start, cur_end)
    trans_activ_conv_prev = detect_transitions(df_pipeline_semaine, "En activation", "En conversion", prev_start, prev_end)
    
    trans_conv_ret_cur = detect_transitions(df_pipeline_semaine, "En conversion", "En rétention", cur_start, cur_end)
    trans_conv_ret_prev = detect_transitions(df_pipeline_semaine, "En conversion", "En rétention", prev_start, prev_end)
    
    delta_activ_conv = trans_activ_conv_cur - trans_activ_conv_prev
    delta_conv_ret = trans_conv_ret_cur - trans_conv_ret_prev
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label="En activation → En conversion",
            value=trans_activ_conv_cur,
            delta=f"{delta_activ_conv:+d}",
            delta_color="normal",
            help="Nombre de CT ayant effectué cette transition pendant la période"
        )
    with col2:
        st.metric(
            label="En conversion → En rétention",
            value=trans_conv_ret_cur,
            delta=f"{delta_conv_ret:+d}",
            delta_color="normal",
            help="Nombre de CT ayant effectué cette transition pendant la période"
        )

st.markdown("---")

st.badge('Rétention', icon="🕊️", color="green")

# Fonction pour détecter les transitions vers "En pilotage multiplans"
def detect_transitions_to_multiplans(df_pipe, start_date, end_date):
    """
    Détecte les CT qui sont passées de "En rétention" vers "En pilotage" ou "En pilotage multiplans" pendant la période donnée.
    Retourne le nombre de CT ayant effectué cette transition.
    """
    if df_pipe.empty:
        return 0
    
    # Convertir la colonne semaine en datetime si nécessaire
    df_pipe_copy = df_pipe.copy()
    df_pipe_copy['semaine'] = pd.to_datetime(df_pipe_copy['semaine'])
    
    # Filtrer les données dans la plage de dates
    df_period = df_pipe_copy[(df_pipe_copy['semaine'] >= start_date) & (df_pipe_copy['semaine'] <= end_date)].copy()
    if df_period.empty:
        return 0
    
    # Trier par collectivite_id et semaine
    df_period = df_period.sort_values(['collectivite_id', 'semaine'])
    
    # Pour chaque CT, regarder les transitions
    transitions = []
    for ct_id, group in df_period.groupby('collectivite_id'):
        group = group.sort_values('semaine')
        pipelines = group['pipeline'].tolist()
        
        # Vérifier si la transition "En rétention" -> "En pilotage" OU "En pilotage multiplans" apparaît
        for i in range(len(pipelines) - 1):
            if pipelines[i] == "En rétention" and pipelines[i + 1] in ["En pilotage", "En pilotage multiplans"]:
                transitions.append(ct_id)
                break  # Compter une seule fois par CT
    
    return len(set(transitions))

def detect_all_transitions_to_multiplans(df_pipe, end_date):
    """
    Détecte toutes les CT qui ont fait la transition de "En rétention" vers "En pilotage" ou "En pilotage multiplans" depuis le début jusqu'à end_date.
    """
    if df_pipe.empty:
        return 0
    
    # Convertir la colonne semaine en datetime si nécessaire
    df_pipe_copy = df_pipe.copy()
    df_pipe_copy['semaine'] = pd.to_datetime(df_pipe_copy['semaine'])
    
    # Filtrer toutes les données jusqu'à end_date
    df_all = df_pipe_copy[df_pipe_copy['semaine'] <= end_date].copy()
    if df_all.empty:
        return 0
    
    # Trier par collectivite_id et semaine
    df_all = df_all.sort_values(['collectivite_id', 'semaine'])
    
    # Pour chaque CT, regarder les transitions
    transitions = []
    
    for ct_id, group in df_all.groupby('collectivite_id'):
        group = group.sort_values('semaine')
        pipelines = group['pipeline'].tolist()
        
        # Vérifier transition "En rétention" -> "En pilotage" OU "En pilotage multiplans"
        for i in range(len(pipelines) - 1):
            if pipelines[i] == "En rétention" and pipelines[i + 1] in ["En pilotage", "En pilotage multiplans"]:
                transitions.append(ct_id)
                break
    
    return len(set(transitions))

# === Progression des notes ===
def calculate_note_progression_period(df_note, df_passage_pap, start_prev, end_prev, start_cur, end_cur):
    """
    Calcule le nombre de CT dont la note a progressé entre deux périodes et la progression moyenne.
    Compare la dernière note de la période précédente avec la dernière note de la période actuelle.
    La note d'une collectivité est définie comme la meilleure note parmi tous ses plans.
    """
    if df_note.empty or df_passage_pap.empty:
        return 0, 0.0
    
    df = df_note.copy()
    df['mois'] = pd.to_datetime(df['mois'])
    
    # Jointure avec df_passage_pap pour obtenir collectivite_id
    df = df.merge(df_passage_pap[['collectivite_id', 'plan']], on='plan', how='inner')
    
    if df.empty:
        return 0, 0.0
    
    # Pour chaque période, obtenir la meilleure note par collectivité
    df_prev = df[(df['mois'] >= start_prev) & (df['mois'] <= end_prev)].copy()
    df_cur = df[(df['mois'] >= start_cur) & (df['mois'] <= end_cur)].copy()
    
    if df_prev.empty or df_cur.empty:
        return 0, 0.0
    
    # Pour chaque collectivité, obtenir la meilleure note (max) de la dernière date de chaque période
    # D'abord, obtenir la dernière date par collectivité pour chaque période
    df_prev_last_date = df_prev.groupby('collectivite_id')['mois'].max().reset_index()
    df_cur_last_date = df_cur.groupby('collectivite_id')['mois'].max().reset_index()
    
    # Merger avec les notes pour obtenir toutes les notes de cette dernière date
    df_prev_last = df_prev.merge(df_prev_last_date, on=['collectivite_id', 'mois'])
    df_cur_last = df_cur.merge(df_cur_last_date, on=['collectivite_id', 'mois'])
    
    # Prendre la meilleure note par collectivité
    df_prev_best = df_prev_last.groupby('collectivite_id')['note_plan'].max().reset_index()
    df_cur_best = df_cur_last.groupby('collectivite_id')['note_plan'].max().reset_index()
    
    # Merge pour comparer
    df_compare = df_prev_best.merge(df_cur_best, on='collectivite_id', suffixes=('_prev', '_cur'))
    
    # Calculer la progression
    df_compare['progression'] = df_compare['note_plan_cur'] - df_compare['note_plan_prev']
    
    # Compter les CT avec progression positive
    nb_progression = len(df_compare[df_compare['progression'] > 0])
    
    # Progression moyenne (uniquement pour celles qui ont progressé)
    if nb_progression > 0:
        prog_moyenne = df_compare[df_compare['progression'] > 0]['progression'].mean()
    else:
        prog_moyenne = 0.0
    
    return nb_progression, prog_moyenne

def calculate_note_progression_alltime(df_note, df_passage_pap, end_date):
    """
    Calcule le nombre de CT dont la note a progressé entre la valeur la plus ancienne et la plus récente.
    La note d'une collectivité est définie comme la meilleure note parmi tous ses plans.
    """
    if df_note.empty or df_passage_pap.empty:
        return 0, 0.0
    
    df = df_note.copy()
    df['mois'] = pd.to_datetime(df['mois'])
    df = df[df['mois'] <= end_date]
    
    # Jointure avec df_passage_pap pour obtenir collectivite_id
    df = df.merge(df_passage_pap[['collectivite_id', 'plan']], on='plan', how='inner')
    
    if df.empty:
        return 0, 0.0
    
    # Pour chaque collectivité, obtenir la première et dernière date
    df_sorted = df.sort_values('mois')
    df_first_date = df_sorted.groupby('collectivite_id')['mois'].min().reset_index()
    df_last_date = df_sorted.groupby('collectivite_id')['mois'].max().reset_index()
    
    # Merger avec les notes pour obtenir toutes les notes de ces dates
    df_first = df_sorted.merge(df_first_date, on=['collectivite_id', 'mois'])
    df_last = df_sorted.merge(df_last_date, on=['collectivite_id', 'mois'])
    
    # Prendre la meilleure note par collectivité pour chaque période
    df_first_best = df_first.groupby('collectivite_id')['note_plan'].max().reset_index()
    df_last_best = df_last.groupby('collectivite_id')['note_plan'].max().reset_index()
    
    # Merge pour comparer
    df_compare = df_first_best.merge(df_last_best, on='collectivite_id', suffixes=('_first', '_last'))
    
    # Calculer la progression
    df_compare['progression'] = df_compare['note_plan_last'] - df_compare['note_plan_first']
    
    # Compter les CT avec progression positive
    nb_progression = len(df_compare[df_compare['progression'] > 0])
    
    # Progression moyenne (uniquement pour celles qui ont progressé)
    if nb_progression > 0:
        prog_moyenne = df_compare[df_compare['progression'] > 0]['progression'].mean()
    else:
        prog_moyenne = 0.0
    
    return nb_progression, prog_moyenne

# Calcul des transitions vers multiplans et progression des notes
if is_all_time:
    # Mode All Time : afficher les totaux depuis le début
    total_to_multiplans = detect_all_transitions_to_multiplans(df_pipeline_semaine, today)
    nb_ct_prog, prog_moyenne = calculate_note_progression_alltime(df_note_plan, df_passage_pap, today)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            label="En rétention → En pilotage / En pilotage multiplans",
            value=total_to_multiplans,
            help="Nombre total de CT ayant effectué cette transition"
        )
    with col2:
        st.metric(
            label="CT dont la note a progressé",
            value=nb_ct_prog,
            help="Nombre de CT dont la note du plan a progressé depuis la première mesure"
        )
    with col3:
        st.metric(
            label="Progression moyenne",
            value=f"{prog_moyenne:.2f}",
            help="Progression moyenne de la note pour les CT ayant progressé"
        )
else:
    # Mode période : afficher avec deltas
    trans_to_multiplans_cur = detect_transitions_to_multiplans(df_pipeline_semaine, cur_start, cur_end)
    trans_to_multiplans_prev = detect_transitions_to_multiplans(df_pipeline_semaine, prev_start, prev_end)
    delta_to_multiplans = trans_to_multiplans_cur - trans_to_multiplans_prev
    
    nb_ct_prog, prog_moyenne = calculate_note_progression_period(df_note_plan, df_passage_pap, prev_start, prev_end, cur_start, cur_end)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            label="En rétention → En pilotage / En pilotage multiplans",
            value=trans_to_multiplans_cur,
            delta=f"{delta_to_multiplans:+d}",
            delta_color="normal",
            help="Nombre de CT ayant effectué cette transition pendant la période"
        )
    with col2:
        st.metric(
            label="CT dont la note a progressé",
            value=nb_ct_prog,
            help="Nombre de CT dont la note du plan a progressé entre la période précédente et la période actuelle"
        )
    with col3:
        st.metric(
            label="Progression moyenne",
            value=f"{prog_moyenne:.2f}",
            help="Progression moyenne de la note pour les CT ayant progressé"
        )

st.markdown("---")
st.badge("Support", icon="💬", color="gray")

# Préparation des données de passage PAP
df_pap = df_passage_pap.copy()
if not df_pap.empty and 'passage_pap' in df_pap.columns:
    df_pap['passage_pap'] = pd.to_datetime(df_pap['passage_pap'], errors='coerce')
    # Supprimer la timezone si présente pour permettre les comparaisons avec today
    if df_pap['passage_pap'].dt.tz is not None:
        df_pap['passage_pap'] = df_pap['passage_pap'].dt.tz_localize(None)

# Calcul des plans autonomes vs importés
if is_all_time:
    # Mode All Time : graphique avec évolution mensuelle
    if not df_pap.empty and 'import' in df_pap.columns:
        df_pap_at = df_pap[df_pap['passage_pap'] <= today].copy()
        df_pap_at['mois'] = df_pap_at['passage_pap'].dt.to_period('M').dt.to_timestamp()
        
        # Grouper par mois et type d'import
        df_pap_monthly = df_pap_at.groupby(['mois', 'import']).size().reset_index(name='nb_plans')
        df_pap_monthly = df_pap_monthly.sort_values('mois')
        
        if not df_pap_monthly.empty:
            # Compléter les mois manquants
            all_imports = df_pap_monthly['import'].unique()
            first_month = df_pap_monthly['mois'].min()
            all_months = pd.date_range(start=first_month, end=today, freq='MS')
            full_index = pd.MultiIndex.from_product([all_months, all_imports], names=['mois', 'import'])
            df_pap_chart = df_pap_monthly.set_index(['mois', 'import']).reindex(full_index, fill_value=0).reset_index()
            df_pap_chart = df_pap_chart.sort_values('mois')
            df_pap_chart['mois_label'] = df_pap_chart['mois'].dt.strftime('%Y-%m')
            
            # Créer le graphique avec les couleurs appropriées
            colors_import = {
                'Importé': '#f97316',    # orange
                'Autonome': '#22c55e'     # vert
            }
            
            fig = px.line(
                df_pap_chart, 
                x='mois_label', 
                y='nb_plans', 
                color='import', 
                markers=True, 
                height=400,
                color_discrete_map=colors_import
            )
            fig.update_layout(
                xaxis_title="Mois",
                yaxis_title="Nombre de plans",
                xaxis_tickangle=-45,
                legend_title="Type"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée disponible")
    else:
        st.info("Aucune donnée disponible")
else:
    # Mode période : métriques avec deltas
    if not df_pap.empty and 'import' in df_pap.columns:
        # Filtrer par période
        df_pap_cur = df_pap[(df_pap['passage_pap'] >= cur_start) & (df_pap['passage_pap'] <= cur_end)]
        df_pap_prev = df_pap[(df_pap['passage_pap'] >= prev_start) & (df_pap['passage_pap'] <= prev_end)]
        
        # Compter par type
        nb_autonome_cur = len(df_pap_cur[df_pap_cur['import'] == 'Autonome'])
        nb_autonome_prev = len(df_pap_prev[df_pap_prev['import'] == 'Autonome'])
        nb_importe_cur = len(df_pap_cur[df_pap_cur['import'] == 'Importé'])
        nb_importe_prev = len(df_pap_prev[df_pap_prev['import'] == 'Importé'])
        
        delta_autonome = nb_autonome_cur - nb_autonome_prev
        delta_importe = nb_importe_cur - nb_importe_prev
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                label="Plans autonomes",
                value=nb_autonome_cur,
                delta=f"{delta_autonome:+d}",
                delta_color="normal",
                help="Plans créés de manière autonome"
            )
        with col2:
            st.metric(
                label="Plans importés",
                value=nb_importe_cur,
                delta=f"{delta_importe:+d}",
                delta_color="normal",
                help="Plans importés"
            )
    else:
        st.info("Aucune donnée disponible")



############################################
# === COMMENT ONT-ILS TROUVÉ LA DÉMO 1/2 ?
############################################
st.markdown("---")
st.badge("Démo 1/2", icon="🎥", color="violet")

if is_all_time:
    demo12 = df_invitees_active[
        (df_invitees_active['type'] == '▶️ Démo Pilotage - Découverte & prise en main (1/2)') &
        (df_invitees_active['start_time'] >= alltime_min) &
        (df_invitees_active['start_time'] <= today)
    ][['reponse']].copy()
else:
    demo12 = df_invitees_active[
        (df_invitees_active['type'] == '▶️ Démo Pilotage - Découverte & prise en main (1/2)') &
        (df_invitees_active['start_time'] >= cur_start) &
        (df_invitees_active['start_time'] <= cur_end)
    ][['reponse']].copy()

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
    # En mode All Time, filtrer les réponses avec une seule occurrence
    if is_all_time:
        total_counts_filtre = total_counts[total_counts['nb'] > 1]
    else:
        total_counts_filtre = total_counts[total_counts['nb'] > 0]
    
    if total_counts_filtre.empty:
        st.info("Aucun retour avec plusieurs occurrences disponible.")
    else:
        fig_pie = px.pie(
            total_counts_filtre, 
            values='nb', 
            names='items', 
            title="Comment avez vous trouvé la démo 1/2 ?",
            height=600
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Export CSV des comptes agrégés affichés
    csv_pie = total_counts.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Exporter CSV retours démo 1/2",
        data=csv_pie,
        file_name="retours_demo12_agg.csv",
        mime="text/csv"
    )


st.markdown("---")
st.badge("Pipelines", icon="🚧", color="orange")
st.warning("Cette section est la seule section indépendante de la période sélectionnée plus haut. Les deltas sont calculés par rapport à l'état des pipes 4 semaines plus tôt.")

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
    
    # Filtre par semaine uniquement
    semaine_selection = st.selectbox(
        "Sélectionner une semaine",
        options=df_pipe['semaine'].sort_values(ascending=False).unique().tolist(),
        key="semaine_selection"
    )
    
    # Appliquer le filtre
    df_pipe = df_pipe[df_pipe['pipeline'] != 'A acquérir'].copy()
    df_pipe_filtre = df_pipe[df_pipe['semaine'] == semaine_selection].copy()
    
    if not df_pipe_filtre.empty:
        # Calcul des comptes par pipeline
        pipeline_counts = df_pipe_filtre['pipeline'].value_counts().reset_index()
        pipeline_counts.columns = ['Pipeline', 'Nombre de collectivités']
        
        # Trouver la semaine S-4
        semaines_triees = sorted(df_pipe['semaine'].unique())
        idx_semaine_actuelle = semaines_triees.index(semaine_selection) if semaine_selection in semaines_triees else -1
        
        if idx_semaine_actuelle >= 4:
            semaine_s4 = semaines_triees[idx_semaine_actuelle - 4]
            
            # Calculer les counts pour S-4
            df_pipe_s4 = df_pipe[df_pipe['semaine'] == semaine_s4].copy()
            
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

    else:
        st.info("Aucune donnée disponible pour la semaine sélectionnée.")
else:
    st.info("Aucune donnée de pipeline disponible.")