import streamlit as st
import pandas as pd
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
Cette page permet de créer des groupements d'indicateurs en 3 étapes :
1. 📝 **Nommer le groupement** et l'insérer en base
2. 🏘️ **Sélectionner les collectivités** du groupement
3. 📊 **Importer les indicateurs** depuis un fichier Excel (à venir)
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
    """Insère un nouveau groupement dans la table groupement."""
    try:
        query = text("""
            INSERT INTO groupement (nom)
            VALUES (:nom)
            RETURNING id, nom
        """)
        
        with engine.begin() as conn:
            result = conn.execute(query, {"nom": nom_groupement})
            row = result.fetchone()
            return True, row[0], row[1]
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
        # Créer un mappin   g id -> nom pour le selectbox
        groupements_dict = dict(zip(df_groupements_select['id'], df_groupements_select['nom']))
        
        # Pré-sélectionner le dernier groupement créé si disponible
        default_index = 0
        if 'dernier_groupement_cree' in st.session_state:
            dernier_id = st.session_state.dernier_groupement_cree['id']
            if dernier_id in groupements_dict:
                default_index = list(groupements_dict.keys()).index(dernier_id)
        
        # Sélection du groupement
        groupement_id_selectionne = st.selectbox(
            "Sélectionnez le groupement",
            options=list(groupements_dict.keys()),
            format_func=lambda x: groupements_dict[x],
            index=default_index,
            key="selectbox_groupement"
        )
        
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
            key="selectbox_groupement_import"
        )
        
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
                        with st.spinner(f"Import en cours vers {env_label}..."):
                            success_import = importer_indicateurs_groupement(df_final, engine_ecriture)
                        
                        if success_import:
                            st.success(f"✅ {len(df_final)} indicateur(s) importé(s) avec succès en {env_label} !")
                            st.balloons()
                
                with col_non:
                    if st.button("❌ NON - Annuler l'import", use_container_width=True):
                        st.warning("❌ Import annulé")
                        st.rerun()
                
            except Exception as e:
                st.error(f"❌ Erreur lors de la lecture du fichier : {str(e)}")
