import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from utils.data import (
    load_df_pap, 
    load_df_collectivite
)


st.set_page_config(layout="wide")
st.title("⚡ Dashboard Weekly")

# === CHARGEMENT DES DONNÉES ===
df_pap = load_df_pap()
df_ct = load_df_collectivite()

if df_pap.empty:
    st.info("Aucune donnée. Branchez vos sources dans `utils/data.py`.")
    st.stop()

# Jointure avec les collectivités
df_pap_enrichi = pd.merge(df_pap, df_ct, on='collectivite_id', how='left')

# Préparation des dates
df_pap_enrichi['passage_pap'] = pd.to_datetime(df_pap_enrichi['passage_pap'], errors='coerce').dt.tz_localize(None)
df_pap_enrichi['semaine_pap'] = df_pap_enrichi['passage_pap'].dt.to_period('W').dt.to_timestamp()

# === IDENTIFICATION DES SEMAINES S-1 ET S-2 ===
semaines_disponibles = sorted(df_pap_enrichi['semaine_pap'].dropna().unique(), reverse=True)

if len(semaines_disponibles) < 2:
    st.warning("⚠️ Pas assez de données pour comparer S-1 et S-2.")
    st.stop()

# S-1 = dernière semaine, S-2 = avant-dernière semaine
s1 = semaines_disponibles[0]
s2 = semaines_disponibles[1]

s1_str = pd.to_datetime(s1).strftime("%d/%m/%Y")
s2_str = pd.to_datetime(s2).strftime("%d/%m/%Y")

st.markdown("---")

# === DONNÉES S-1 ET S-2 ===
df_s1 = df_pap_enrichi[df_pap_enrichi['semaine_pap'] == s1].copy()
df_s2 = df_pap_enrichi[df_pap_enrichi['semaine_pap'] == s2].copy()

# Nouveaux PAP en S-1
nouveaux_pap_s1 = len(df_s1)
nouveaux_pap_s2 = len(df_s2)
diff_pap = nouveaux_pap_s1 - nouveaux_pap_s2

# Nouvelles collectivités en S-1
nouvelles_ct_s1 = df_s1['collectivite_id'].nunique()
nouvelles_ct_s2 = df_s2['collectivite_id'].nunique()
diff_ct = nouvelles_ct_s1 - nouvelles_ct_s2

# Répartition Import/Autonome
if 'import' in df_s1.columns and 'import' in df_s2.columns:
    nb_importes_s1 = len(df_s1[df_s1['import'] == 'Importé'])
    nb_importes_s2 = len(df_s2[df_s2['import'] == 'Importé'])
    diff_importes = nb_importes_s1 - nb_importes_s2
    
    nb_autonomes_s1 = len(df_s1[df_s1['import'] == 'Autonome'])
    nb_autonomes_s2 = len(df_s2[df_s2['import'] == 'Autonome'])
    diff_autonomes = nb_autonomes_s1 - nb_autonomes_s2
else:
    nb_importes_s1 = 0
    nb_autonomes_s1 = 0
    diff_importes = 0
    diff_autonomes = 0

# === INDICATEURS CLÉS ===
st.markdown("## 🎯 Indicateurs clés de la semaine")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Nouveaux PAP",
        nouveaux_pap_s1,
        delta=f"{diff_pap:+d}",
        delta_color="normal"
    )

with col2:
    st.metric(
        "Nouvelles collectivités",
        nouvelles_ct_s1,
        delta=f"{diff_ct:+d}",
        delta_color="normal"
    )

with col3:
    if 'import' in df_s1.columns:
        st.metric(
            "PAP Importés",
            nb_importes_s1,
            delta=f"{diff_importes:+d}",
            delta_color="normal"
        )
    else:
        st.metric("PAP Importés", "N/A")

with col4:
    if 'import' in df_s1.columns:
        st.metric(
            "PAP Autonomes",
            nb_autonomes_s1,
            delta=f"{diff_autonomes:+d}",
            delta_color="normal"
        )
    else:
        st.metric("PAP Autonomes", "N/A")

st.markdown("---")

# === GRAPHIQUES DE RÉPARTITION ===
st.markdown("## 🌈 Répartition des nouveaux PAP")

