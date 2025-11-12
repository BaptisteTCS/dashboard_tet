import streamlit as st
import pandas as pd
from datetime import datetime, date
from utils.data import load_df_analyse_campagne_region, load_df_campagne_region_reached

# Configuration de la page
st.set_page_config(
    page_title="Suivi Campagne Régions",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Suivi Campagne des Régions")
st.markdown("""
Ce tableau de bord permet de suivre l'activité et l'engagement des collectivités 
dans le cadre de la campagne régionale.
""")

st.markdown("---")

# ==========================
# FONCTIONS
# ==========================

@st.cache_data(ttl=3600)
def charger_donnees_campagne(show_spinner="⏳ Chargement des données de campagne..."):
    """Charge les données d'analyse de campagne."""
    try:
        df = load_df_analyse_campagne_region()
        # Convertir 'day' en datetime si ce n'est pas déjà fait et retirer la timezone
        if 'day' in df.columns:
            # Convertir en datetime
            df['day'] = pd.to_datetime(df['day'], errors='coerce')
            # Retirer la timezone si elle existe
            if pd.api.types.is_datetime64_any_dtype(df['day']):
                try:
                    # Vérifier si la colonne a une timezone
                    if hasattr(df['day'].dtype, 'tz') and df['day'].dtype.tz is not None:
                        df['day'] = df['day'].dt.tz_localize(None)
                except (AttributeError, TypeError):
                    # Si ça échoue, la colonne n'a probablement pas de timezone
                    pass
        return df
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des données de campagne : {str(e)}")
        return pd.DataFrame()


@st.cache_data(ttl=3600)
def charger_collectivites_reached(show_spinner="⏳ Chargement des collectivités reached..."):
    """Charge la liste des collectivités reached."""
    try:
        df = load_df_campagne_region_reached()
        return df
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des collectivités reached : {str(e)}")
        return pd.DataFrame()


# ==========================
# CHARGEMENT DES DONNÉES
# ==========================

df_campagne = charger_donnees_campagne()
df_reached = charger_collectivites_reached()

if df_campagne.empty:
    st.error("❌ Impossible de charger les données de campagne")
    st.stop()

# ==========================
# SÉLECTION DE LA RÉGION
# ==========================

st.header("🔎 Sélectionnez une région et période")

col1, col2, col3 = st.columns(3)

with col1:

    # Liste des régions disponibles
    regions = sorted(df_campagne['region_name'].dropna().unique())

    selected_region = st.selectbox(
        "🌍 Région",
        options=regions,
        index=0 if regions else None,
        help="Sélectionnez une région pour afficher les statistiques"
    )

    if not selected_region:
        st.warning("⚠️ Aucune région sélectionnée")
        st.stop()

# ==========================
# SÉLECTION DE LA PÉRIODE
# ==========================

# Date par défaut : du 22-09-2025 à aujourd'hui
date_debut_default = date(2025, 9, 22)
date_fin_default = date.today()

with col2:
    date_debut = st.date_input(
        "Date de début",
        value=date_debut_default,
        help="Date de début de la période d'analyse"
    )

with col3:
    date_fin = st.date_input(
        "Date de fin",
        value=date_fin_default,
        help="Date de fin de la période d'analyse"
    )

# Validation des dates
if date_debut > date_fin:
    st.error("❌ La date de début doit être antérieure à la date de fin")
    st.stop()

st.markdown("---")

# ==========================
# FILTRAGE DES DONNÉES
# ==========================

# Filtrer par région
df_region = df_campagne[df_campagne['region_name'] == selected_region].copy()

# Filtrer les CT reached pour cette région (depuis campagne_region_reached)
# C'est la source de vérité pour le nombre de CT reached et les plans/FA créés
df_reached_region = df_reached[df_reached['region_name'] == selected_region].copy()
collectivites_reached_region = set(df_reached_region['collectivite_id'].unique())

# Filtrer par période (convertir les dates en datetime tz-naive)
date_debut_ts = datetime.combine(date_debut, datetime.min.time())
date_fin_ts = datetime.combine(date_fin, datetime.max.time())

# Filtrer df_campagne (pageviews) par période
df_region_filtered = df_region[
    (df_region['day'] >= date_debut_ts) &
    (df_region['day'] <= date_fin_ts)
].copy()

# Note: On ne fait pas de st.stop() ici car on peut avoir des CT reached sans activité
if df_region_filtered.empty and len(collectivites_reached_region) == 0:
    st.warning(f"⚠️ Aucune donnée disponible pour la région **{selected_region}**")
    st.stop()

# ==========================
# STATISTIQUES GÉNÉRALES
# ==========================

st.header("📈 Vue d'ensemble")

col1, col2, col3, col4 = st.columns(4)

with col1:
    nb_reached = len(collectivites_reached_region)
    st.metric("🎯 Collectivités reached", nb_reached)

with col2:
    # Collectivités avec au moins une pageview
    ct_avec_pageviews = df_region_filtered[df_region_filtered['nb_pageviews'] > 0]['collectivite_id'].nunique()
    st.metric("👀 CT avec pageviews", ct_avec_pageviews)

with col3:
    # Collectivités avec au moins un plan créé (depuis campagne_region_reached)
    ct_avec_plans = df_reached_region[df_reached_region['nb_plans_crees'] > 0]['collectivite_id'].nunique() if 'nb_plans_crees' in df_reached_region.columns else 0
    st.metric("📋 CT avec plan créé", ct_avec_plans)

with col4:
    # Collectivités avec au moins une FA créée (depuis campagne_region_reached)
    ct_avec_fa = df_reached_region[df_reached_region['nb_fa_crees'] > 0]['collectivite_id'].nunique() if 'nb_fa_crees' in df_reached_region.columns else 0
    st.metric("✅ CT avec FA créées", ct_avec_fa)


# ==========================
# ONGLETS
# ==========================

tab1, tab2 = st.tabs([
    "📊 Activité par collectivité",
    "👥 Utilisateurs connectés par collectivité"
])

# ==========================
# ONGLET 1: ACTIVITÉ PAR COLLECTIVITÉ
# ==========================

with tab1:
    st.header("📊 Activité par collectivité")
    
    # Agréger les pageviews par collectivité depuis analyse_campagne_region
    df_agg_pageviews = df_region_filtered.groupby(['collectivite_id', 'nom_ct']).agg({
        'nb_pageviews': 'sum'
    }).reset_index()
    
    # Agréger les plans et FA depuis campagne_region_reached
    if not df_reached_region.empty and 'nb_plans_crees' in df_reached_region.columns and 'nb_fa_crees' in df_reached_region.columns:
        df_agg_plans_fa = df_reached_region.groupby(['collectivite_id']).agg({
            'nb_plans_crees': 'sum',
            'nb_fa_crees': 'sum'
        }).reset_index()
    else:
        df_agg_plans_fa = pd.DataFrame(columns=['collectivite_id', 'nb_plans_crees', 'nb_fa_crees'])
    
    # Merger les deux sources de données
    df_agg_ct = df_agg_pageviews.merge(
        df_agg_plans_fa,
        on='collectivite_id',
        how='left'
    )
    
    # Remplir les valeurs manquantes par 0
    df_agg_ct['nb_plans_crees'] = df_agg_ct['nb_plans_crees'].fillna(0).astype(int)
    df_agg_ct['nb_fa_crees'] = df_agg_ct['nb_fa_crees'].fillna(0).astype(int)
    
    # Trier par nombre de pageviews décroissant
    df_agg_ct = df_agg_ct.sort_values('nb_pageviews', ascending=False)
    
    # Renommer les colonnes pour l'affichage
    df_agg_ct_display = df_agg_ct.copy()
    df_agg_ct_display.columns = [
        'ID Collectivité',
        'Collectivité',
        'Nb Pageviews',
        'Nb Plans créés',
        'Nb FA créées'
    ]
    
    st.write(f"**{len(df_agg_ct)}** collectivités dans la région **{selected_region}**")
    
    st.dataframe(
        df_agg_ct_display,
        use_container_width=True,
        hide_index=True,
        height=300,
        column_config={
            "ID Collectivité": st.column_config.NumberColumn("🆔 ID", format="%d"),
            "Collectivité": st.column_config.TextColumn("🏛️ Collectivité", width="large"),
            "Nb Pageviews": st.column_config.NumberColumn("👀 Pageviews", format="%d"),
            "Nb Plans créés": st.column_config.NumberColumn("📋 Plans créés", format="%d"),
            "Nb FA créées": st.column_config.NumberColumn("✅ FA créées", format="%d")
        }
    )
    
    # Statistiques sur les données affichées
    st.markdown("---")
    st.subheader("📈 Statistiques sur la sélection")
    
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    
    with col_stat1:
        total_pageviews = df_agg_ct_display['Nb Pageviews'].sum()
        st.metric("👀 Total pageviews", f"{total_pageviews:,.0f}")
    
    with col_stat2:
        total_plans = df_agg_ct_display['Nb Plans créés'].sum()
        st.metric("📋 Total plans créés", f"{total_plans:,.0f}")
    
    with col_stat3:
        total_fa = df_agg_ct_display['Nb FA créées'].sum()
        st.metric("✅ Total FA créées", f"{total_fa:,.0f}")

# ==========================
# ONGLET 2: UTILISATEURS PAR COLLECTIVITÉ
# ==========================

with tab2:
    st.header("👥 Utilisateurs connectés par collectivité")
    
    # Filtrer les données pour ne garder que celles avec un email
    df_avec_email = df_region_filtered[df_region_filtered['email'].notna()].copy()
    
    if df_avec_email.empty:
        st.warning("⚠️ Aucun utilisateur connecté trouvé pour cette région et cette période")
    else:
        # Agréger par collectivité et email
        df_users = df_avec_email.groupby(['collectivite_id', 'nom_ct', 'email']).agg({
            'nb_pageviews': 'sum',
            'day': 'count'  # Nombre de jours d'activité
        }).reset_index()
        
        df_users.columns = ['collectivite_id', 'nom_ct', 'email', 'nb_pageviews', 'nb_jours_actifs']
        
        # Ajouter une colonne pour indiquer si la CT est reached
        df_users['reached'] = df_users['collectivite_id'].isin(collectivites_reached_region)
        
        # Trier par collectivité puis par nombre de pageviews
        df_users = df_users.sort_values(['nom_ct', 'nb_pageviews'], ascending=[True, False])
        
        st.write(f"**{df_users['email'].nunique()}** utilisateurs uniques sur **{df_users['collectivite_id'].nunique()}** collectivités")
        
        # Sélecteur de collectivité
        collectivites_list = ['Toutes'] + sorted(df_users['nom_ct'].unique().tolist())
        selected_ct = st.selectbox(
            "Filtrer par collectivité",
            options=collectivites_list,
            key="ct_filter"
        )
        
        # Appliquer le filtre
        df_users_display = df_users.copy()
        
        if selected_ct != 'Toutes':
            df_users_display = df_users_display[df_users_display['nom_ct'] == selected_ct]
        
        # Renommer pour l'affichage
        df_users_display_final = df_users_display[['nom_ct', 'email', 'nb_pageviews', 'nb_jours_actifs']].copy()
        df_users_display_final.columns = ['Collectivité', 'Email', 'Nb Pageviews', 'Nb Jours actifs']
        
        st.dataframe(
            df_users_display_final,
            use_container_width=True,
            hide_index=True,
            height=300,
            column_config={
                "Collectivité": st.column_config.TextColumn("🏛️ Collectivité", width="large"),
                "Email": st.column_config.TextColumn("📧 Email", width="large"),
                "Nb Pageviews": st.column_config.NumberColumn("👀 Pageviews", format="%d"),
                "Nb Jours actifs": st.column_config.NumberColumn("📅 Jours actifs", format="%d")
            }
        )
        
        # Statistiques
        st.markdown("---")
        st.subheader("📈 Statistiques des utilisateurs")
        
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        
        with col_stat1:
            nb_users = df_users_display['email'].nunique()
            st.metric("👥 Utilisateurs uniques", nb_users)
        
        with col_stat2:
            nb_ct = df_users_display['collectivite_id'].nunique()
            st.metric("🏛️ Collectivités", nb_ct)
        
        with col_stat3:
            avg_pageviews = df_users_display['nb_pageviews'].mean()
            st.metric("📊 Pageviews moyen/utilisateur", f"{avg_pageviews:.1f}")

