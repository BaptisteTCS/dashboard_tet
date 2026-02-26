import streamlit as st

st.set_page_config(
    page_title="Dashboard Produit",
    page_icon="🚀",
    layout="wide"
)

import json
import pandas as pd
import plotly.graph_objects as go
from sqlalchemy import text
from utils.db import read_table, get_engine_prod

CATEGORY10_COLORS = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
    '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
    '#bcbd22', '#17becf'
]

PLOTLY_LAYOUT = {
    'font': {'family': 'Source Sans Pro, sans-serif', 'size': 13, 'color': '#31333F'},
    'hovermode': 'x unified',
    'plot_bgcolor': 'white',
    'paper_bgcolor': 'white',
}

# ==========================
# Chargement des données
# ==========================

@st.cache_resource(ttl="2d")
def load_data():
    engine_prod = get_engine_prod()
    feature = read_table('feature')
    airtable = read_table('airtable_sync')
    pcm = pd.read_sql_query(
        text("SELECT pcm.*, u.email FROM private_collectivite_membre pcm JOIN auth.users u ON pcm.user_id = u.id"),
        engine_prod
    )
    return feature, airtable, pcm

feature_df, airtable_df, pcm_df = load_data()

# Exclure les collectivités de type 'test'
test_ids = airtable_df.loc[airtable_df['type'] == 'test', 'collectivite_id']
feature_df = feature_df[~feature_df['collectivite_id'].isin(test_ids)].copy()

feature_df['datetime'] = pd.to_datetime(feature_df['datetime'])


def parse_sub_feature(val):
    if isinstance(val, dict):
        return val
    if isinstance(val, str):
        try:
            return json.loads(val)
        except (json.JSONDecodeError, TypeError):
            return {}
    return {}


feature_df['sub_feature_parsed'] = feature_df['sub-feature'].apply(parse_sub_feature)

FEATURE_DOCS = {
    ("Bandeau incitation à la complétude", "Total"): "Nombre de fois où le CTA du bandeau d'incitation à la complétude a été cliqué.",
    ("Bandeau incitation à la complétude", "Bandeau"): "Breakdown par type de bandeau affiché.",
    ("Exporter une sauvegarde (référentiel)", "Total"): "Nombre d'exports de sauvegarde de référentiel réalisés.",
    ("Exporter une sauvegarde (référentiel)", "Type d'export"): "Breakdown par type d'export.",
    ("Rapport automatique", "Total"): "Nombre de rapports automatiques demandés.",
    ("Rapport automatique", "Type de plan"): "Breakdown par type de plan utilisé pour le rapport.",
    ("Rapport automatique", "Success/Fail"): "Breakdown par résultat de la génération (succès ou échec).",
    ("Rapport automatique", "Retry"): "Breakdown par retry : nouvelle demande sur le même plan moins de 5 min après une première génération. `True` signifique que la tentative est un retry.",
    ("Role contributeur", "Total"): "Nombre de user avec le rôle contributeur.",
    ("Référent plan", "Total"): "Nombre de référents de plan.",
    ("Référent plan", "Réel/Tag"): "Breakdown selon que le référent est un utilisateur réel ou un simple tag.",
    ("Sous actions", "Total"): "Nombre de sous-actions créées.",
    ("Sous actions", "Présence d'un pilote"): "Breakdown selon la présence ou non d'un pilote sur la sous-action.",
}

# ==========================
# Interface
# ==========================

st.title("🚀 Dashboard Produit")

all_features = sorted(feature_df['feature'].dropna().unique().tolist())
if not all_features:
    st.warning("Aucune feature trouvée dans la table.")
    st.stop()

col_feat, col_usage = st.columns([3, 1])

with col_feat:
    selected_feature = st.selectbox("Feature", all_features, index=0)

df = feature_df[feature_df['feature'] == selected_feature].copy()

if df.empty:
    st.info("Aucune donnée pour cette feature.")
    st.stop()

# Extraire les clés du dictionnaire sub-feature
sample_dict = df['sub_feature_parsed'].iloc[0]
sub_feature_keys = list(sample_dict.keys()) if isinstance(sample_dict, dict) else []
sub_feature_options = ["Total"] + sub_feature_keys

with col_usage:
    selected_sub_feature = st.selectbox("Usage", sub_feature_options, index=0)

doc_text = FEATURE_DOCS.get((selected_feature, selected_sub_feature))
if doc_text:
    st.caption(doc_text)

col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1.5])

with col1:
    metric = st.selectbox("Métrique", ["Total count", "Unique users", "Unique collectivité"])

