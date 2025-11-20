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

st.set_page_config(layout="wide")
st.title("📢 Stats publiques")
st.markdown('---')

# === FONCTIONS DE CHARGEMENT AVEC CACHE ===

@st.cache_data(ttl=3600)  # Cache pendant 1 heure
def load_data_from_engine_prod():
    """Charge toutes les données depuis engine_prod en une seule connexion pour optimiser les performances"""
    engine_prod = get_engine_prod()
    
    with engine_prod.connect() as conn:
        # Toutes les requêtes vers la base prod en une seule connexion
        df_collectivites_actives = pd.read_sql_query(
            text("""
                SELECT * 
                FROM collectivite
                WHERE id IN (
                    SELECT DISTINCT collectivite_id
                    FROM private_collectivite_membre
                )
            """),
            conn
        )
        
        df_collectivites = pd.read_sql_query(
            text("""
                SELECT * 
                FROM collectivite
            """),
            conn
        )
        
        df_cci = pd.read_sql_query(
            text("""
                SELECT * 
                FROM collectivite_carte_identite
            """),
            conn
        )
        
        df_users = pd.read_sql_query(
            text("""
                SELECT id, email_confirmed_at
                FROM auth.users
                WHERE id IN (SELECT user_id FROM public.private_collectivite_membre)
            """),
            conn
        )
        
        df_labellisation = pd.read_sql_query(
            text("""
                SELECT * 
                FROM labellisation
            """),
            conn
        )
    
    # Post-traitement des dates
    df_users['email_confirmed_at'] = pd.to_datetime(df_users['email_confirmed_at'])
    
    return {
        'collectivites_actives': df_collectivites_actives,
        'collectivites': df_collectivites,
        'cci': df_cci,
        'users': df_users,
        'labellisation': df_labellisation,
    }

# Fonctions individuelles qui utilisent engine_prod (regroupées)
@st.cache_data(ttl=3600)
def load_collectivites_actives():
    """Charge les collectivités actives depuis la base de données"""
    return load_data_from_engine_prod()['collectivites_actives']

@st.cache_data(ttl=3600)
def load_collectivites():
    """Charge toutes les collectivités depuis la base de données"""
    return load_data_from_engine_prod()['collectivites']

@st.cache_data(ttl=3600)
def load_collectivite_carte_identite():
    """Charge les cartes d'identité des collectivités"""
    return load_data_from_engine_prod()['cci']

@st.cache_data(ttl=3600)
def load_users():
    """Charge les utilisateurs depuis la base de données"""
    return load_data_from_engine_prod()['users']

@st.cache_data(ttl=3600)
def load_labellisation():
    """Charge les labellisations depuis la base de données"""
    return load_data_from_engine_prod()['labellisation']

# Fonctions qui utilisent read_table (base différente, non optimisées)
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

@st.cache_data(ttl=3600)
def load_evolution_ind_od():
    return read_table('evolution_ind_od')

@st.cache_data(ttl=3600)
def load_evolution_ind_pers():
    return read_table('evolution_ind_pers')
# === CHARGEMENT DES DONNÉES ===

# Chargement optimisé : toutes les données depuis engine_prod en une seule connexion
data_prod = load_data_from_engine_prod()

df_collectivites_actives = data_prod['collectivites_actives']
df_collectivites = data_prod['collectivites']
df_cci = data_prod['cci']
df_users = data_prod['users']
df_labellisation = data_prod['labellisation']

# Chargement des données depuis read_table (base différente)
df_user_actif = load_user_actif_mois()
df_pap = load_plans_action()
df_pap_12_mois = load_pap_12_mois()
evolution_fa = load_evolution_fa()
evolution_ind_od = load_evolution_ind_od()
evolution_ind_pers = load_evolution_ind_pers()


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
    st.markdown("Territoires en Transitions c'est autant de collectivités avec un profil :")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("EPCI à fiscalité propre", nb_epci)
        st.metric("Communes", nb_commune)
    with col2:
        st.metric("Régions et départements", nb_reg_et_dep)
        st.metric("Syndicats, PETR et autres", nb_autres)

# === Trackers ===

with cols[1]:
    st.markdown("Et parmis les EPCI à fiscalité propre :")
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
        Patch(facecolor=color_orange, label='Avec profil'),
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

st.markdown("Imaginer la carte de France ou region ou département sélectionné ici.")
st.markdown("La selection ne fait rien sur ce prototype.")

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
    st.markdown("Sur les 12 derniers mois nous comptons :")
    delta=df_users[df_users['email_confirmed_at'] >= date_12_mois]['id'].nunique()
    st.metric("Utilisateurs actifs", df_user_actif[filtre]['email'].nunique(), delta=delta)
