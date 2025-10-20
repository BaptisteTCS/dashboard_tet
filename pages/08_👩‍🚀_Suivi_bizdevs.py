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
    'https://api.calendly.com/event_types/01a671ef-0151-423b-b8fc-875562ebb4b7': '🆘 Support - 15min pour vous débloquer',
    'https://api.calendly.com/event_types/0759411f-17c3-4528-85ea-a50d91c8306d': '🆘 Support - 15min pour vous débloquer',
    'https://api.calendly.com/event_types/0d8512ff-e307-4434-9900-7be0b0541c6c': '🎬 Les RDV Territoires en Transitions',
    'https://api.calendly.com/event_types/2859f624-013e-4560-be2c-5f10ace7f022': '⏏️ Démo - Commencez votre état des lieux (T.E.T.E)',
    'https://api.calendly.com/event_types/60033b52-21d5-47e3-8c39-dcd00024568c': '⏩ Démo Pilotage - Fonctionnalités expertes (2/2)',
    'https://api.calendly.com/event_types/61757879-a6d4-4e90-87e8-f97d516a9ea9': '🌟 Suivi Super-Utilisateurs',
    'https://api.calendly.com/event_types/cd9b2d14-85bf-46d3-8839-21bd8d7e64ba': '⏩ Démo Pilotage - Fonctionnalités expertes (2/2)',
    'https://api.calendly.com/event_types/d6ab7313-ef74-4f26-8d87-90c68d0204b2': '🌟 Suivi Super-Utilisateurs ( > 3 mois de pilotage)',
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

############################
# === INDICATEURS CLÉS === #
############################
st.markdown("---")
st.markdown("## 🔑 Indicateurs clés sur les 30 derniers jours")

st.markdown("### Prise de contacts")

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
        label="Contacts",
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
inv_cur_g = inv_cur.groupby('type').size().rename('inscrits_30j')
inv_prev_g = inv_prev.groupby('type').size().rename('inscrits_prev')

# Participants réels (nouvelle colonne nb_participants_reel)
if 'nb_participants_reel' in events_cur.columns:
    part_cur_g = events_cur.groupby('type')['nb_participants_reel'].sum().rename('participants_30j')
    part_prev_g = events_prev.groupby('type')['nb_participants_reel'].sum().rename('participants_prev')
else:
    part_cur_g = pd.Series(dtype=int, name='participants_30j')
    part_prev_g = pd.Series(dtype=int, name='participants_prev')

kpis = pd.concat([events_cur_g, events_prev_g, inv_cur_g, inv_prev_g, part_cur_g, part_prev_g], axis=1).fillna(0).astype(int).reset_index().rename(columns={'index': 'type'})

def pct_delta(cur: int, prev: int) -> str:
    if prev == 0:
        return "+∞%" if cur > 0 else "0%"
    return f"{((cur - prev) / prev * 100):+.0f}%"

