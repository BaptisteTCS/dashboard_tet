import streamlit as st
import pandas as pd
import requests
import time
from sqlalchemy import text
from utils.db import get_engine, get_engine_pre_prod

# Configuration de la page
st.set_page_config(layout="wide")
st.title("🚢 Livraison des indicateurs")

st.markdown("""
Cette page compare les données **staging** (table `indicateurs_valeurs_olap`) 
avec les données en **pré-production** (table `indicateur_valeur`) pour identifier :
- 🆕 Les nouveaux indicateurs à importer
- 📅 Les nouvelles années pour des indicateurs existants
- 🔄 Les données à mettre à jour
""")

st.markdown("---")

# ==========================
# FONCTIONS
# ==========================

def load_staged_data():
    """Charge les données de la table indicateurs_valeurs_olap."""
    engine = get_engine()
    
    try:
        query = text("""
            SELECT 
                collectivite_id,
                indicateur_id,
                metadonnee_id,
                date_valeur,
                resultat
            FROM indicateurs_valeurs_olap
        """)
        
        with engine.connect() as conn:
            df = pd.read_sql_query(query, conn)
        
        # Convertir explicitement date_valeur en datetime
        df['date_valeur'] = pd.to_datetime(df['date_valeur'])
        
        return df
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des données staging : {str(e)}")
        return pd.DataFrame()


def load_indicateurs_titres():
    """Charge le mapping id -> titre des indicateurs depuis la pré-prod."""
    engine_preprod = get_engine_pre_prod()
    
    try:
        query = text("""
            SELECT DISTINCT id, titre
            FROM indicateur_definition
            WHERE collectivite_id IS NULL
        """)
        
        with engine_preprod.connect() as conn:
            df = pd.read_sql_query(query, conn)
        
        # Créer un dictionnaire pour le mapping
        mapping = dict(zip(df['id'], df['titre']))
        
        return mapping
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des titres d'indicateurs : {str(e)}")
        return {}


def load_preprod_data(df_staged):
    """Charge les données de la table indicateur_valeur en pré-prod.
    
    Ne charge QUE les données correspondant aux clés primaires présentes dans le staging
    pour optimiser les performances sur les grosses tables.
    
    Args:
        df_staged: DataFrame staging pour extraire les clés primaires à charger
    """
    engine_preprod = get_engine_pre_prod()
    
    if df_staged.empty:
        return pd.DataFrame()
    
    try:
        # Extraire les valeurs uniques pour chaque colonne de la clé primaire
        indicateurs_ids = df_staged['indicateur_id'].unique().tolist()
        collectivite_ids = df_staged['collectivite_id'].unique().tolist()
        metadonnee_ids = df_staged['metadonnee_id'].unique().tolist()
        
        st.info(f"🔍 Filtrage pré-prod : {len(indicateurs_ids)} indicateurs, {len(collectivite_ids)} collectivités, {len(metadonnee_ids)} métadonnées")
        
        # Requête avec filtres sur les clés primaires - ne charger que les colonnes nécessaires
        query = text("""
            SELECT 
                collectivite_id,
                indicateur_id,
                metadonnee_id,
                date_valeur,
                resultat
            FROM indicateur_valeur
            WHERE indicateur_id = ANY(:indicateurs_ids)
              AND collectivite_id = ANY(:collectivite_ids)
              AND metadonnee_id = ANY(:metadonnee_ids)
        """)
        
        with engine_preprod.connect() as conn:
            df = pd.read_sql_query(
                query, 
                conn, 
                params={
                    'indicateurs_ids': indicateurs_ids,
                    'collectivite_ids': collectivite_ids,
                    'metadonnee_ids': metadonnee_ids
                }
            )
        
        # Convertir explicitement date_valeur en datetime
        df['date_valeur'] = pd.to_datetime(df['date_valeur'])
        
        st.success(f"✅ {len(df):,} lignes chargées depuis la pré-prod")
        
        return df
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des données pré-prod : {str(e)}")
        return pd.DataFrame()