with cols_users[1]:
    # Chart Nivo - Pie chart utilisateurs actifs par collectivité
    st.markdown("Les collectivités qui pilotent un plan le font à plusieurs :")
    
    # Grouper par collectivité et compter les emails uniques
    users_par_collectivite = df_user_actif[filtre].groupby('collectivite_id')['email'].nunique().reset_index()
    users_par_collectivite.columns = ['collectivite_id', 'nb_users']

    users_par_collectivite = users_par_collectivite[users_par_collectivite.collectivite_id.isin(ct_pap['collectivite_id'])].copy()
    
    # Créer les tranches
    def categoriser_users(nb):
        if nb <= 2:
            return "1-2 utilisateurs"
        elif 3 <= nb <= 5:
            return "3-5 utilisateurs"
        elif 6 <= nb <= 20:
            return "6-20 utilisateurs"
        else:
            return ">20 utilisateurs"
    
    users_par_collectivite['tranche'] = users_par_collectivite['nb_users'].apply(categoriser_users)
    
    # Compter le nombre de collectivités par tranche
    tranches_count = users_par_collectivite.groupby('tranche').size().reset_index(name='count')
    
    # Définir l'ordre des tranches pour le graphique
    ordre_tranches = [
        "1-2 utilisateurs",
        "3-5 utilisateurs",
        "6-20 utilisateurs",
        ">20 utilisateurs"
    ]
    
    # S'assurer que toutes les tranches sont présentes (même avec count=0)
    tranches_count = tranches_count.set_index('tranche').reindex(ordre_tranches, fill_value=0).reset_index()
    tranches_count.columns = ['tranche', 'count']
    
    # Préparer les données pour Nivo
    pie_data = [
        {"id": row['tranche'], "label": row['tranche'], "value": row['count']}
        for _, row in tranches_count.iterrows() if row['count'] > 0
    ]
    
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
                colors={"scheme": "yellow_orange_red"},
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
    filtre = pap_evolution['mois'] >= pd.Timestamp(date_18_mois)
else:
    filtre = pap_evolution['mois'] >= pd.Timestamp(date_18_mois).replace(tzinfo=None)

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
    st.markdown("Evolution des plans d'actions pilotables actifs (12 mois) :")
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
                enableGridY=True
            )

with cols_pap[1]:
    st.markdown("Evolution des fiches actions pilotables")
    # S'assurer que 'mois' est de type datetime64[ns, UTC], pour comparaison correcte
    if evolution_fa['modified_at'].dt.tz is not None:
        filtre = evolution_fa['modified_at'] >= pd.Timestamp(date_18_mois)
    else:
        filtre = evolution_fa['modified_at'] >= pd.Timestamp(date_18_mois).replace(tzinfo=None)

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
                colors={"scheme": "nivo"},
                theme=theme_actif,
                enableGridX=False,
                enableGridY=True
            )

st.markdown("---")
st.markdown("### Des stats sur les indicateurs")

if evolution_ind_od['mois'].dt.tz is not None:
    filtre = evolution_ind_od['mois'] >= pd.Timestamp(date_18_mois)
else:
    filtre = evolution_ind_od['mois'] >= pd.Timestamp(date_18_mois).replace(tzinfo=None)

evolution_ind_od_18_mois = evolution_ind_od[filtre].copy()

# Formater les données pour Nivo Area
area_data = [
    {
        "id": "Couples indicateur/collectivité",
        "data": [
            {"x": row['mois'].strftime('%Y-%m'), "y": row['somme']}
            for _, row in evolution_ind_od_18_mois.iterrows()
        ]
    }
]

cols_pap = st.columns(2)
with cols_pap[0]:
    st.markdown("Des indicateurs mis à disposition des collectivités en Open Data :")
    # Afficher le graphique Area avec Nivo
    with elements("area_od_evolution"):
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
                enableGridY=True
            )

with cols_pap[1]:

    if evolution_ind_pers['mois'].dt.tz is not None:
        filtre = evolution_ind_pers['mois'] >= pd.Timestamp(date_18_mois)
    else:
        filtre = evolution_ind_pers['mois'] >= pd.Timestamp(date_18_mois).replace(tzinfo=None)

    evolution_ind_pers_18_mois = evolution_ind_pers[filtre].copy()

    # Formater les données pour Nivo Area
    area_data = [
        {
            "id": "Indicateurs personnalisés",
            "data": [
                {"x": row['mois'].strftime('%Y-%m'), "y": row['somme']}
                for _, row in evolution_ind_pers_18_mois.iterrows()
            ]
        }
    ]

    st.markdown("Des indicateurs personnalisés à foison :")
    # Afficher le graphique Area avec Nivo
    with elements("area_pers_evolution"):
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
                colors={"scheme": "nivo"},
                theme=theme_actif,
                enableGridX=False,
                enableGridY=True
            )

