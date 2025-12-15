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

@st.cache_data(ttl=3600)
def load_evolution_ct_activee_mois():
    return read_table('evolution_ct_activee_mois')

@st.cache_data(ttl=3600)
def load_evolution_users_mois():
    return read_table('evolution_users_mois')

@st.cache_data(ttl=3600)
def load_ct_actives():
    return read_table('ct_actives')

# === CHARGEMENT DES DONNÉES ===

# Chargement optimisé : toutes les données depuis engine_prod en une seule connexion
data_prod = load_data_from_engine_prod()

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
df_evolution_ct_activee_mois = load_evolution_ct_activee_mois()
df_evolution_users_mois = load_evolution_users_mois()
df_ct_actives = load_ct_actives()

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

st.markdown("### Territoires en Transitions c'est")

# === Metrics ===



nb_epci = df_evolution_ct_activee_mois[df_evolution_ct_activee_mois['categorie'] == 'EPCI à fiscalité propre']['nb_ct_cumule'].max()
nb_commune = df_evolution_ct_activee_mois[df_evolution_ct_activee_mois['categorie'] == 'Communes']['nb_ct_cumule'].max()
nb_reg_et_dep = df_evolution_ct_activee_mois[df_evolution_ct_activee_mois['categorie'].isin(['Régions', 'Départements'])]['nb_ct_cumule'].max()
nb_autres = df_evolution_ct_activee_mois[df_evolution_ct_activee_mois['categorie'] == 'Syndicats, PETR, pôles métropolitains et autres']['nb_ct_cumule'].max()

cols= st.columns(4)
with cols[0]:
    st.metric("EPCI à fiscalité propre", nb_epci)
with cols[1]:
    st.metric("Communes", nb_commune)
with cols[2]:
    st.metric("Régions et départements", nb_reg_et_dep)
with cols[3]:
    st.metric("Syndicats, PETR et autres", nb_autres)

# === Evolution des collectivités activées par type ===
types_ordre = ['EPCI à fiscalité propre', 'Communes', 'Syndicats, PETR, pôles métropolitains et autres', 'Régions', 'Départements']

# Obtenir tous les mois uniques triés
all_mois = df_evolution_ct_activee_mois['mois'].sort_values().unique()

