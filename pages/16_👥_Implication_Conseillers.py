import streamlit as st
import pandas as pd
from sqlalchemy import text
from utils.db import get_engine, get_engine_prod
from utils.data import load_df_pap_note_max_by_collectivite

# Configuration de la page
st.set_page_config(
    page_title="Implication des Conseillers",
    page_icon="👥",
    layout="wide"
)

st.title("👥 Tableau de Bord - Implication des Conseillers")
st.markdown("""
Ce tableau de bord permet de suivre l'implication des conseillers sur les collectivités.
Visualisez les collectivités suivies, les notes PAP associées et les statistiques d'activité.
""")

st.info("💡 Les données peuvent prendre un certain temps à charger...")
st.markdown("---")

# ==========================
# FONCTIONS
# ==========================

@st.cache_data(ttl=3600)
def charger_conseillers_collectivites(show_spinner="⏳ Chargement des conseillers et collectivités..."):
    """Charge la liste des conseillers avec leurs collectivités depuis la base de production."""
    try:
        engine = get_engine_prod()
        
        query = text("""
            SELECT 
                u.email,
                pcm.user_id,
                c.id as collectivite_id,
                c.nom as nom_collectivite,
                c.type as type_collectivite
            FROM private_collectivite_membre pcm
            JOIN auth.users u ON pcm.user_id = u.id
            JOIN collectivite c ON pcm.collectivite_id = c.id
            WHERE pcm.fonction = 'conseiller'
                AND c.type <> 'test'
            ORDER BY u.email, c.nom
        """)
        
        with engine.connect() as conn:
            df = pd.read_sql_query(query, conn)
        
        return df
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des conseillers : {str(e)}")
        return pd.DataFrame()


@st.cache_data(ttl=3600)
def charger_stats_modifications_conseillers(show_spinner="⏳ Chargement des statistiques d'activité..."):
    """Charge les stats de modifications par conseiller depuis la base de production."""
    try:
        engine = get_engine_prod()
        
        query = text("""
            WITH all_comments AS (
                SELECT collectivite_id, modified_by, action_id
                FROM historique.action_statut 
                
                UNION ALL
                
                SELECT collectivite_id, modified_by, action_id
                FROM action_commentaire
            )
            
            SELECT 
                email, 
                COUNT(DISTINCT ac.collectivite_id) as nb_collectivite, 
                COUNT(DISTINCT action_id) as nb_mesures_modifies,
                COUNT(*) as nb_modifications
            FROM all_comments ac
            JOIN auth.users u ON ac.modified_by = u.id
            JOIN private_collectivite_membre pcm ON pcm.user_id = u.id
            WHERE pcm.fonction = 'conseiller'
            GROUP BY email
            ORDER BY COUNT(DISTINCT ac.collectivite_id) DESC, COUNT(DISTINCT action_id) DESC
        """)
        
        with engine.connect() as conn:
            df = pd.read_sql_query(query, conn)
        
        return df
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des statistiques : {str(e)}")
        return pd.DataFrame()


@st.cache_data(ttl=3600)
def charger_collectivites_avec_pap(show_spinner="⏳ Chargement des collectivités avec PAP..."):
    """Charge les collectivités ayant un PAP depuis la base OLAP."""
    try:
        df = load_df_pap_note_max_by_collectivite()
        return df
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des PAP : {str(e)}")
        return pd.DataFrame()


# ==========================
# CHARGEMENT DES DONNÉES
# ==========================

df_conseillers = charger_conseillers_collectivites()
df_stats = charger_stats_modifications_conseillers()
df_pap = charger_collectivites_avec_pap()

if df_conseillers.empty:
    st.error("❌ Impossible de charger les données des conseillers")
    st.stop()

# ==========================
# STATISTIQUES GÉNÉRALES
# ==========================

st.header("📈 Vue d'ensemble")

col1, col2, col3, col4 = st.columns(4)

