import streamlit as st
import pandas as pd
import requests
import time
from sqlalchemy import text
from utils.db import (
    get_engine_prod,
    get_engine_prod_writing,
    get_engine_pre_prod
)

# Configuration de la page
st.set_page_config(layout="wide")
st.title("🪇 Import de groupements d'indicateurs")

st.markdown("""
Cette page permet de créer des groupements d'indicateurs en 4 étapes :
1. 📝 **Nommer le groupement** et l'insérer en base
2. 🏘️ **Sélectionner les collectivités** du groupement
3. 📊 **Importer les indicateurs** depuis un fichier CSV
4. 📈 **Importer les valeurs** des indicateurs depuis un fichier CSV
""")

st.markdown("---")

# ==========================
# TOGGLE PRE-PROD / PROD
# ==========================

col_toggle, col_space = st.columns([1, 5])
with col_toggle:
    environnement = st.toggle("🚀 Mode Production", value=False)

if environnement:
    st.info("🚀 **Mode Production** : Toutes les opérations seront effectuées sur la base de données de **PRODUCTION**")
    engine_lecture = get_engine_prod()
    engine_ecriture = get_engine_prod_writing()
    env_label = "Production"
else:
    st.success("🧪 **Mode Pré-production** : Toutes les opérations seront effectuées sur la base de données de **PRÉ-PRODUCTION**")
    engine_lecture = get_engine_pre_prod()
    engine_ecriture = get_engine_pre_prod()
    env_label = "Pré-production"

st.markdown("---")

# ==========================
# FONCTIONS
# ==========================

def verifier_groupement_existe(nom_groupement, engine):
    """Vérifie si un groupement avec ce nom existe déjà."""
    try:
        query = text("""
            SELECT id, nom
            FROM groupement
            WHERE nom = :nom
        """)
        
        with engine.connect() as conn:
            result = pd.read_sql_query(query, conn, params={"nom": nom_groupement})
        
        return not result.empty, result
    except Exception as e:
        st.error(f"❌ Erreur lors de la vérification du groupement : {str(e)}")
        return False, pd.DataFrame()


def inserer_groupement(nom_groupement, engine):
    """Insère un nouveau groupement dans la table groupement et crée la catégorie_tag associée."""
    try:
        # Transaction pour insérer à la fois le groupement et la catégorie_tag
        with engine.begin() as conn:
            # 1. Insérer le groupement
            query_groupement = text("""
                INSERT INTO groupement (nom)
                VALUES (:nom)
                RETURNING id, nom
            """)
            
            result = conn.execute(query_groupement, {"nom": nom_groupement})
            row = result.fetchone()
            groupement_id = row[0]
            groupement_nom = row[1]
            
            # 2. Insérer la catégorie_tag associée
            query_categorie = text("""
                INSERT INTO categorie_tag (groupement_id, nom, visible)
                VALUES (:groupement_id, :nom, True)
            """)
            
            conn.execute(query_categorie, {
                "groupement_id": groupement_id,
                "nom": nom_groupement
            })
            
            return True, groupement_id, groupement_nom
    except Exception as e:
        st.error(f"❌ Erreur lors de l'insertion du groupement : {str(e)}")
        return False, None, None


def charger_collectivites(engine):
    """Charge la liste des collectivités depuis la base."""
    try:
        query = text("""
            SELECT id, nom
            FROM collectivite
            ORDER BY nom
        """)
        
        with engine.connect() as conn:
            df = pd.read_sql_query(query, conn)
        
        return df
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des collectivités : {str(e)}")
        return pd.DataFrame()


def charger_groupements(engine):
    """Charge la liste des groupements existants."""
    try:
        query = text("""
            SELECT id, nom
            FROM groupement
            ORDER BY nom
        """)
        
        with engine.connect() as conn:
            df = pd.read_sql_query(query, conn)
        
        return df
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des groupements : {str(e)}")
        return pd.DataFrame()