kpis['Δ événements'] = kpis.apply(lambda r: pct_delta(r['events_30j'], r['events_prev']), axis=1)
kpis['Δ inscrits'] = kpis.apply(lambda r: pct_delta(r['inscrits_30j'], r['inscrits_prev']), axis=1)
kpis['Δ participants'] = kpis.apply(lambda r: pct_delta(r['participants_30j'], r['participants_prev']), axis=1)
kpis = kpis[['type', 'events_30j', 'Δ événements', 'inscrits_30j', 'Δ inscrits', 'participants_30j', 'Δ participants']].sort_values('events_30j', ascending=False)

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
                    value=int(row['events_30j']),
                    delta=row['Δ événements'],
                    delta_color="normal"
                )
            with c_in:
                st.metric(
                    label="Inscrits",
                    value=int(row['inscrits_30j']),
                    delta=row['Δ inscrits'],
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

st.markdown("### Reach")

# Sélection des dates pour Reach
left_pad_reach, center_reach, right_pad_reach = st.columns([1, 2, 1])
with center_reach:
    cstart_reach, cend_reach = st.columns([1, 1])
    with cstart_reach:
        d1_reach = st.date_input("Début (Reach)", value=pd.Timestamp(2025, 1, 1).date(), key="reach_debut")
        affichage_type = st.segmented_control(
        "Type d'affichage",
        options=["Graphe", "Tableau"],
        default="Graphe",
        key="reach_affichage",
    )
    with cend_reach:
        d2_reach = st.date_input("Fin (Reach)", value=today.date(), key="reach_fin")
        niveau_agregation = st.segmented_control(
        "Niveau d'agrégation",
        options=["Brut", "Collectivités"],
        default="Brut",
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
    df_reach_mois['mois'] = df_reach_mois['date_contact'].dt.to_period('M').dt.to_timestamp()
    
    # Calcul du reach brut et des collectivités par mois
    df_agg_mois = df_reach_mois.groupby('mois').agg({
        'date_contact': 'count',  # Reach brut
        'collectivite_id': 'nunique'  # Collectivités uniques
    }).reset_index()
    df_agg_mois.columns = ['Mois', 'Reach brut', 'Collectivités']
    df_agg_mois['Mois'] = df_agg_mois['Mois'].dt.strftime('%Y-%m')
    
    # Ajouter ligne Total
    total_row = pd.Series({
        'Mois': 'Total',
        'Reach brut': int(df_agg_mois['Reach brut'].sum()),
        'Collectivités': int(df_biz_reach_filtre['collectivite_id'].nunique())
    })
    df_agg_mois = pd.concat([df_agg_mois, total_row.to_frame().T], ignore_index=True)
    
    left_pad2, center_sel, right_pad2 = st.columns([1, 2, 1])
    with center_sel:
        if affichage_type == "Graphe":
            # Graphe selon le niveau d'agrégation
            df_plot = df_agg_mois[df_agg_mois['Mois'] != 'Total'].copy()
             
            if niveau_agregation == "Brut":
                fig_reach = px.line(df_plot, x='Mois', y='Reach brut', title="Évolution du reach brut par mois")
                fig_reach.update_layout(xaxis_title="Mois", yaxis_title="Reach brut")
            else:
                fig_reach = px.line(df_plot, x='Mois', y='Collectivités', title="Évolution des collectivités contactées par mois")
                fig_reach.update_layout(xaxis_title="Mois", yaxis_title="Nombre de collectivités")
            
            st.plotly_chart(fig_reach, use_container_width=True)
        else:
            # Affichage tableau avec les deux colonnes
            st.dataframe(df_agg_mois, use_container_width=True)
else:
    st.info("Aucune donnée de reach sur la période sélectionnée.")

st.markdown("### Événements Calendly")

# Sélection Début / Fin (dates) – centré
left_pad, center_col, right_pad = st.columns([1, 2, 1])
with center_col:
    cstart, cend = st.columns([1, 1])
    with cstart:
        d1 = st.date_input("Début", value=pd.Timestamp(2025, 1, 1).date(), key="focus_debut")
    with cend:
        d2 = st.date_input("Fin", value=today.date(), key="focus_fin")

start_date = pd.to_datetime(d1)
end_date = pd.to_datetime(d2) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

# Sélection des types d'événements (centré et plus étroit)
left_pad2, center_sel, right_pad2 = st.columns([1, 2, 1])
with center_sel:
    types_disponibles = df_calendly_events['type'].dropna().sort_values().unique().tolist()
    type_defaut = '▶️ Démo Pilotage - Découverte & prise en main (1/2)'
    types_selection = st.multiselect(
        "Type d'événement",
        options=types_disponibles,
        default=[type_defaut] if type_defaut in types_disponibles else ([types_disponibles[0]] if types_disponibles else []),
        key="types_focus",
    )

# Filtres focus
events_filtres = df_calendly_events[(df_calendly_events['start_time'] >= start_date) & (df_calendly_events['start_time'] <= end_date) & (df_calendly_events['type'].isin(types_selection))]
invitees_filtres = df_invitees_active[(df_invitees_active['start_time'] >= start_date) & (df_invitees_active['start_time'] <= end_date) & (df_invitees_active['type'].isin(types_selection))]

# Préparation des données pour les participants réels
if 'nb_participants_reel' in events_filtres.columns:
    # Créer un dataframe avec les participants réels par événement
    participants_reel_filtres = events_filtres[['start_time', 'type', 'nb_participants_reel']].copy()
    participants_reel_filtres = participants_reel_filtres[participants_reel_filtres['nb_participants_reel'] > 0]
else:
    # Fallback sur les inscrits actifs si la colonne n'existe pas
    participants_reel_filtres = invitees_filtres.copy()

# === TABLEAUX MENSUELS ===

def monthly_table(df: pd.DataFrame, date_col: str, group_col: str, value_col: str = None) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    tmp = df.copy()
    tmp[date_col] = pd.to_datetime(tmp[date_col]).dt.tz_localize(None)
    tmp['mois'] = tmp[date_col].dt.to_period('M').dt.to_timestamp()
    
    # Utiliser la colonne de valeur si spécifiée, sinon compter les lignes
    if value_col and value_col in tmp.columns:
        pivot = tmp.groupby(['mois', group_col])[value_col].sum().unstack(fill_value=0)
    else:
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
    dfm.index = dfm.index.strftime('%Y-%m')
    dfm['Total'] = dfm.sum(axis=1)
    
    # Ajouter ligne Total
    total_row = pd.Series({
        'Événements': int(dfm['Événements'].sum()),
        'Inscrits': int(dfm['Inscrits'].sum()),
        'Participants': int(dfm['Participants'].sum()),
        'Total': int(dfm['Total'].sum())
    }, name='Total')
    dfm = pd.concat([dfm, total_row.to_frame().T])
    return dfm

# Rendu des tableaux recentrés
pad_l, center_table, pad_r = st.columns([1, 2, 1])
with center_table:
    # Bloc single/multi avec dataframes et boutons
    if len(types_selection) == 1:
        st.markdown(f"**{types_selection[0]}**")
        table_single = monthly_single_table(events_filtres, invitees_filtres, participants_reel_filtres, 'start_time')
        if not table_single.empty:
            st.dataframe(table_single, use_container_width=True)
            csv_single = table_single.to_csv(index=True).encode('utf-8')
            st.download_button(
                label="Exporter CSV",
                data=csv_single,
                file_name="focus_single_event.csv",
                mime="text/csv"
            )
        else:
            st.info("Aucune donnée disponible pour la période et l'événement sélectionnés.")
    else:
        st.markdown("**Tableaux par type d'événement**")
        st.markdown("##### Événements")
        table_events = monthly_table(events_filtres, 'start_time', 'type')
        if not table_events.empty:
            st.dataframe(table_events, use_container_width=True)
            csv_events = table_events.to_csv(index=True).encode('utf-8')
            st.download_button(
                label="Exporter CSV événements",
                data=csv_events,
                file_name="focus_events.csv",
                mime="text/csv"
            )
        else:
            st.info("Aucun événement sur la période sélectionnée.")

        st.markdown("##### Inscrits")
        table_inscrits = monthly_table(invitees_filtres, 'start_time', 'type')
        if not table_inscrits.empty:
            st.dataframe(table_inscrits, use_container_width=True)
            csv_inscrits = table_inscrits.to_csv(index=True).encode('utf-8')
            st.download_button(
                label="Exporter CSV inscrits",
                data=csv_inscrits,
                file_name="focus_inscrits.csv",
                mime="text/csv"
            )
        else:
            st.info("Aucun inscrit sur la période sélectionnée.")

        st.markdown("##### Participants")
        if 'nb_participants_reel' in participants_reel_filtres.columns:
            table_participants = monthly_table(participants_reel_filtres, 'start_time', 'type', 'nb_participants_reel')
        else:
            table_participants = monthly_table(participants_reel_filtres, 'start_time', 'type')
        if not table_participants.empty:
            st.dataframe(table_participants, use_container_width=True)
            csv_participants = table_participants.to_csv(index=True).encode('utf-8')
            st.download_button(
                label="Exporter CSV participants",
                data=csv_participants,
                file_name="focus_participants.csv",
                mime="text/csv"
            )
        else:
            st.info("Aucun participant sur la période sélectionnée.")

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

