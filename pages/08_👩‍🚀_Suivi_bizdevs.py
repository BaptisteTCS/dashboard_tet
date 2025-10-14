import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data import (
    load_df_calendly_events,
    load_df_calendly_invitees,
    load_df_bizdev_contact_collectivite
)
from utils.plots import plot_area_with_totals


st.set_page_config(layout="wide")
st.title("👩‍🚀 Suivi des actions bizdevs")

# === CHARGEMENT ===
df_calendly_events = load_df_calendly_events()
df_calendly_invitees = load_df_calendly_invitees()
df_bizdev_contact_collectivite = load_df_bizdev_contact_collectivite()

mapping_events = {
    'https://api.calendly.com/event_types/01a671ef-0151-423b-b8fc-875562ebb4b7': 'Support',
    'https://api.calendly.com/event_types/0759411f-17c3-4528-85ea-a50d91c8306d': 'Support',
    'https://api.calendly.com/event_types/0d8512ff-e307-4434-9900-7be0b0541c6c': 'Les RDV TET',
    'https://api.calendly.com/event_types/2859f624-013e-4560-be2c-5f10ace7f022': 'Démo 1/2',
    'https://api.calendly.com/event_types/42dc86a2-9cc6-45d6-9302-f911cac21427': 'PAT',
    'https://api.calendly.com/event_types/60033b52-21d5-47e3-8c39-dcd00024568c': 'Démo 2/2',
    'https://api.calendly.com/event_types/61757879-a6d4-4e90-87e8-f97d516a9ea9': 'Suivi Super-Utilisateur',
    'https://api.calendly.com/event_types/cd9b2d14-85bf-46d3-8839-21bd8d7e64ba': 'Démo 1/2',
    'https://api.calendly.com/event_types/d6ab7313-ef74-4f26-8d87-90c68d0204b2': 'Suivi Super-Utilisateur',
    'https://api.calendly.com/event_types/e065aec8-0a0a-4683-97ea-d79c76ea321f': 'Démo EdL',
    'https://api.calendly.com/event_types/f7554b84-1bab-40c5-ae0a-c1493b2c0d42': 'Démo 1/2',
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

############################
# === INDICATEURS CLÉS === #
############################
st.markdown("---")
st.markdown("## 🌟 Indicateurs clés sur les 30 derniers jours")

st.markdown("### Reach Collectivités")

today = pd.Timestamp.today().normalize()
cur_start = today - pd.Timedelta(days=30)
prev_start = cur_start - pd.Timedelta(days=30)
prev_end = cur_start - pd.Timedelta(seconds=1)

# Préparation des dates pour le reach
df_biz = df_bizdev_contact_collectivite.copy()
if not df_biz.empty:
    df_biz['date_contact'] = pd.to_datetime(df_biz['date_contact'], errors='coerce').dt.tz_localize(None)

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
        label="Reach total",
        value=total_reach_cur,
        delta=delta_reach,
        delta_color="normal"
    )
with col_r2:
    st.metric(
        label="Collectivités atteintes",
        value=ct_reach_cur,
        delta=delta_ct,
        delta_color="normal"
    )

st.markdown("### Événements Calendly")

# Filtrages
events_cur = df_calendly_events[(df_calendly_events['start_time'] >= cur_start) & (df_calendly_events['start_time'] <= today)]
events_prev = df_calendly_events[(df_calendly_events['start_time'] >= prev_start) & (df_calendly_events['start_time'] <= prev_end)]

inv_cur = df_invitees_active[(df_invitees_active['start_time'] >= cur_start) & (df_invitees_active['start_time'] <= today)]
inv_prev = df_invitees_active[(df_invitees_active['start_time'] >= prev_start) & (df_invitees_active['start_time'] <= prev_end)]

# Comptages par type
events_cur_g = events_cur.groupby('type').size().rename('events_30j')
events_prev_g = events_prev.groupby('type').size().rename('events_prev')
inv_cur_g = inv_cur.groupby('type').size().rename('participants_30j')
inv_prev_g = inv_prev.groupby('type').size().rename('participants_prev')

kpis = pd.concat([events_cur_g, events_prev_g, inv_cur_g, inv_prev_g], axis=1).fillna(0).astype(int).reset_index().rename(columns={'index': 'type'})

def pct_delta(cur: int, prev: int) -> str:
    if prev == 0:
        return "+∞%" if cur > 0 else "0%"
    return f"{((cur - prev) / prev * 100):+.0f}%"

