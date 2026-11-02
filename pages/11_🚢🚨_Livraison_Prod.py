import streamlit as st
import pandas as pd
import requests
import time
from sqlalchemy import text
from utils.db import get_engine, get_engine_prod, get_engine_prod_writing
from utils.config_indicateurs import charger_indicateurs, index_par_identifiant, valider_indicateurs

# Configuration de la page
st.set_page_config(layout="wide")
st.title("🚢🚨 Livraison des indicateurs en PRODUCTION")

st.markdown("""
Cette page compare les données **staging** (table `indicateurs_valeurs_olap`) 
avec les données en **production** (table `indicateur_valeur`) pour identifier :
- 🆕 Les nouveaux indicateurs à importer
- 📅 Les nouvelles années pour des indicateurs existants
- 🔄 Les données à mettre à jour
""")

st.error("⚠️ **ATTENTION : Cette page effectue des modifications en PRODUCTION !**")

st.markdown("---")

# ==========================
# FONCTIONS
# ==========================

def check_and_handle_duplicates(df):
    """Vérifie et gère les doublons dans les données staging.
    
    Args:
        df: DataFrame avec les données staging
        
    Returns:
        tuple: (df_cleaned, has_conflicts)
            - df_cleaned: DataFrame nettoyé (sans doublons complets)
            - has_conflicts: True si des conflits ont été détectés
    """
    if df.empty:
        return df, False
    
    # Définir la clé primaire
    pk_cols = ['indicateur_id', 'collectivite_id', 'date_valeur']
    
    # 1. Vérifier les doublons complets (toutes colonnes identiques)
    duplicates_full = df.duplicated(keep='first')
    nb_duplicates_full = duplicates_full.sum()
    
    if nb_duplicates_full > 0:
        st.info(f"ℹ️ {nb_duplicates_full} ligne(s) complètement dupliquée(s) détectée(s) et supprimée(s)")
        df = df[~duplicates_full].copy()
    
    # 2. Vérifier les doublons partiels (même clé primaire, valeurs différentes)
    duplicates_pk = df.duplicated(subset=pk_cols, keep=False)
    
    if duplicates_pk.any():
        # Il y a des doublons sur la clé primaire
        df_duplicates = df[duplicates_pk].copy()
        
        # Vérifier s'il y a des conflits (valeurs différentes pour la même clé)
        conflicts = []
        for _, group in df_duplicates.groupby(pk_cols):
            if len(group) > 1:
                # Vérifier si les valeurs sont différentes
                other_cols = [col for col in df.columns if col not in pk_cols]
                for col in other_cols:
                    if group[col].nunique() > 1:
                        # Conflit détecté
                        conflicts.append(group)
                        break
        
        if conflicts:
            st.error("❌ **ERREUR : Doublons avec valeurs conflictuelles détectés !**")
            st.markdown("""
            Des lignes avec la même clé primaire (indicateur_id, collectivite_id, date_valeur) 
            mais des valeurs différentes ont été trouvées. Cela indique un problème dans les données sources.
            """)
            
            # Afficher les lignes en conflit
            df_conflicts = pd.concat(conflicts).sort_values(pk_cols)
            st.dataframe(
                df_conflicts.style.apply(
                    lambda x: ['background-color: #ffcccc' if x.name in df_conflicts.index else '' for _ in x],
                    axis=1
                ),
                use_container_width=True
            )
            
            # Statistiques sur les conflits
            st.markdown(f"""
            **📊 Statistiques des conflits :**
            - Nombre de groupes en conflit : {len(conflicts)}
            - Nombre total de lignes concernées : {len(df_conflicts)}
            """)
            
            return df, True
    
    return df, False


def load_staged_data():
    """Charge les données de la table indicateurs_valeurs_olap avec l'identifiant_referentiel et api_nom_cube."""
    engine = get_engine()
    
    try:
        query = text("""
            SELECT 
                collectivite_id,
                indicateur_id,
                metadonnee_id,
                date_valeur,
                resultat,
                api_nom_cube,
                identifiant_referentiel
            FROM indicateurs_valeurs_olap
        """)
        
        with engine.connect() as conn:
            df = pd.read_sql_query(query, conn)
        
        # Convertir explicitement date_valeur en datetime
        df['date_valeur'] = pd.to_datetime(df['date_valeur'])

        df['resultat'] = df['resultat'].round(2)
        
        # Vérifier et gérer les doublons
        df, has_conflicts = check_and_handle_duplicates(df)
        
        if has_conflicts:
            st.stop()  # Arrêter l'exécution si des conflits sont détectés
        
        return df
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des données staging : {str(e)}")
        return pd.DataFrame()


