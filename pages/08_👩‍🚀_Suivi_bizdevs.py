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

_MOIS_FR = ["", "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
            "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
_today_for_picker = pd.Timestamp.today().normalize()
_col_seg, _col_sel, _ = st.columns(3)
with _col_seg:
    st.segmented_control(
        "Période",
        options=["Semaine", "Mois", "Trimestre", "Année", "All Time", "Custom"],
        default="Mois",
        key="view_bizdevs",
    )
_view_picker = st.session_state.get("view_bizdevs", "Mois")

with _col_sel:
    if _view_picker == "Semaine":
        _week_cursor = pd.Timestamp("2025-01-01") - pd.Timedelta(days=pd.Timestamp("2025-01-01").weekday())
        _week_options = []
        while _week_cursor <= _today_for_picker:
            _week_options.append(_week_cursor.strftime("%Y-%m-%d"))
            _week_cursor += pd.Timedelta(days=7)
        st.selectbox(
            "Semaine",
            options=_week_options,
            index=len(_week_options) - 1,
            format_func=lambda x: f"Semaine du {pd.Timestamp(x).strftime('%d/%m/%Y')}",
            key="selected_week_bizdevs",
        )
    elif _view_picker == "Mois":
        _month_options = []
        _y, _m = 2025, 1
        while (_y, _m) <= (_today_for_picker.year, _today_for_picker.month):
            _month_options.append(f"{_y}-{_m:02d}")
            _m += 1
            if _m > 12:
                _m = 1
                _y += 1
        st.selectbox(
            "Mois",
            options=_month_options,
            index=len(_month_options) - 1,
            format_func=lambda x: f"{_MOIS_FR[int(x.split('-')[1])]} {x.split('-')[0]}",
            key="selected_month_bizdevs",
        )
    elif _view_picker == "Trimestre":
        _quarter_options = []
        _y, _q = 2025, 1
        _cur_q = (_today_for_picker.month - 1) // 3 + 1
        while (_y, _q) <= (_today_for_picker.year, _cur_q):
            _quarter_options.append(f"T{_q} {_y}")
            _q += 1
            if _q > 4:
                _q = 1
                _y += 1
        st.selectbox(
            "Trimestre",
            options=_quarter_options,
            index=len(_quarter_options) - 1,
            key="selected_quarter_bizdevs",
        )
    elif _view_picker == "Année":
        _year_options = list(range(2025, _today_for_picker.year + 1))
        st.selectbox(
            "Année",
            options=_year_options,
            index=len(_year_options) - 1,
            format_func=lambda x: str(x),
            key="selected_year_bizdevs",
        )
    elif _view_picker == "Custom":
        _c_de, _c_a = st.columns(2)
        with _c_de:
            st.date_input(
                "De",
                value=_today_for_picker.replace(day=1).date(),
                max_value=_today_for_picker.date(),
                key="custom_start_bizdevs",
            )
        with _c_a:
            st.date_input(
                "A",
                value=_today_for_picker.date(),
                max_value=_today_for_picker.date(),
                key="custom_end_bizdevs",
            )

if _view_picker == "Custom":
    if pd.Timestamp(st.session_state["custom_start_bizdevs"]) > pd.Timestamp(st.session_state["custom_end_bizdevs"]):
        st.error("La date de début doit être antérieure ou égale à la date de fin.")
        st.stop()

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
df_note_mensuel = df_note_plan.copy()
df_note_mensuel['mois'] = pd.to_datetime(df_note_mensuel['mois'])
df_note_mensuel['mois'] = df_note_mensuel['mois'].dt.to_period('M').dt.to_timestamp()
df_note_mensuel = df_note_mensuel[df_note_mensuel['mois'] >= '2024-01-01']

def _agg_plans_par_seuil(df, seuil):
    d = df.copy()
    d['statut'] = d['note_plan'].apply(lambda x: f'>= {seuil}' if x >= seuil else f'< {seuil}')
    return d.groupby(['mois', 'statut'])['plan'].nunique().reset_index(name='nb_plans').sort_values('mois')

df_evolution_note_5 = _agg_plans_par_seuil(df_note_mensuel, 5)
df_evolution_note_8 = _agg_plans_par_seuil(df_note_mensuel, 8)
df_plans_5plus = df_evolution_note_5[df_evolution_note_5['statut'] == '>= 5'].copy()
df_plans_8plus = df_evolution_note_8[df_evolution_note_8['statut'] == '>= 8'].copy()


def _month_start(ts):
    return pd.Timestamp(year=ts.year, month=ts.month, day=1)


def _snapshot_statut(df_statut, ref_month):
    df_f = df_statut[df_statut['mois'] <= ref_month]
    if df_f.empty:
        return 0, 0
    latest = df_f['mois'].max()
    df_l = df_f[df_f['mois'] == latest]
    actif = int(df_l.loc[df_l['statut'] == 'actif', 'nb_collectivites'].sum())
    inactif = int(df_l.loc[df_l['statut'] == 'inactif', 'nb_collectivites'].sum())
    return actif, inactif


def _snapshot_plans(df_plans, ref_month):
    df_f = df_plans[df_plans['mois'] <= ref_month]
    if df_f.empty:
        return 0
    latest = df_f['mois'].max()
    return int(df_f.loc[df_f['mois'] == latest, 'nb_plans'].sum())


def _nouveaux_plans_periode(df_plans, end_m, start_before_m):
    df_by_month = df_plans.set_index('mois')['nb_plans']
    if end_m not in df_by_month.index or start_before_m not in df_by_month.index:
        available = df_by_month.index[df_by_month.index <= end_m]
        if len(available) < 2:
            return None
        end_m = available[-1]
        start_before_m = available[-2]
    return int(df_by_month.loc[end_m] - df_by_month.loc[start_before_m])


_NS_GRAPH_START = pd.Timestamp('2025-01-01')


def _plot_statut_evolution(df_statut, end_date, target=None, height=280):
    if df_statut.empty:
        st.info("Aucune donnée disponible")
        return
    all_statuts = df_statut['statut'].unique()
    all_months = pd.date_range(start=_NS_GRAPH_START, end=end_date, freq='MS')
    full_index = pd.MultiIndex.from_product([all_months, all_statuts], names=['mois', 'statut'])
    df_chart = df_statut.set_index(['mois', 'statut']).reindex(full_index, fill_value=0).reset_index()
    df_chart = df_chart.sort_values('mois')
    df_chart['mois_label'] = df_chart['mois'].dt.strftime('%Y-%m')
    fig = px.line(
        df_chart,
        x='mois_label',
        y='nb_collectivites',
        color='statut',
        markers=True,
        height=height,
        color_discrete_map={'actif': '#22c55e', 'inactif': '#f97316'},
    )
    fig.update_layout(xaxis_title="", yaxis_title="", xaxis_tickangle=-45, legend_title="Statut")
    if target is not None:
        fig.add_hline(y=target, line_dash="dash", line_color="#94a3b8", line_width=1.5)
    st.plotly_chart(fig, use_container_width=True)


def _plot_plans_evolution(df_plans, end_date, target=None, height=280):
    if df_plans.empty:
        st.info("Aucune donnée disponible")
        return
    start_date = df_plans['mois'].min()
    all_months = pd.date_range(start=start_date, end=end_date, freq='MS')
    df_chart = df_plans.set_index('mois').reindex(all_months, fill_value=0).reset_index().rename(columns={'index': 'mois'})
    df_chart['nb_plans'] = df_chart['nb_plans'].fillna(0).astype(int)
    df_chart = df_chart.sort_values('mois')
    df_chart['mois_label'] = df_chart['mois'].dt.strftime('%Y-%m')
    fig = px.line(df_chart, x='mois_label', y='nb_plans', markers=True, height=height)
    fig.update_traces(line_color='#22c55e')
    fig.update_layout(xaxis_title="", yaxis_title="", xaxis_tickangle=-45)
    if target is not None:
        fig.add_hline(y=target, line_dash="dash", line_color="#94a3b8", line_width=1.5)
    st.plotly_chart(fig, use_container_width=True)


def _prepare_pipeline_semaine(df_pipe):
    if df_pipe.empty:
        return df_pipe
    df = df_pipe.copy()
    df['semaine'] = pd.to_datetime(df['semaine'], errors='coerce').dt.normalize()
    return df.dropna(subset=['semaine'])


def get_pipe_transitions_to(df_pipe, target_states, start_date, end_date):
    """
    Retourne les CT passées à l'un des target_states sur la période.
    Compare le dernier état pipe avant start_date avec le plus récent dans [start_date, end_date].
    """
    if isinstance(target_states, str):
        target_states = [target_states]

    df = _prepare_pipeline_semaine(df_pipe)
    if df.empty or not target_states:
        return pd.DataFrame(columns=['collectivite_id', 'pipeline'])

    start_date = pd.Timestamp(start_date).normalize()
    end_date = pd.Timestamp(end_date).normalize()
    target_states = set(target_states)

    period_df = df[(df['semaine'] >= start_date) & (df['semaine'] <= end_date)]
    if period_df.empty:
        return pd.DataFrame(columns=['collectivite_id', 'pipeline'])

    before_df = df[df['semaine'] < start_date]
    period_latest = period_df.sort_values('semaine').groupby('collectivite_id')['pipeline'].last()
    before_latest = (
        before_df.sort_values('semaine').groupby('collectivite_id')['pipeline'].last()
        if not before_df.empty else pd.Series(dtype=object)
    )

    rows = []
    for ct_id, state_in_period in period_latest.items():
        if state_in_period not in target_states:
            continue
        if ct_id not in before_latest.index:
            continue
        if before_latest[ct_id] != state_in_period:
            rows.append({'collectivite_id': ct_id, 'pipeline': state_in_period})
    return pd.DataFrame(rows)


def count_pipe_transitions_to(df_pipe, target_state, start_date, end_date):
    return len(get_pipe_transitions_to(df_pipe, target_state, start_date, end_date))


def _has_pipe_history_before(df_pipe, date):
    df = _prepare_pipeline_semaine(df_pipe)
    if df.empty:
        return False
    return (df['semaine'] < pd.Timestamp(date).normalize()).any()


def get_note_progression_period(df_note, df_passage_pap, start_prev, end_prev, start_cur, end_cur):
    """
    Retourne les CT dont la note a progressé entre deux périodes.
    La note d'une collectivité est la meilleure note parmi tous ses plans.
    """
    empty = pd.DataFrame(columns=['collectivite_id', 'progression'])
    if df_note.empty or df_passage_pap.empty:
        return empty

    df = df_note.copy()
    df['mois'] = pd.to_datetime(df['mois'])
    df = df.merge(df_passage_pap[['collectivite_id', 'plan']], on='plan', how='inner')
    if df.empty:
        return empty

    df_prev = df[(df['mois'] >= start_prev) & (df['mois'] <= end_prev)].copy()
    df_cur = df[(df['mois'] >= start_cur) & (df['mois'] <= end_cur)].copy()
    if df_prev.empty or df_cur.empty:
        return empty

    df_prev_last_date = df_prev.groupby('collectivite_id')['mois'].max().reset_index()
    df_cur_last_date = df_cur.groupby('collectivite_id')['mois'].max().reset_index()
    df_prev_last = df_prev.merge(df_prev_last_date, on=['collectivite_id', 'mois'])
    df_cur_last = df_cur.merge(df_cur_last_date, on=['collectivite_id', 'mois'])
    df_prev_best = df_prev_last.groupby('collectivite_id')['note_plan'].max().reset_index()
    df_cur_best = df_cur_last.groupby('collectivite_id')['note_plan'].max().reset_index()

    df_compare = df_prev_best.merge(df_cur_best, on='collectivite_id', suffixes=('_prev', '_cur'))
    df_compare['progression'] = df_compare['note_plan_cur'] - df_compare['note_plan_prev']
    return df_compare.loc[df_compare['progression'] > 0, ['collectivite_id', 'progression']].copy()


def get_note_progression_alltime(df_note, df_passage_pap, end_date):
    """
    Retourne les CT dont la note a progressé entre la première et la dernière mesure disponible.
    """
    empty = pd.DataFrame(columns=['collectivite_id', 'progression'])
    if df_note.empty or df_passage_pap.empty:
        return empty

    df = df_note.copy()
    df['mois'] = pd.to_datetime(df['mois'])
    df = df[df['mois'] <= end_date]
    df = df.merge(df_passage_pap[['collectivite_id', 'plan']], on='plan', how='inner')
    if df.empty:
        return empty

    df_sorted = df.sort_values('mois')
    df_first_date = df_sorted.groupby('collectivite_id')['mois'].min().reset_index()
    df_last_date = df_sorted.groupby('collectivite_id')['mois'].max().reset_index()
    df_first = df_sorted.merge(df_first_date, on=['collectivite_id', 'mois'])
    df_last = df_sorted.merge(df_last_date, on=['collectivite_id', 'mois'])
    df_first_best = df_first.groupby('collectivite_id')['note_plan'].max().reset_index()
    df_last_best = df_last.groupby('collectivite_id')['note_plan'].max().reset_index()

    df_compare = df_first_best.merge(df_last_best, on='collectivite_id', suffixes=('_first', '_last'))
    df_compare['progression'] = df_compare['note_plan_last'] - df_compare['note_plan_first']
    return df_compare.loc[df_compare['progression'] > 0, ['collectivite_id', 'progression']].copy()


# Calcul des périodes selon la vue sélectionnée
today = pd.Timestamp.today().normalize()
view = st.session_state.get("view_bizdevs", "Mois")
is_all_time = (view == "All Time")

if view == "Semaine":
    _default_monday = (today - pd.Timedelta(days=today.weekday())).strftime("%Y-%m-%d")
    _selected = st.session_state.get("selected_week_bizdevs", _default_monday)
    cur_start = pd.Timestamp(_selected)
    cur_end = cur_start + pd.Timedelta(days=6)
    if cur_end > today:
        cur_end = today
    prev_start = cur_start - pd.Timedelta(days=7)
    prev_end = cur_start - pd.Timedelta(days=1)
elif view == "Mois":
    _selected = st.session_state.get("selected_month_bizdevs", f"{today.year}-{today.month:02d}")
    sel_y, sel_m = int(_selected.split('-')[0]), int(_selected.split('-')[1])
    cur_start = pd.Timestamp(year=sel_y, month=sel_m, day=1)
    if sel_y == today.year and sel_m == today.month:
        cur_end = today
    else:
        cur_end = pd.Timestamp(year=sel_y, month=sel_m, day=calendar.monthrange(sel_y, sel_m)[1])
    prev_m = sel_m - 1 if sel_m > 1 else 12
    prev_y = sel_y if sel_m > 1 else sel_y - 1
    prev_start = pd.Timestamp(year=prev_y, month=prev_m, day=1)
    prev_end = pd.Timestamp(year=prev_y, month=prev_m, day=calendar.monthrange(prev_y, prev_m)[1])
elif view == "Trimestre":
    _cur_q = (today.month - 1) // 3 + 1
    _default_quarter = f"T{_cur_q} {today.year}"
    _selected = st.session_state.get("selected_quarter_bizdevs", _default_quarter)
    _q = int(_selected[1])
    sel_y = int(_selected.split(" ")[1])
    month_start = (_q - 1) * 3 + 1
    month_end = _q * 3
    cur_start = pd.Timestamp(year=sel_y, month=month_start, day=1)
    cur_end_month = pd.Timestamp(year=sel_y, month=month_end, day=calendar.monthrange(sel_y, month_end)[1])
    if sel_y == today.year and _q == _cur_q:
        cur_end = today
    else:
        cur_end = cur_end_month
    prev_q = _q - 1 if _q > 1 else 4
    prev_y = sel_y if _q > 1 else sel_y - 1
    prev_month_start = (prev_q - 1) * 3 + 1
    prev_month_end = prev_q * 3
    prev_start = pd.Timestamp(year=prev_y, month=prev_month_start, day=1)
    prev_end = pd.Timestamp(year=prev_y, month=prev_month_end, day=calendar.monthrange(prev_y, prev_month_end)[1])
elif view == "Année":
    sel_y = st.session_state.get("selected_year_bizdevs", today.year)
    cur_start = pd.Timestamp(year=sel_y, month=1, day=1)
    if sel_y == today.year:
        cur_end = today
    else:
        cur_end = pd.Timestamp(year=sel_y, month=12, day=31)
    prev_y = sel_y - 1
    prev_start = pd.Timestamp(year=prev_y, month=1, day=1)
    prev_end = pd.Timestamp(year=prev_y, month=12, day=31)
elif view == "Custom":
    cur_start = pd.Timestamp(st.session_state["custom_start_bizdevs"])
    cur_end = pd.Timestamp(st.session_state["custom_end_bizdevs"])
    _duration = (cur_end - cur_start).days + 1
    prev_end = cur_start - pd.Timedelta(days=1)
    prev_start = prev_end - pd.Timedelta(days=_duration - 1)
elif view == "All Time":
    cur_start = today - pd.Timedelta(days=31)
    cur_end = today
    prev_start = cur_start - pd.Timedelta(days=31)
    prev_end = cur_start - pd.Timedelta(days=1)

# === North Stars : grille 2×2 ===
end_date = today if is_all_time else cur_end
end_month = _month_start(end_date)
prev_snapshot_month = _month_start(prev_end) if not is_all_time else end_month - pd.DateOffset(months=1)
before_period = _month_start(cur_start - pd.Timedelta(days=1))
prev_end_month = _month_start(prev_end)

row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)