kpis['Δ événements'] = kpis.apply(lambda r: pct_delta(r['events_30j'], r['events_prev']), axis=1)
kpis['Δ participants'] = kpis.apply(lambda r: pct_delta(r['participants_30j'], r['participants_prev']), axis=1)
kpis = kpis[['type', 'events_30j', 'Δ événements', 'participants_30j', 'Δ participants']].sort_values('events_30j', ascending=False)

# Affichage "sexy" façon Weekly: cartes de métriques par type
nb_types = len(kpis)
if nb_types == 0:
    st.info("Pas de données sur les 30 derniers jours.")
else:
    cols_per_row = 4
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
            c_ev, c_pa = st.columns(2)
            with c_ev:
                st.metric(
                    label="Événements",
                    value=int(row['events_30j']),
                    delta=row['Δ événements'],
                    delta_color="normal"
                )
            with c_pa:
                st.metric(
                    label="Participants",
                    value=int(row['participants_30j']),
                    delta=row['Δ participants'],
                    delta_color="normal"
                )

###############
# === FOCUS ===
###############
st.markdown("---")
st.markdown("## 🔭 Focus")

min_dt = df_calendly_events['start_time'].min()
max_dt = df_calendly_events['start_time'].max()

f1, f2, f3 = st.columns([1, 1, 1])
with f1:
    # Plage personnalisée uniquement (par défaut: 30 derniers jours)
    cstart, cend = st.columns(2)
    with cstart:
        d1 = st.date_input("Début", value=max(min_dt.date(), (today - pd.Timedelta(days=30)).date()))
    with cend:
        d2 = st.date_input("Fin", value=today.date())
    start_date = pd.to_datetime(d1)
    end_date = pd.to_datetime(d2) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
with f2:
    types_disponibles = df_calendly_events['type'].dropna().sort_values().unique().tolist()
    types_selection = st.multiselect("Type d'événement", options=types_disponibles, default=types_disponibles)

time_granularity = 'M'
x_title = "Mois"
cumulatif = False

# Filtres focus
events_filtres = df_calendly_events[(df_calendly_events['start_time'] >= start_date) & (df_calendly_events['start_time'] <= end_date) & (df_calendly_events['type'].isin(types_selection))]
invitees_filtres = df_invitees_active[(df_invitees_active['start_time'] >= start_date) & (df_invitees_active['start_time'] <= end_date) & (df_invitees_active['type'].isin(types_selection))]

st.markdown("#### Évolutions")
g1, g2 = st.columns(2)
with g1:
    fig_events = plot_area_with_totals(
        df=events_filtres,
        date_col='start_time',
        group_col='type',
        time_granularity=time_granularity,
        legend_title="Type d'événement",
        min_date=str(start_date.date()),
        cumulatif=cumulatif,
        x_title=x_title,
        y_title="Nombre d'événements",
        title="Évolution des événements par type"
    )
    st.plotly_chart(fig_events, use_container_width=True)
with g2:
    fig_participants = plot_area_with_totals(
        df=invitees_filtres,
        date_col='start_time',
        group_col='type',
        time_granularity=time_granularity,
        legend_title="Type d'événement",
        min_date=str(start_date.date()),
        cumulatif=cumulatif,
        x_title=x_title,
        y_title="Nombre de participants (actifs)",
        title="Évolution des participants actifs par type"
    )
    st.plotly_chart(fig_participants, use_container_width=True)

# === TABLEAUX MENSUELS ===
st.markdown("#### Vue tableau")

def monthly_table(df: pd.DataFrame, date_col: str, group_col: str) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    tmp = df.copy()
    tmp[date_col] = pd.to_datetime(tmp[date_col]).dt.tz_localize(None)
    tmp['mois'] = tmp[date_col].dt.to_period('M').dt.to_timestamp()
    pivot = tmp.groupby(['mois', group_col]).size().unstack(fill_value=0)
    pivot = pivot.sort_index()
    pivot.index = pivot.index.strftime('%Y-%m')
    # Totaux par ligne (mois)
    pivot['Total'] = pivot.sum(axis=1)
    # Totaux par colonne (type), tri décroissant et réordonnancement des colonnes
    col_totals = pivot.drop(columns=['Total']).sum(axis=0).sort_values(ascending=False)
    ordered_cols = list(col_totals.index) + ['Total']
    pivot = pivot[ordered_cols]
    # Ajouter ligne Total en bas
    total_row = pivot.drop(columns=['Total']).sum(axis=0)
    total_row['Total'] = total_row.sum()
    pivot.loc['Total'] = total_row
    return pivot