# Préparer les données pour le graphique Nivo (une série par type, avec les trous bouchés)
area_data_ct_evolution = []
for type_ct in types_ordre:
    df_filtered = df_evolution_ct_activee_mois[df_evolution_ct_activee_mois['categorie'] == type_ct].copy()
    if not df_filtered.empty:
        # Créer un dataframe avec tous les mois
        df_all_mois = pd.DataFrame({'mois': all_mois})
        # Merger avec les données existantes
        df_complete = df_all_mois.merge(df_filtered[['mois', 'nb_ct_cumule']], on='mois', how='left')
        # Remplir les trous avec la valeur précédente (forward fill), puis 0 pour les premiers mois sans données
        df_complete['nb_ct_cumule'] = df_complete['nb_ct_cumule'].ffill().fillna(0).astype(int)
        
        area_data_ct_evolution.append({
            "id": type_ct,
            "data": [
                {"x": row['mois'].strftime('%Y-%m') if hasattr(row['mois'], 'strftime') else str(row['mois']), "y": row['nb_ct_cumule']}
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

# === Trackers ===
st.markdown("---")
st.markdown("### Transition Tracker des EPCI à fiscalité propre")


trackers = st.columns(2)
with trackers[0]:
    st.markdown('Définir ce qu\'est un PAP actif, etc.')
with trackers[1]:
    
    df_ct_actives['active'] = True

    df_ct_actives = df_ct_actives[df_ct_actives['type'] == 'epci']

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

    "commune": "Communes",
    "departement": "Départements",
    "region": "Régions"
    }


    df_collectivites['categorie'] = df_collectivites['nature_insee'].map(nature_to_categorie)

    df_collectivites_epci_fiscalite_propre = df_collectivites[(df_collectivites['type'] == 'epci') & (df_collectivites['categorie'] == 'EPCI à fiscalité propre')]

    ct_pap = df_pap[['collectivite_id', 'passage_pap']].groupby('collectivite_id').min().reset_index()

    df_final = df_collectivites_epci_fiscalite_propre.merge(df_ct_actives[['collectivite_id', 'active']], right_on='collectivite_id', left_on='id', how='left') \
        .merge(ct_pap, left_on='id', right_on='collectivite_id', how='left')    

    # EPCI avec profil et plan d'action actif
    nb_avec_pap = df_final[df_final['passage_pap'].notna()].shape[0]
    nb_avec_profil = df_final[(df_final['active'].notna()) & (df_final['passage_pap'].isna())].shape[0]
    nb_sans_profil = df_final[df_final['active'].isna()].shape[0]

    # Total pour vérification
    total_epci = df_final.shape[0]

    # === Visualisation Waffle Chart avec Nivo (streamlit-elements) ===

    # Paramètres du waffle 10x10
    total_cells = 100

    # Calculer les proportions pour 100 cellules
    prop_avec_pap = nb_avec_pap / total_epci
    prop_avec_profil = nb_avec_profil / total_epci
    prop_sans_profil = nb_sans_profil / total_epci

    # Nombre de cellules pour chaque catégorie
    cells_avec_pap = int(np.round(prop_avec_pap * total_cells))
    cells_avec_profil = int(np.round(prop_avec_profil * total_cells))
    cells_sans_profil = total_cells - cells_avec_pap - cells_avec_profil  # Pour garantir exactement 100 cellules

    # Données pour le waffle chart Nivo (avec vraies valeurs pour le tooltip)
    waffle_data = [
        {"id": "avec_pap", "label": f"Avec profil et plan d'action actif: {nb_avec_pap}", "value": cells_avec_pap, "realValue": nb_avec_pap},
        {"id": "avec_profil", "label": f"Avec profil: {nb_avec_profil}", "value": cells_avec_profil, "realValue": nb_avec_profil},
        {"id": "sans_profil", "label": f"Sans profil: {nb_sans_profil}", "value": cells_sans_profil, "realValue": nb_sans_profil},
    ]

    # Afficher le waffle chart avec streamlit-elements
    with elements("waffle_epci"):
        with mui.Box(sx={"height": 300}):
            nivo.Waffle(
                data=waffle_data,
                total=100,
                rows=10,
                columns=10,
                padding=1,
                colors=["#10b981", "#f59e0b", "#ef4444"],
                borderRadius="10px",
                animate=True,
                motionStiffness=90,
                motionDamping=11,
                legends=[
                    {
                        "anchor": "bottom",
                        "direction": "row",
                        "justify": False,
                        "translateX": 0,
                        "translateY": 30,
                        "itemsSpacing": 10,
                        "itemWidth": 200,
                        "itemHeight": 20,
                        "itemDirection": "left-to-right",
                        "itemOpacity": 1,
                        "itemTextColor": "#777",
                        "symbolSize": 14,
                    }
                ],
            )

st.markdown("---")
st.markdown('### Un développement national')

with st.container(border=True):
    st.selectbox("Sélectionnez une région", options=df_cci['region_name'].unique())
    st.selectbox("Sélectionnez un département", options=df_cci['departement_name'].unique())

st.markdown("Imaginer la carte de France ou region ou département sélectionné ici.")
st.markdown("La selection ne fait rien sur ce prototype.")

st.markdown("---")

st.markdown("### Un outil adopté par les collectivités")

# Calculer la date d'il y a 12 mois
date_12_mois = datetime.now(timezone.utc) - relativedelta(months=12)
# Pour df_user_actif, on prend le premier du mois d'il y a 12 mois
debut_mois_12_mois = date_12_mois.replace(day=1)

# S'assurer que 'mois' est de type datetime64[ns, UTC], pour comparaison correcte
if df_user_actif['mois'].dt.tz is not None:
    filtre = df_user_actif['mois'] >= pd.Timestamp(debut_mois_12_mois)
else:
    filtre = df_user_actif['mois'] >= pd.Timestamp(debut_mois_12_mois).replace(tzinfo=None)

area_data_users_evolution = [
    {
        "id": "users",
        "data": [
            {"x": row['mois'].strftime('%Y-%m') if hasattr(row['mois'], 'strftime') else str(row['mois']), "y": row['nb_users_cumule']}
            for _, row in df_evolution_users_mois.iterrows()
        ]
    }
]

with elements("area_users_evolution"):
    with mui.Box(sx={"height": 500}):
        nivo.Line(
            data=area_data_users_evolution,
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
                "legend": "Mois",
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
            pointSize=6,
            pointColor={"theme": "background"},
            pointBorderWidth=2,
            pointBorderColor={"from": "serieColor"},
            useMesh=True,
            enableSlices="x",
            legends=[],
            colors={"scheme": "pastel2"},
            theme=theme_actif,
        )

# delta=df_users[df_users['email_confirmed_at'] >= date_12_mois]['id'].nunique()
# st.metric("Utilisateurs actifs", df_user_actif[filtre]['email'].nunique(), delta=delta)


# Chart Nivo - Pie chart utilisateurs actifs par collectivité
st.markdown("### Un outil qui facilite la collaboration")

# Grouper par collectivité et compter les emails uniques
users_par_collectivite = df_user_actif[filtre].groupby('collectivite_id')['email'].nunique().reset_index()
users_par_collectivite.columns = ['collectivite_id', 'nb_users']

users_par_collectivite = users_par_collectivite[users_par_collectivite.collectivite_id.isin(ct_pap['collectivite_id'])].copy()

cols_collab = st.columns(2)
with cols_collab[0]:

    stats_collab = st.columns(2)
    with stats_collab[0]:
        st.metric("Moyenne utilisateurs actifs par collectivité", int(round(users_par_collectivite['nb_users'].mean(), 0)))
    with stats_collab[1]:
        st.metric("Max utilisateurs actifs par collectivité", users_par_collectivite['nb_users'].max())

with cols_collab[1]:

    st.markdown("Répartition des collectivités par nombre d'utilisateurs actifs")

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
st.markdown("### Un outil de gestion de projets")

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
    st.markdown("750+ plans d'actions pilotables actifs*")
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
    st.markdown("30 000+ fiches actions pilotables*")
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

cols_pap = st.columns(2)
with cols_pap[0]:
    st.markdown("Nous mettons à disposition des collectivités des indicateurs en Open Data ...")
    metrics_od = st.columns(2)
    with metrics_od[0]:
        st.metric("Indicateurs disponibles en Open Data", 176)
    with metrics_od[1]:
        st.metric("Sources de données", 36)

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
                colors={"scheme": "pastel2"},
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




