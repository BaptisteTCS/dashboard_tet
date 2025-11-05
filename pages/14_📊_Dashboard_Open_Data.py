import streamlit as st
import pandas as pd
from sqlalchemy import text
from utils.db import get_engine_prod

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
    """Charge les données open data disponibles depuis la base de production."""
    try:
        engine = get_engine_prod()
        
        query = text("""
            SELECT DISTINCT 
                id.titre, 
                id.unite, 
                id.identifiant_referentiel, 
                maille.types_collectivite,
                t.md_id as thematique,
                sources.sources_libelle
            FROM indicateur_definition id
            JOIN indicateur_valeur iv 
                ON id.id = iv.indicateur_id
            JOIN (
                SELECT 
                    id.identifiant_referentiel, 
                    ARRAY_AGG(DISTINCT c.type) AS types_collectivite
                FROM indicateur_definition id
                JOIN indicateur_valeur iv 
                    ON id.id = iv.indicateur_id
                JOIN collectivite c 
                    ON iv.collectivite_id = c.id
                WHERE 
                    id.collectivite_id IS NULL 
                    AND iv.metadonnee_id IS NOT NULL 
                    AND c.type <> 'test'
                GROUP BY 
                    id.identifiant_referentiel
            ) AS maille 
                ON maille.identifiant_referentiel = id.identifiant_referentiel
            LEFT JOIN (
                SELECT 
                    id.identifiant_referentiel, 
                    ARRAY_AGG(DISTINCT is2.libelle) AS sources_libelle
                FROM indicateur_definition id
                JOIN indicateur_valeur iv 
                    ON id.id = iv.indicateur_id
                JOIN indicateur_source_metadonnee ism 
                    ON ism.id = iv.metadonnee_id
                JOIN indicateur_source is2 
                    ON is2.id = ism.source_id
                WHERE 
                    id.collectivite_id IS NULL 
                    AND iv.metadonnee_id IS NOT NULL 
                    AND is2.libelle NOT IN ('SNBC', 'Territoires&Climat')
                GROUP BY 
                    id.identifiant_referentiel
            ) AS sources 
                ON sources.identifiant_referentiel = id.identifiant_referentiel
            LEFT JOIN indicateur_thematique it 
                ON id.id=it.indicateur_id 
            LEFT JOIN thematique t 
                ON t.id=it.thematique_id
            WHERE 
                id.collectivite_id IS NULL 
                AND iv.metadonnee_id IS NOT NULL
                AND sources.sources_libelle IS NOT NULL
            ORDER BY 
                id.identifiant_referentiel
        """)
        
        with engine.connect() as conn:
            df = pd.read_sql_query(query, conn)
        
        return df
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des données : {str(e)}")
        return pd.DataFrame()


def formater_liste(liste_str):
    """Formate une liste PostgreSQL en chaîne lisible."""
    if pd.isna(liste_str):
        return ""
    # Supprime les accolades et formate
    return liste_str.replace('{', '').replace('}', '').replace(',', ', ')


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
    st.metric("🔗 Sources uniques", len(sources_uniques))

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
    # Recherche par titre
    search_titre = st.text_input(
        "🔎 Rechercher par titre d'indicateur",
        placeholder="Ex: émissions, déchets, énergie...",
        help="La recherche n'est pas sensible à la casse"
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

if search_titre:
    mask = df_filtered['Titre'].str.contains(search_titre, case=False, na=False)
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

st.header(f"📋 Résultats ({len(df_filtered)} indicateur{'s' if len(df_filtered) > 1 else ''})")

if df_filtered.empty:
    st.warning("🔍 Aucun résultat ne correspond à vos critères de recherche")
else:
    # Options d'affichage
    col_opt1, col_opt2 = st.columns([3, 1])
    
    with col_opt2:
        hauteur_tableau = st.slider(
            "Hauteur du tableau (pixels)",
            min_value=300,
            max_value=1000,
            value=600,
            step=50
        )
    
    # Affichage du tableau avec scroll
    st.dataframe(
        df_filtered,
        use_container_width=True,
        height=hauteur_tableau,
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
    
    # Bouton d'export
    st.markdown("---")
    st.subheader("💾 Exporter les données")
    
    col_export1, col_export2, col_export3 = st.columns([1, 1, 3])
    
    with col_export1:
        # Export CSV
        csv = df_filtered.to_csv(index=False, sep=';', encoding='utf-8-sig')
        st.download_button(
            label="📥 Télécharger en CSV",
            data=csv,
            file_name="indicateurs_open_data.csv",
            mime="text/csv",
            help="Télécharger les résultats au format CSV"
        )
    
    with col_export2:
        # Export Excel
        import io
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df_filtered.to_excel(writer, index=False, sheet_name='Open Data')
        buffer.seek(0)
        
        st.download_button(
            label="📥 Télécharger en Excel",
            data=buffer,
            file_name="indicateurs_open_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            help="Télécharger les résultats au format Excel"
        )

# ==========================
# ANALYSES COMPLÉMENTAIRES
# ==========================

st.markdown("---")
st.header("📊 Analyses complémentaires")

tab1, tab2, tab3 = st.tabs(["📈 Par source", "🎯 Par thématique", "🏛️ Par type de collectivité"])

with tab1:
    st.subheader("Répartition des indicateurs par source")
    
    # Compter les sources
    sources_count = {}
    for sources in df_filtered['Sources'].dropna():
        for source in sources.split(', '):
            source = source.strip()
            sources_count[source] = sources_count.get(source, 0) + 1
    
    if sources_count:
        df_sources = pd.DataFrame(
            list(sources_count.items()),
            columns=['Source', 'Nombre d\'indicateurs']
        ).sort_values('Nombre d\'indicateurs', ascending=False)
        
        st.bar_chart(
            df_sources.set_index('Source'),
            height=400
        )
        
        st.dataframe(
            df_sources,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Aucune source disponible dans les résultats filtrés")

with tab2:
    st.subheader("Répartition des indicateurs par thématique")
    
    # Compter les thématiques
    thematiques_count = df_filtered['Thématique'].value_counts().reset_index()
    thematiques_count.columns = ['Thématique', 'Nombre d\'indicateurs']
    
    if not thematiques_count.empty:
        st.bar_chart(
            thematiques_count.set_index('Thématique'),
            height=400
        )
        
        st.dataframe(
            thematiques_count,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Aucune thématique disponible dans les résultats filtrés")

with tab3:
    st.subheader("Répartition des indicateurs par type de collectivité")
    
    # Compter les types
    types_count = {}
    for types in df_filtered['Types de collectivité'].dropna():
        for type_coll in types.split(', '):
            type_coll = type_coll.strip()
            types_count[type_coll] = types_count.get(type_coll, 0) + 1
    
    if types_count:
        df_types = pd.DataFrame(
            list(types_count.items()),
            columns=['Type de collectivité', 'Nombre d\'indicateurs']
        ).sort_values('Nombre d\'indicateurs', ascending=False)
        
        st.bar_chart(
            df_types.set_index('Type de collectivité'),
            height=400
        )
        
        st.dataframe(
            df_types,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Aucun type de collectivité disponible dans les résultats filtrés")

# Footer
st.markdown("---")
st.caption("💡 Les données sont mises en cache pendant 1 heure pour optimiser les performances. Rechargez la page pour actualiser.")