def monthly_single_table(events_df: pd.DataFrame, invitees_df: pd.DataFrame, date_col: str) -> pd.DataFrame:
    # Table unique quand un seul type est sélectionné
    e = events_df.copy()
    i = invitees_df.copy()
    if e.empty and i.empty:
        return pd.DataFrame()
    for df in (e, i):
        if not df.empty:
            df[date_col] = pd.to_datetime(df[date_col]).dt.tz_localize(None)
            df['mois'] = df[date_col].dt.to_period('M').dt.to_timestamp()
    ev = e.groupby('mois').size().rename('Nombre d\'événements') if not e.empty else pd.Series(dtype=int, name='Nombre d\'événements')
    pa = i.groupby('mois').size().rename('Nombre de participants') if not i.empty else pd.Series(dtype=int, name='Nombre de participants')
    dfm = pd.concat([ev, pa], axis=1).fillna(0).astype(int).sort_index()
    dfm.index = dfm.index.strftime('%Y-%m')
    dfm['Total'] = dfm['Nombre d\'événements'] + dfm['Nombre de participants']
    # Ajouter ligne Total
    total_row = pd.Series({
        'Nombre d\'événements': int(dfm['Nombre d\'événements'].sum()),
        'Nombre de participants': int(dfm['Nombre de participants'].sum()),
        'Total': int(dfm['Total'].sum())
    }, name='Total')
    dfm = pd.concat([dfm, total_row.to_frame().T])
    return dfm

if len(types_selection) == 1:
    st.markdown(f"Tableau unique — {types_selection[0]}")
    table_single = monthly_single_table(events_filtres, invitees_filtres, 'start_time')
    left, center, right = st.columns([1, 2, 1])
    with center:
        st.dataframe(table_single, use_container_width=True)
        if not table_single.empty:
            csv_single = table_single.to_csv(index=True).encode('utf-8')
            st.download_button(
                label="Exporter CSV",
                data=csv_single,
                file_name="evenements_participants_mensuel.csv",
                mime="text/csv"
            )
else:
    tab1, tab2 = st.columns(2)
    with tab1:
        st.markdown("Événements par mois et type")
        table_events = monthly_table(events_filtres, 'start_time', 'type')
        st.dataframe(table_events, use_container_width=True)
        if not table_events.empty:
            csv_events = table_events.to_csv(index=True).encode('utf-8')
            st.download_button(
                label="Exporter CSV événements",
                data=csv_events,
                file_name="evenements_par_mois.csv",
                mime="text/csv"
            )
    with tab2:
        st.markdown("Participants (actifs) par mois et type")
        table_participants = monthly_table(invitees_filtres, 'start_time', 'type')
        st.dataframe(table_participants, use_container_width=True)
        if not table_participants.empty:
            csv_participants = table_participants.to_csv(index=True).encode('utf-8')
            st.download_button(
                label="Exporter CSV participants",
                data=csv_participants,
                file_name="participants_par_mois.csv",
                mime="text/csv"
            )

############################################
# === COMMENT ONT-ILS TROUVÉ LA DÉMO 1/2 ?
############################################
st.markdown("---")
st.markdown("### 🔍 Comment ont-ils trouvé la démo 1/2 ?")

pie_c1, pie_c2 = st.columns(2)
with pie_c1:
    d1_pie = st.date_input("Début (démo)", value=max(min_dt.date(), (today - pd.Timedelta(days=30)).date()))
with pie_c2:
    d2_pie = st.date_input("Fin (démo)", value=today.date())

pie_start = pd.to_datetime(d1_pie)
pie_end = pd.to_datetime(d2_pie) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

demo12 = df_invitees_active[(df_invitees_active['type'] == 'Démo 1/2') & (df_invitees_active['start_time'] >= pie_start) & (df_invitees_active['start_time'] <= pie_end)][['reponse']].copy()

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
    left, center, right = st.columns([1, 3, 1])
    with center:
        fig_pie = px.pie(total_counts, values='nb', names='items', title="Répartition des retours (Démo 1/2)")
        st.plotly_chart(fig_pie, use_container_width=True)
        # Export CSV des comptes agrégés affichés
        csv_pie = total_counts.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Exporter CSV retours démo 1/2",
            data=csv_pie,
            file_name="retours_demo12_agg.csv",
            mime="text/csv"
        )