with col1:
    nb_conseillers = df_conseillers['email'].nunique()
    st.metric("👥 Conseillers actifs", nb_conseillers)

with col2:
    nb_collectivites_suivies = df_conseillers['collectivite_id'].nunique()
    st.metric("🏛️ Collectivités suivies", nb_collectivites_suivies)

with col3:
    avg_collectivites_par_conseiller = round(df_conseillers.groupby('email')['collectivite_id'].nunique().mean(), 1)
    st.metric("📊 Moyenne collectivités/conseiller", f"{avg_collectivites_par_conseiller}")

with col4:
    # Collectivités avec PAP mais sans conseiller
    if not df_pap.empty:
        collectivites_pap_ids = set(df_pap['collectivite_id'].unique())
        collectivites_conseiller_ids = set(df_conseillers['collectivite_id'].unique())
        nb_sans_conseiller = len(collectivites_pap_ids - collectivites_conseiller_ids)
        st.metric("⚠️ Collectivités PAP sans conseiller", nb_sans_conseiller)
    else:
        st.metric("⚠️ Collectivités PAP sans conseiller", "N/A")

st.markdown("---")

# ==========================
# ONGLETS
# ==========================

tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Collectivités par conseiller", 
    "📊 Statistiques d'activité", 
    "⚠️ Collectivités sans conseiller",
    "🎯 Vue détaillée par conseiller"
])

# ==========================
# ONGLET 1: COLLECTIVITÉS PAR CONSEILLER
# ==========================

with tab1:
    st.header("📋 Collectivités suivies par conseiller")
    
    # Fusion avec les notes PAP
    df_conseillers_pap = df_conseillers.merge(
        df_pap[['collectivite_id', 'nom_plan', 'score_pap', 'derniere_semaine']],
        on='collectivite_id',
        how='left'
    )
    
    # Créer un tableau agrégé
    df_agg = df_conseillers_pap.groupby('email').agg({
        'collectivite_id': 'count',
        'score_pap': ['max', 'mean']
    }).reset_index()
    
    df_agg.columns = ['Email', 'Nb Collectivités', 'Score PAP Max', 'Score PAP Moyen']
    df_agg['Score PAP Moyen'] = df_agg['Score PAP Moyen'].round(1)
    
    # Trier par nombre de collectivités
    df_agg = df_agg.sort_values('Nb Collectivités', ascending=False)
    
    st.dataframe(
        df_agg,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Email": st.column_config.TextColumn("📧 Email", width="large"),
            "Nb Collectivités": st.column_config.NumberColumn("🏛️ Nombre de collectivités", format="%d"),
            "Score PAP Max": st.column_config.NumberColumn("🎯 Score PAP Max", format="%.1f"),
            "Score PAP Moyen": st.column_config.NumberColumn("📊 Score PAP Moyen", format="%.1f"),
        }
    )
    
    st.markdown("---")
    
    # Détail par conseiller
    st.subheader("🔍 Détail des collectivités par conseiller")
    
    conseiller_selectionne = st.selectbox(
        "Sélectionnez un conseiller",
        options=sorted(df_conseillers['email'].unique()),
        key="conseiller_tab1"
    )
    
    if conseiller_selectionne:
        df_detail = df_conseillers_pap[df_conseillers_pap['email'] == conseiller_selectionne].copy()
        df_detail = df_detail.sort_values('score_pap', ascending=False, na_position='last')
        
        st.write(f"**{len(df_detail)}** collectivités suivies par **{conseiller_selectionne}**")
        
        st.dataframe(
            df_detail[['nom_collectivite', 'type_collectivite', 'nom_plan', 'score_pap', 'derniere_semaine']],
            use_container_width=True,
            hide_index=True,
            column_config={
                "nom_collectivite": st.column_config.TextColumn("🏛️ Collectivité", width="large"),
                "type_collectivite": st.column_config.TextColumn("📑 Type", width="small"),
                "nom_plan": st.column_config.TextColumn("📋 Plan PAP", width="medium"),
                "score_pap": st.column_config.NumberColumn("🎯 Score PAP", format="%.1f"),
                "derniere_semaine": st.column_config.DateColumn("📅 Dernière semaine", format="DD/MM/YYYY"),
            }
        )