def inserer_collectivites_groupement(groupement_nom, collectivite_ids, engine):
    """Insère les collectivités associées à un groupement."""
    try:
        # Construire la requête avec les IDs des collectivités
        values_str = ",\n        ".join([f"({cid})" for cid in collectivite_ids])
        
        query_str = f"""
            INSERT INTO groupement_collectivite (groupement_id, collectivite_id)
            SELECT g.id as groupement_id, c.id as collectivite_id
            FROM (
                VALUES 
                    {values_str}
                ) as c(id)
            JOIN groupement g ON g.nom = :nom_groupement
        """
        
        query = text(query_str)
        
        with engine.begin() as conn:
            result = conn.execute(query, {"nom_groupement": groupement_nom})
            return True, result.rowcount
    except Exception as e:
        st.error(f"❌ Erreur lors de l'insertion des collectivités : {str(e)}")
        return False, 0


def charger_collectivites_groupement(groupement_id, engine):
    """Charge les collectivités déjà associées à un groupement."""
    try:
        query = text("""
            SELECT c.id, c.nom
            FROM collectivite c
            JOIN groupement_collectivite gc ON c.id = gc.collectivite_id
            WHERE gc.groupement_id = :groupement_id
            ORDER BY c.nom
        """)
        
        with engine.connect() as conn:
            df = pd.read_sql_query(query, conn, params={"groupement_id": groupement_id})
        
        return df
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des collectivités du groupement : {str(e)}")
        return pd.DataFrame()


def importer_indicateurs_groupement(df, engine):
    """Importe les indicateurs d'un groupement dans la table indicateur_definition."""
    try:
        # Convertir le dataframe en liste de dictionnaires pour l'insertion
        records = df.to_dict('records')
        
        # Construire la liste des colonnes pour l'insertion
        colonnes = df.columns.tolist()
        colonnes_str = ', '.join(colonnes)
        
        # Construire les placeholders pour les valeurs
        placeholders = ', '.join([f":{col}" for col in colonnes])
        
        query_str = f"""
            INSERT INTO indicateur_definition ({colonnes_str})
            VALUES ({placeholders})
        """
        
        query = text(query_str)
        
        with engine.begin() as conn:
            for record in records:
                # Convertir les valeurs NaN en None pour PostgreSQL
                record_clean = {k: (None if pd.isna(v) else v) for k, v in record.items()}
                conn.execute(query, record_clean)
        
        return True
    except Exception as e:
        st.error(f"❌ Erreur lors de l'import : {str(e)}")
        return False


def associer_indicateurs_categorie_tag(groupement_id, groupement_nom, engine):
    """Associe tous les indicateurs d'un groupement à leur catégorie_tag."""
    try:
        query = text("""
            WITH id_categorie AS (
                SELECT id AS categorie_tag_id
                FROM categorie_tag
                WHERE nom = :groupement_nom
            )
            INSERT INTO indicateur_categorie_tag (indicateur_id, categorie_tag_id)
            SELECT 
                i.id AS indicateur_id,
                ic.categorie_tag_id
            FROM indicateur_definition i
            CROSS JOIN id_categorie ic
            WHERE i.groupement_id = :groupement_id
        """)
        
        with engine.begin() as conn:
            result = conn.execute(query, {
                "groupement_nom": groupement_nom,
                "groupement_id": groupement_id
            })
            return True, result.rowcount
    except Exception as e:
        st.error(f"❌ Erreur lors de l'association des indicateurs à la catégorie tag : {str(e)}")
        return False, 0


def charger_mapping_titre_indicateur_id(engine):
    """Charge le mapping titre -> indicateur_id depuis la table indicateur_definition."""
    try:
        query = text("""
            SELECT id, titre
            FROM indicateur_definition
            WHERE titre IS NOT NULL
        """)
        
        with engine.connect() as conn:
            df = pd.read_sql_query(query, conn)
        
        # Créer un dictionnaire pour le mapping
        mapping = dict(zip(df['titre'], df['id']))
        
        return mapping
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du mapping titre -> id : {str(e)}")
        return {}