col_graph1, col_graph2 = st.columns(2)

with col_graph1:
    st.markdown("### Par type de plan")
    if not df_s1.empty and 'nom_plan' in df_s1.columns:
        pap_par_plan_s1 = df_s1['nom_plan'].value_counts().reset_index()
        pap_par_plan_s1.columns = ['Type de plan', 'Nombre']
        
        fig_s1 = px.bar(
            pap_par_plan_s1,
            x='Type de plan',
            y='Nombre',
            text='Nombre',
            color='Type de plan',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_s1.update_traces(textposition='outside')
        fig_s1.update_layout(showlegend=False, height=450)
        st.plotly_chart(fig_s1, use_container_width=True)
    else:
        st.info("Pas de données pour S-1")

with col_graph2:
    st.markdown("### Importé vs Autonome")
    if 'import' in df_s1.columns and not df_s1.empty:
        import_s1 = df_s1['import'].value_counts().reset_index()
        import_s1.columns = ['Statut', 'Nombre']
        
        fig_import_s1 = px.pie(
            import_s1,
            names='Statut',
            values='Nombre',
            color='Statut',
            color_discrete_map={'Importé': '#FFB6C1', 'Autonome': '#98D8C8'}
        )
        fig_import_s1.update_traces(textposition='inside', textinfo='percent+label+value')
        fig_import_s1.update_layout(height=450)
        st.plotly_chart(fig_import_s1, use_container_width=True)
    else:
        st.info("Pas de données pour S-1")

st.markdown("---")

# === NOUVELLES COLLECTIVITÉS DE LA SEMAINE S-1 ===
st.markdown("## 🆕 Liste des nouvelles collectivités")

# Collectivités uniques de S-1
collectivites_s1 = df_s1.groupby('collectivite_id').agg({
    'nom': 'first',
    'type_collectivite': 'first',
    'nature_collectivite': 'first',
    'region_name': 'first',
    'departement_name': 'first',
    'population_totale': 'first',
    'import': 'first' if 'import' in df_s1.columns else lambda x: 'N/A',
    'nom_plan': lambda x: ', '.join(x.unique())  # Liste des plans
}).reset_index()

collectivites_s1.columns = [
    'ID Collectivité', 'Nom', 'Type', 'Nature', 
    'Région', 'Département', 'Population', 'Statut Import', 'Plans'
]

# Tri par population décroissante
collectivites_s1 = collectivites_s1.sort_values(by='Population', ascending=False)
collectivites_s1['Population'] = collectivites_s1['Population'].fillna(0).astype(int)

# Affichage du tableau
st.dataframe(
    collectivites_s1[['Nom', 'Plans', 'Statut Import', 'Type', 'Nature', 'Région', 'Département', 'Population']],
    use_container_width=True,
    hide_index=True,
    height=400
)

st.markdown("---")

# === STATISTIQUES DÉTAILLÉES ===
st.markdown("## 📈 Statistiques détaillées")

col_stat1, col_stat2, col_stat3 = st.columns(3)

with col_stat1:
    st.markdown("### Par type de collectivité")
    if not df_s1.empty and 'type_collectivite' in df_s1.columns:
        type_ct_s1 = df_s1['type_collectivite'].value_counts().reset_index()
        type_ct_s1.columns = ['Type', 'Nombre']
        st.dataframe(type_ct_s1, hide_index=True, use_container_width=True)
    else:
        st.info("Pas de données")

with col_stat2:
    st.markdown("### Par région")
    if not df_s1.empty and 'region_name' in df_s1.columns:
        region_s1 = df_s1['region_name'].value_counts().head(10).reset_index()
        region_s1.columns = ['Région', 'Nombre']
        st.dataframe(region_s1, hide_index=True, use_container_width=True)
    else:
        st.info("Pas de données")

with col_stat3:
    st.markdown("### Par nature ")
    if not df_s1.empty and 'nature_collectivite' in df_s1.columns:
        nature_s1 = df_s1['nature_collectivite'].value_counts().reset_index()
        nature_s1.columns = ['Nature', 'Nombre']
        st.dataframe(nature_s1, hide_index=True, use_container_width=True)
    else:
        st.info("Pas de données")