st.markdown("---")

st.markdown("### Des stats sur les labellisations pour finir en beauté")

last_labellisation = df_labellisation.sort_values('obtenue_le').drop_duplicates(subset=['collectivite_id', 'referentiel'], keep='last')

last_labellisation = last_labellisation[last_labellisation['etoiles'] != 0].copy()

cols_label = st.columns(2)

with cols_label[0]:
    st.markdown("Les étoiles CAE")
    
    # Filtrer pour CAE
    cae_data = last_labellisation[last_labellisation['referentiel'] == 'cae']
    
    # Compter la distribution des étoiles
    cae_etoiles = cae_data['etoiles'].value_counts().reset_index()
    cae_etoiles.columns = ['etoiles', 'count']
    cae_etoiles = cae_etoiles.sort_values('etoiles')
    
    # Préparer les données pour Nivo
    pie_data_cae = [
        {"id": f"{int(row['etoiles'])} étoile{'s' if row['etoiles'] > 1 else ''}", 
         "label": f"{int(row['etoiles'])} étoile{'s' if row['etoiles'] > 1 else ''}", 
         "value": int(row['count'])}
        for _, row in cae_etoiles.iterrows()
    ]
    
    # Afficher le pie chart avec Nivo
    with elements("pie_cae_etoiles"):
        with mui.Box(sx={"height": 450}):
            nivo.Pie(
                data=pie_data_cae,
                margin={"top": 40, "right": 80, "bottom": 80, "left": 80},
                innerRadius=0.5,
                padAngle=0.7,
                cornerRadius=3,
                activeOuterRadiusOffset=8,
                borderWidth=1,
                colors={"scheme": "yellow_orange_red"},
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

with cols_label[1]:
    st.markdown("Les étoiles ECI")
    
    # Filtrer pour ECI
    eci_data = last_labellisation[last_labellisation['referentiel'] == 'eci']
    
    # Compter la distribution des étoiles
    eci_etoiles = eci_data['etoiles'].value_counts().reset_index()
    eci_etoiles.columns = ['etoiles', 'count']
    eci_etoiles = eci_etoiles.sort_values('etoiles')
    
    # Préparer les données pour Nivo
    pie_data_eci = [
        {"id": f"{int(row['etoiles'])} étoile{'s' if row['etoiles'] > 1 else ''}", 
         "label": f"{int(row['etoiles'])} étoile{'s' if row['etoiles'] > 1 else ''}", 
         "value": int(row['count'])}
        for _, row in eci_etoiles.iterrows()
    ]
    
    # Afficher le pie chart avec Nivo
    with elements("pie_eci_etoiles"):
        with mui.Box(sx={"height": 450}):
            nivo.Pie(
                data=pie_data_eci,
                margin={"top": 40, "right": 80, "bottom": 80, "left": 80},
                innerRadius=0.5,
                padAngle=0.7,
                cornerRadius=3,
                activeOuterRadiusOffset=8,
                borderWidth=1,
                colors={"scheme": "yellow_orange_red"},
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


# Filtrer uniquement pour CAE
df_cae = df_labellisation[
    (df_labellisation['referentiel'] == 'cae') & 
    (df_labellisation['etoiles'] != 0)
].copy()

# S'assurer que la colonne de date est datetime
df_cae['obtenue_le'] = pd.to_datetime(df_cae['obtenue_le'])

# Créer une plage de mois pour les 18 derniers mois
if df_cae['obtenue_le'].dt.tz is not None:
    date_debut = pd.Timestamp(date_18_mois)
else:
    date_debut = pd.Timestamp(date_18_mois).replace(tzinfo=None)

date_fin = pd.Timestamp(datetime.now(timezone.utc))
if df_cae['obtenue_le'].dt.tz is None:
    date_fin = date_fin.replace(tzinfo=None)

# Générer tous les mois entre date_debut et date_fin
mois_range = pd.date_range(start=date_debut.replace(day=1), end=date_fin, freq='MS')

# Pour chaque mois, calculer le nombre de collectivités par nombre d'étoiles
evolution_etoiles = []

for mois in mois_range:
    # Pour ce mois, prendre la dernière labellisation de chaque collectivité jusqu'à cette date
    df_jusqu_au_mois = df_cae[df_cae['obtenue_le'] <= mois]
    
    if len(df_jusqu_au_mois) > 0:
        # Garder seulement la dernière labellisation par collectivité
        derniere_label_par_collectivite = df_jusqu_au_mois.sort_values('obtenue_le').groupby('collectivite_id').last()
        
        # Compter le nombre de collectivités par nombre d'étoiles
        comptage_etoiles = derniere_label_par_collectivite['etoiles'].value_counts().to_dict()
        
        # Ajouter les résultats
        for nb_etoiles in [1, 2, 3, 4, 5]:
            evolution_etoiles.append({
                'mois': mois.strftime('%Y-%m'),
                'etoiles': nb_etoiles,
                'count': comptage_etoiles.get(nb_etoiles, 0)
            })

# Convertir en DataFrame
df_evolution_etoiles = pd.DataFrame(evolution_etoiles)

# Préparer les données pour Nivo Area en format stacked
# Chaque série représente un nombre d'étoiles
area_data_labellisation = []

for nb_etoiles in sorted(df_evolution_etoiles['etoiles'].unique()):
    df_etoile = df_evolution_etoiles[df_evolution_etoiles['etoiles'] == nb_etoiles].sort_values('mois')
    area_data_labellisation.append({
        "id": f"{int(nb_etoiles)} étoile{'s' if nb_etoiles > 1 else ''}",
        "data": [
            {"x": row['mois'], "y": int(row['count'])}
            for _, row in df_etoile.iterrows()
        ]
    })

st.markdown("Évolution du stock de collectivités labellisées CAE (me parait pas super pertinent)")

# Afficher le graphique Area stacked avec Nivo
with elements("area_labellisation_cae"):
    with mui.Box(sx={"height": 500}):
        nivo.Line(
            data=area_data_labellisation,
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
                "legend": "",
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
                    "itemsSpacing": 0,
                    "itemDirection": "left-to-right",
                    "itemWidth": 80,
                    "itemHeight": 20,
                    "itemOpacity": 0.75,
                    "symbolSize": 12,
                    "symbolShape": "circle",
                    "effects": [
                        {
                            "on": "hover",
                            "style": {
                                "itemBackground": "rgba(0, 0, 0, .03)",
                                "itemOpacity": 1
                            }
                        }
                    ]
                }
            ],
            colors={"scheme": "yellow_orange_red"},
            theme=theme_actif,
            enableGridX=False,
            enableGridY=True
        )