with col2:
    EXCLUSION_OPTIONS = [
        "Type : epci",
        "Type : departement",
        "Type : region",
        "Type : commune",
        "Fonction : conseiller",
        "Fonction : partenaire",
        "Fonction : politique",
        "Fonction : technique",
        "PAP : actif",
        "PAP : inactif",
        "PAP : pas de PAP",
    ]
    selected_exclusions = st.multiselect("Filters", EXCLUSION_OPTIONS)

with col3:
    granularity = st.segmented_control(
        "Granularité",
        options=["day", "week", "month"],
        default="week",
    )

with col4:
    chart_type = st.selectbox("Type de graphe", [
        "Evolution : line chart",
        "Evolution : bar chart",
        "Total : Number",
        "Total : Pie chart",
        "Total : Liste",
    ])

with col5:
    breakdown_options = {
        "PAP actif/inactif": "statut",
        "Type de collectivité": "type",
        "Fonction": "fonction",
    }
    selected_breakdowns = st.multiselect("Breakdowns", list(breakdown_options.keys()))

# ==========================
# Pipeline d'agrégation
# ==========================

if not granularity:
    granularity = "week"

freq_map = {"day": "D", "week": "W", "month": "MS"}
freq = freq_map[granularity]

working_df = df.copy()

# Déterminer quelles jointures sont nécessaires (exclusions + breakdowns)
need_airtable_type = (
    any(e.startswith("Type : ") for e in selected_exclusions)
    or "Type de collectivité" in selected_breakdowns
)
need_airtable_statut = (
    any(e.startswith("PAP : ") for e in selected_exclusions)
    or "PAP actif/inactif" in selected_breakdowns
)
need_pcm_fonction = (
    any(e.startswith("Fonction : ") for e in selected_exclusions)
    or "Fonction" in selected_breakdowns
)

if need_airtable_type or need_airtable_statut:
    airtable_cols = ['collectivite_id']
    if need_airtable_type:
        airtable_cols.append('type')
    if need_airtable_statut:
        airtable_cols.append('statut')
    airtable_subset = airtable_df[airtable_cols].drop_duplicates(subset=['collectivite_id'])
    working_df = working_df.merge(airtable_subset, on='collectivite_id', how='left')

if need_pcm_fonction:
    pcm_subset = pcm_df[['collectivite_id', 'email', 'fonction']].drop_duplicates(subset=['collectivite_id', 'email'])
    working_df = working_df.merge(pcm_subset, on=['collectivite_id', 'email'], how='left')

# Appliquer les exclusions
for excl in selected_exclusions:
    if excl == "Type : epci":
        working_df = working_df[working_df['type'] != 'epci']
    elif excl == "Type : departement":
        working_df = working_df[working_df['type'] != 'departement']
    elif excl == "Type : region":
        working_df = working_df[working_df['type'] != 'region']
    elif excl == "Type : commune":
        working_df = working_df[working_df['type'] != 'commune']
    elif excl == "Fonction : conseiller":
        working_df = working_df[working_df['fonction'] != 'conseiller']
    elif excl == "Fonction : partenaire":
        working_df = working_df[working_df['fonction'] != 'partenaire']
    elif excl == "Fonction : politique":
        working_df = working_df[working_df['fonction'] != 'politique']
    elif excl == "Fonction : technique":
        working_df = working_df[working_df['fonction'] != 'technique']
    elif excl == "PAP : actif":
        working_df = working_df[working_df['statut'] != 'actif']
    elif excl == "PAP : inactif":
        working_df = working_df[working_df['statut'] != 'inactif']
    elif excl == "PAP : pas de PAP":
        working_df = working_df[working_df['statut'].notna()]

# Construction de la colonne de breakdown composite
breakdown_cols = []

if selected_sub_feature != "Total":
    working_df['_sf_val'] = working_df['sub_feature_parsed'].apply(
        lambda d: str(d.get(selected_sub_feature, 'N/A')) if isinstance(d, dict) else 'N/A'
    )
    breakdown_cols.append('_sf_val')

for label in selected_breakdowns:
    col_name = breakdown_options[label]
    if col_name == 'statut':
        working_df[col_name] = working_df[col_name].fillna('non PAP').astype(str)
        working_df.loc[working_df[col_name].isin(['', 'None', 'nan']), col_name] = 'non PAP'
    elif col_name == 'fonction':
        working_df[col_name] = working_df[col_name].fillna('Non renseigné').astype(str)
        working_df.loc[working_df[col_name].isin(['', 'None', 'nan']), col_name] = 'Non renseigné'
    else:
        working_df[col_name] = working_df[col_name].fillna('N/A').astype(str)
    breakdown_cols.append(col_name)

if breakdown_cols:
    if len(breakdown_cols) == 1:
        working_df['_group'] = working_df[breakdown_cols[0]]
    else:
        working_df['_group'] = working_df[breakdown_cols].apply(lambda row: ' | '.join(row), axis=1)