def livrer_en_preprod(comparison, df_staged, progress_container=None):
    """Fait l'upsert des données staging vers la pré-prod via API.
    
    N'envoie que les données qui ont vraiment changé :
    - Nouveaux indicateurs
    - Nouvelles années
    - Données avec résultats différents
    
    Args:
        comparison: Résultats de la comparaison staging vs pré-prod
        df_staged: DataFrame contenant toutes les données staging
        progress_container: Container Streamlit pour afficher la progression
    
    Returns:
        dict: Statistiques de la livraison
    """
    # Construire le DataFrame des données à envoyer
    dfs_to_send = []
    
    # 1. Nouveaux indicateurs
    if len(comparison['nouveaux_indicateurs']) > 0:
        dfs_to_send.append(comparison['nouveaux_indicateurs'])
    
    # 2. Nouvelles années
    if len(comparison['nouvelles_annees']) > 0:
        dfs_to_send.append(comparison['nouvelles_annees'])
    
    # 3. Données à updater (extraire depuis les dataframes par indicateur)
    for indic_id, stats in comparison['donnees_a_updater'].items():
        if 'dataframe' in stats:
            df_update = stats['dataframe'].copy()
            # Sélectionner les colonnes nécessaires et renommer
            df_update = df_update[['collectivite_id', 'indicateur_id', 'metadonnee_id', 'date_valeur', 'resultat_staged']]
            df_update = df_update.rename(columns={'resultat_staged': 'resultat'})
            dfs_to_send.append(df_update)
    
    # Concaténer toutes les données à envoyer
    if not dfs_to_send:
        return {'nb_total': 0, 'success': True, 'message': 'Aucune donnée à livrer (tout est déjà à jour)'}
    
    df_to_send = pd.concat(dfs_to_send, ignore_index=True)
    
    try:
        # Récupérer les credentials depuis les secrets
        try:
            api_url = st.secrets.get("api_pre_prod_url", "https://api.preprod.territoiresentransitions.fr/indicateurs/valeurs")
            api_token = st.secrets.get("api_pre_prod_token", "")
        except:
            return {
                'nb_total': 0,
                'success': False,
                'message': 'Configuration API manquante dans secrets.toml'
            }
        
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        
        # 1. Préparer la liste de dicts à partir du DataFrame
        df_to_insert = df_to_send.copy()
        df_to_insert['date_valeur'] = pd.to_datetime(df_to_insert['date_valeur'])
        
        valeurs_payload = df_to_insert.apply(lambda row: {
            "collectiviteId": int(row["collectivite_id"]),
            "indicateurId": int(row["indicateur_id"]),
            "dateValeur": row["date_valeur"].isoformat(),
            "metadonneeId": int(row["metadonnee_id"]),
            "resultat": float(row["resultat"]) if pd.notnull(row["resultat"]) else None,
        }, axis=1).tolist()

        print(f"{valeurs_payload}")
        
        # 2. Paramétrage du batch
        batch_size = 500
        total_rows = len(valeurs_payload)
        total_inserted = 0
        failed_batches = 0
        
        max_batches_per_minute = 90
        pause_seconds = 60
        
        # Calculer le nombre total de batches
        total_batches = (total_rows + batch_size - 1) // batch_size
        
        if progress_container:
            progress_bar = progress_container.progress(0)
            status_text = progress_container.empty()
        
        # 3. Envoi des batchs
        for batch_start in range(0, total_rows, batch_size):
            batch_num = batch_start // batch_size + 1
            
            # Pause si on atteint un multiple de 90 (sauf au tout début)
            if batch_num > 1 and (batch_num - 1) % max_batches_per_minute == 0:
                if progress_container:
                    status_text.info(f"⏸️ Pause de {pause_seconds}s pour respecter la limite de 90 requêtes/minute...")
                time.sleep(pause_seconds)
            
            batch = valeurs_payload[batch_start : batch_start + batch_size]
            payload = {"valeurs": batch}
            
            if progress_container:
                status_text.text(f"📤 Envoi du batch {batch_num}/{total_batches} ({len(batch)} lignes)...")
            
            response = requests.post(api_url, headers=headers, json=payload)
            
            if response.status_code == 201:
                # Si l'API renvoie un objet { "valeurs": [...] }
                try:
                    inserted = len(response.json().get("valeurs", []))
                except ValueError:
                    inserted = len(batch)
                total_inserted += inserted
                
                if progress_container:
                    status_text.success(f"✅ Batch {batch_num}/{total_batches} OK ({inserted} lignes)")
            else:
                failed_batches += 1
                
                # Logger l'erreur dans la console
                #print(f"\n{'='*80}")
                #print(f"❌ ERREUR - Batch {batch_num}/{total_batches} échoué (HTTP {response.status_code})")
                #print(f"{'='*80}")
                
                #try:
                    #error_json = response.json()
                    #print("Réponse API (JSON):")
                    #import json
                    #print(json.dumps(error_json, indent=2, ensure_ascii=False))
                # except:
                    #print("Réponse serveur (texte):")
                    #print(response.text)
                
                #print(f"{'='*80}\n")
                
                if progress_container:
                    status_text.error(f"❌ Batch {batch_num}/{total_batches} échoué (HTTP {response.status_code}) - voir console pour détails")
                
                # On continue même en cas d'erreur sur un batch
            
            # Mettre à jour la barre de progression
            if progress_container:
                progress_bar.progress(batch_num / total_batches)
        
        if progress_container:
            status_text.empty()
            progress_bar.empty()
        
        success = failed_batches == 0
        message = 'Livraison réussie' if success else f'Livraison partielle ({failed_batches} batch(s) échoué(s))'
        
        return {
            'nb_total': total_rows,
            'nb_inserted': total_inserted,
            'nb_batches': total_batches,
            'failed_batches': failed_batches,
            'success': success,
            'message': message
        }
        
    except Exception as e:
        return {
            'nb_total': 0,
            'nb_inserted': 0,
            'success': False,
            'message': f'Erreur lors de la livraison : {str(e)}'
        }