# ==========================
# ONGLET 2: STATISTIQUES D'ACTIVITÉ
# ==========================

with tab2:
    st.header("📊 Statistiques d'activité des conseillers")
    
    if not df_stats.empty:
        st.write("""
        Ces statistiques montrent l'activité des conseillers sur la plateforme, 
        basées sur les modifications d'actions et les commentaires.
        """)
        
        # Renommer les colonnes pour l'affichage
        df_stats_display = df_stats.copy()
        df_stats_display.columns = [
            'Email',
            'Nb Collectivités',
            'Nb Mesures modifiées',
            'Nb Modifications'
        ]
        
        st.dataframe(
            df_stats_display,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Email": st.column_config.TextColumn("📧 Email", width="large"),
                "Nb Collectivités": st.column_config.NumberColumn("🏛️ Collectivités", format="%d"),
                "Nb Mesures modifiées": st.column_config.NumberColumn("📝 Mesures modifiées", format="%d"),
                "Nb Modifications": st.column_config.NumberColumn("✏️ Total modifications", format="%d"),
            }
        )
        
        # Statistiques agrégées
        st.markdown("---")
        st.subheader("📈 Statistiques globales")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_modifications = df_stats['nb_modifications'].sum()
            st.metric("✏️ Total modifications", f"{total_modifications:,.0f}")
        
        with col2:
            total_mesures = df_stats['nb_mesures_modifies'].sum()
            st.metric("📝 Total mesures modifiées", f"{total_mesures:,.0f}")
        
        with col3:
            avg_modifications = round(df_stats['nb_modifications'].mean(), 0)
            st.metric("📊 Moyenne modifications/conseiller", f"{avg_modifications:,.0f}")
    else:
        st.warning("⚠️ Aucune statistique d'activité disponible")

# ==========================
# ONGLET 3: COLLECTIVITÉS SANS CONSEILLER
# ==========================

with tab3:
    st.header("⚠️ Collectivités avec PAP mais sans conseiller")
    
    if not df_pap.empty:
        # Identifier les collectivités sans conseiller
        collectivites_pap_ids = set(df_pap['collectivite_id'].unique())
        collectivites_conseiller_ids = set(df_conseillers['collectivite_id'].unique())
        collectivites_sans_conseiller_ids = collectivites_pap_ids - collectivites_conseiller_ids
        
        if collectivites_sans_conseiller_ids:
            df_sans_conseiller = df_pap[df_pap['collectivite_id'].isin(collectivites_sans_conseiller_ids)].copy()
            df_sans_conseiller = df_sans_conseiller.sort_values('score_pap', ascending=False)
            
            st.write(f"**{len(df_sans_conseiller)}** collectivités ont un PAP mais ne sont suivies par aucun conseiller")
            
            st.dataframe(
                df_sans_conseiller[['collectivite_id', 'nom_collectivite', 'nom_plan', 'score_pap', 'derniere_semaine']],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "collectivite_id": st.column_config.NumberColumn("🆔 ID", format="%d"),
                    "nom_collectivite": st.column_config.TextColumn("🏛️ Collectivité", width="large"),
                    "nom_plan": st.column_config.TextColumn("📋 Plan PAP", width="medium"),
                    "score_pap": st.column_config.NumberColumn("🎯 Score PAP", format="%.1f"),
                    "derniere_semaine": st.column_config.DateColumn("📅 Dernière semaine", format="DD/MM/YYYY"),
                }
            )
            
            # Statistiques
            st.markdown("---")
            st.subheader("📊 Statistiques")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                score_moyen = round(df_sans_conseiller['score_pap'].mean(), 1)
                st.metric("📊 Score PAP moyen", f"{score_moyen}")
            
            with col2:
                score_max = round(df_sans_conseiller['score_pap'].max(), 1)
                st.metric("🎯 Score PAP maximum", f"{score_max}")
            
            with col3:
                pct_sans_conseiller = round(len(collectivites_sans_conseiller_ids) / len(collectivites_pap_ids) * 100, 1)
                st.metric("📈 % sans conseiller", f"{pct_sans_conseiller}%")
        else:
            st.success("✅ Toutes les collectivités avec PAP ont un conseiller assigné")
    else:
        st.warning("⚠️ Aucune donnée PAP disponible")