# --- NS1 : CT PAP actifs ---
with row1_col1:
    st.badge(
        "NS1 — CT PAP actifs",
        color="orange",
        help="Collectivités avec un plan d'action ayant au moins 5 fiches pilotables (titre, description, statut et pilote) modifiées au cours des 3 derniers mois.",
    )
    m1, m2, m3 = st.columns(3)
    with m1:
        if not ct_first_pap.empty:
            new_pap_cur = len(ct_first_pap[(ct_first_pap['date_premier_pap'] >= cur_start) & (ct_first_pap['date_premier_pap'] <= cur_end)])
            new_pap_prev = len(ct_first_pap[(ct_first_pap['date_premier_pap'] >= prev_start) & (ct_first_pap['date_premier_pap'] <= prev_end)])
            st.metric(label="Nouvelles CT PAP", value=new_pap_cur, delta=f"{new_pap_cur - new_pap_prev:+d}", delta_color="normal")
        else:
            st.metric(label="Nouvelles CT PAP", value=0)
    actif_pap, inactif_pap = _snapshot_statut(df_pap_statut, end_month)
    actif_pap_prev, inactif_pap_prev = _snapshot_statut(df_pap_statut, prev_snapshot_month)
    with m2:
        st.metric(label="CT PAP actives", value=actif_pap, delta=f"{actif_pap - actif_pap_prev:+d}", delta_color="normal")
    with m3:
        st.metric(label="CT PAP inactives", value=inactif_pap, delta=f"{inactif_pap - inactif_pap_prev:+d}", delta_color="normal")
    _plot_statut_evolution(df_pap_statut, end_date, target=350)