def compare_data(df_staged, df_preprod):
    """Compare les données staging et pré-prod avec une approche par merge.
    
    Returns:
        dict: {
            'nouveaux_indicateurs': DataFrame,
            'nouvelles_annees': DataFrame,
            'donnees_a_updater': dict with DataFrames by indicateur_id
        }
    """
    # Colonnes de la clé primaire
    pk_cols = ['collectivite_id', 'indicateur_id', 'metadonnee_id', 'date_valeur']
    
    df_staged = df_staged.copy()
    df_preprod = df_preprod.copy()
    
    # 1. NOUVEAUX INDICATEURS
    indicateurs_staged = set(df_staged['indicateur_id'].unique())
    indicateurs_preprod = set(df_preprod['indicateur_id'].unique())
    nouveaux_indicateurs_ids = indicateurs_staged - indicateurs_preprod
    
    df_nouveaux_indicateurs = df_staged[
        df_staged['indicateur_id'].isin(nouveaux_indicateurs_ids)
    ].copy()
    
    # 2. INDICATEURS EXISTANTS
    indicateurs_existants = indicateurs_staged & indicateurs_preprod
    
    # 3. NOUVELLES ANNÉES ET DONNÉES À UPDATER - par indicateur
    donnees_a_updater = {}
    all_nouvelles_annees = []
    
    for indic_id in indicateurs_existants:
        # Filtrer par indicateur
        df_staged_indic = df_staged[df_staged['indicateur_id'] == indic_id].copy()
        df_preprod_indic = df_preprod[df_preprod['indicateur_id'] == indic_id].copy()
        
        # Merge sur les clés primaires
        df_merge = df_staged_indic.merge(
            df_preprod_indic,
            on=pk_cols,
            how='outer',
            suffixes=('_staged', '_preprod'),
            indicator=True
        )
        
        # Nouvelles années : présent dans staging mais pas dans pre-prod
        df_nouvelles = df_merge[df_merge['_merge'] == 'left_only'].copy()
        if len(df_nouvelles) > 0:
            # Garder les colonnes staging (sans suffixe)
            cols_to_keep = pk_cols + [col for col in df_nouvelles.columns if col.endswith('_staged')]
            df_nouvelles = df_nouvelles[cols_to_keep].copy()
            # Renommer en enlevant le suffixe
            df_nouvelles.columns = [col.replace('_staged', '') for col in df_nouvelles.columns]
            all_nouvelles_annees.append(df_nouvelles)
        
        # Données à updater : présent dans les deux avec résultats différents
        df_both = df_merge[df_merge['_merge'] == 'both'].copy()
        
        if len(df_both) > 0:
            # Comparer les résultats
            df_both['resultat_diff'] = df_both['resultat_staged'] != df_both['resultat_preprod']
            df_diff = df_both[df_both['resultat_diff']].copy()
            
            if len(df_diff) > 0:
                # Calculer l'écart en %
                df_diff['ecart_abs'] = df_diff['resultat_staged'] - df_diff['resultat_preprod']
                
                # Écart en % (gérer division par zéro)
                df_diff['ecart_pct'] = 0.0
                mask_non_zero = df_diff['resultat_preprod'] != 0
                df_diff.loc[mask_non_zero, 'ecart_pct'] = (
                    abs(df_diff.loc[mask_non_zero, 'ecart_abs'] / df_diff.loc[mask_non_zero, 'resultat_preprod']) * 100
                ).round(0)
                
                # Pour les valeurs où pre-prod = 0 mais staged != 0
                mask_div_zero = (df_diff['resultat_preprod'] == 0) & (df_diff['resultat_staged'] != 0)
                df_diff.loc[mask_div_zero, 'ecart_pct'] = float('inf')
                
                # Sélectionner les colonnes pertinentes
                cols_result = pk_cols + ['resultat_preprod', 'resultat_staged', 'ecart_abs', 'ecart_pct']
                df_result = df_diff[cols_result].copy()
                
                # Calculer les statistiques
                df_result_finis = df_result[df_result['ecart_pct'] != float('inf')]
                
                if len(df_result_finis) > 0:
                    ecart_moyen = df_result_finis['ecart_pct'].mean()
                    idx_max = df_result_finis['ecart_pct'].idxmax()
                    max_row = df_result_finis.loc[idx_max]
                    
                    donnees_a_updater[indic_id] = {
                        'nb_lignes': len(df_result),
                        'ecart_moyen_pct': ecart_moyen,
                        'ecart_max_pct': max_row['ecart_pct'],
                        'collectivite_id_max': max_row['collectivite_id'],
                        'date_valeur_max': max_row['date_valeur'],
                        'resultat_preprod_max': max_row['resultat_preprod'],
                        'resultat_staged_max': max_row['resultat_staged'],
                        'dataframe': df_result.sort_values('ecart_pct', ascending=False)
                    }
                else:
                    # Tous les écarts sont des divisions par zéro
                    donnees_a_updater[indic_id] = {
                        'nb_lignes': len(df_result),
                        'ecart_moyen_pct': None,
                        'message': 'Tous les écarts sont de division par zéro',
                        'dataframe': df_result
                    }
    
    # Concaténer toutes les nouvelles années
    if all_nouvelles_annees:
        df_nouvelles_annees = pd.concat(all_nouvelles_annees, ignore_index=True)
    else:
        df_nouvelles_annees = pd.DataFrame()
    
    return {
        'nouveaux_indicateurs': df_nouveaux_indicateurs,
        'nouvelles_annees': df_nouvelles_annees,
        'donnees_a_updater': donnees_a_updater
    }