# ==========================
# ONGLET 4: VUE DÉTAILLÉE PAR CONSEILLER
# ==========================

with tab4:
    st.header("🎯 Vue détaillée par conseiller")
    
    conseiller_selectionne = st.selectbox(
        "Sélectionnez un conseiller pour voir le détail",
        options=sorted(df_conseillers['email'].unique()),
        key="conseiller_tab4"
    )
    
    if conseiller_selectionne:
        # Fusion des données
        df_conseiller_detail = df_conseillers[df_conseillers['email'] == conseiller_selectionne].copy()
        df_conseiller_detail = df_conseiller_detail.merge(
            df_pap[['collectivite_id', 'nom_plan', 'score_pap', 'derniere_semaine']],
            on='collectivite_id',
            how='left'
        )
        
        # Stats du conseiller
        stats_conseiller = None
        if not df_stats.empty:
            stats_conseiller = df_stats[df_stats['email'] == conseiller_selectionne]
        
        # Affichage des métriques
        st.subheader(f"📊 Statistiques de {conseiller_selectionne}")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            nb_collectivites = len(df_conseiller_detail)
            st.metric("🏛️ Collectivités suivies", nb_collectivites)
        
        with col2:
            if not stats_conseiller.empty:
                nb_modif = stats_conseiller['nb_modifications'].values[0]
                st.metric("✏️ Modifications", f"{nb_modif:,.0f}")
            else:
                st.metric("✏️ Modifications", "N/A")
        
        with col3:
            if not stats_conseiller.empty:
                nb_mesures = stats_conseiller['nb_mesures_modifies'].values[0]
                st.metric("📝 Mesures modifiées", f"{nb_mesures:,.0f}")
            else:
                st.metric("📝 Mesures modifiées", "N/A")
        
        with col4:
            score_moyen = df_conseiller_detail['score_pap'].mean()
            if pd.notna(score_moyen):
                st.metric("📊 Score PAP moyen", f"{score_moyen:.1f}")
            else:
                st.metric("📊 Score PAP moyen", "N/A")
        
        st.markdown("---")
        
        # Tableau des collectivités
        st.subheader(f"📋 Collectivités suivies")
        
        df_conseiller_detail_sorted = df_conseiller_detail.sort_values('score_pap', ascending=False, na_position='last')
        
        st.dataframe(
            df_conseiller_detail_sorted[['nom_collectivite', 'type_collectivite', 'nom_plan', 'score_pap', 'derniere_semaine']],
            use_container_width=True,
            hide_index=True,
            height=600,
            column_config={
                "nom_collectivite": st.column_config.TextColumn("🏛️ Collectivité", width="large"),
                "type_collectivite": st.column_config.TextColumn("📑 Type", width="small"),
                "nom_plan": st.column_config.TextColumn("📋 Plan PAP", width="medium"),
                "score_pap": st.column_config.NumberColumn("🎯 Score PAP", format="%.1f"),
                "derniere_semaine": st.column_config.DateColumn("📅 Dernière semaine", format="DD/MM/YYYY"),
            }
        )

st.markdown("---")
st.caption("💡 Données mises à jour depuis la base de production et la base OLAP")

