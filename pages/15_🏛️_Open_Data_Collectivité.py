import streamlit as st
import pandas as pd
from sqlalchemy import text
from utils.db import get_engine_prod

# Configuration de la page
st.set_page_config(
    page_title="Open Data par Collectivité",
    page_icon="🏛️",
    layout="wide"
)

st.title("🏛️ Open Data par Collectivité")
st.markdown("""
Recherchez votre collectivité pour découvrir les **données open data** disponibles sur notre application.
Visualisez les indicateurs, les dates disponibles, les sources et les thématiques associées.
""")

st.info("💡 Les données peuvent prendre un certain temps à charger, ne partez pas ;)")
st.markdown("---")

# ==========================
# FONCTIONS
# ==========================

@st.cache_data(ttl=3600)
def charger_collectivites(show_spinner="⏳ Chargement des collectivités..."):
    """Charge la liste des collectivités depuis la base de production."""
    try:
        engine = get_engine_prod()
        
        query = text("""
            SELECT 
                id,
                nom,
                type
            FROM collectivite
            WHERE type <> 'test'
            ORDER BY nom
        """)
        
        with engine.connect() as conn:
            df = pd.read_sql_query(query, conn)
        
        return df
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des collectivités : {str(e)}")
        return pd.DataFrame()


@st.cache_data(ttl=3600)
def charger_donnees_collectivite(collectivite_id, show_spinner="⏳ Chargement des données open data pour la collectivité..."):
    """Charge les données open data disponibles pour une collectivité spécifique."""
    try:
        engine = get_engine_prod()
        
        query = text("""
            SELECT DISTINCT 
                id.titre, 
                id.unite, 
                id.identifiant_referentiel,
                t.md_id as thematique,
                producteurs.producteurs
            FROM indicateur_definition id
            JOIN indicateur_valeur iv 
                ON id.id = iv.indicateur_id
            LEFT JOIN (
                SELECT 
                    iv.indicateur_id,
                    iv.collectivite_id,
                    ARRAY_AGG(DISTINCT ism.producteur) AS producteurs
                FROM indicateur_valeur iv
                JOIN indicateur_source_metadonnee ism 
                    ON ism.id = iv.metadonnee_id
                WHERE iv.collectivite_id = :collectivite_id
                    AND iv.metadonnee_id IS NOT NULL
                    AND ism.producteur IS NOT NULL
                    AND ism.producteur <> ''
                GROUP BY 
                    iv.indicateur_id,
                    iv.collectivite_id
            ) AS producteurs 
                ON producteurs.indicateur_id = id.id 
                AND producteurs.collectivite_id = iv.collectivite_id
            LEFT JOIN indicateur_thematique it 
                ON id.id = it.indicateur_id 
            LEFT JOIN thematique t 
                ON t.id = it.thematique_id
            WHERE 
                iv.collectivite_id = :collectivite_id
                AND id.collectivite_id IS NULL 
                AND iv.metadonnee_id IS NOT NULL
                AND producteurs.producteurs IS NOT NULL
            ORDER BY 
                id.identifiant_referentiel
        """)
        
        with engine.connect() as conn:
            df = pd.read_sql_query(query, conn, params={"collectivite_id": collectivite_id})
        
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
# SÉLECTION DE LA COLLECTIVITÉ
# ==========================

st.header("🔎 Sélectionnez votre collectivité")

df_collectivites = charger_collectivites()

if df_collectivites.empty:
    st.error("❌ Impossible de charger la liste des collectivités")
    st.stop()

# Créer une liste combinant nom et type pour l'affichage
df_collectivites['display_name'] = df_collectivites['nom'] + ' (' + df_collectivites['type'] + ')'

# Recherche et sélection de la collectivité
selected_collectivite = st.selectbox(
    "🏛️ Recherchez et sélectionnez votre collectivité",
    options=df_collectivites['id'].tolist(),
    format_func=lambda x: df_collectivites[df_collectivites['id'] == x]['display_name'].values[0],
    index=None,
    placeholder="Tapez pour rechercher votre collectivité...",
    help="Tapez le nom de votre collectivité pour la rechercher"
)

if not selected_collectivite:
    st.info("👆 Veuillez sélectionner une collectivité pour visualiser ses données open data")
    st.stop()

# Récupérer les infos de la collectivité sélectionnée
collectivite_info = df_collectivites[df_collectivites['id'] == selected_collectivite].iloc[0]
st.success(f"✅ Collectivité sélectionnée : **{collectivite_info['nom']}** ({collectivite_info['type']})")

st.markdown("---")

# ==========================
# CHARGEMENT DES DONNÉES
# ==========================

df_open_data = charger_donnees_collectivite(selected_collectivite)

if df_open_data.empty:
    st.warning(f"⚠️ Aucune donnée open data disponible pour {collectivite_info['nom']}")
    st.stop()

# Formater les colonnes avec des listes PostgreSQL
if 'producteurs' in df_open_data.columns:
    df_open_data['producteurs'] = df_open_data['producteurs'].apply(formater_liste)

# Renommer les colonnes pour l'affichage
df_display = df_open_data.copy()
df_display.columns = [
    'Titre', 
    'Unité', 
    'Identifiant', 
    'Thématique',
    'Producteurs'
]

# ==========================
# STATISTIQUES GÉNÉRALES
# ==========================

st.header("📈 Vue d'ensemble")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📊 Indicateurs disponibles", len(df_display))

with col2:
    # Compter le nombre de producteurs uniques
    producteurs_uniques = set()
    for producteurs in df_open_data['producteurs'].dropna():
        producteurs_uniques.update(producteurs.split(', '))
    st.metric("🔗 Producteurs de données", len(producteurs_uniques))

with col3:
    # Compter le nombre de thématiques uniques
    thematiques_uniques = df_open_data['thematique'].nunique()
    st.metric("🎯 Thématiques", thematiques_uniques)

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

# Filtre par producteur
all_producteurs = set()
for producteurs in df_open_data['producteurs'].dropna():
    all_producteurs.update(producteurs.split(', '))
producteurs_list = ['Tous'] + sorted(list(all_producteurs))
selected_producteur = st.selectbox(
    "🔗 Filtrer par producteur",
    options=producteurs_list
)

# Appliquer les filtres
df_filtered = df_display.copy()

if selected_titre:
    mask = df_filtered['Titre'] == selected_titre
    df_filtered = df_filtered[mask]

if selected_thematique != 'Toutes':
    mask = df_filtered['Thématique'] == selected_thematique
    df_filtered = df_filtered[mask]

if selected_producteur != 'Tous':
    mask = df_filtered['Producteurs'].str.contains(selected_producteur, na=False)
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
            "Thématique": st.column_config.TextColumn(
                "Thématique",
                width="medium"
            ),
            "Producteurs": st.column_config.TextColumn(
                "Producteurs",
                width="medium",
                help="Producteurs des données"
            )
        }
    )