# ==========================
# INTERFACE
# ==========================

# Initialiser le session state
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
if 'df_staged' not in st.session_state:
    st.session_state.df_staged = None
if 'comparison' not in st.session_state:
    st.session_state.comparison = None
if 'indicateurs_titres' not in st.session_state:
    st.session_state.indicateurs_titres = {}

# Bouton pour lancer la comparaison
col_b1, col_b2, col_b3 = st.columns([2, 3, 2])
with col_b2:
    if st.button("🔍 Analyser les données à livrer", type="primary", use_container_width=True):
        
        with st.spinner("Chargement des titres d'indicateurs..."):
            # Charger le mapping id -> titre
            st.session_state.indicateurs_titres = load_indicateurs_titres()
        
        with st.spinner("Chargement des données staging..."):
            # Chargement des données staging d'abord
            st.session_state.df_staged = load_staged_data()
        
        if st.session_state.df_staged.empty:
            st.warning("⚠️ Aucune donnée dans la table staging `indicateurs_valeurs_olap`")
            st.session_state.analysis_done = False
            st.stop()
        
        with st.spinner("Chargement des données pré-prod (filtré)..."):
            # Chargement des données pré-prod avec filtre sur les clés primaires du staging
            df_preprod = load_preprod_data(st.session_state.df_staged)
        
        with st.spinner("Comparaison en cours..."):
            st.session_state.comparison = compare_data(st.session_state.df_staged, df_preprod)
        
        st.session_state.analysis_done = True