def transform_staged_for_prod(df_staged):
    """Transforme les données staged pour les adapter à la production.
    
    Effectue deux transformations principales :
    1. Mapping des indicateur_id via identifiant_referentiel
    2. Mapping des metadonnee_id (avec insertion en prod si nécessaire)
    
    Args:
        df_staged: DataFrame avec les données staging (IDs preprod)
    
    Returns:
        DataFrame avec les IDs prod
    """
    if df_staged.empty:
        return df_staged
    
    # Vérifier que les engines sont bien configurés
    try:
        engine_prod = get_engine_prod()
        engine_prod_writing = get_engine_prod_writing()
    except Exception as e:
        st.error(f"❌ Erreur de configuration des engines de base de données : {str(e)}")
        st.error("Vérifiez que les secrets 'database_prod' et 'database_prod_writing' sont bien configurés dans .streamlit/secrets.toml")
        return pd.DataFrame()
    
    df_result = df_staged.copy()
    
    # ============================================
    # 1. MAPPING DES INDICATEUR_ID
    # ============================================
    
    st.info("🔄 Mapping des indicateur_id (preprod → prod)...")
    
    try:        
        # Charger le mapping depuis production
        with engine_prod.connect() as conn:
            mapping_prod = pd.read_sql_query(
                text("SELECT id as indicateur_id_prod, identifiant_referentiel FROM indicateur_definition WHERE collectivite_id IS NULL"),
                conn
            )

        mapping_dict = dict(zip(mapping_prod["identifiant_referentiel"], mapping_prod["indicateur_id_prod"]))
        
        # Appliquer le mapping
        df_result['indicateur_id'] = df_result['identifiant_referentiel'].map(mapping_dict)
        
        st.success(f"✅ Mapping indicateur_id effectué : {len(mapping_dict)} indicateurs")
        
    except Exception as e:
        st.error(f"❌ Erreur lors du mapping des indicateur_id : {str(e)}")
        return pd.DataFrame()
    
    # ============================================
    # 2. CHARGEMENT DU YAML
    # ============================================
    
    st.info("🔄 Chargement du fichier de configuration YAML...")
    
    try:
        indicateurs_yaml = charger_indicateurs()
        st.success(f"✅ {len(indicateurs_yaml)} indicateurs chargés depuis le YAML")
        
        erreurs_config = valider_indicateurs(indicateurs_yaml)
        if erreurs_config:
            st.error("❌ config.yaml incohérent :\n" + "\n".join(f"- {e}" for e in erreurs_config))
            return pd.DataFrame()
        
        # Un même cube peut porter plusieurs entrées (mesures ou axes différents) : on retrouve
        # l'entrée de chaque ligne par son identifiant_referentiel, unique dans le YAML
        yaml_par_identifiant = index_par_identifiant(indicateurs_yaml)
        
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du YAML : {str(e)}")
        import traceback
        st.error(traceback.format_exc())
        return pd.DataFrame()
    
    # ============================================
    # 3. INSERTION DES SOURCES ET METADONNEES EN PROD
    # ============================================
    
    st.info("🔄 Insertion/vérification des sources et métadonnées en prod...")
    
    try:
        identifiants = df_result['identifiant_referentiel'].unique().tolist()
        
        # Mapping identifiant_referentiel -> metadonnee_id_prod
        dict_mapping_meta = {}
        nb_sources_inserees = 0
        nb_sources_existantes = 0
        nb_meta_insertions = 0
        nb_meta_updates = 0
        
        sources_traitees = set()  # Pour éviter de traiter la même source plusieurs fois
        meta_id_par_cle = {}  # (source_id, nom_donnees) -> metadonnee_id_prod, partagé entre identifiants
        
        for identifiant in identifiants:
            # Récupérer les infos depuis le YAML
            if identifiant not in yaml_par_identifiant:
                st.warning(f"⚠️ identifiant_referentiel '{identifiant}' non trouvé dans le YAML, ignoré")
                continue
            
            indic_yaml = yaml_par_identifiant[identifiant]
            source_info = indic_yaml['source']
            metadata_info = indic_yaml['metadata']
            
            cle_meta = (metadata_info["source_id"], metadata_info["nom_donnees"])
            if cle_meta in meta_id_par_cle:
                dict_mapping_meta[identifiant] = meta_id_par_cle[cle_meta]
                continue
            
            # ====================================
            # A. INSERTION/VERIFICATION DE LA SOURCE
            # ====================================
            source_id = source_info['id']
            
            if source_id not in sources_traitees:
                sources_traitees.add(source_id)
                
                try:
                    with engine_prod_writing.begin() as conn:
                        # Vérifier si la source existe déjà
                        check_query = text("""
                            SELECT 1 FROM indicateur_source WHERE id = :id
                        """)
                        result = conn.execute(check_query, {"id": source_id}).first()
                        
                        if result is None:
                            # Insertion si la source n'existe pas encore
                            insert_query = text("""
                                INSERT INTO indicateur_source (id, libelle, ordre_affichage)
                                VALUES (:id, :libelle, :ordre_affichage)
                            """)
                            conn.execute(insert_query, {
                                "id": source_id,
                                "libelle": source_info["libelle"],
                                "ordre_affichage": source_info["ordre_affichage"]
                            })
                            nb_sources_inserees += 1
                        else:
                            nb_sources_existantes += 1
                except Exception as conn_error:
                    st.error(f"❌ Erreur de connexion à la base prod lors de l'insertion de la source '{source_id}' : {str(conn_error)}")
                    st.error("Vérifiez que le secret 'database_prod_writing' est correctement configuré dans .streamlit/secrets.toml")
                    raise
            
            # ====================================
            # B. INSERTION/UPDATE DE LA METADONNEE
            # ====================================
            
            # Clé d'unicité
            cle = {
                "source_id": metadata_info["source_id"],
                "nom_donnees": metadata_info["nom_donnees"]
            }
            
            # Colonnes à mettre à jour si ligne déjà existante
            update_fields = {
                "date_version": metadata_info["date_version"],
                "methodologie": metadata_info["methodologie"],
                "diffuseur": metadata_info["diffuseur"],
                "producteur": metadata_info["producteur"],
                "limites": metadata_info["limites"]
            }
            
            # Utiliser engine_prod pour la lecture
            with engine_prod.connect() as conn_read:
                # 1. Recherche d'une ligne existante selon la clé logique
                result = conn_read.execute(text("""
                    SELECT id FROM indicateur_source_metadonnee
                    WHERE source_id = :source_id
                    AND nom_donnees = :nom_donnees
                    LIMIT 1;
                """), cle).first()
            
            # Utiliser engine_prod_writing pour l'écriture
            with engine_prod_writing.begin() as conn_write:
                if result is None:
                    # 2. Si aucune ligne existante → INSERT
                    meta_dict = {
                        "source_id": metadata_info["source_id"],
                        "date_version": metadata_info["date_version"],
                        "nom_donnees": metadata_info["nom_donnees"],
                        "diffuseur": metadata_info["diffuseur"],
                        "producteur": metadata_info["producteur"],
                        "methodologie": metadata_info["methodologie"],
                        "limites": metadata_info["limites"]
                    }
                    
                    result = conn_write.execute(text("""
                        INSERT INTO indicateur_source_metadonnee (
                            source_id, date_version, nom_donnees, diffuseur,
                            producteur, methodologie, limites
                        ) VALUES (
                            :source_id, :date_version, :nom_donnees, :diffuseur,
                            :producteur, :methodologie, :limites
                        ) RETURNING id;
                    """), meta_dict).first()
                    
                    id_prod = result[0]
                    nb_meta_insertions += 1
                    
                else:
                    # 3. Si ligne existante → UPDATE
                    id_prod = result[0]
                    update_fields["id"] = id_prod
                    
                    conn_write.execute(text("""
                        UPDATE indicateur_source_metadonnee
                        SET date_version = :date_version,
                            methodologie = :methodologie,
                            diffuseur = :diffuseur,
                            producteur = :producteur,
                            limites = :limites
                        WHERE id = :id;
                    """), update_fields)
                    
                    nb_meta_updates += 1
            
            meta_id_par_cle[cle_meta] = id_prod
            dict_mapping_meta[identifiant] = id_prod
        
        # Appliquer le mapping
        df_result['metadonnee_id'] = df_result['identifiant_referentiel'].map(dict_mapping_meta)
        
        st.success(f"✅ Sources : {nb_sources_inserees} insertion(s), {nb_sources_existantes} existante(s)")
        st.success(f"✅ Métadonnées : {nb_meta_insertions} insertion(s), {nb_meta_updates} mise(s) à jour")
        
    except Exception as e:
        st.error(f"❌ Erreur lors de l'insertion des sources/métadonnées : {str(e)}")
        import traceback
        st.error(traceback.format_exc())
        return pd.DataFrame()
    
    # Vérifier qu'il n'y a pas de valeurs nulles après transformation
    if df_result['indicateur_id'].isna().any() or df_result['metadonnee_id'].isna().any():
        nb_nulls = df_result[['indicateur_id', 'metadonnee_id']].isna().sum()
        st.warning(f"⚠️ Valeurs nulles détectées après transformation : {nb_nulls.to_dict()}")
        st.warning("Suppression des lignes avec des valeurs nulles...")
        df_result = df_result.dropna(subset=['indicateur_id', 'metadonnee_id'])
    
    # Convertir les IDs en int (peuvent être en float après le mapping)
    df_result['indicateur_id'] = df_result['indicateur_id'].astype(int)
    df_result['metadonnee_id'] = df_result['metadonnee_id'].astype(int)
    
    # Supprimer les colonnes qui ne servent plus
    df_result = df_result.drop(columns=['identifiant_referentiel', 'api_nom_cube'])
    
    st.success(f"✅ Transformation terminée : {len(df_result):,} lignes prêtes pour la prod")
    
    return df_result


