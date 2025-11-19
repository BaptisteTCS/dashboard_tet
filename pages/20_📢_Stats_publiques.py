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

from utils.data import (
    load_df_pap
)

from utils.plots import plot_area_with_totals

st.set_page_config(layout="wide")
st.title("📢 Stats publiques")
st.markdown('---')

# === FONCTIONS DE CHARGEMENT AVEC CACHE ===

@st.cache_data(ttl=3600)  # Cache pendant 1 heure
def load_collectivites_actives():
    """Charge les collectivités actives depuis la base de données"""
    engine_prod = get_engine_prod()
    with engine_prod.connect() as conn:
        df = pd.read_sql_query(
            text("""
            select * 
            from collectivite
            where id in (
                select distinct collectivite_id
                from private_collectivite_membre)
            """),
            conn
        )
    return df

@st.cache_data(ttl=3600)
def load_collectivites():
    """Charge toutes les collectivités depuis la base de données"""
    engine_prod = get_engine_prod()
    with engine_prod.connect() as conn:
        df = pd.read_sql_query(
            text("""
            select * 
            from collectivite
            """),
            conn
        )
    return df

@st.cache_data(ttl=3600)
def load_collectivite_carte_identite():
    """Charge les cartes d'identité des collectivités"""
    engine_prod = get_engine_prod()
    with engine_prod.connect() as conn:
        df = pd.read_sql_query(
            text("""
            select * 
            from collectivite_carte_identite
            """),
            conn
        )
    return df

@st.cache_data(ttl=3600)
def load_users():
    """Charge les utilisateurs depuis la base de données"""
    engine_prod = get_engine_prod()
    with engine_prod.connect() as conn:
        df = pd.read_sql_query(
            text("""
            select id, email_confirmed_at
            from auth.users
            where id in (select user_id from public.private_collectivite_membre)
            """),
            conn
        )
    # Convertir la colonne de date en datetime
    df['email_confirmed_at'] = pd.to_datetime(df['email_confirmed_at'])
    return df

@st.cache_data(ttl=3600)
def load_pap_12_mois():
    """Charge les plans d'action par mois"""
    df = read_table('pap_12_mois_statut')
    return df

@st.cache_data(ttl=3600)
def load_user_actif_mois():
    """Charge les utilisateurs actifs par mois"""
    df = read_table('user_actif_mois')
    # Convertir la colonne de date en datetime
    df['mois'] = pd.to_datetime(df['mois'])
    return df

@st.cache_data(ttl=3600)
def load_plans_action():
    """Charge les plans d'action"""
    return load_df_pap()

@st.cache_data(ttl=3600)
def load_evolution_fa():
    return read_table('evolution_typologie_fa')

# === Définitions des thèmes ===

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


# === CHARGEMENT DES DONNÉES ===

df_collectivites_actives = load_collectivites_actives()
df_collectivites = load_collectivites()
df_cci = load_collectivite_carte_identite()
df_users = load_users()
df_user_actif = load_user_actif_mois()
df_pap = load_plans_action()
df_pap_12_mois = load_pap_12_mois()
evolution_fa = load_evolution_fa()

st.markdown("### Quelques stats impactantes")

# === Metrics ===

nature_to_categorie = {
    "CC": "EPCI à fiscalité propre",
    "CA": "EPCI à fiscalité propre",
    "CU": "EPCI à fiscalité propre",
    "METRO": "EPCI à fiscalité propre",
    "EPT": "EPCI à fiscalité propre",

    "SIVU": "Syndicats, PETR, pôles métropolitains et autres",
    "SIVOM": "Syndicats, PETR, pôles métropolitains et autres",
    "SMF": "Syndicats, PETR, pôles métropolitains et autres",
    "SMO": "Syndicats, PETR, pôles métropolitains et autres",
    "PETR": "Syndicats, PETR, pôles métropolitains et autres",
    "POLEM": "Syndicats, PETR, pôles métropolitains et autres",
    None: "Syndicats, PETR, pôles métropolitains et autres"
}

df_collectivites_actives['categorie'] = df_collectivites_actives['nature_insee'].map(nature_to_categorie)
df_collectivites['categorie'] = df_collectivites['nature_insee'].map(nature_to_categorie)