else:
    working_df['_group'] = 'Total'

working_df['_period'] = working_df['datetime'].dt.to_period(
    {'D': 'D', 'W': 'W', 'MS': 'M'}[freq]
)


def aggregate(group_df, metric_name):
    if metric_name == "Total count":
        return len(group_df)
    elif metric_name == "Unique users":
        return group_df['email'].nunique()
    elif metric_name == "Unique collectivité":
        return group_df['collectivite_id'].nunique()
    return 0


is_evolution = chart_type.startswith("Evolution")

if is_evolution:
    agg_df = (
        working_df
        .groupby(['_period', '_group'])
        .apply(lambda g: aggregate(g, metric), include_groups=False)
        .reset_index(name='value')
    )
    agg_df['date'] = agg_df['_period'].dt.to_timestamp()
    agg_df = agg_df.sort_values('date')
else:
    agg_df = (
        working_df
        .groupby('_group')
        .apply(lambda g: aggregate(g, metric), include_groups=False)
        .reset_index(name='value')
    )

# ==========================
# Rendu du graphe
# ==========================

groups = sorted(agg_df['_group'].unique().tolist())
colors = CATEGORY10_COLORS

if chart_type == "Evolution : line chart":
    fig = go.Figure()
    for idx, grp in enumerate(groups):
        grp_data = agg_df[agg_df['_group'] == grp]
        fig.add_trace(go.Scatter(
            x=grp_data['date'],
            y=grp_data['value'],
            mode='lines+markers',
            name=str(grp),
            line=dict(color=colors[idx % len(colors)], width=2),
            marker=dict(size=5),
        ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=500,
        xaxis=dict(
            title="Date",
            showgrid=True,
            gridcolor='rgba(128,128,128,0.2)',
        ),
        yaxis=dict(
            title=metric,
            showgrid=True,
            gridcolor='rgba(128,128,128,0.2)',
            rangemode='tozero',
        ),
        legend=dict(
            yanchor="top", y=0.99,
            xanchor="left", x=1.01,
            bgcolor='rgba(255,255,255,0.8)',
        ),
        margin=dict(l=60, r=140, t=20, b=60),
    )
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Evolution : bar chart":
    fig = go.Figure()
    for idx, grp in enumerate(groups):
        grp_data = agg_df[agg_df['_group'] == grp]
        fig.add_trace(go.Bar(
            x=grp_data['date'],
            y=grp_data['value'],
            name=str(grp),
            marker_color=colors[idx % len(colors)],
        ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        barmode='group',
        height=500,
        xaxis=dict(
            title="Date",
            showgrid=True,
            gridcolor='rgba(128,128,128,0.2)',
        ),
        yaxis=dict(
            title=metric,
            showgrid=True,
            gridcolor='rgba(128,128,128,0.2)',
            rangemode='tozero',
        ),
        legend=dict(
            yanchor="top", y=0.99,
            xanchor="left", x=1.01,
            bgcolor='rgba(255,255,255,0.8)',
        ),
        margin=dict(l=60, r=140, t=20, b=60),
    )
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Total : Number":
    cols = st.columns(min(len(groups), 6))
    for idx, grp in enumerate(groups):
        val = int(agg_df[agg_df['_group'] == grp]['value'].sum())
        with cols[idx % len(cols)]:
            st.metric(label=str(grp), value=f"{val:,}".replace(",", " "))

elif chart_type == "Total : Pie chart":
    fig = go.Figure(data=[go.Pie(
        labels=agg_df['_group'].tolist(),
        values=agg_df['value'].tolist(),
        marker=dict(colors=colors[:len(groups)]),
        textinfo='label+percent+value',
    )])
    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=500,
        margin=dict(l=40, r=40, t=20, b=40),
    )
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Total : Liste":
    display_cols = ['datetime', 'collectivite_id', 'email']
    if selected_sub_feature != "Total":
        working_df['_sf_display'] = working_df['sub_feature_parsed'].apply(
            lambda d: str(d.get(selected_sub_feature, '')) if isinstance(d, dict) else ''
        )
        display_cols.append('_sf_display')
    for label in selected_breakdowns:
        col_name = breakdown_options[label]
        if col_name in working_df.columns and col_name not in display_cols:
            display_cols.append(col_name)
    rename_map = {'_sf_display': selected_sub_feature}
    st.info("Vous pouvez trier les colonnes en cliquant sur leur en-tête et télécharger les données via l'icône en haut à droite du tableau.")
    st.dataframe(
        working_df[display_cols].rename(columns=rename_map).sort_values('datetime', ascending=False),
        use_container_width=True,
        hide_index=True,
    )