def importer_valeurs_via_api(df, env_label, progress_container=None):
    """Importe les valeurs d'indicateurs via l'API.
    
    Args:
        df: DataFrame contenant les colonnes collectivite_id, indicateur_id, date_valeur, resultat
        env_label: "Production" ou "Pré-production"
        progress_container: Container Streamlit pour afficher la progression
    
    Returns:
        dict: Statistiques de l'import
    """
    try:
        # Récupérer les credentials depuis les secrets
        if env_label == "Production":
            api_url = st.secrets.get("api_prod_url", "https://api.territoiresentransitions.fr/api/v1/indicateur-valeurs")
            api_token = st.secrets.get("api_prod_token", "")
        else:
            api_url = st.secrets.get("api_pre_prod_url", "https://preprod-api.territoiresentransitions.fr/api/v1/indicateur-valeurs")
            api_token = st.secrets.get("api_pre_prod_token", "")
        
        if not api_token:
            return {
                'nb_total': 0,
                'success': False,
                'message': f'Token API manquant pour {env_label} dans secrets.toml'
            }
        
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        
        # Préparer la liste de dicts à partir du DataFrame
        df_to_insert = df.copy()
        df_to_insert['date_valeur'] = pd.to_datetime(df_to_insert['date_valeur'])
        
        # Construire le payloads
        if 'metadonnee_id' in df_to_insert.columns:
            valeurs_payload = df_to_insert.apply(lambda row: {
                "collectiviteId": int(row["collectivite_id"]),
                "indicateurId": int(row["indicateur_id"]),
                "dateValeur": row["date_valeur"].isoformat(),
                "metadonneeId": int(row["metadonnee_id"]),
                "resultat": float(row["resultat"]) if pd.notnull(row["resultat"]) else None,
            }, axis=1).tolist()
        else:
            valeurs_payload = df_to_insert.apply(lambda row: {
                "collectiviteId": int(row["collectivite_id"]),
                "indicateurId": int(row["indicateur_id"]),
                "dateValeur": row["date_valeur"].isoformat(),
                "resultat": float(row["resultat"]) if pd.notnull(row["resultat"]) else None,
            }, axis=1).tolist()
        
        # Paramétrage du batch
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
        
        # Envoi des batchs
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
                print(f"\n{'='*80}")
                print(f"❌ ERREUR - Batch {batch_num}/{total_batches} échoué (HTTP {response.status_code})")
                print(f"{'='*80}")
                
                try:
                    error_json = response.json()
                    print("Réponse API (JSON):")
                    import json
                    print(json.dumps(error_json, indent=2, ensure_ascii=False))
                except:
                    print("Réponse serveur (texte):")
                    print(response.text)
                
                print(f"{'='*80}\n")
                
                if progress_container:
                    status_text.error(f"❌ Batch {batch_num}/{total_batches} échoué (HTTP {response.status_code}) - voir console pour détails")
            
            # Mettre à jour la barre de progression
            if progress_container:
                progress_bar.progress(batch_num / total_batches)
        
        if progress_container:
            status_text.empty()
            progress_bar.empty()
        
        success = failed_batches == 0
        message = 'Import réussi' if success else f'Import partiel ({failed_batches} batch(s) échoué(s))'
        
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
            'message': f'Erreur lors de l\'import : {str(e)}'
        }


# ==========================
# ÉTAPE 1 : CRÉER UN GROUPEMENT
# ==========================