# --- NS2 : CT multiplan ---
with row1_col2:
    st.badge(
        "NS2 — CT multiplan",
        color="orange",
        help="Collectivités avec au moins 2 PAP ayant chacun au moins 5 fiches pilotables modifiées au cours des 3 derniers mois.",
    )
    m1, m2, m3 = st.columns(3)
    with m1:
        if not ct_first_multiplan.empty:
            new_mp_cur = len(ct_first_multiplan[(ct_first_multiplan['date_premier_multiplan'] >= cur_start) & (ct_first_multiplan['date_premier_multiplan'] <= cur_end)])
            new_mp_prev = len(ct_first_multiplan[(ct_first_multiplan['date_premier_multiplan'] >= prev_start) & (ct_first_multiplan['date_premier_multiplan'] <= prev_end)])
            st.metric(label="Nouvelles CT multiplans", value=new_mp_cur, delta=f"{new_mp_cur - new_mp_prev:+d}", delta_color="normal")
        else:
            st.metric(label="Nouvelles CT multiplans", value=0)
    actif_mp, inactif_mp = _snapshot_statut(df_multiplans_statut, end_month)
    actif_mp_prev, inactif_mp_prev = _snapshot_statut(df_multiplans_statut, prev_snapshot_month)
    with m2:
        st.metric(label="CT multiplans actives", value=actif_mp, delta=f"{actif_mp - actif_mp_prev:+d}", delta_color="normal")
    with m3:
        st.metric(label="CT multiplans inactives", value=inactif_mp, delta=f"{inactif_mp - inactif_mp_prev:+d}", delta_color="normal")
    _plot_statut_evolution(df_multiplans_statut, end_date, target=100)