def load_indicateurs_titres():
    """Charge le mapping id -> titre des indicateurs depuis la production."""
    engine_prod = get_engine_prod()
    
    try:
        query = text("""
            SELECT DISTINCT id, titre
            FROM indicateur_definition
            WHERE collectivite_id IS NULL
        """)
        
        with engine_prod.connect() as conn:
            df = pd.read_sql_query(query, conn)
        
        # Créer un dictionnaire pour le mapping
        mapping = dict(zip(df['id'], df['titre']))
        
        return mapping
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des titres d'indicateurs : {str(e)}")
        return {}


def load_prod_data(df_staged):
    """Charge les données de la table indicateur_valeur en production.
    
    Ne charge QUE les données correspondant aux clés primaires présentes dans le staging
    pour optimiser les performances sur les grosses tables.
    
    Args:
        df_staged: DataFrame staging pour extraire les clés primaires à charger
    """
    engine_prod = get_engine_prod()
    
    if df_staged.empty:
        return pd.DataFrame()
    
    try:
        # Extraire les valeurs uniques pour chaque colonne de la clé primaire
        indicateurs_ids = df_staged['indicateur_id'].unique().tolist()
        collectivite_ids = df_staged['collectivite_id'].unique().tolist()
        metadonnee_ids = df_staged['metadonnee_id'].unique().tolist()
        
        st.info(f"🔍 Filtrage production : {len(indicateurs_ids)} indicateurs, {len(collectivite_ids)} collectivités, {len(metadonnee_ids)} métadonnées")
        
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
        
        with engine_prod.connect() as conn:
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
        
        st.success(f"✅ {len(df):,} lignes chargées depuis la production")
        
        return df
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des données production : {str(e)}")
        return pd.DataFrame()


