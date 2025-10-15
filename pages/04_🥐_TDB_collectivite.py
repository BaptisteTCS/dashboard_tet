import streamlit as st
import pandas as pd

from utils.data import load_df_pap_notes
from utils.plots import radar_spider_graph_plotly


st.title("🥐 Tableau de bord des collectivités")

# Charger les données
df_notes = load_df_pap_notes()

# Conserver la dernière note par plan
pap_note = df_notes.sort_values(by='semaine', ascending=False).drop_duplicates(subset=['plan_id'], keep='first').copy()

# === SIDEBAR - FILTRES DE RECHERCHE ===
st.sidebar.header("🔍 Filtres de recherche")

# Filtre par type de collectivité
types_available = sorted(pap_note['type_collectivite'].dropna().unique().tolist())
selected_types = st.sidebar.multiselect(
    "Type de collectivité",
    options=types_available,
    default=None,
    help="Sélectionnez un ou plusieurs types"
)

# Filtre par nature de collectivité
natures_available = sorted(pap_note['nature_collectivite'].dropna().unique().tolist())
selected_natures = st.sidebar.multiselect(
    "Nature de collectivité",
    options=natures_available,
    default=None,
    help="Sélectionnez une ou plusieurs natures"
)

# Filtre par région
regions_available = sorted(pap_note['region_name'].dropna().unique().tolist())
selected_regions = st.sidebar.multiselect(
    "Région",
    options=regions_available,
    default=None,
    help="Sélectionnez une ou plusieurs régions"
)

# Filtre par département
departements_available = sorted(pap_note['departement_name'].dropna().unique().tolist())
selected_departements = st.sidebar.multiselect(
    "Département",
    options=departements_available,
    default=None,
    help="Sélectionnez un ou plusieurs départements"
)

# Filtre par tranche de population
st.sidebar.markdown("**Tranche de population**")
pop_min = int(pap_note['population_totale'].min()) if pap_note['population_totale'].notna().any() else 0
pop_max = int(pap_note['population_totale'].max()) if pap_note['population_totale'].notna().any() else 1000000

selected_pop_range = st.sidebar.slider(
    "Population (habitants)",
    min_value=pop_min,
    max_value=pop_max,
    value=(pop_min, pop_max),
    step=1000,
    format="%d",
    help="Ajustez la tranche de population"
)

# === APPLICATION DES FILTRES ===
filtered_df = pap_note.copy()

# Filtre par type
if selected_types:
    filtered_df = filtered_df[filtered_df['type_collectivite'].isin(selected_types)]

# Filtre par nature
if selected_natures:
    filtered_df = filtered_df[filtered_df['nature_collectivite'].isin(selected_natures)]

# Filtre par région
if selected_regions:
    filtered_df = filtered_df[filtered_df['region_name'].isin(selected_regions)]

# Filtre par département
if selected_departements:
    filtered_df = filtered_df[filtered_df['departement_name'].isin(selected_departements)]

# Filtre par population
filtered_df = filtered_df[
    (filtered_df['population_totale'] >= selected_pop_range[0]) &
    (filtered_df['population_totale'] <= selected_pop_range[1])
]

# Tri par score décroissant
filtered_df = filtered_df.sort_values(by='score', ascending=False)

# === AFFICHAGE DES RÉSULTATS ===
st.sidebar.markdown("---")
st.sidebar.metric("📊 Collectivités trouvées", len(filtered_df['nom_ct'].unique()))

if len(filtered_df) == 0:
    st.warning("⚠️ Aucune collectivité ne correspond à vos critères de recherche.")