# --- NS3 externe : Qualité >= 5/10 ---
with row2_col1:
    st.badge(
        "NS3 externe — Qualité",
        color="orange",
        help="Plans dont la note est supérieure à 5/10.",
    )
    m1, m2 = st.columns(2)
    new_5_cur = _nouveaux_plans_periode(df_plans_5plus, end_month, before_period)
    new_5_prev = _nouveaux_plans_periode(df_plans_5plus, prev_end_month, _month_start(prev_start - pd.Timedelta(days=1)))
    with m1:
        if new_5_cur is not None:
            delta_5 = new_5_cur - (new_5_prev if new_5_prev is not None else 0)
            st.metric(label="Nouveaux plans >=5/10", value=new_5_cur, delta=f"{delta_5:+d}", delta_color="normal")
        else:
            st.metric(label="Nouveaux plans >=5/10", value=0)
    with m2:
        st.metric(label="Plans >=5/10", value=_snapshot_plans(df_plans_5plus, end_month))
    _plot_plans_evolution(df_plans_5plus, end_date, target=800)

# --- NS3 interne : Qualité >= 8/10 ---
with row2_col2:
    st.badge(
        "NS3 interne — Qualité",
        color="orange",
        help="Plans dont la note est supérieure à 8/10.",
    )
    m1, m2 = st.columns(2)
    new_8_cur = _nouveaux_plans_periode(df_plans_8plus, end_month, before_period)
    new_8_prev = _nouveaux_plans_periode(df_plans_8plus, prev_end_month, _month_start(prev_start - pd.Timedelta(days=1)))
    with m1:
        if new_8_cur is not None:
            delta_8 = new_8_cur - (new_8_prev if new_8_prev is not None else 0)
            st.metric(label="Nouveaux plans >=8/10", value=new_8_cur, delta=f"{delta_8:+d}", delta_color="normal")
        else:
            st.metric(label="Nouveaux plans >=8/10", value=0)
    with m2:
        st.metric(label="Plans >=8/10", value=_snapshot_plans(df_plans_8plus, end_month))
    _plot_plans_evolution(df_plans_8plus, end_date, target=50)