st.markdown("Évolution des labellisations")

# Compter le nombre de labellisations par mois (nouvelles labellisations)
df_cae_nouvelles = df_cae.copy()
df_cae_nouvelles['mois'] = df_cae_nouvelles['obtenue_le'].dt.to_period('M').dt.to_timestamp()

# Filtrer pour les 18 derniers mois
if df_cae_nouvelles['mois'].dt.tz is not None:
    filtre_18m = df_cae_nouvelles['mois'] >= pd.Timestamp(date_18_mois)
else:
    filtre_18m = df_cae_nouvelles['mois'] >= pd.Timestamp(date_18_mois).replace(tzinfo=None)

df_cae_nouvelles_18m = df_cae_nouvelles[filtre_18m].copy()

# Compter le nombre de nouvelles labellisations par mois
labellisations_par_mois = df_cae_nouvelles_18m.groupby('mois').size().reset_index(name='count')

# Calculer la somme cumulative
labellisations_par_mois['cumsum'] = labellisations_par_mois['count'].cumsum()

# Si le premier mois n'est pas à 0, ajouter le nombre de labellisations avant
nb_avant = df_cae[df_cae['obtenue_le'] < labellisations_par_mois['mois'].min()].shape[0]
labellisations_par_mois['cumsum'] = labellisations_par_mois['cumsum'] + nb_avant

# Préparer les données pour Nivo Area
area_data_cumsum = [
    {
        "id": "Nombre de labellisations",
        "data": [
            {"x": row['mois'].strftime('%Y-%m'), "y": int(row['cumsum'])}
            for _, row in labellisations_par_mois.iterrows()
        ]
    }
]

# Afficher le graphique Area avec Nivo
with elements("area_labellisation_cumsum"):
    with mui.Box(sx={"height": 500}):
        nivo.Line(
            data=area_data_cumsum,
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
                "legend": "Nombre total de labellisations",
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
            enableGridY=True
        )