else:
    # === VUE LISTE DES COLLECTIVITÉS ===
    st.markdown("---")
    st.markdown(f"**{len(filtered_df['nom_ct'].unique())} collectivité(s) trouvée(s)** - Triées par score moyen décroissant")
    
    # Grouper par collectivité et calculer le score moyen et nombre de plans
    collectivites_summary = filtered_df.groupby('nom_ct').agg({
        'score': 'mean',
        'plan_id': 'count',
        'type_collectivite': 'first',
        'nature_collectivite': 'first',
        'region_name': 'first',
        'departement_name': 'first',
        'population_totale': 'first',
        'collectivite_id': 'first'
    }).reset_index()
    
    collectivites_summary.columns = ['Collectivité', 'Score moyen', 'Nombre de plans', 'Type', 'Nature', 'Région', 'Département', 'Population', 'ID']
    collectivites_summary = collectivites_summary.sort_values(by='Score moyen', ascending=False)
    collectivites_summary['Score moyen'] = collectivites_summary['Score moyen'].round(2)
    collectivites_summary['Population'] = collectivites_summary['Population'].fillna(0).astype(int)
    
    # Afficher le tableau des collectivités
    st.dataframe(
        collectivites_summary[['Collectivité', 'Score moyen', 'Nombre de plans', 'Type', 'Nature', 'Région', 'Département', 'Population']],
        use_container_width=True,
        hide_index=True,
        height=400
    )
    
    # === SÉLECTION D'UNE COLLECTIVITÉ ===
    st.markdown("---")
    st.markdown("### 🔎 Sélectionnez une collectivité pour voir ses plans en détail")
    
    # Liste des collectivités triées par score
    collectivites_list = collectivites_summary['Collectivité'].tolist()
    
    selected_collectivite = st.selectbox(
        "Collectivité",
        options=collectivites_list,
        help="Sélectionnez une collectivité pour afficher tous ses plans en mode galerie"
    )
    
    if selected_collectivite:
        # Filtrer les plans de la collectivité sélectionnée
        plans_collectivite = filtered_df[filtered_df['nom_ct'] == selected_collectivite].sort_values(by='score', ascending=False)
        
        # Informations sur la collectivité
        ct_info = collectivites_summary[collectivites_summary['Collectivité'] == selected_collectivite].iloc[0]
        
        st.markdown("---")
        col_info1, col_info2, col_info3, col_info4 = st.columns(4)
        with col_info1:
            st.metric("Score moyen", f"{ct_info['Score moyen']} / 5")
        with col_info2:
            st.metric("Nombre de plans", int(ct_info['Nombre de plans']))
        with col_info3:
            st.info(f"**Type :** {ct_info['Type']}")
        with col_info4:
            st.info(f"**Population :** {int(ct_info['Population']):,} hab.".replace(',', ' '))
        
        # Options d'affichage
        st.markdown("---")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### ⬇️ Plans de {selected_collectivite}")
        with col2:
            nb_cols = st.selectbox("Graphes par ligne", options=[1, 2, 3], index=1, help="Nombre de graphes par ligne")
        
        st.markdown("---")
        
        # === GALERIE DE GRAPHES RADAR POUR LES PLANS DE LA COLLECTIVITÉ ===
        for idx in range(0, len(plans_collectivite), nb_cols):
            cols = st.columns(nb_cols)
            for col_idx, col in enumerate(cols):
                row_idx = idx + col_idx
                if row_idx < len(plans_collectivite):
                    row = plans_collectivite.iloc[row_idx]
                    with col:
                        # Informations du plan
                        with st.expander(f"ℹ️ {row['nom']}", expanded=False):
                            st.write(f"**Nom du plan :** {row['nom']}")
                            st.write(f"**Score global :** {round(row['score'], 2)} / 5")
                            st.write(f"**Score Pilotabilité :** {round(row['score_pilotabilite'], 2)} / 5")
                            st.write(f"**Score Indicateur :** {round(row['score_indicateur'], 2)} / 5")
                            st.write(f"**Score Objectif :** {round(row['score_objectif'], 2)} / 5")
                            st.write(f"**Score Référentiel :** {round(row['score_referentiel'], 2)} / 5")
                            st.write(f"**Score Avancement :** {round(row['score_avancement'], 2)} / 5")
                            st.write(f"**Score Budget :** {round(row['score_budget'], 2)} / 5")
                        
                        # Graphe radar
                        fig = radar_spider_graph_plotly(row)
                        st.plotly_chart(fig, width='stretch')