st.markdown("---")

st.badge("Zoom plans", icon="🔍", color="violet")

_cols_zoom = ['nom', 'nom_plan_ct', 'import', 'createur_plan']
df_pap_zoom_base = df_passage_pap.copy()
if not df_pap_zoom_base.empty and 'passage_pap' in df_pap_zoom_base.columns:
    df_pap_zoom_base['passage_pap'] = pd.to_datetime(df_pap_zoom_base['passage_pap'], errors='coerce')
    if df_pap_zoom_base['passage_pap'].dt.tz is not None:
        df_pap_zoom_base['passage_pap'] = df_pap_zoom_base['passage_pap'].dt.tz_localize(None)

    df_pap_cur = df_pap_zoom_base[
        (df_pap_zoom_base['passage_pap'] >= cur_start) & (df_pap_zoom_base['passage_pap'] <= cur_end)
    ]
    df_pap_prev = df_pap_zoom_base[
        (df_pap_zoom_base['passage_pap'] >= prev_start) & (df_pap_zoom_base['passage_pap'] <= prev_end)
    ]

    nb_nouveaux_cur = len(df_pap_cur)
    nb_nouveaux_prev = len(df_pap_prev)
    nb_autonome_cur = len(df_pap_cur[df_pap_cur['import'] == 'Autonome']) if 'import' in df_pap_cur.columns else 0
    nb_autonome_prev = len(df_pap_prev[df_pap_prev['import'] == 'Autonome']) if 'import' in df_pap_prev.columns else 0
    nb_importe_cur = len(df_pap_cur[df_pap_cur['import'] == 'Importé']) if 'import' in df_pap_cur.columns else 0
    nb_importe_prev = len(df_pap_prev[df_pap_prev['import'] == 'Importé']) if 'import' in df_pap_prev.columns else 0

    part_autonome_cur = round(nb_autonome_cur / nb_nouveaux_cur * 100) if nb_nouveaux_cur > 0 else 0
    part_autonome_prev = round(nb_autonome_prev / nb_nouveaux_prev * 100) if nb_nouveaux_prev > 0 else 0

    m_nouveaux, m_autonome, m_importe, m_part = st.columns(4)
    with m_nouveaux:
        st.metric(
            label="Nouveaux PAP",
            value=nb_nouveaux_cur,
            delta=f"{nb_nouveaux_cur - nb_nouveaux_prev:+d}",
            delta_color="normal",
        )
    with m_autonome:
        st.metric(
            label="PAP autonome",
            value=nb_autonome_cur,
            delta=f"{nb_autonome_cur - nb_autonome_prev:+d}",
            delta_color="normal",
        )
    with m_importe:
        st.metric(
            label="PAP importés",
            value=nb_importe_cur,
            delta=f"{nb_importe_cur - nb_importe_prev:+d}",
            delta_color="normal",
        )
    with m_part:
        st.metric(
            label="Part de nouveaux plan autonome",
            value=f"{part_autonome_cur:.0f}%",
            delta=f"{part_autonome_cur - part_autonome_prev:+.0f}%",
            delta_color="normal",
        )

    df_pap_zoom = df_pap_cur.sort_values('passage_pap', ascending=False)
    _cols_present = [c for c in _cols_zoom if c in df_pap_zoom.columns]
    if _cols_present and not df_pap_zoom.empty:
        df_table_zoom = df_pap_zoom[_cols_present].rename(columns={
            'nom': 'Collectivité',
            'nom_plan_ct': 'Nom du plan',
            'import': 'Import',
            'createur_plan': 'Créateur du plan',
        })
        st.dataframe(df_table_zoom, width='stretch', hide_index=True)
    else:
        st.info("Aucun passage PAP sur la période sélectionnée.")