# Fonction helper pour formater l'affichage des indicateurs
def format_indicateur(indic_id):
    """Retourne 'Titre' ou juste 'ID' si pas de titre."""
    titre = st.session_state.indicateurs_titres.get(indic_id, None)
    if titre:
        return f"{titre}"
    return str(indic_id)

# Afficher les résultats si l'analyse a été faite
if st.session_state.analysis_done:
    df_staged = st.session_state.df_staged
    comparison = st.session_state.comparison
    
    # Statistiques globales
    st.markdown("---")
    st.markdown("## 📊 Statistiques globales")
    
    nb_indicateurs_staged = df_staged['indicateur_id'].nunique()
    nb_lignes_staged = len(df_staged)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📦 Indicateurs staged", nb_indicateurs_staged)
    with col2:
        st.metric("📝 Lignes totales staged", f"{nb_lignes_staged:,}")
    
    # Liste des indicateurs staged
    with st.expander("📋 Liste des indicateurs staged"):
        indicateurs_info = df_staged.groupby('indicateur_id').agg({
            'collectivite_id': 'nunique',
            'date_valeur': ['min', 'max', 'count']
        }).reset_index()
        indicateurs_info.columns = ['Indicateur ID', 'Nb collectivités', 'Date min', 'Date max', 'Nb lignes']
        
        # Ajouter le titre de l'indicateur
        indicateurs_info['Indicateur'] = indicateurs_info['Indicateur ID'].apply(format_indicateur)
        
        # Réorganiser les colonnes pour avoir le titre en premier
        indicateurs_info = indicateurs_info[['Indicateur', 'Nb collectivités', 'Date min', 'Date max', 'Nb lignes']]
        
        st.dataframe(indicateurs_info, use_container_width=True)
    
    # Comparaison
    st.markdown("---")
    st.markdown("## 🔄 Comparaison avec pré-production")
    
    # Affichage des résultats
    nb_nouveaux = len(comparison['nouveaux_indicateurs'])
    nb_nouvelles_annees = len(comparison['nouvelles_annees'])
    
    # Compter le nombre total de lignes à updater
    nb_updates = sum(stats['nb_lignes'] for stats in comparison['donnees_a_updater'].values())
    nb_indicateurs_updates = len(comparison['donnees_a_updater'])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🆕 Nouveaux indicateurs", nb_nouveaux)
    with col2:
        st.metric("📅 Nouvelles années", nb_nouvelles_annees)
    with col3:
        st.metric("🔄 Données à updater", f"{nb_updates} ({nb_indicateurs_updates} indic.)")
    
    # --- NOUVEAUX INDICATEURS ---
    if nb_nouveaux > 0:
        st.markdown("---")
        st.markdown("### 🆕 Nouveaux indicateurs à importer")
        st.info(f"Ces {nb_nouveaux} lignes correspondent à des indicateurs qui n'existent pas encore en pré-production.")
        
        # Grouper par indicateur
        indicateurs_nouveaux = comparison['nouveaux_indicateurs']['indicateur_id'].unique()
        
        for indic_id in indicateurs_nouveaux:
            df_indic = comparison['nouveaux_indicateurs'][
                comparison['nouveaux_indicateurs']['indicateur_id'] == indic_id
            ]
            
            nb_lignes = len(df_indic)
            nb_collectivites = df_indic['collectivite_id'].nunique()
            annees = sorted(df_indic['date_valeur'].dt.year.unique())
            
            with st.expander(
                f"📌 {format_indicateur(indic_id)} - {nb_lignes} lignes, {nb_collectivites} collectivités"
            ):
                st.markdown(f"**Années :** {', '.join(map(str, annees))}")
                st.dataframe(df_indic, use_container_width=True, height=300)
    
    # --- NOUVELLES ANNÉES ---
    if nb_nouvelles_annees > 0:
        st.markdown("---")
        st.markdown("### 📅 Nouvelles années à importer")
        st.info(f"Ces {nb_nouvelles_annees} lignes correspondent à de nouvelles années pour des indicateurs existants.")
        
        # Grouper par indicateur
        indicateurs_nouvelles_annees = comparison['nouvelles_annees']['indicateur_id'].unique()
        
        for indic_id in indicateurs_nouvelles_annees:
            df_indic = comparison['nouvelles_annees'][
                comparison['nouvelles_annees']['indicateur_id'] == indic_id
            ]
            
            nb_lignes = len(df_indic)
            nb_collectivites = df_indic['collectivite_id'].nunique()
            annees = sorted(df_indic['date_valeur'].dt.year.unique())
            
            with st.expander(
                f"📌 {format_indicateur(indic_id)} - {nb_lignes} nouvelles lignes, {nb_collectivites} collectivités"
            ):
                st.markdown(f"**Nouvelles années :** {', '.join(map(str, annees))}")
                st.dataframe(df_indic, use_container_width=True, height=300)
    
    # --- DONNÉES À UPDATER ---
    if nb_updates > 0:
        st.markdown("---")
        st.markdown("### 🔄 Données à mettre à jour")
        st.warning(f"Ces {nb_updates} lignes (sur {nb_indicateurs_updates} indicateurs) ont des résultats différents.")
        
        # Afficher par indicateur
        for indic_id, stats in comparison['donnees_a_updater'].items():
            with st.expander(f"📌 {format_indicateur(indic_id)} - {stats['nb_lignes']} ligne(s)", expanded=False):
                
                # Statistiques d'écart
                if stats.get('ecart_moyen_pct') is not None:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric(
                            "📊 Écart moyen", 
                            f"{stats['ecart_moyen_pct']:.0f}%",
                            help="Écart moyen en % pour cet indicateur"
                        )
                    
                    with col2:
                        st.metric(
                            "📈 Écart maximum", 
                            f"{stats['ecart_max_pct']:.0f}%",
                            help="Écart maximum observé pour cet indicateur"
                        )
                    
                    # Détail de l'écart maximum
                    st.markdown("**🔍 Écart maximum :**")
                    col_info1, col_info2 = st.columns(2)
                    with col_info1:
                        st.markdown(f"- **Collectivité ID:** {stats['collectivite_id_max']}")
                        st.markdown(f"- **Date:** {stats['date_valeur_max']}")
                    with col_info2:
                        st.markdown(f"- **Valeur pré-prod:** {stats['resultat_preprod_max']}")
                        st.markdown(f"- **Valeur staging:** {stats['resultat_staged_max']}")
                else:
                    st.info("ℹ️ " + stats.get('message', 'Aucun écart calculable'))
                
                # Afficher le dataframe complet
                st.markdown("---")
                st.markdown("**📋 Détails complets :**")
                st.dataframe(stats['dataframe'], use_container_width=True, height=300)
    
    # Message de synthèse
    if nb_nouveaux == 0 and nb_nouvelles_annees == 0 and nb_updates == 0:
        st.success("✅ Aucune différence détectée ! Les données staging sont identiques à la pré-production.")