nb_epci = df_collectivites_actives[(df_collectivites_actives.type == 'epci') & (df_collectivites_actives.categorie == 'EPCI à fiscalité propre')].shape[0]
nb_commune = df_collectivites_actives[df_collectivites_actives.type == 'commune'].shape[0]
nb_reg_et_dep = df_collectivites_actives[df_collectivites_actives.type.isin(['region', 'departement'])].shape[0]
nb_autres = df_collectivites_actives[(df_collectivites_actives.type == 'epci') & (df_collectivites_actives.categorie == 'Syndicats, PETR, pôles métropolitains et autres')].shape[0]

cols = st.columns(2)
with cols[0]:
    col1, col2 = st.columns(2)
    with col1:
        st.metric("EPCI à fiscalité propre", nb_epci)
        st.metric("Communes", nb_commune)
    with col2:
        st.metric("Régions et départements", nb_reg_et_dep)
        st.metric("Syndicats, PETR et autres", nb_autres)

# === Trackers ===

with cols[1]:
    st.markdown("Tracker EPCI à fiscalité propre")
    df_collectivites_actives['active'] = True

    df_collectivites_epci_fiscalite_propre = df_collectivites[(df_collectivites.type == 'epci') & (df_collectivites.categorie == 'EPCI à fiscalité propre')]

    ct_pap = df_pap[['collectivite_id', 'passage_pap']].groupby('collectivite_id').min().reset_index()

    df_final = df_collectivites_epci_fiscalite_propre.merge(df_collectivites_actives[['id', 'active']], on='id', how='left') \
        .merge(ct_pap, left_on='id', right_on='collectivite_id', how='left')    

    # EPCI avec profil et plan d'action actif
    nb_avec_pap = df_final[df_final['passage_pap'].notna()].shape[0]
    nb_avec_profil = df_final[(df_final['active'].notna()) & (df_final['passage_pap'].isna())].shape[0]
    nb_sans_profil = df_final[df_final['active'].isna()].shape[0]

    # Total pour vérification
    total_epci = df_final.shape[0]

    # === Visualisation matricielle avec matplotlib ===

    # Paramètres de la matrice
    rows, cols = 10, 12
    total_cells = rows * cols

    # Calculer les proportions
    prop_avec_pap = nb_avec_pap / total_epci
    prop_avec_profil = nb_avec_profil / total_epci
    prop_sans_profil = nb_sans_profil / total_epci

    # Nombre de cellules pour chaque catégorie
    cells_avec_pap = int(np.round(prop_avec_pap * total_cells))
    cells_avec_profil = int(np.round(prop_avec_profil * total_cells))
    cells_sans_profil = total_cells - cells_avec_pap - cells_avec_profil  # Pour garantir exactement 120 cellules

    # Créer le tableau de couleurs
    # Vert pour avec PAP, Orange pour avec profil, Rouge pour sans profil
    colors_array = np.zeros((rows, cols, 3))

    # Définir les couleurs RGB (normalisées entre 0 et 1)
    color_vert = np.array([0.063, 0.725, 0.506])  # #10b981
    color_orange = np.array([0.961, 0.620, 0.043])  # #f59e0b
    color_rouge = np.array([0.937, 0.267, 0.267])  # #ef4444

    # Remplir le tableau avec les couleurs appropriées
    cell_index = 0
    for i in range(rows):
        for j in range(cols):
            if cell_index < cells_avec_pap:
                colors_array[i, j] = color_vert
            elif cell_index < cells_avec_pap + cells_avec_profil:
                colors_array[i, j] = color_orange
            else:
                colors_array[i, j] = color_rouge
            cell_index += 1

    # Créer la figure
    fig, ax = plt.subplots(figsize=(4, 2))

    # Fond transparent
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)

    # Afficher la matrice
    ax.imshow(colors_array, aspect='equal')

    # Retirer les axes
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Ajouter une grille subtile
    for i in range(rows + 1):
        ax.axhline(i - 0.5, color='white', linewidth=0.8)
    for j in range(cols + 1):
        ax.axvline(j - 0.5, color='white', linewidth=0.8)

    # Créer une légende personnalisée
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=color_vert, label='Avec profil et plan d\'action actif'),
        Patch(facecolor=color_orange, label='Avec profil uniquement'),
        Patch(facecolor=color_rouge, label='Sans profil')
    ]
    ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.02), 
            ncol=3, frameon=False, fontsize=4)

    plt.tight_layout()

    # Afficher dans Streamlit
    st.pyplot(fig, transparent=True, width="content")

st.markdown("---")
st.markdown('### Un développement national')

with st.container(border=True):
    st.selectbox("Sélectionnez une région", options=df_cci['region_name'].unique())
    st.selectbox("Sélectionnez un département", options=df_cci['departement_name'].unique())