else:
    st.info("Aucune donnée disponible.")

st.markdown("---")

st.badge("Evolution du pipe", icon="📈", color="violet")

_PIPE_EVOLUTION_TARGETS_POSITIVE = [
    "En conversion",
    "En rétention - activé",
    "En rétention - multiplan",
    "En pilotage",
    "En pilotage - multiplan",
]
_PIPE_EVOLUTION_TARGETS_WATCH = [
    "En pilotage - à surveiller",
    "En rétention - à surveiller",
    "A réactiver - 6 mois",
    "A réactiver - 12 mois",
    "A réactiver - 18 mois"
]
_can_pipe_delta = _has_pipe_history_before(df_pipeline_semaine, prev_start)

_row_pipe_pos = st.columns(5)
for _col, _target in zip(_row_pipe_pos, _PIPE_EVOLUTION_TARGETS_POSITIVE):
    _cur = count_pipe_transitions_to(df_pipeline_semaine, _target, cur_start, cur_end)
    with _col:
        if _can_pipe_delta:
            _prev = count_pipe_transitions_to(df_pipeline_semaine, _target, prev_start, prev_end)
            st.metric(
                label=f"{_target}",
                value=_cur,
                delta=f"{_cur - _prev:+d}",
                delta_color="normal",
            )
        else:
            st.metric(label=f"{_target}", value=_cur)