# Bouton de livraison - en dehors du bloc d'analyse pour rester visible
if st.session_state.analysis_done and st.session_state.df_staged is not None:
    st.markdown("---")
    st.markdown("## 🚀 Livraison en pré-production")
    
    # Calculer le nombre de lignes à envoyer
    comparison = st.session_state.comparison
    nb_to_send = len(comparison['nouveaux_indicateurs']) + len(comparison['nouvelles_annees'])
    nb_to_send += sum(stats.get('nb_lignes', 0) for stats in comparison['donnees_a_updater'].values())
    
    if nb_to_send == 0:
        st.info("✅ Aucune donnée à livrer : tout est déjà à jour en pré-production !")
    else:
        st.warning(f"⚠️ **Attention :** Cette action va envoyer **{nb_to_send:,} lignes** à la pré-production via API.")
        
        # Préparer le DataFrame à envoyer pour le téléchargement
        dfs_to_send = []
        if len(comparison['nouveaux_indicateurs']) > 0:
            dfs_to_send.append(comparison['nouveaux_indicateurs'])
        if len(comparison['nouvelles_annees']) > 0:
            dfs_to_send.append(comparison['nouvelles_annees'])
        for indic_id, stats in comparison['donnees_a_updater'].items():
            if 'dataframe' in stats:
                df_update = stats['dataframe'].copy()
                df_update = df_update[['collectivite_id', 'indicateur_id', 'metadonnee_id', 'date_valeur', 'resultat_staged']]
                df_update = df_update.rename(columns={'resultat_staged': 'resultat'})
                dfs_to_send.append(df_update)

        # Détail de ce qui sera envoyé
        message_lines = []
        if len(comparison['nouveaux_indicateurs']) > 0:
            message_lines.append(f"🆕 {len(comparison['nouveaux_indicateurs']):,} lignes de nouveaux indicateurs")
        if len(comparison['nouvelles_annees']) > 0:
            message_lines.append(f"📅 {len(comparison['nouvelles_annees']):,} lignes de nouvelles années")
        nb_updates_lines = sum(stats.get('nb_lignes', 0) for stats in comparison['donnees_a_updater'].values())
        if nb_updates_lines > 0:
            message_lines.append(f"🔄 {nb_updates_lines:,} lignes à mettre à jour")
        st.info(" - ".join(message_lines))
        
        if dfs_to_send:
            df_to_download = pd.concat(dfs_to_send, ignore_index=True)
            csv_data = df_to_download.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="📥 Télécharger les données à envoyer (CSV)",
                data=csv_data,
                file_name=f"donnees_a_livrer_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

    col_btn1, col_btn2, col_btn3 = st.columns([2, 3, 2])
    with col_btn2:
        if st.button("🚢 Livrer en pré-prod", type="primary", use_container_width=True, disabled=(nb_to_send == 0)):
            # Container pour la progression
            progress_container = st.container()
            
            result = livrer_en_preprod(st.session_state.comparison, st.session_state.df_staged, progress_container)
            
            st.markdown("---")
            
            if result['success']:
                st.success(f"✅ {result['message']}")
                
                col_stat1, col_stat2, col_stat3 = st.columns(3)
                with col_stat1:
                    st.metric("📊 Total de lignes", f"{result['nb_total']:,}")
                with col_stat2:
                    st.metric("📤 Lignes insérées", f"{result['nb_inserted']:,}")
                with col_stat3:
                    st.metric("📦 Batches envoyés", result.get('nb_batches', 0))
                
                st.info("💡 Vous pouvez relancer l'analyse pour vérifier que les données ont bien été livrées.")
            else:
                st.error(f"❌ {result['message']}")
                
                if result.get('failed_batches', 0) > 0:
                    st.warning(f"⚠️ {result['failed_batches']} batch(s) ont échoué sur {result.get('nb_batches', 0)} total")
                    st.info(f"💡 {result['nb_inserted']:,} lignes ont quand même été insérées avec succès")