st.markdown("Imaginer la carte de France ou region ou département sélectionné ici")

st.markdown("---")

st.markdown("### Des stats utilisateurs")

# Calculer la date d'il y a 12 mois
date_12_mois = datetime.now(timezone.utc) - relativedelta(months=12)
# Pour df_user_actif, on prend le premier du mois d'il y a 12 mois
debut_mois_12_mois = date_12_mois.replace(day=1)

# S'assurer que 'mois' est de type datetime64[ns, UTC], pour comparaison correcte
if df_user_actif['mois'].dt.tz is not None:
    filtre = df_user_actif['mois'] >= pd.Timestamp(debut_mois_12_mois)
else:
    filtre = df_user_actif['mois'] >= pd.Timestamp(debut_mois_12_mois).replace(tzinfo=None)

cols_users = st.columns(2)
with cols_users[0]: 
    st.markdown("#### Sur les 12 derniers mois :")
    cols_users_metrics = st.columns(2)
    with cols_users_metrics[0]: 
        st.metric("Nombre d'utilisateurs actifs", df_user_actif[filtre]['email'].nunique())
    with cols_users_metrics[1]:
        st.metric("Nombre d'utilisateurs qui nous ont rejoints", df_users[df_users['email_confirmed_at'] >= date_12_mois]['id'].nunique())
with cols_users[1]:
    # Chart Nivo - Pie chart utilisateurs actifs par collectivité
    
    # Grouper par collectivité et compter les emails uniques
    users_par_collectivite = df_user_actif[filtre].groupby('collectivite_id')['email'].nunique().reset_index()
    users_par_collectivite.columns = ['collectivite_id', 'nb_users']

    users_par_collectivite = users_par_collectivite[users_par_collectivite.collectivite_id.isin(ct_pap['collectivite_id'])].copy()
    
    # Créer les tranches
    def categoriser_users(nb):
        if nb <= 2:
            return "1-2"
        elif 3 <= nb <= 5:
            return "3-5"
        elif 6 <= nb <= 20:
            return "6-20"
        else:
            return ">20"
    
    users_par_collectivite['tranche'] = users_par_collectivite['nb_users'].apply(categoriser_users)
    
    # Compter le nombre de collectivités par tranche
    tranches_count = users_par_collectivite.groupby('tranche').size().reset_index(name='count')
    
    # Définir l'ordre des tranches pour le graphique
    ordre_tranches = [
        "1-2",
        "3-5",
        "6-20",
        ">20"
    ]
    
    # S'assurer que toutes les tranches sont présentes (même avec count=0)
    tranches_count = tranches_count.set_index('tranche').reindex(ordre_tranches, fill_value=0).reset_index()
    tranches_count.columns = ['tranche', 'count']
    
    # Préparer les données pour Nivo
    pie_data = [
        {"id": row['tranche'], "label": row['tranche'], "value": row['count']}
        for _, row in tranches_count.iterrows() if row['count'] > 0
    ]
    
    st.markdown("**Utilisateurs actifs par collectivités ayant un plan d'action actif**")
    
    # Afficher le pie chart avec Nivo
    with elements("pie_users_collectivite"):
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
    
st.markdown("---")
st.markdown("### Des stats sur les plans d'actions et actions")

# Filtrer pour les plans d'action actifs
df_pap_actif = df_pap_12_mois[df_pap_12_mois['statut'] == 'actif'].copy()

# Compter le nombre de PAP actifs par mois
pap_evolution = df_pap_actif.groupby('mois').size().reset_index(name='count')

# Convertir en format datetime si nécessaire
if not pd.api.types.is_datetime64_any_dtype(pap_evolution['mois']):
    pap_evolution['mois'] = pd.to_datetime(pap_evolution['mois'])

# Trier par mois
pap_evolution = pap_evolution.sort_values('mois')

date_18_mois = datetime.now(timezone.utc) - relativedelta(months=18)

# S'assurer que 'mois' est de type datetime64[ns, UTC], pour comparaison correcte
if pap_evolution['mois'].dt.tz is not None:
    filtre = pap_evolution['mois'] >= pd.Timestamp(debut_mois_12_mois)
else:
    filtre = pap_evolution['mois'] >= pd.Timestamp(debut_mois_12_mois).replace(tzinfo=None)

pap_evolution_18_mois = pap_evolution[filtre].copy()