_row_pipe_watch = st.columns(5)
for _col, _target in zip(_row_pipe_watch, _PIPE_EVOLUTION_TARGETS_WATCH):
    _cur = count_pipe_transitions_to(df_pipeline_semaine, _target, cur_start, cur_end)
    with _col:
        if _can_pipe_delta:
            _prev = count_pipe_transitions_to(df_pipeline_semaine, _target, prev_start, prev_end)
            st.metric(
                label=f"{_target}",
                value=_cur,
                delta=f"{_cur - _prev:+d}",
                delta_color="normal",
            )
        else:
            st.metric(label=f"{_target}", value=_cur)

_PIPE_EVOLUTION_ALL = _PIPE_EVOLUTION_TARGETS_POSITIVE + _PIPE_EVOLUTION_TARGETS_WATCH
_selected_pipelines = st.multiselect(
    "Pipelines",
    options=_PIPE_EVOLUTION_ALL,
    default=["En pilotage - multiplan"],
    key="pipe_evolution_filter",
)
if _selected_pipelines:
    df_pipe_evolution = get_pipe_transitions_to(
        df_pipeline_semaine, _selected_pipelines, cur_start, cur_end
    )
    if not df_pipe_evolution.empty and not df_passage_pap.empty and 'nom' in df_passage_pap.columns:
        df_ct_nom = df_passage_pap[['collectivite_id', 'nom']].drop_duplicates(subset='collectivite_id', keep='first')
        df_pipe_evolution = df_pipe_evolution.merge(df_ct_nom, on='collectivite_id', how='left')
        df_pipe_table = df_pipe_evolution[['nom', 'pipeline']].rename(columns={'nom': 'collectivite'})
        df_pipe_table = df_pipe_table.sort_values('collectivite', na_position='last')
        st.dataframe(df_pipe_table, use_container_width=True, hide_index=True)
    elif df_pipe_evolution.empty:
        st.info("Aucune collectivité n'a évolué vers les pipelines sélectionnés sur cette période.")
    else:
        st.info("Impossible d'afficher les noms de collectivités (données pap_date_passage indisponibles).")