def get_valid_collectivite_ids_prod():
    """Récupère la liste des collectivite_id valides depuis la table collectivite en production.
    
    Returns:
        set: Ensemble des collectivite_id valides
    """
    engine_prod = get_engine_prod()
    
    try:
        query = text("SELECT id FROM collectivite")
        
        with engine_prod.connect() as conn:
            df = pd.read_sql_query(query, conn)
        
        valid_ids = set(df['id'].tolist())
        st.info(f"✅ {len(valid_ids)} collectivités valides trouvées en production")
        
        return valid_ids
    except Exception as e:
        st.error(f"❌ Erreur lors de la récupération des collectivités production : {str(e)}")
        return set()


def _resume_erreur_api(response, max_len=300):
    """Extrait un message d'erreur court (sans dump console)."""
    try:
        error_json = response.json()
        error_msg = (
            error_json.get("message")
            or error_json.get("error")
            or error_json.get("detail")
            or error_json.get("code")
        )
        if error_msg is None:
            error_msg = "Erreur API"
    except ValueError:
        error_msg = response.text or "Erreur API"
    error_msg = str(error_msg)
    if len(error_msg) > max_len:
        return error_msg[:max_len] + "…"
    return error_msg


def livrer_en_prod(comparison, df_staged, progress_container=None, batch_size=500):
    """Fait l'upsert des données staging vers la production via API.
    
    N'envoie que les données qui ont vraiment changé :
    - Nouveaux indicateurs
    - Nouvelles années
    - Données avec résultats différents
    
    Filtre automatiquement les données pour ne garder que les collectivite_id
    qui existent en production (évite les violations de clé étrangère).
    
    Args:
        comparison: Résultats de la comparaison staging vs production
        df_staged: DataFrame contenant toutes les données staging
        progress_container: Container Streamlit pour afficher la progression
        batch_size: Nombre de lignes par requête API (défaut 500)
    
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
    
    # Filtrer pour ne garder que les collectivite_id qui existent en production
    nb_lignes_avant = len(df_to_send)
    nb_lignes_filtrees = 0
    valid_collectivite_ids = get_valid_collectivite_ids_prod()
    
    if valid_collectivite_ids:
        df_to_send = df_to_send[df_to_send['collectivite_id'].isin(valid_collectivite_ids)]
        nb_lignes_apres = len(df_to_send)
        nb_lignes_filtrees = nb_lignes_avant - nb_lignes_apres
        
        if nb_lignes_filtrees > 0:
            st.warning(f"⚠️ {nb_lignes_filtrees} ligne(s) filtrée(s) (collectivités inexistantes en production)")
        
        if nb_lignes_apres == 0:
            return {
                'nb_total': 0, 
                'nb_filtered': nb_lignes_filtrees,
                'success': True, 
                'message': f'Aucune donnée à livrer après filtrage des collectivités ({nb_lignes_filtrees} lignes filtrées)'
            }
    
    try:
        # Récupérer les credentials depuis les secrets
        try:
            api_url = st.secrets.get("api_prod_url", "https://api.territoiresentransitions.fr/api/v1/indicateur-valeurs")
            api_token = st.secrets.get("api_prod_token", "")
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
            "dateValeur": pd.Timestamp(row["date_valeur"]).strftime("%Y-%m-%d"),
            "metadonneeId": int(row["metadonnee_id"]),
            "resultat": float(row["resultat"]) if pd.notnull(row["resultat"]) else None,
        }, axis=1).tolist()
        
        # 2. Paramétrage du batch
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
                error_resume = _resume_erreur_api(response)
                console_resume = _resume_erreur_api(response, max_len=120)
                try:
                    api_code = response.json().get("code")
                except ValueError:
                    api_code = None
                console_line = (
                    f"❌ Batch {batch_num}/{total_batches} échoué (HTTP {response.status_code})"
                )
                if api_code is not None:
                    console_line += f" — code {api_code}"
                console_line += f" — {console_resume}"
                print(console_line)
                
                if progress_container:
                    status_text.error(
                        f"❌ Batch {batch_num}/{total_batches} échoué (HTTP {response.status_code}) — {error_resume}"
                    )
                
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
            'nb_filtered': nb_lignes_filtrees,
            'failed_batches': failed_batches,
            'success': success,
            'message': message
        }
        
    except Exception as e:
        return {
            'nb_total': 0,
            'nb_inserted': 0,
            'nb_filtered': nb_lignes_filtrees if 'nb_lignes_filtrees' in locals() else 0,
            'success': False,
            'message': f'Erreur lors de la livraison : {str(e)}'
        }


def compare_data(df_staged, df_prod):
    """Compare les données staging et production avec une approche par merge.
    
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
    df_prod = df_prod.copy()
    
    # 1. NOUVEAUX INDICATEURS
    indicateurs_staged = set(df_staged['indicateur_id'].unique())
    indicateurs_prod = set(df_prod['indicateur_id'].unique())
    nouveaux_indicateurs_ids = indicateurs_staged - indicateurs_prod
    
    df_nouveaux_indicateurs = df_staged[
        df_staged['indicateur_id'].isin(nouveaux_indicateurs_ids)
    ].copy()
    
    # 2. INDICATEURS EXISTANTS
    indicateurs_existants = indicateurs_staged & indicateurs_prod
    
    # 3. NOUVELLES ANNÉES ET DONNÉES À UPDATER - par indicateur
    donnees_a_updater = {}
    all_nouvelles_annees = []
    
    for indic_id in indicateurs_existants:
        # Filtrer par indicateur
        df_staged_indic = df_staged[df_staged['indicateur_id'] == indic_id].copy()
        df_prod_indic = df_prod[df_prod['indicateur_id'] == indic_id].copy()
        
        # Merge sur les clés primaires
        df_merge = df_staged_indic.merge(
            df_prod_indic,
            on=pk_cols,
            how='outer',
            suffixes=('_staged', '_prod'),
            indicator=True
        )
        
        # Nouvelles années : présent dans staging mais pas dans production
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
            df_both['resultat_diff'] = df_both['resultat_staged'] != df_both['resultat_prod']
            df_diff = df_both[df_both['resultat_diff']].copy()
            
            if len(df_diff) > 0:
                # Calculer l'écart en %
                df_diff['ecart_abs'] = df_diff['resultat_staged'] - df_diff['resultat_prod']
                
                # Écart en % (gérer division par zéro)
                df_diff['ecart_pct'] = 0.0
                mask_non_zero = df_diff['resultat_prod'] != 0
                df_diff.loc[mask_non_zero, 'ecart_pct'] = (
                    abs(df_diff.loc[mask_non_zero, 'ecart_abs'] / df_diff.loc[mask_non_zero, 'resultat_prod']) * 100
                ).round(0)
                
                # Pour les valeurs où production = 0 mais staged != 0
                mask_div_zero = (df_diff['resultat_prod'] == 0) & (df_diff['resultat_staged'] != 0)
                df_diff.loc[mask_div_zero, 'ecart_pct'] = float('inf')
                
                # Sélectionner les colonnes pertinentes
                cols_result = pk_cols + ['resultat_prod', 'resultat_staged', 'ecart_abs', 'ecart_pct']
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
                        'resultat_prod_max': max_row['resultat_prod'],
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
if 'confirmation_prod' not in st.session_state:
    st.session_state.confirmation_prod = False

