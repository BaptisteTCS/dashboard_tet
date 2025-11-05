import streamlit as st
import pandas as pd
from sqlalchemy import text
from utils.db import get_engine

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Open Data",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard Open Data")
st.markdown("""
Cette page présente les **données open data** disponibles sur notre application pour les collectivités.
Explorez les indicateurs, leurs sources, les mailles territoriales et les thématiques associées.
""")

st.markdown("---")

# ==========================
# FONCTIONS
# ==========================

@st.cache_data(ttl=3600)
def charger_donnees_open_data():
    """Charge les données open data disponibles depuis la table indicateurs_open_data de la base OLAP."""
    try:
        engine = get_engine()
        
        query = text("""
            SELECT 
                titre, 
                unite, 
                identifiant_referentiel, 
                types_collectivite,
                thematique,
                sources_libelle
            FROM indicateurs_od
            ORDER BY identifiant_referentiel
        """)
        
        with engine.connect() as conn:
            df = pd.read_sql_query(query, conn)
        
        return df
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des données : {str(e)}")
        return pd.DataFrame()


def formater_liste(valeur):
    """Formate une liste PostgreSQL en chaîne lisible."""
    # Gérer les valeurs None/NaN
    if valeur is None:
        return ""
    
    # Si c'est déjà une liste Python
    if isinstance(valeur, list):
        return ', '.join(str(item) for item in valeur)
    
    # Si c'est une chaîne
    if isinstance(valeur, str):
        # Supprime les accolades PostgreSQL et formate
        return valeur.replace('{', '').replace('}', '').replace(',', ', ')
    
    # Pour les autres types (incluant NaN)
    try:
        if pd.isna(valeur):
            return ""
    except (TypeError, ValueError):
        pass
    
    return str(valeur)


# ==========================
# CHARGEMENT DES DONNÉES
# ==========================

with st.spinner("🔄 Chargement des données open data..."):
    df_open_data = charger_donnees_open_data()

if df_open_data.empty:
    st.warning("⚠️ Aucune donnée open data disponible")
    st.stop()

# Formater les colonnes avec des listes PostgreSQL
if 'types_collectivite' in df_open_data.columns:
    df_open_data['types_collectivite'] = df_open_data['types_collectivite'].apply(formater_liste)
if 'sources_libelle' in df_open_data.columns:
    df_open_data['sources_libelle'] = df_open_data['sources_libelle'].apply(formater_liste)

# Renommer les colonnes pour l'affichage
df_display = df_open_data.copy()
df_display.columns = [
    'Titre', 
    'Unité', 
    'Identifiant', 
    'Types de collectivité',
    'Thématique',
    'Sources'
]

# ==========================
# STATISTIQUES GÉNÉRALES
# ==========================

st.header("📈 Vue d'ensemble")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📊 Indicateurs disponibles", len(df_display))

with col2:
    # Compter le nombre de sources uniques
    sources_uniques = set()
    for sources in df_open_data['sources_libelle'].dropna():
        sources_uniques.update(sources.split(', '))
    st.metric("🔗 Producteurs de données", len(sources_uniques))

with col3:
    # Compter le nombre de thématiques uniques
    thematiques_uniques = df_open_data['thematique'].nunique()
    st.metric("🎯 Thématiques", thematiques_uniques)

with col4:
    # Compter le nombre de types de collectivités uniques
    types_uniques = set()
    for types in df_open_data['types_collectivite'].dropna():
        types_uniques.update(types.split(', '))
    st.metric("🏛️ Types de collectivité", len(types_uniques))

st.markdown("---")

# ==========================
# FILTRES ET RECHERCHE
# ==========================

st.header("🔍 Rechercher et filtrer")

col_search1, col_search2 = st.columns(2)

with col_search1:
    # Recherche par titre avec sélection
    titres_list = sorted(df_display['Titre'].unique().tolist())
    selected_titre = st.selectbox(
        "🔎 Rechercher et sélectionner un indicateur",
        options=titres_list,
        index=None,
        placeholder="Tapez pour rechercher un indicateur...",
        help="Tapez pour rechercher et sélectionnez un indicateur spécifique"
    )

with col_search2:
    # Filtre par thématique
    thematiques = ['Toutes'] + sorted(df_open_data['thematique'].dropna().unique().tolist())
    selected_thematique = st.selectbox(
        "🎯 Filtrer par thématique",
        options=thematiques
    )

col_filter1, col_filter2 = st.columns(2)

with col_filter1:
    # Filtre par type de collectivité
    all_types = set()
    for types in df_open_data['types_collectivite'].dropna():
        all_types.update(types.split(', '))
    types_list = ['Tous'] + sorted(list(all_types))
    selected_type = st.selectbox(
        "🏛️ Filtrer par type de collectivité",
        options=types_list
    )

with col_filter2:
    # Filtre par source
    all_sources = set()
    for sources in df_open_data['sources_libelle'].dropna():
        all_sources.update(sources.split(', '))
    sources_list = ['Toutes'] + sorted(list(all_sources))
    selected_source = st.selectbox(
        "🔗 Filtrer par source",
        options=sources_list
    )

# Appliquer les filtres
df_filtered = df_display.copy()

if selected_titre:
    mask = df_filtered['Titre'] == selected_titre
    df_filtered = df_filtered[mask]

if selected_thematique != 'Toutes':
    mask = df_filtered['Thématique'] == selected_thematique
    df_filtered = df_filtered[mask]

if selected_type != 'Tous':
    mask = df_filtered['Types de collectivité'].str.contains(selected_type, na=False)
    df_filtered = df_filtered[mask]

if selected_source != 'Toutes':
    mask = df_filtered['Sources'].str.contains(selected_source, na=False)
    df_filtered = df_filtered[mask]

st.markdown("---")

# ==========================
# AFFICHAGE DES RÉSULTATS
# ==========================

if df_filtered.empty:
    st.warning("🔍 Aucun résultat ne correspond à vos critères de recherche")
else:
    # Affichage du tableau avec scroll
    st.dataframe(
        df_filtered,
        use_container_width=True,
        height=800,
        hide_index=True,
        column_config={
            "Titre": st.column_config.TextColumn(
                "Titre",
                width="large",
                help="Titre de l'indicateur"
            ),
            "Unité": st.column_config.TextColumn(
                "Unité",
                width="small"
            ),
            "Identifiant": st.column_config.TextColumn(
                "Identifiant",
                width="medium"
            ),
            "Types de collectivité": st.column_config.TextColumn(
                "Types de collectivité",
                width="medium"
            ),
            "Thématique": st.column_config.TextColumn(
                "Thématique",
                width="medium"
            ),
            "Sources": st.column_config.TextColumn(
                "Sources",
                width="medium"
            )
        }
    )