else:
    st.info("Sélectionnez au moins un pipeline pour afficher le détail des collectivités.")

st.markdown("---")

st.badge("Progression plan", icon="📊", color="violet")

if is_all_time:
    df_note_progression = get_note_progression_alltime(df_note_plan, df_passage_pap, today)
    _help_nb = "Nombre de CT dont la note du plan a progressé depuis la première mesure"
    _help_moy = "Progression moyenne de la note pour les CT ayant progressé"
else:
    df_note_progression = get_note_progression_period(
        df_note_plan, df_passage_pap, prev_start, prev_end, cur_start, cur_end
    )
    _help_nb = "Nombre de CT dont la note du plan a progressé entre la période précédente et la période actuelle"
    _help_moy = "Progression moyenne de la note pour les CT ayant progressé"

_nb_ct_prog = len(df_note_progression)
_prog_moyenne = df_note_progression['progression'].mean() if _nb_ct_prog > 0 else 0.0

_col_prog_nb, _col_prog_moy = st.columns(2)
with _col_prog_nb:
    st.metric(label="CT dont la note a progressé", value=_nb_ct_prog, help=_help_nb)
with _col_prog_moy:
    st.metric(label="Progression moyenne", value=f"{_prog_moyenne:.2f}", help=_help_moy)

if not df_note_progression.empty and not df_passage_pap.empty and 'nom' in df_passage_pap.columns:
    df_ct_nom_prog = df_passage_pap[['collectivite_id', 'nom']].drop_duplicates(subset='collectivite_id', keep='first')
    df_note_progression_table = df_note_progression.merge(df_ct_nom_prog, on='collectivite_id', how='left')
    df_note_progression_table = (
        df_note_progression_table[['nom', 'progression']]
        .rename(columns={'nom': 'collectivite'})
        .sort_values('progression', ascending=False)
    )
    st.dataframe(df_note_progression_table, use_container_width=True, hide_index=True)
elif df_note_progression.empty:
    st.info("Aucune collectivité n'a progressé sur la période sélectionnée.")
else:
    st.info("Impossible d'afficher les noms de collectivités (données pap_date_passage indisponibles).")

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

_DEMO_TYPES = [
    '▶️ Démo Pilotage - Découverte & prise en main (1/2)',
    '⏩ Démo Pilotage - Fonctionnalités expertes (2/2)',
    '⏏️ Démo - Commencez votre état des lieux (T.E.T.E)',
]

st.badge("Activation", icon="🐣", color="blue")

if is_all_time:
    _time_min_activation = pd.Timestamp('2025-05-01')
    _total_demos = len(df_calendly_events[
        (df_calendly_events['type'].isin(_DEMO_TYPES))
        & (df_calendly_events['start_time'] >= _time_min_activation)
        & (df_calendly_events['start_time'] <= today)
    ])
else:
    _total_demos = len(df_calendly_events[
        (df_calendly_events['type'].isin(_DEMO_TYPES))
        & (df_calendly_events['start_time'] >= cur_start)
        & (df_calendly_events['start_time'] <= cur_end)
    ])

st.markdown(f"Il y a eu **{_total_demos}** démo au total.")

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
        st.dataframe(table_single, width='stretch')
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
    types_ordre = _DEMO_TYPES
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