# Bouton pour lancer la comparaison
col_b1, col_b2, col_b3 = st.columns([2, 3, 2])
with col_b2:
    if st.button("🔍 Analyser les données à livrer", type="primary", use_container_width=True):
        
        with st.spinner("Chargement des titres d'indicateurs..."):
            # Charger le mapping id -> titre
            st.session_state.indicateurs_titres = load_indicateurs_titres()
        
        with st.spinner("Chargement des données staging..."):
            # Chargement des données staging d'abord
            df_staged_raw = load_staged_data()
        
        if df_staged_raw.empty:
            st.warning("⚠️ Aucune donnée dans la table staging `indicateurs_valeurs_olap`")
            st.session_state.analysis_done = False
            st.stop()
        
        with st.spinner("Transformation des données staging pour la prod (mapping ID)..."):
            # Transformation des IDs preprod → prod
            st.session_state.df_staged = transform_staged_for_prod(df_staged_raw)
        
        if st.session_state.df_staged.empty:
            st.error("❌ Aucune donnée après transformation (vérifiez les mappings)")
            st.session_state.analysis_done = False
            st.stop()
        
        with st.spinner("Chargement des données production (filtré)..."):
            # Chargement des données production avec filtre sur les clés primaires du staging
            df_prod = load_prod_data(st.session_state.df_staged)
        
        with st.spinner("Comparaison en cours..."):
            st.session_state.comparison = compare_data(st.session_state.df_staged, df_prod)
        
        st.session_state.analysis_done = True
        st.session_state.confirmation_prod = False

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
    st.markdown("## 🔄 Comparaison avec production")
    
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
        st.info(f"Ces {nb_nouveaux} lignes correspondent à des indicateurs qui n'existent pas encore en production.")
        
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
                        st.markdown(f"- **Valeur production:** {stats['resultat_prod_max']}")
                        st.markdown(f"- **Valeur staging:** {stats['resultat_staged_max']}")
                else:
                    st.info("ℹ️ " + stats.get('message', 'Aucun écart calculable'))
                
                # Afficher le dataframe complet
                st.markdown("---")
                st.markdown("**📋 Détails complets :**")
                st.dataframe(stats['dataframe'], use_container_width=True, height=300)
    
    # Message de synthèse
    if nb_nouveaux == 0 and nb_nouvelles_annees == 0 and nb_updates == 0:
        st.success("✅ Aucune différence détectée ! Les données staging sont identiques à la production.")