left, center, right = st.columns([1, 5, 1])
with center:
    
    st.header("1️⃣ Créer un nouveau groupement")

    with st.form("form_groupement"):
        st.markdown("### Nom du groupement")
        nom_groupement = st.text_input(
            "Saisissez le nom du groupement",
            placeholder="Ex: PETR FOLS",
            help="Le nom doit être unique dans la base de données"
        )
        
        submit_groupement = st.form_submit_button("✅ Créer le groupement", use_container_width=True)
        
        if submit_groupement:
            if not nom_groupement or nom_groupement.strip() == "":
                st.error("❌ Veuillez saisir un nom de groupement")
            else:
                nom_groupement = nom_groupement.strip()
                
                # Vérifier si le groupement existe déjà
                existe, df_exist = verifier_groupement_existe(nom_groupement, engine_lecture)
                
                if existe:
                    st.warning(f"⚠️ Le groupement **{nom_groupement}** existe déjà en {env_label}")
                    st.dataframe(df_exist, use_container_width=True)
                else:
                    # Insérer le nouveau groupement
                    with st.spinner(f"Insertion du groupement en {env_label}..."):
                        success, groupement_id, groupement_nom = inserer_groupement(nom_groupement, engine_ecriture)
                    
                    if success:
                        st.success(f"✅ Groupement **{groupement_nom}** créé avec succès (ID: {groupement_id}) en {env_label} !")
                        st.info(f"ℹ️ Catégorie tag **{groupement_nom}** créée automatiquement")
                        st.balloons()
                        # Stocker dans session state pour utilisation dans l'étape 2
                        st.session_state.dernier_groupement_cree = {
                            "id": groupement_id,
                            "nom": groupement_nom
                        }

    # Afficher les groupements existants
    st.markdown("### Groupements existants")
    df_groupements = charger_groupements(engine_lecture)

    if not df_groupements.empty:
        st.dataframe(df_groupements.sort_values(by='id'), use_container_width=True, hide_index=True)
    else:
        st.info("ℹ️ Aucun groupement trouvé en base")

    st.markdown("---")

    # ==========================
    # ÉTAPE 2 : ASSOCIER LES COLLECTIVITÉS
    # ==========================

    st.header("2️⃣ Associer des collectivités à un groupement")

    # Charger les groupements pour la sélection
    df_groupements_select = charger_groupements(engine_lecture)

    if df_groupements_select.empty:
        st.warning("⚠️ Aucun groupement disponible. Veuillez d'abord créer un groupement à l'étape 1.")
    else:
        # Créer un mapping id -> nom pour le selectbox
        groupements_dict = dict(zip(df_groupements_select['id'], df_groupements_select['nom']))
        
        # Sélection du groupement (rien de présélectionné)
        groupement_id_selectionne = st.selectbox(
            "Sélectionnez le groupement",
            options=list(groupements_dict.keys()),
            format_func=lambda x: groupements_dict[x],
            index=None,
            placeholder="Choisir un groupement...",
            key="selectbox_groupement"
        )
        
        if groupement_id_selectionne is None:
            st.info("ℹ️ Veuillez sélectionner un groupement pour commencer")
        else:
            groupement_nom_selectionne = groupements_dict[groupement_id_selectionne]
            
            # Afficher les collectivités déjà associées
            st.markdown(f"### Collectivités actuellement associées à **{groupement_nom_selectionne}**")
            df_collectivites_actuelles = charger_collectivites_groupement(groupement_id_selectionne, engine_lecture)
            
            if not df_collectivites_actuelles.empty:
                st.dataframe(df_collectivites_actuelles, use_container_width=True, hide_index=True)
                st.info(f"ℹ️ {len(df_collectivites_actuelles)} collectivité(s) déjà associée(s)")
            else:
                st.info("ℹ️ Aucune collectivité associée pour le moment")
            
            st.markdown("---")
            
            # Charger toutes les collectivités pour la sélection
            df_collectivites = charger_collectivites(engine_lecture)
            
            if df_collectivites.empty:
                st.warning("⚠️ Aucune collectivité trouvée en base")
            else:
                with st.form("form_collectivites"):
                    st.markdown("### Ajouter de nouvelles collectivités")
                    
                    # Créer un mapping pour l'affichage
                    collectivites_dict = dict(zip(df_collectivites['id'], df_collectivites['nom']))
                    
                    # Multiselect avec recherche
                    collectivites_selectionnees = st.multiselect(
                        "Recherchez et sélectionnez les collectivités",
                        options=list(collectivites_dict.keys()),
                        format_func=lambda x: f"{collectivites_dict[x]} (ID: {x})",
                        help="Vous pouvez rechercher par nom et sélectionner plusieurs collectivités",
                        key="multiselect_collectivites"
                    )
                    
                    if collectivites_selectionnees:
                        st.markdown(f"**{len(collectivites_selectionnees)} collectivité(s) sélectionnée(s)**")
                        
                        # Afficher un aperçu des collectivités sélectionnées
                        with st.expander("👀 Voir les collectivités sélectionnées"):
                            df_preview = df_collectivites[df_collectivites['id'].isin(collectivites_selectionnees)]
                            st.dataframe(df_preview, use_container_width=True, hide_index=True)
                    
                    submit_collectivites = st.form_submit_button(
                        "✅ Associer les collectivités au groupement", 
                        use_container_width=True
                    )
                    
                    if submit_collectivites:
                        if not collectivites_selectionnees:
                            st.error("❌ Veuillez sélectionner au moins une collectivité")
                        else:
                            # Insérer les associations
                            with st.spinner(f"Association des collectivités en {env_label}..."):
                                success, nb_insertions = inserer_collectivites_groupement(
                                    groupement_nom_selectionne,
                                    collectivites_selectionnees,
                                    engine_ecriture
                                )
                            
                            if success:
                                st.success(f"✅ {nb_insertions} collectivité(s) associée(s) au groupement **{groupement_nom_selectionne}** avec succès en {env_label} !")
                                st.balloons()
                                st.rerun()

    st.markdown("---")

    # ==========================
    # ÉTAPE 3 : IMPORT CSV DES INDICATEURS
    # ==========================

    st.header("3️⃣ Importer les indicateurs depuis un fichier CSV")

    # Charger les groupements pour la sélection
    df_groupements_import = charger_groupements(engine_lecture)

    if df_groupements_import.empty:
        st.warning("⚠️ Aucun groupement disponible. Veuillez d'abord créer un groupement à l'étape 1.")
    else:
        # Sélection du groupement pour l'import
        groupements_dict_import = dict(zip(df_groupements_import['id'], df_groupements_import['nom']))
        
        groupement_id_import = st.selectbox(
            "Sélectionnez le groupement pour l'import des indicateurs",
            options=list(groupements_dict_import.keys()),
            format_func=lambda x: groupements_dict_import[x],
            index=None,
            placeholder="Choisir un groupement...",
            key="selectbox_groupement_import"
        )
        
        if groupement_id_import is None:
            st.info("ℹ️ Veuillez sélectionner un groupement pour commencer l'import")
        else:
            groupement_nom_import = groupements_dict_import[groupement_id_import]
            
            st.markdown(f"### Import des indicateurs pour **{groupement_nom_import}**")
            
            # Upload du fichier CSV
            uploaded_file = st.file_uploader(
                "📁 Glissez-déposez ou sélectionnez votre fichier CSV",
                type=['csv'],
                help="Le fichier doit contenir les colonnes des indicateurs à importer"
            )
            
            if uploaded_file is not None:
                try:
                    # Lire le fichier CSV
                    df_upload = pd.read_csv(uploaded_file, sep=';')
                    
                    
                    # Colonnes de indicateur_definition (celles qui sont pertinentes pour l'import)
                    colonnes_indicateur_definition = ['groupement_id', 'collectivite_id', 'identifiant_referentiel',
                        'titre', 'titre_long', 'description', 'unite', 'borne_min', 'borne_max',
                        'participation_score', 'sans_valeur_utilisateur', 'valeur_calcule',
                        'modified_at', 'created_at', 'modified_by', 'created_by', 'titre_court',
                        'version', 'precision', 'expr_cible', 'expr_seuil', 'libelle_cible_seuil']
                    
                    # Filtrer les colonnes du CSV pour ne garder que celles dans indicateur_definition
                    colonnes_disponibles = df_upload.columns.tolist()
                    colonnes_a_garder = [col for col in colonnes_disponibles if col in colonnes_indicateur_definition]
                    
                    # Créer le dataframe final
                    df_final = df_upload[colonnes_a_garder].copy()
                    
                    # Vérifier si la colonne identifiant_referentiel existe
                    if 'identifiant_referentiel' not in df_final.columns:
                        st.info("⚙️ Génération automatique des identifiants référentiels...")
                        # Générer les identifiants basés sur le nom du groupement
                        prefix = groupement_nom_import.lower().replace(' ', '_')
                        df_final['identifiant_referentiel'] = [f"{prefix}_{i+1}" for i in range(len(df_final))]
                    
                    # Remplir la colonne groupement_id avec l'ID du groupement sélectionné
                    df_final['groupement_id'] = groupement_id_import
                    
                    # Afficher les colonnes manquantes nécessaires pour l'import
                    colonnes_necessaires = [
                        'identifiant_referentiel', 'titre', 'groupement_id'
                    ]
                    colonnes_manquantes = [col for col in colonnes_necessaires if col not in df_final.columns or df_final[col].isna().all()]
                    
                    if colonnes_manquantes and 'groupement_id' not in colonnes_manquantes:
                        st.warning(f"⚠️ Colonnes obligatoires manquantes : {', '.join(colonnes_manquantes)}")
                    
                    # Afficher le dataframe final
                    st.markdown("### 📋 Aperçu du dataframe final à importer")
                    st.dataframe(df_final, use_container_width=True)
                    
                    st.info(f"ℹ️ Total : {len(df_final)} indicateur(s) prêt(s) pour l'import")
                    
                    # Demander confirmation
                    st.markdown("---")
                    st.markdown("### ✅ Confirmation de l'import")
                    
                    col_oui, col_non = st.columns(2)
                    
                    with col_oui:
                        if st.button("✅ OUI - Importer les indicateurs", use_container_width=True, type="primary"):
                            with st.spinner(f"Import des indicateurs en cours vers {env_label}..."):
                                success_import = importer_indicateurs_groupement(df_final, engine_ecriture)
                            
                            if success_import:
                                st.success(f"✅ {len(df_final)} indicateur(s) importé(s) avec succès en {env_label} !")
                                
                                # Associer les indicateurs à leur catégorie_tag
                                with st.spinner(f"Association des indicateurs à la catégorie tag '{groupement_nom_import}'..."):
                                    success_assoc, nb_associations = associer_indicateurs_categorie_tag(
                                        groupement_id_import,
                                        groupement_nom_import,
                                        engine_ecriture
                                    )
                                
                                if success_assoc:
                                    st.success(f"✅ {nb_associations} indicateur(s) associé(s) à la catégorie tag **{groupement_nom_import}** !")
                                    st.balloons()
                                else:
                                    st.warning("⚠️ Les indicateurs ont été importés mais l'association à la catégorie tag a échoué")
                    
                    with col_non:
                        if st.button("❌ NON - Annuler l'import", use_container_width=True):
                            st.warning("❌ Import annulé")
                            st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Erreur lors de la lecture du fichier : {str(e)}")
    
    st.markdown("---")
    
    # ==========================
    # ÉTAPE 4 : IMPORT DES VALEURS
    # ==========================
    
    st.header("4️⃣ Importer les valeurs des indicateurs")
    
    st.markdown("""
    Cette étape permet d'importer les valeurs des indicateurs depuis un fichier CSV.
    
    **Colonnes obligatoires :**
    - `resultat` : La valeur de l'indicateur
    - `date_valeur` : La date de la valeur (sera convertie au 1er janvier de l'année)
    - `collectivite_id` : L'ID de la collectivité
    - `indicateur_id` OU `titre` : L'ID de l'indicateur ou son titre
    """)
    
    # Upload du fichier
    uploaded_file_valeurs = st.file_uploader(
        "📁 Glissez-déposez ou sélectionnez votre fichier CSV",
        type=['csv'],
        help="Le fichier doit contenir les colonnes obligatoires mentionnées ci-dessus",
        key="file_uploader_valeurs"
    )
    
    if uploaded_file_valeurs is not None:
        try:
            # Lire le fichier CSV
            df_valeurs = pd.read_csv(uploaded_file_valeurs, sep=',')
            
            st.success(f"✅ Fichier chargé : {len(df_valeurs)} lignes")
            
            # Vérifier les colonnes obligatoires
            colonnes_obligatoires_base = ['resultat', 'date_valeur', 'collectivite_id']
            colonnes_manquantes = [col for col in colonnes_obligatoires_base if col not in df_valeurs.columns]
            
            # Vérifier qu'on a soit indicateur_id soit titre
            has_indicateur_id = 'indicateur_id' in df_valeurs.columns
            has_titre = 'titre' in df_valeurs.columns
            
            if not has_indicateur_id and not has_titre:
                colonnes_manquantes.append('indicateur_id OU titre')
            
            if colonnes_manquantes:
                st.error(f"❌ Colonnes obligatoires manquantes : {', '.join(colonnes_manquantes)}")
                st.stop()
            
            st.success("✅ Toutes les colonnes obligatoires sont présentes")
            
            # Créer le dataframe final
            df_final_valeurs = df_valeurs.copy()
            
            # 1. Transformer date_valeur en datetime au 1er janvier de l'année
            st.info("⚙️ Transformation des dates au 1er janvier de l'année...")
            df_final_valeurs['date_valeur'] = pd.to_datetime(df_final_valeurs['date_valeur'], errors='coerce')
            df_final_valeurs['date_valeur'] = df_final_valeurs['date_valeur'].apply(
                lambda x: pd.Timestamp(year=x.year, month=1, day=1) if pd.notnull(x) else None
            )
            
            # Supprimer les lignes avec date_valeur null
            nb_avant = len(df_final_valeurs)
            df_final_valeurs = df_final_valeurs.dropna(subset=['date_valeur'])
            nb_apres = len(df_final_valeurs)
            if nb_avant > nb_apres:
                st.warning(f"⚠️ {nb_avant - nb_apres} ligne(s) supprimée(s) (date_valeur invalide)")
            
            # 2. Si on a "titre" au lieu de "indicateur_id", faire la jointure
            if not has_indicateur_id and has_titre:
                st.info("⚙️ Récupération des indicateur_id depuis les titres...")
                
                # Charger le mapping titre -> indicateur_id
                mapping_titre_id = charger_mapping_titre_indicateur_id(engine_lecture)
                
                if not mapping_titre_id:
                    st.error("❌ Impossible de charger le mapping des titres. Assurez-vous que les indicateurs existent en base.")
                    st.stop()
                
                # Ajouter la colonne indicateur_id
                df_final_valeurs['indicateur_id'] = df_final_valeurs['titre'].map(mapping_titre_id)
                
                # Vérifier s'il y a des titres non trouvés
                titres_non_trouves = df_final_valeurs[df_final_valeurs['indicateur_id'].isna()]['titre'].unique()
                if len(titres_non_trouves) > 0:
                    st.error(f"❌ Titres d'indicateurs non trouvés en base ({len(titres_non_trouves)} titres uniques) :")
                    st.write(titres_non_trouves.tolist())
                    st.warning("⚠️ Ces lignes seront supprimées du fichier final")
                    
                    # Supprimer les lignes sans indicateur_id
                    nb_avant = len(df_final_valeurs)
                    df_final_valeurs = df_final_valeurs.dropna(subset=['indicateur_id'])
                    nb_apres = len(df_final_valeurs)
                    st.info(f"ℹ️ {nb_avant - nb_apres} ligne(s) supprimée(s)")
            
            # 3. Sélectionner uniquement les colonnes nécessaires
            if 'metadonnee_id' in df_final_valeurs.columns:
                colonnes_finales = ['collectivite_id', 'indicateur_id', 'date_valeur', 'resultat', 'metadonnee_id']
            else:
                colonnes_finales = ['collectivite_id', 'indicateur_id', 'date_valeur', 'resultat']
            
            df_final_valeurs = df_final_valeurs[colonnes_finales].copy()
            
            # Convertir les types
            df_final_valeurs['collectivite_id'] = df_final_valeurs['collectivite_id'].astype(int)
            df_final_valeurs['indicateur_id'] = df_final_valeurs['indicateur_id'].astype(int)
            df_final_valeurs['metadonnee_id'] = df_final_valeurs['metadonnee_id'].astype(int)
            df_final_valeurs['resultat'] = pd.to_numeric(df_final_valeurs['resultat'], errors='coerce')
            
            # Supprimer les lignes avec resultat null
            nb_avant = len(df_final_valeurs)
            df_final_valeurs = df_final_valeurs.dropna(subset=['resultat'])
            nb_apres = len(df_final_valeurs)
            if nb_avant > nb_apres:
                st.warning(f"⚠️ {nb_avant - nb_apres} ligne(s) supprimée(s) (resultat invalide)")
            
            if len(df_final_valeurs) == 0:
                st.error("❌ Aucune donnée valide à importer après nettoyage")
                st.stop()
            
            # 4. Vérifier les doublons sur (date_valeur, collectivite_id, indicateur_id)
            st.info("🔍 Vérification des doublons...")
            pk_cols = ['date_valeur', 'collectivite_id', 'indicateur_id']
            doublons = df_final_valeurs.duplicated(subset=pk_cols, keep=False)
            
            if doublons.any():
                st.error("❌ **ERREUR : Doublons détectés !**")
                st.markdown("""
                Des lignes avec la même combinaison (date_valeur, collectivite_id, indicateur_id) 
                ont été trouvées. Vous devez corriger ces doublons avant l'import.
                """)
                
                df_doublons = df_final_valeurs[doublons].copy()
                
                # Charger les titres des indicateurs pour affichage
                st.info("⚙️ Chargement des titres d'indicateurs...")
                query_titres = text("""
                    SELECT id, titre
                    FROM indicateur_definition
                    WHERE id = ANY(:indicateur_ids)
                """)
                
                indicateur_ids = df_doublons['indicateur_id'].unique().tolist()
                
                with engine_lecture.connect() as conn:
                    df_titres = pd.read_sql_query(query_titres, conn, params={"indicateur_ids": indicateur_ids})
                
                # Créer un mapping id -> titre
                mapping_id_titre = dict(zip(df_titres['id'], df_titres['titre']))
                
                # Ajouter la colonne titre
                df_doublons['titre'] = df_doublons['indicateur_id'].map(mapping_id_titre)
                
                # Réorganiser les colonnes pour mettre titre en premier
                cols_ordre = ['titre', 'collectivite_id', 'date_valeur', 'resultat', 'indicateur_id']
                df_doublons_affichage = df_doublons[cols_ordre].sort_values(['titre', 'collectivite_id', 'date_valeur'])
                
                # Afficher les doublons
                st.dataframe(
                    df_doublons_affichage,
                    use_container_width=True
                )
                
                # Statistiques sur les doublons
                nb_groupes_doublons = df_final_valeurs[doublons].groupby(pk_cols).size().shape[0]
                st.markdown(f"""
                **📊 Statistiques des doublons :**
                - Nombre de groupes en doublon : {nb_groupes_doublons}
                - Nombre total de lignes concernées : {len(df_doublons)}
                """)
                
                st.stop()
            
            st.success("✅ Aucun doublon détecté")
            
            # Afficher le dataframe final
            st.markdown("---")
            st.markdown("### 📋 Aperçu du dataframe final à importer")
            st.dataframe(df_final_valeurs.head(100), use_container_width=True)
            
            if len(df_final_valeurs) > 100:
                st.info(f"ℹ️ Affichage des 100 premières lignes sur {len(df_final_valeurs)} total")
            
            # Statistiques
            col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
            with col_stat1:
                st.metric("📝 Total de lignes", f"{len(df_final_valeurs):,}")
            with col_stat2:
                st.metric("📊 Indicateurs uniques", df_final_valeurs['indicateur_id'].nunique())
            with col_stat3:
                st.metric("🏘️ Collectivités uniques", df_final_valeurs['collectivite_id'].nunique())
            with col_stat4:
                annees = df_final_valeurs['date_valeur'].dt.year.unique()
                st.metric("📅 Années", f"{annees.min()}-{annees.max()}")
            
            # Demander confirmation
            st.markdown("---")
            st.markdown("### ✅ Confirmation de l'import")
            
            st.warning(f"⚠️ **Attention :** Cette action va envoyer **{len(df_final_valeurs):,} lignes** vers l'environnement **{env_label}** via l'API.")
            
            col_oui_valeurs, col_non_valeurs = st.columns(2)
            
            with col_oui_valeurs:
                if st.button("✅ OUI - Importer les valeurs", use_container_width=True, type="primary", key="btn_import_valeurs"):
                    # Container pour la progression
                    progress_container = st.container()
                    
                    result = importer_valeurs_via_api(df_final_valeurs, env_label, progress_container)
                    
                    st.markdown("---")
                    
                    if result['success']:
                        st.success(f"✅ {result['message']}")
                        st.balloons()
                        
                        col_res1, col_res2, col_res3 = st.columns(3)
                        with col_res1:
                            st.metric("📊 Total de lignes", f"{result['nb_total']:,}")
                        with col_res2:
                            st.metric("📤 Lignes insérées", f"{result['nb_inserted']:,}")
                        with col_res3:
                            st.metric("📦 Batches envoyés", result.get('nb_batches', 0))
                    else:
                        st.error(f"❌ {result['message']}")
                        
                        if result.get('failed_batches', 0) > 0:
                            st.warning(f"⚠️ {result['failed_batches']} batch(s) ont échoué sur {result.get('nb_batches', 0)} total")
                            st.info(f"💡 {result['nb_inserted']:,} lignes ont quand même été insérées avec succès")
            
            with col_non_valeurs:
                if st.button("❌ NON - Annuler l'import", use_container_width=True, key="btn_annuler_valeurs"):
                    st.warning("❌ Import annulé")
                    st.rerun()
        
        except Exception as e:
            st.error(f"❌ Erreur lors du traitement du fichier : {str(e)}")
            import traceback
            st.code(traceback.format_exc())