# Formater les données pour Nivo Area
area_data = [
    {
        "id": "Plans d'actions actifs",
        "data": [
            {"x": row['mois'].strftime('%Y-%m'), "y": row['count']}
            for _, row in pap_evolution_18_mois.iterrows()
        ]
    }
]

cols_pap = st.columns(2)
with cols_pap[0]:
    st.markdown("Evolution des PAP actifs (12 mois)")
    # Afficher le graphique Area avec Nivo
    with elements("area_pap_evolution"):
        with mui.Box(sx={"height": 500}):
            nivo.Line(
                data=area_data,
                margin={"top": 20, "right": 30, "bottom": 50, "left": 60},
                xScale={"type": "point"},
                yScale={"type": "linear", "min": "auto", "max": "auto", "stacked": False, "reverse": False},
                curve="monotoneX",
                axisTop=None,
                axisRight=None,
                axisBottom={
                    "tickSize": 5,
                    "tickPadding": 5,
                    "tickRotation": -45,
                    "legend": "",
                    "legendOffset": 45,
                    "legendPosition": "middle"
                },
                axisLeft={
                    "tickSize": 5,
                    "tickPadding": 5,
                    "tickRotation": 0,
                    "legend": "",
                    "legendOffset": -50,
                    "legendPosition": "middle"
                },
                enableArea=True,
                areaOpacity=0.3,
                enablePoints=True,
                pointSize=6,
                pointColor={"theme": "background"},
                pointBorderWidth=2,
                pointBorderColor={"from": "serieColor"},
                useMesh=True,
                enableSlices="x",
                legends=[],
                colors={"scheme": "pastel2"},
                theme=theme_actif,
                enableGridX=False,
                enableGridY=False
            )

with cols_pap[1]:
    st.markdown("Evolution des fiches actions pilotables")
    # S'assurer que 'mois' est de type datetime64[ns, UTC], pour comparaison correcte
    if evolution_fa['modified_at'].dt.tz is not None:
        filtre = evolution_fa['modified_at'] >= pd.Timestamp(debut_mois_12_mois)
    else:
        filtre = evolution_fa['modified_at'] >= pd.Timestamp(debut_mois_12_mois).replace(tzinfo=None)

    evolution_fa_18_mois = evolution_fa[filtre].copy()

    # Extraire le mois de modified_at
    evolution_fa_18_mois['mois'] = evolution_fa_18_mois['modified_at'].dt.to_period('M')

    # Grouper par mois et compter le nombre de lignes
    evolution_fa_par_mois = evolution_fa_18_mois.groupby('mois').size().reset_index(name='count')

    # Calculer la somme cumulative
    evolution_fa_par_mois['cumsum'] = evolution_fa_par_mois['count'].cumsum()

    # Convertir le mois en format datetime pour l'affichage
    evolution_fa_par_mois['mois_str'] = evolution_fa_par_mois['mois'].astype(str)

    # Formater les données pour Nivo Area
    area_data_fa = [
        {
            "id": "Fiches actions pilotables",
            "data": [
                {"x": row['mois_str'], "y": row['cumsum']}
                for _, row in evolution_fa_par_mois.iterrows()
            ]
        }
    ]

    # Afficher le graphique Area avec Nivo
    with elements("area_fa_evolution"):
        with mui.Box(sx={"height": 500}):
            nivo.Line(
                data=area_data_fa,
                margin={"top": 20, "right": 30, "bottom": 50, "left": 60},
                xScale={"type": "point"},
                yScale={"type": "linear", "min": "auto", "max": "auto", "stacked": False, "reverse": False},
                curve="monotoneX",
                axisTop=None,
                axisRight=None,
                axisBottom={
                    "tickSize": 5,
                    "tickPadding": 5,
                    "tickRotation": -45,
                    "legend": "",
                    "legendOffset": 45,
                    "legendPosition": "middle"
                },
                axisLeft={
                    "tickSize": 5,
                    "tickPadding": 5,
                    "tickRotation": 0,
                    "legend": "",
                    "legendOffset": -50,
                    "legendPosition": "middle"
                },
                enableArea=True,
                areaOpacity=0.3,
                enablePoints=True,
                pointSize=6,
                pointColor={"theme": "background"},
                pointBorderWidth=2,
                pointBorderColor={"from": "serieColor"},
                useMesh=True,
                enableSlices="x",
                legends=[],
                colors={"scheme": "pastel1"},
                theme=theme_actif,
                enableGridX=False,
                enableGridY=False
            )