# Bouton de livraison - en dehors du bloc d'analyse pour rester visible
if st.session_state.analysis_done and st.session_state.df_staged is not None:
    st.markdown("---")
    st.markdown("## 🚀 Livraison en PRODUCTION")
    
    # Calculer le nombre de lignes à envoyer
    comparison = st.session_state.comparison
    nb_to_send = len(comparison['nouveaux_indicateurs']) + len(comparison['nouvelles_annees'])
    nb_to_send += sum(stats.get('nb_lignes', 0) for stats in comparison['donnees_a_updater'].values())
    
    if nb_to_send == 0:
        st.info("✅ Aucune donnée à livrer : tout est déjà à jour en production !")
    else:
        st.error(f"🚨 **ATTENTION : Cette action va envoyer {nb_to_send:,} lignes en PRODUCTION via API.**")
        
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
                file_name=f"donnees_a_livrer_prod_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

    petits_paquets = st.toggle(
        "Paquets de 50 lignes (au lieu de 500)",
        value=False,
        help="Réduit la taille des requêtes API en cas d'erreurs serveur (ex. stack overflow).",
    )
    batch_size_livraison = 50 if petits_paquets else 500

    col_btn1, col_btn2, col_btn3 = st.columns([2, 3, 2])
    with col_btn2:
        if st.button("🚢🚨 Livrer en PRODUCTION", type="primary", use_container_width=True, disabled=(nb_to_send == 0)):
            st.session_state.confirmation_prod = True
    
    # Message de confirmation après le clic sur le bouton
    if st.session_state.confirmation_prod:
        st.markdown("---")
        st.error("### ⚠️ CONFIRMATION REQUISE")
        st.warning("**Êtes-vous sûr de vouloir livrer en production ?**")
        st.markdown("""
        Cette action est **irréversible** et va modifier les données en **PRODUCTION**.
        
        ✅ Assurez-vous d'avoir :
        - Vérifié les données à livrer
        - Testé en pré-production
        - L'autorisation nécessaire
        """)
        
        col_conf1, col_conf2, col_conf3 = st.columns([1, 1, 1])
        
        with col_conf1:
            if st.button("❌ Annuler", use_container_width=True):
                st.session_state.confirmation_prod = False
                st.rerun()
        
        with col_conf3:
            if st.button("✅ OUI, LIVRER EN PROD", type="primary", use_container_width=True):
                # Container pour la progression
                progress_container = st.container()
                
                result = livrer_en_prod(
                    st.session_state.comparison,
                    st.session_state.df_staged,
                    progress_container,
                    batch_size=batch_size_livraison,
                )
                
                st.markdown("---")
                
                if result['success']:
                    st.success(f"✅ {result['message']}")
                    
                    # Afficher les statistiques avec ou sans le filtrage
                    if result.get('nb_filtered', 0) > 0:
                        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
                        with col_stat1:
                            st.metric("📊 Total de lignes", f"{result['nb_total']:,}")
                        with col_stat2:
                            st.metric("📤 Lignes insérées", f"{result['nb_inserted']:,}")
                        with col_stat3:
                            st.metric("🚫 Lignes filtrées", f"{result['nb_filtered']:,}")
                        with col_stat4:
                            st.metric("📦 Batches envoyés", result.get('nb_batches', 0))
                    else:
                        col_stat1, col_stat2, col_stat3 = st.columns(3)
                        with col_stat1:
                            st.metric("📊 Total de lignes", f"{result['nb_total']:,}")
                        with col_stat2:
                            st.metric("📤 Lignes insérées", f"{result['nb_inserted']:,}")
                        with col_stat3:
                            st.metric("📦 Batches envoyés", result.get('nb_batches', 0))

                else:
                    st.error(f"❌ {result['message']}")
                    
                    if result.get('failed_batches', 0) > 0:
                        st.warning(f"⚠️ {result['failed_batches']} batch(s) ont échoué sur {result.get('nb_batches', 0)} total")
                        st.info(f"💡 {result['nb_inserted']:,} lignes ont quand même été insérées avec succès")
                
                # Réinitialiser la confirmation
                st.session_state.confirmation_prod = False

