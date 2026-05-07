import streamlit as st
import pandas as pd
import requests
import json
import yaml
from sqlalchemy import text
from datetime import datetime

try:
    from ruamel.yaml import YAML
    RUAMEL_AVAILABLE = True
except ImportError:
    RUAMEL_AVAILABLE = False

from utils.db import (
    get_engine,
    get_engine_prod,
    get_engine_pre_prod
)

# Configuration de la page
st.set_page_config(layout="wide")
st.title("🌀 Import des indicateurs")

# Mode debug
if 'debug_mode' not in st.session_state:
    st.session_state.debug_mode = False

col_debug, col_space = st.columns([1, 5])
with col_debug:
    st.session_state.debug_mode = st.toggle("🐛 Mode Debug", value=st.session_state.debug_mode)

st.markdown("---")

# ==========================
# FONCTIONS
# ==========================

def charger_config(path_yaml: str) -> list:
    """Charge la configuration YAML des indicateurs."""
    with open(path_yaml, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config["indicateurs"]


def extract_type_collectivite(dimensions):
    """Retourne la liste des types de collectivités présents dans les dimensions."""
    types_valides = ["commune", "epci", "ept", "departement", "region"]
    result = []

    for dim in dimensions:
        name = dim.get("name", "")
        if "geocode_" in name:
            suffix = name.split("geocode_")[-1]
            if suffix in types_valides and suffix not in result:
                result.append(suffix)

    return result


def extract_api_nom_axe(dimensions):
    """Retourne la liste des 'axes' non temporels ou géographiques."""
    exclude_keywords = ["annee", "date", "libelle", "geocode"]
    result = []

    for dim in dimensions:
        name = dim.get("name", "")
        if all(excl not in name for excl in exclude_keywords):
            suffix = name.split(".")[-1]
            if suffix not in result:
                result.append(suffix)

    return result[0] if result else ""  # Retourne le premier axe ou chaîne vide


def recuperer_metadonnees_api():
    """Récupère les métadonnées des cubes depuis l'API.
    
    Retourne un dictionnaire avec comme clé un tuple (ID, api_nom_cube)
    car un même ID peut apparaître dans plusieurs cubes différents.
    """
    # Récupérer le token depuis les secrets Streamlit
    api_indicateurs_token = st.secrets.get("api_indicateurs_token", "")
    if not api_indicateurs_token:
        raise ValueError(
            "Token API manquant. Configurez 'api_indicateurs_token' dans .streamlit/secrets.toml"
        )
    
    URL_META = "https://api.indicateurs.ecologie.gouv.fr/cubejs-api/v1/meta"
    HEADERS = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_indicateurs_token}",
    }

    response = requests.get(URL_META, headers=HEADERS)
    response.raise_for_status()
    data = response.json()

    d = {}

    for cube in data.get("cubes", []):
        cube_name = cube.get("name")
        measures = cube.get("measures", [])
        if not measures:
            continue

        dimensions = cube.get("dimensions", [])
        type_collectivite = extract_type_collectivite(dimensions)
        api_nom_axe = extract_api_nom_axe(dimensions)

        # Boucle sur toutes les mesures du cube
        for measure in measures:
            short_title = measure.get("shortTitle", "")
            if not short_title.startswith("Id"):
                continue  # ignore les mesures sans identifiant clair

            ID = short_title[2:]  # "Id141" → "141"

            # Utiliser le couple (ID, cube_name) comme clé unique
            key = (ID, cube_name)
            d[key] = {
                "ID": ID,
                "api_nom_cube": cube_name,
                "type_collectivite": type_collectivite,
                "api_nom_axe": api_nom_axe,
            }

    return d


def comparer_avec_yaml(metadonnees_api: dict, indicateurs_yaml: list) -> dict:
    """Compare les métadonnées de l'API avec le fichier YAML.
    
    Args:
        metadonnees_api: dict avec clés (ID, api_nom_cube)
        indicateurs_yaml: list des indicateurs du YAML
    
    Returns:
        dict avec les différences trouvées
    """
    differences = {
        "a_jour": [],
        "a_mettre_a_jour": [],
        "manquants_yaml": [],
        "manquants_api": []
    }
    
    # Créer un dictionnaire des indicateurs YAML par (ID, api_nom_cube)
    yaml_dict = {}
    for idx, ind in enumerate(indicateurs_yaml):
        key = (ind['ID'], ind.get('api_nom_cube'))
        yaml_dict[key] = {**ind, '_yaml_index': idx}  # Garder l'index pour la mise à jour
    
    # Vérifier les indicateurs dans le YAML
    for key, indic_yaml in yaml_dict.items():
        ID, cube_name = key
        
        if key in metadonnees_api:
            meta_api = metadonnees_api[key]
            
            # Comparer les champs
            differences_indic = {}
            
            # api_nom_cube devrait déjà matcher (c'est dans la clé)
            # mais on vérifie quand même
            if indic_yaml.get('api_nom_cube') != meta_api['api_nom_cube']:
                differences_indic['api_nom_cube'] = {
                    'yaml': indic_yaml.get('api_nom_cube'),
                    'api': meta_api['api_nom_cube']
                }
            
            # Comparer les types de collectivités (en tant que listes triées)
            yaml_types = sorted(indic_yaml.get('type_collectivite', []))
            api_types = sorted(meta_api['type_collectivite'])
            if yaml_types != api_types:
                differences_indic['type_collectivite'] = {
                    'yaml': yaml_types,
                    'api': api_types
                }
            
            # Comparer api_nom_axe
            yaml_axe = indic_yaml.get('api_nom_axe', '')
            api_axe = meta_api['api_nom_axe']
            if yaml_axe != api_axe:
                differences_indic['api_nom_axe'] = {
                    'yaml': yaml_axe,
                    'api': api_axe
                }
            
            if differences_indic:
                differences['a_mettre_a_jour'].append({
                    'ID': ID,
                    'api_nom_cube': cube_name,
                    'nom': indic_yaml.get('metadata', {}).get('nom_donnees', 'N/A'),
                    'differences': differences_indic,
                    '_yaml_index': indic_yaml['_yaml_index']
                })
            else:
                differences['a_jour'].append({
                    'ID': ID,
                    'api_nom_cube': cube_name,
                    'nom': indic_yaml.get('metadata', {}).get('nom_donnees', 'N/A')
                })
        else:
            differences['manquants_api'].append({
                'ID': ID,
                'api_nom_cube': cube_name,
                'nom': indic_yaml.get('metadata', {}).get('nom_donnees', 'N/A')
            })
    
    # Vérifier les indicateurs de l'API manquants dans le YAML
    for key in metadonnees_api.keys():
        if key not in yaml_dict:
            ID, cube_name = key
            differences['manquants_yaml'].append({
                'ID': ID,
                'api_nom_cube': cube_name,
                'meta': metadonnees_api[key]
            })
    
    return differences


def mettre_a_jour_yaml(indicateurs_yaml: list, metadonnees_api: dict, keys_a_modifier: list, path_yaml: str, debug_container=None):
    """Met à jour le fichier YAML avec les nouvelles métadonnées.
    
    Args:
        indicateurs_yaml: liste des indicateurs du YAML
        metadonnees_api: dict avec clés (ID, api_nom_cube)
        keys_a_modifier: liste de tuples (ID, api_nom_cube) à modifier
        path_yaml: chemin du fichier YAML
        debug_container: conteneur Streamlit pour afficher les logs
    """
    
    debug_messages = []
    
    def debug_print(msg):
        print(f"[YAML UPDATE] {msg}")  # Log dans le terminal
        debug_messages.append(msg)
        if debug_container:
            debug_container.code('\n'.join(debug_messages))
    
    print("\n" + "="*60)
    print("[YAML UPDATE] DÉBUT DE LA MISE À JOUR DU FICHIER YAML")
    print("="*60)
    debug_print("🔍 Début de la mise à jour...")
    
    if RUAMEL_AVAILABLE:
        debug_print("✅ ruamel.yaml disponible")
        # Utiliser ruamel.yaml pour préserver le formatage
        yaml_handler = YAML()
        yaml_handler.preserve_quotes = True
        yaml_handler.default_flow_style = False
        
        debug_print(f"📖 Lecture du fichier {path_yaml}...")
        with open(path_yaml, 'r', encoding='utf-8') as f:
            config = yaml_handler.load(f)
        debug_print("✅ Fichier lu avec succès")
        
        # Mettre à jour les indicateurs
        debug_print(f"🔄 Mise à jour de {len(keys_a_modifier)} indicateur(s)...")
        for indic in config.get('indicateurs', []):
            key = (indic.get('ID'), indic.get('api_nom_cube'))
            if key in keys_a_modifier and key in metadonnees_api:
                meta_api = metadonnees_api[key]
                indic['api_nom_cube'] = meta_api['api_nom_cube']
                indic['type_collectivite'] = meta_api['type_collectivite']
                indic['api_nom_axe'] = meta_api['api_nom_axe']
                debug_print(f"  ✓ ID {indic['ID']} / cube {indic['api_nom_cube']} mis à jour")
        
        debug_print(f"💾 Écriture du fichier {path_yaml}...")
        with open(path_yaml, 'w', encoding='utf-8') as f:
            yaml_handler.dump(config, f)
        debug_print("✅ Fichier écrit avec succès")
    else:
        debug_print("⚠️ ruamel.yaml non disponible, utilisation de la manipulation de texte")
        # Méthode alternative : manipulation de texte ligne par ligne
        debug_print(f"📖 Lecture du fichier {path_yaml}...")
        with open(path_yaml, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        debug_print(f"✅ {len(lines)} lignes lues")
        
        modifications = {}
        for key in keys_a_modifier:
            if key in metadonnees_api:
                modifications[key] = metadonnees_api[key]
        debug_print(f"🔄 Préparation des modifications pour {len(modifications)} indicateur(s)")
        
        new_lines = []
        current_key = None
        current_id = None
        current_cube = None
        in_indicateur = False
        in_type_collectivite = False
        skip_next_type_collectivite_lines = False
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Détecter le début d'un nouvel indicateur
            if line.strip().startswith('- api_nom_cube:'):
                # Reset
                in_indicateur = False
                current_id = None
                current_cube = None
                current_key = None
                
                # Extraire le cube
                cube_match = line.split('api_nom_cube:')[-1].strip()
                current_cube = cube_match
                new_lines.append(line)
            
            # Détecter l'ID de l'indicateur actuel
            elif "ID:" in line or "ID :" in line:
                id_match = line.split("ID:")[-1].strip() if "ID:" in line else line.split("ID :")[-1].strip()
                id_value = id_match.strip("'\"")
                current_id = id_value
                
                # Créer la clé composite
                if current_id and current_cube:
                    current_key = (current_id, current_cube)
                    if current_key in modifications:
                        in_indicateur = True
                        debug_print(f"  📝 Détecté ID {current_id} / cube {current_cube} à modifier")
                    else:
                        in_indicateur = False
                new_lines.append(line)
            
            # Si on est dans un indicateur à modifier
            elif in_indicateur and current_key:
                # Mettre à jour api_nom_cube
                if line.strip().startswith('api_nom_cube:'):
                    indent = len(line) - len(line.lstrip())
                    new_lines.append(' ' * indent + f"api_nom_cube: {modifications[current_key]['api_nom_cube']}\n")
                    debug_print(f"    ✓ api_nom_cube modifié")
                
                # Mettre à jour api_nom_axe
                elif line.strip().startswith('api_nom_axe:'):
                    indent = len(line) - len(line.lstrip())
                    new_axe = modifications[current_key]['api_nom_axe']
                    new_lines.append(' ' * indent + f"api_nom_axe: {new_axe}\n")
                    debug_print(f"    ✓ api_nom_axe modifié")
                
                # Détecter le début de type_collectivite
                elif line.strip().startswith('type_collectivite:'):
                    indent = len(line) - len(line.lstrip())
                    new_lines.append(line)
                    in_type_collectivite = True
                    skip_next_type_collectivite_lines = True
                    # Ajouter les nouvelles valeurs
                    for tc in modifications[current_key]['type_collectivite']:
                        new_lines.append(' ' * (indent + 2) + f"- {tc}\n")
                    debug_print(f"    ✓ type_collectivite modifié")
                
                # Ignorer les anciennes valeurs de type_collectivite
                elif skip_next_type_collectivite_lines and line.strip().startswith('-'):
                    # Ne rien faire, on ignore cette ligne
                    pass
                
                # Fin de la section type_collectivite
                elif skip_next_type_collectivite_lines and not line.strip().startswith('-'):
                    skip_next_type_collectivite_lines = False
                    in_type_collectivite = False
                    new_lines.append(line)
                
                # Fin de l'indicateur (nouvelle section ou nouveau tiret principal)
                elif line.strip().startswith('- api_nom_cube:'):
                    in_indicateur = False
                    current_key = None
                    # On traite cette ligne dans la prochaine itération
                    i -= 1
                
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
            
            i += 1
        
        # Écrire le fichier
        debug_print(f"💾 Écriture du fichier {path_yaml}...")
        with open(path_yaml, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        debug_print("✅ Fichier écrit avec succès")


def recuperer_donnees_api(
    indic: dict,
    detail_container=None,
    ct_filter=None,
    paginer_par_annee: bool = True,
) -> pd.DataFrame:
    """Récupère les données d'un indicateur depuis l'API data.gouv.
    
    Applique automatiquement le ratio défini dans la config YAML sur les résultats
    (par exemple, ratio=100 pour convertir 0.5 en 50%).
    
    Args:
        indic: Dictionnaire de configuration de l'indicateur (doit contenir 'ratio')
        detail_container: Container Streamlit pour afficher les détails
        ct_filter: Dictionnaire de filtres par type de collectivité {'commune': [list_siren], 'epci': [list_siren]}
        paginer_par_annee: Si True, pagine par tranches d'années pour commune/epci.
            Si False, on bascule sur la pagination simple (par offset uniquement) pour
            tous les types de collectivités.
    
    Returns:
        DataFrame avec les résultats (déjà multipliés par le ratio)
    """
    
    # Récupérer le token depuis les secrets Streamlit
    api_token = st.secrets.get("api_indicateurs_token", "")
    if not api_token:
        raise ValueError(
            "Token API manquant. Configurez 'api_indicateurs_token' dans .streamlit/secrets.toml"
        )
    
    url_post = "https://api.indicateurs.ecologie.gouv.fr/cubejs-api/v1/load"
    headers_post = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}",
    }

    all_dfs = []
    api_nom_cube = indic['api_nom_cube']
    ID = indic['ID']
    total_lignes = 0

    for tc in indic['type_collectivite']:
        measure_name = f"{api_nom_cube}.id_{ID}"
        geocode_dim = f"{api_nom_cube}.geocode_{tc}"
        libelle_dim = f"{api_nom_cube}.libelle_{tc}"
        date_dim = f"{api_nom_cube}.date_mesure"

        # Dimensions dynamiques
        dimensions = [geocode_dim, libelle_dim]
        if indic.get('api_nom_axe'):
            axe_dim = f"{api_nom_cube}.{indic['api_nom_axe']}"
            dimensions.append(axe_dim)

        # Requêtes paginées
        limit = 10000
        lignes_tc = 0
        
        # Pour commune et epci : pagination par tranches d'années (beaucoup de données)
        # Pour region, departement, ept : pagination simple (peu de données)
        # Si paginer_par_annee=False, on bascule tout le monde sur la pagination simple.
        if tc in ['commune', 'epci'] and paginer_par_annee:
            annee_actuelle = datetime.now().year
            # On récupère les années par paquets pour limiter le nombre d'allers-retours HTTP
            BATCH_YEARS = 3
            annee_debut = 2010
            
            for batch_start in range(annee_debut, annee_actuelle + 1, BATCH_YEARS):
                batch_end = min(batch_start + BATCH_YEARS - 1, annee_actuelle)
                
                # Libellé de la plage d'années (réutilisé pour tous les messages du batch)
                if batch_start == batch_end:
                    libelle_plage = f"{batch_start}"
                else:
                    libelle_plage = f"{batch_start} → {batch_end}"
                
                # Affichage de la plage en cours AVANT la requête (pour suivre l'avancement)
                if detail_container:
                    detail_container.caption(
                        f"    📅 {tc} — récupération {libelle_plage}… "
                        f"(cumul {tc} : {lignes_tc:,} lignes)"
                    )
                
                offset = 0
                lignes_batch = 0
                
                # Pagination avec offset pour chaque batch d'années
                while True:
                    # Construction de la requête avec filtre sur la plage d'années
                    query = {
                        "measures": [measure_name],
                        "timezone": "UTC",
                        "dimensions": dimensions,
                        "timeDimensions": [
                            {
                                "dimension": date_dim,
                                "granularity": "year",
                                "dateRange": [f"{batch_start}-01-01", f"{batch_end}-12-31"]
                            }
                        ],
                        "order": {date_dim: "asc"},
                        "limit": limit,
                        "offset": offset
                    }
                    
                    # Ajouter les filtres de collectivités si nécessaire
                    if ct_filter and tc in ct_filter and ct_filter[tc]:
                        query["filters"] = [
                            {
                                "dimension": geocode_dim,
                                "operator": "equals",
                                "values": ct_filter[tc]
                            }
                        ]
                    
                    data_post = {"query": query}
                    
                    response = requests.post(url_post, headers=headers_post, data=json.dumps(data_post), timeout=60)
                    
                    if response.status_code == 200:
                        rows = response.json().get("data", [])
                        if not rows:
                            break

                        df = pd.DataFrame(rows)
                        df["type_collectivite"] = tc
                        all_dfs.append(df)

                        lignes_batch += len(rows)
                        lignes_tc += len(rows)
                        total_lignes += len(rows)
                        
                        # Affichage en temps réel après chaque page reçue
                        if detail_container:
                            detail_container.caption(
                                f"    📥 {tc} — {libelle_plage} : "
                                f"{lignes_batch:,} lignes reçues "
                                f"(cumul {tc} : {lignes_tc:,} | total : {total_lignes:,})"
                            )
                        
                        # Si on reçoit moins de lignes que la limite, on a tout récupéré pour ce batch
                        if len(rows) < limit:
                            break
                        
                        offset += limit
                    else:
                        st.error(
                            f"Erreur {response.status_code} pour {tc} - années {batch_start}-{batch_end} : {response.text}"
                        )
                        break
                
                # Affichage du résumé pour ce batch d'années
                if detail_container and lignes_batch > 0:
                    detail_container.caption(
                        f"    ✅ {tc} — {libelle_plage} : {lignes_batch:,} lignes "
                        f"(cumul {tc} : {lignes_tc:,} | total : {total_lignes:,})"
                    )
        
        else:
            # Pagination simple pour region, departement, ept (peu de données)
            offset = 0
            
            if detail_container:
                detail_container.caption(
                    f"    🔄 Pagination simple pour {tc}… (cumul {tc} : {lignes_tc:,} lignes)"
                )
            
            while True:
                # Construction de la requête sans filtre d'année
                query = {
                    "measures": [measure_name],
                    "timezone": "UTC",
                    "dimensions": dimensions,
                    "timeDimensions": [{"dimension": date_dim, "granularity": "year"}],
                    "order": {date_dim: "asc"},
                    "limit": limit,
                    "offset": offset
                }
                
                # Ajouter les filtres de collectivités si nécessaire
                if ct_filter and tc in ct_filter and ct_filter[tc]:
                    query["filters"] = [
                        {
                            "dimension": geocode_dim,
                            "operator": "equals",
                            "values": ct_filter[tc]
                        }
                    ]
                
                data_post = {"query": query}
                
                response = requests.post(url_post, headers=headers_post, data=json.dumps(data_post), timeout=60)
                
                if response.status_code == 200:
                    rows = response.json().get("data", [])
                    if not rows:
                        break

                    df = pd.DataFrame(rows)
                    df["type_collectivite"] = tc
                    all_dfs.append(df)

                    lignes_tc += len(rows)
                    total_lignes += len(rows)
                    
                    # Affichage en temps réel après chaque page reçue
                    if detail_container:
                        detail_container.caption(
                            f"    📥 {tc} : {lignes_tc:,} lignes reçues "
                            f"(total : {total_lignes:,})"
                        )
                    
                    # Si on reçoit moins de lignes que la limite, on a tout récupéré
                    if len(rows) < limit:
                        break
                    
                    offset += limit
                else:
                    st.error(f"Erreur {response.status_code} pour {tc} : {response.text}")
                    break
        
        # Affichage du total pour le type de collectivité
        if detail_container:
            detail_container.markdown(f"  - **{tc}** : {lignes_tc:,} lignes récupérées au total")

    if not all_dfs:
        return pd.DataFrame()

    # Concaténation des résultats
    df_total = pd.concat(all_dfs, ignore_index=True)
    
    # Affichage du total
    if detail_container:
        detail_container.markdown(f"**Total : {total_lignes:,} lignes récupérées**")

    # Unification des geocodes/libelles
    geocode_cols = [col for col in df_total.columns if col.startswith(api_nom_cube + '.geocode_')]
    libelle_cols = [col for col in df_total.columns if col.startswith(api_nom_cube + '.libelle_')]

    df_total["geocode"] = df_total[geocode_cols].bfill(axis=1).iloc[:, 0]
    df_total["libelle"] = df_total[libelle_cols].bfill(axis=1).iloc[:, 0]
    df_total.drop(columns=geocode_cols + libelle_cols, inplace=True)

    # Formatage des geocodes pour les régions/départements
    df_total['geocode'] = df_total['geocode'].astype(str)
    df_total.loc[df_total['type_collectivite'] == 'region', 'geocode'] = 'R' + df_total.loc[df_total['type_collectivite'] == 'region', 'geocode'].str.zfill(2)
    df_total.loc[df_total['type_collectivite'] == 'departement', 'geocode'] = 'D' + df_total.loc[df_total['type_collectivite'] == 'departement', 'geocode'].str.zfill(2)
    
    return df_total


def nettoyer_et_joindre_collectivites(df_total: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Jointure avec les collectivités TET et nettoyage des données.
    
    Returns:
        tuple: (df_correspondantes, df_non_correspondantes)
    """
    
    engine_prod = get_engine_prod()

    # Chargement des collectivités TET
    ct_tet = pd.read_sql_query(
        sql=text("SELECT * FROM collectivite WHERE type != 'test' and siren <> ''"),
        con=engine_prod.connect()
    )
    
    ct_tet['code_siren_insee'] = ct_tet['siren'].astype(str)
    ct_tet['code_siren_insee'] = ct_tet.apply(
        lambda x: 'R' + x['region_code'] if x['type'] == 'region' else x['code_siren_insee'], 
        axis=1
    )
    ct_tet['code_siren_insee'] = ct_tet.apply(
        lambda x: 'D' + x['departement_code'] if x['type'] == 'departement' else x['code_siren_insee'], 
        axis=1
    )
    
    # Vérifier les doublons dans ct_tet
    duplicated_codes = ct_tet[ct_tet.duplicated(subset=['code_siren_insee'], keep=False)]
    if len(duplicated_codes) > 0:
        st.warning(f"⚠️ **Attention** : {duplicated_codes['code_siren_insee'].nunique()} code(s) SIREN/INSEE en doublon dans la table collectivite")
        with st.expander("🔍 Voir les doublons dans la table collectivite"):
            st.dataframe(
                duplicated_codes[['id', 'nom', 'code_siren_insee', 'type', 'siren']].sort_values('code_siren_insee'),
                width='stretch'
            )
            st.info("💡 Ces doublons vont créer des lignes dupliquées lors de la jointure. Considérez nettoyer la base de données.")
    
    # Compter les lignes avant jointure
    nb_lignes_avant = len(df_total)
    
    # Jointure avec indicateur pour identifier les lignes non correspondantes
    df_avec_indicateur = df_total.merge(
        ct_tet[['id', 'code_siren_insee']],
        left_on='geocode',
        right_on='code_siren_insee',
        how='left',
        indicator=True
    )
    
    # Séparer les correspondantes et non correspondantes
    df_correspondantes = df_avec_indicateur[df_avec_indicateur['_merge'] == 'both'].copy()
    df_non_correspondantes = df_avec_indicateur[df_avec_indicateur['_merge'] == 'left_only'].copy()
    
    # Vérifier si des doublons ont été créés par la jointure
    nb_lignes_apres = len(df_correspondantes)
    if nb_lignes_apres > nb_lignes_avant:
        nb_doublons = nb_lignes_apres - nb_lignes_avant
        st.warning(f"⚠️ **{nb_doublons} lignes en trop** créées par la jointure ({nb_lignes_avant:,} → {nb_lignes_apres:,})")
        
        # Identifier les geocodes problématiques
        geocodes_problematiques = df_correspondantes.groupby('geocode').size()
        geocodes_problematiques = geocodes_problematiques[geocodes_problematiques > df_total.groupby('geocode').size().max()].sort_values(ascending=False)
        
        if len(geocodes_problematiques) > 0:
            with st.expander("🔍 Voir les geocodes créant des doublons"):
                st.markdown("**Geocodes qui ont plusieurs correspondances dans la table collectivite :**")
                for geocode, count in geocodes_problematiques.head(20).items():
                    original_count = len(df_total[df_total['geocode'] == geocode])
                    st.markdown(f"- **{geocode}** : {original_count} ligne(s) → {count} ligne(s) après jointure")
                
                st.dataframe(
                    df_correspondantes[df_correspondantes['geocode'].isin(geocodes_problematiques.head(20).index)][
                        ['geocode', 'collectivite_id', 'id', 'code_siren_insee']
                    ].sort_values('geocode'),
                    width='stretch'
                )
    
    # Nettoyer les colonnes
    df_correspondantes.drop(columns=['_merge'], inplace=True)
    df_non_correspondantes.drop(columns=['_merge', 'id', 'code_siren_insee'], inplace=True)
    
    df_correspondantes['collectivite_id'] = df_correspondantes['id']
    
    return df_correspondantes, df_non_correspondantes


def formater_pour_tet_v2(df: pd.DataFrame, indic: dict, date_min: str = '1990-01-01', metadonnee_id: int = None) -> pd.DataFrame:
    """Formate les données au format TET v2."""
    
    api_nom_cube = indic['api_nom_cube']
    ID = indic['ID']
    
    # Format final compatible TET v2
    df_format = df.copy()

    if st.session_state.debug_mode:
        with st.expander("df_format"):
            st.dataframe(df_format, width='stretch')
    
    # Renommer les colonnes
    df_format.rename(
        columns={
            f"{api_nom_cube}.id_{ID}": "resultat",
            f"{api_nom_cube}.date_mesure.year": "date_valeur"
        }, 
        inplace=True
    )

    if st.session_state.debug_mode:
        with st.expander("df_format 2"):
            st.dataframe(df_format, width='stretch')
    
    # Sélectionner les colonnes essentielles
    colonnes_necessaires = ['indicateur_id', 'collectivite_id', 'date_valeur', 'resultat', 'identifiant_referentiel', 'api_nom_cube']
    df_format_tet_v2 = df_format[colonnes_necessaires].copy()

    if st.session_state.debug_mode:
        with st.expander("df_format 3"):
            st.dataframe(df_format_tet_v2, width='stretch')
    
    # Supprimer les NaN et appliquer le ratio pour convertir les unités
    df_format_tet_v2 = df_format_tet_v2.dropna(subset=['resultat']).copy(deep=True)
    df_format_tet_v2["resultat"] = pd.to_numeric(df_format_tet_v2["resultat"], errors="coerce")
    df_format_tet_v2['resultat'] = df_format_tet_v2['resultat'] * indic['ratio']

    if st.session_state.debug_mode:
        with st.expander("df_format 4"):
            st.dataframe(df_format_tet_v2, width='stretch')
    
    # Formatage des types
    df_format_tet_v2['date_valeur'] = pd.to_datetime(df_format_tet_v2['date_valeur'])
    df_format_tet_v2["resultat"] = df_format_tet_v2["resultat"].round(2)

    if st.session_state.debug_mode:
        with st.expander("df_format 5"):
            st.dataframe(df_format_tet_v2, width='stretch')
    
    # Suppression des données antérieures à la date limite
    df_format_tet_v2 = df_format_tet_v2[df_format_tet_v2['date_valeur'] >= date_min].copy()
    
    # Ajout des colonnes supplémentaires TET v2
    df_format_tet_v2['metadonnee_id'] = metadonnee_id
    
    return df_format_tet_v2


def enregistrer_donnees(df: pd.DataFrame, nom_indicateur: str):
    """Enregistre les données dans la table indicateurs_valeurs_olap."""
    
    engine = get_engine()
    
    # Suppression des données existantes pour cette table
    with engine.connect() as conn:
        # Vérifier si la table existe et la supprimer si oui
        conn.execute(text("DROP TABLE IF EXISTS indicateurs_valeurs_olap"))
        conn.commit()
    
    # Enregistrement des nouvelles données
    df.to_sql(
        'indicateurs_valeurs_olap', 
        con=engine, 
        if_exists='append',  # On utilise append car on vient de supprimer la table
        index=False
    )
    
    st.success(f"✅ {len(df):,} lignes enregistrées pour {nom_indicateur}")


# ==========================
# INTERFACE
# ==========================
# ==========================
# AJOUT D'UN INDICATEUR DANS LE YAML
# ==========================

st.markdown("---")
st.markdown("## ➕ Ajouter un indicateur dans le fichier de configuration")

with st.expander("Ajouter un nouvel indicateur", expanded=False):
    # Formulaire pour éviter les actualisations permanentes
    with st.form("form_ajout_indicateur", clear_on_submit=False):
        col_a, col_b = st.columns(2)
        with col_a:
            api_nom_cube_input = st.text_input("Nom du cube (api_nom_cube)", placeholder="ex: macantin_epci")
        with col_b:
            id_input = st.text_input("ID de la mesure (ex: 827)", placeholder="ex: 827")

        st.markdown("### Types de collectivités et axe")
        st.info("💡 Laissez ces champs vides pour remplissage automatique depuis l'API")
        
        type_collectivite_str = st.text_input(
            "type_collectivite (séparés par des virgules, ou vide pour auto)", 
            help="Ex: commune, epci, departement, region, ept. Laissez vide pour remplissage automatique depuis l'API"
        )
        
        api_nom_axe = st.text_input(
            "api_nom_axe (vide pour auto ou si non applicable)", 
            help="Ex: mode_transport, type_amenagement. Laissez vide pour remplissage automatique depuis l'API"
        )

        st.markdown("---")
        st.markdown("### Renseigner les champs obligatoires")

        st.markdown("**Correspondance indicateurs**")
        
        # Mappings
        col_map0, col_map1, col_map2 = st.columns([1, 2, 2])
        with col_map0:
            correspondance_unique = st.text_input(
                "Identifiant référentiel unique", 
                placeholder="ex: cae_59",
                help="Utilisez cette option pour un indicateur simple sans axes"
            )
        with col_map1:
            st.markdown("**Clés (identifiants référentiels)**")
            correspondance_keys = st.text_area(
                "Clés", 
                placeholder="- cae_44.aa\n- cae_44.bb\n- cae_44.cc",
                height=200,
                key="corresp_keys",
                label_visibility="collapsed"
            )
        with col_map2:
            st.markdown("**Valeurs (libellés)**")
            correspondance_values = st.text_area(
                "Valeurs",
                placeholder="- pistes cyclables\n- voies vertes\n- zones 30",
                height=200,
                key="corresp_values",
                label_visibility="collapsed"
            )

        st.markdown("**Metadata**")
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            source_id_commun = st.text_input("source_id (utilisé pour metadata.source_id et source.id)")
            meta_nom_donnees = st.text_input("metadata.nom_donnees")
            meta_diffuseur = st.text_input("metadata.diffuseur")
            meta_producteur = st.text_input("metadata.producteur")
        with col_m2:
            meta_methodologie = st.text_area("metadata.methodologie")
            meta_limites = st.text_area("metadata.limites (optionnel)")
            meta_date_version = st.text_input("metadata.date_version (YYYY-MM-DD HH:MM:SS)")

        st.markdown("**Source**")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            source_libelle = st.text_input("source.libelle")
        with col_s2:
            source_ordre = st.text_input("source.ordre_affichage")

        ratio_val = st.number_input("ratio", min_value=0.0, value=1.0, step=0.01)

        # Bouton de soumission du formulaire
        submit_button = st.form_submit_button("✅ Ajouter cet indicateur au YAML", type="primary")

    # Validation et insertion (en dehors du form, exécuté seulement si submit_button est True)
    if submit_button:
        # Récupérer meta_preview pour pré-remplir les valeurs manquantes
        meta_preview = None
        if api_nom_cube_input and id_input:
            with st.spinner("🔍 Récupération des métadonnées depuis l'API..."):
                try:
                    metadonnees_api_tmp = recuperer_metadonnees_api()
                    key = (id_input, api_nom_cube_input)
                    meta_preview = metadonnees_api_tmp.get(key)
                    
                    if not meta_preview:
                        st.warning(f"⚠️ Indicateur ID={id_input} / cube={api_nom_cube_input} non trouvé dans l'API")
                except Exception as e:
                    st.warning(f"⚠️ Impossible de récupérer l'aperçu des métadonnées: {e}")
        
        # Vérifications de base
        errors = []
        if not api_nom_cube_input:
            errors.append("api_nom_cube requis")
        if not id_input:
            errors.append("ID requis")

        # Valider correspondance_indicateurs
        # Détecter automatiquement quel type de mapping est utilisé
        correspondance_value = None
        mapping_simple_rempli = bool(correspondance_unique.strip())
        mapping_multiple_rempli = bool(correspondance_keys.strip() or correspondance_values.strip())
        
        # Vérifier qu'un seul type est rempli
        if mapping_simple_rempli and mapping_multiple_rempli:
            errors.append("⚠️ Vous devez remplir SOIT le mapping simple, SOIT le mapping multiple (pas les deux)")
        elif not mapping_simple_rempli and not mapping_multiple_rempli:
            errors.append("Vous devez remplir au moins un type de mapping (simple ou multiple)")
        elif mapping_simple_rempli:
            # Mapping simple
            correspondance_value = correspondance_unique.strip()

        else:
            # Mapping multiple
            if not correspondance_keys.strip() or not correspondance_values.strip():
                errors.append("Pour le mapping multiple, les deux listes (clés et valeurs) doivent être remplies")
            else:
                # Extraire les éléments des listes (lignes commençant par '-')
                keys_list = [line.strip().lstrip('-').strip() for line in correspondance_keys.split('\n') if line.strip().startswith('-')]
                values_list = [line.strip().lstrip('-').strip() for line in correspondance_values.split('\n') if line.strip().startswith('-')]
                
                if not keys_list:
                    errors.append("Aucune clé valide trouvée (chaque ligne doit commencer par '-')")
                elif not values_list:
                    errors.append("Aucune valeur valide trouvée (chaque ligne doit commencer par '-')")
                elif len(keys_list) != len(values_list):
                    errors.append(f"Nombre de clés ({len(keys_list)}) différent du nombre de valeurs ({len(values_list)})")
                else:
                    # Créer le dictionnaire
                    correspondance_value = dict(zip(keys_list, values_list))
                    

        # Utiliser les valeurs de l'API si le champ type_collectivite est vide
        type_collectivite_list = []
        if type_collectivite_str.strip():
            type_collectivite_list = [t.strip() for t in type_collectivite_str.split(",") if t.strip()]
            st.info(f"✅ Types de collectivités saisis manuellement : {', '.join(type_collectivite_list)}")
        elif meta_preview:
            type_collectivite_list = meta_preview.get("type_collectivite", [])
            if type_collectivite_list:
                st.success(f"✅ Collectivités trouvées : {', '.join(type_collectivite_list)}")
        
        if not type_collectivite_list:
            errors.append("type_collectivite requis (au moins un type) - Aucune valeur saisie et aucune valeur disponible dans l'API")

        # Utiliser l'axe de l'API si le champ api_nom_axe est vide
        api_nom_axe_final = api_nom_axe.strip()
        if api_nom_axe_final:
            st.info(f"✅ Axe API saisi manuellement : `{api_nom_axe_final}`")
        elif meta_preview:
            api_nom_axe_final = meta_preview.get("api_nom_axe", "")
            if api_nom_axe_final:
                st.success(f"✅ Axe trouvé : `{api_nom_axe_final}`")
            else:
                st.info("ℹ️ Aucun axe API (normal pour un indicateur sans axes)")

        # Valider metadata (limites est maintenant optionnel)
        metadata_obj = {
            "source_id": source_id_commun.strip(),
            "nom_donnees": meta_nom_donnees.strip(),
            "diffuseur": meta_diffuseur.strip(),
            "producteur": meta_producteur.strip(),
            "methodologie": meta_methodologie.strip(),
            "limites": meta_limites.strip(),
            "date_version": meta_date_version.strip(),
        }
        for k, v in metadata_obj.items():
            if k != "limites" and not v:  # limites est optionnel
                errors.append(f"metadata.{k} requis")

        # Valider source (utilise le même source_id)
        source_obj = {
            "id": source_id_commun.strip(),
            "libelle": source_libelle.strip(),
            "ordre_affichage": str(source_ordre).strip(),
        }
        for k, v in source_obj.items():
            if not v:
                errors.append(f"source.{k} requis")

        if errors:
            st.error("❌ Erreurs de validation:\n" + "\n".join([f"- {e}" for e in errors]))
        else:
            # Construire l'objet indicateur
            nouvel_indic = {
                "api_nom_cube": api_nom_cube_input,
                "ID": str(id_input),
                "api_nom_axe": api_nom_axe_final,
                "type_collectivite": type_collectivite_list,
                "correspondance_indicateurs": correspondance_value,
                "metadata": metadata_obj,
                "source": source_obj,
                "ratio": float(ratio_val),
            }

            try:
                if RUAMEL_AVAILABLE:
                    yaml_handler = YAML()
                    yaml_handler.preserve_quotes = True
                    yaml_handler.default_flow_style = False
                    with open("utils/config.yaml", "r", encoding="utf-8") as f:
                        cfg = yaml_handler.load(f)
                    if not cfg or 'indicateurs' not in cfg:
                        cfg = {'indicateurs': []}
                    cfg['indicateurs'].append(nouvel_indic)
                    with open("utils/config.yaml", "w", encoding="utf-8") as f:
                        yaml_handler.dump(cfg, f)
                else:
                    # Fallback simple: recharger via chargeur existant et réécrire en YAML std
                    import yaml as _pyyaml
                    indicateurs_existants = charger_config("utils/config.yaml")
                    indicateurs_existants.append(nouvel_indic)
                    with open("utils/config.yaml", "w", encoding="utf-8") as f:
                        _pyyaml.safe_dump({"indicateurs": indicateurs_existants}, f, allow_unicode=True, sort_keys=False)

                st.success("✅ Indicateur ajouté au fichier config.yaml")
            except Exception as e:
                st.error(f"❌ Erreur lors de l'insertion dans le YAML: {e}")

# Section de vérification des métadonnées
st.markdown("---")
st.markdown("## 🔍 Vérification des métadonnées")

# Initialiser le session state pour les métadonnées
if 'metadata_check' not in st.session_state:
    st.session_state.metadata_check = None
if 'update_result' not in st.session_state:
    st.session_state.update_result = None

left_pad_meta, center_meta, right_pad_meta = st.columns([1, 2, 1])
with center_meta:
    st.markdown("Vérifiez si les métadonnées du fichier YAML sont à jour avec l'API")
    
    if st.button("🔄 Vérifier les métadonnées", width='stretch', key="btn_check_metadata"):
        print("\n" + "!"*60)
        print("! BOUTON VÉRIFIER LES MÉTADONNÉES CLIQUÉ")
        print("!"*60)
        with st.spinner("Récupération des métadonnées de l'API..."):
            try:
                print("Récupération des métadonnées de l'API...")
                metadonnees_api = recuperer_metadonnees_api()
                print(f"  → {len(metadonnees_api)} indicateurs trouvés dans l'API")
                
                print("Chargement du fichier YAML...")
                indicateurs_yaml = charger_config("utils/config.yaml")
                print(f"  → {len(indicateurs_yaml)} indicateurs trouvés dans le YAML")
                
                print("Comparaison...")
                differences = comparer_avec_yaml(metadonnees_api, indicateurs_yaml)
                print(f"  → {len(differences['a_jour'])} à jour")
                print(f"  → {len(differences['a_mettre_a_jour'])} à mettre à jour")
                print(f"  → {len(differences['manquants_api'])} manquants API")
                print(f"  → {len(differences['manquants_yaml'])} manquants YAML")
                
                # Stocker dans session_state
                st.session_state.metadata_check = {
                    'metadonnees_api': metadonnees_api,
                    'indicateurs_yaml': indicateurs_yaml,
                    'differences': differences
                }
                print("Résultats stockés dans session_state")
                
            except Exception as e:
                st.error(f"❌ Erreur lors de la récupération des métadonnées : {str(e)}")
                print(f"ERREUR: {str(e)}")

# Afficher les résultats s'ils existent
if st.session_state.metadata_check:
    print("\n>>> Affichage des résultats de vérification depuis session_state")
    
    metadonnees_api = st.session_state.metadata_check['metadonnees_api']
    indicateurs_yaml = st.session_state.metadata_check['indicateurs_yaml']
    differences = st.session_state.metadata_check['differences']
    
    st.markdown("---")
    
    # Afficher les résultats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("✅ À jour", len(differences['a_jour']))
    with col2:
        st.metric("⚠️ À mettre à jour", len(differences['a_mettre_a_jour']))
    with col3:
        st.metric("🔴 Manquants API", len(differences['manquants_api']))
    with col4:
        st.metric("🆕 Nouveaux dans API", len(differences['manquants_yaml']))
    
    # Indicateurs à mettre à jour
    if differences['a_mettre_a_jour']:
        st.markdown("---")
        st.markdown("### ⚠️ Indicateurs à mettre à jour")
        
        for indic_diff in differences['a_mettre_a_jour']:
            with st.expander(f"📝 ID {indic_diff['ID']} (cube: `{indic_diff['api_nom_cube']}`) - {indic_diff['nom']}"):
                
                for champ, valeurs in indic_diff['differences'].items():
                    st.markdown(f"**{champ}**:")
                    col_yaml, col_api = st.columns(2)
                    with col_yaml:
                        st.markdown(f"🟡 **YAML actuel:**")
                        st.code(str(valeurs['yaml']))
                    with col_api:
                        st.markdown(f"🟢 **API (nouveau):**")
                        st.code(str(valeurs['api']))
        
        # Bouton pour mettre à jour
        st.markdown("---")
        # Utiliser les clés composites (ID, api_nom_cube) au lieu de juste l'ID
        keys_a_modifier = [(indic['ID'], indic['api_nom_cube']) for indic in differences['a_mettre_a_jour']]
        
        if st.button(
            f"✏️ Mettre à jour les {len(keys_a_modifier)} indicateur(s)",
            type="primary",
            width='stretch',
            key="btn_update_yaml"
        ):
            print("\n" + "#"*60)
            print("# BOUTON DE MISE À JOUR CLIQUÉ")
            print("#"*60)
            print(f"Clés à modifier: {keys_a_modifier}")
            
            methode = "ruamel.yaml (formatage préservé)" if RUAMEL_AVAILABLE else "manipulation de texte (formatage préservé)"
            print(f"Méthode: {methode}")
            print(f"RUAMEL_AVAILABLE: {RUAMEL_AVAILABLE}")
            
            # Container pour les messages de debug
            debug_container = st.container()
            
            try:
                print("Début du spinner...")
                with st.spinner(f"🔄 Mise à jour du fichier YAML via {methode}..."):
                    print("Appel de mettre_a_jour_yaml()...")
                    mettre_a_jour_yaml(
                        indicateurs_yaml, 
                        metadonnees_api, 
                        keys_a_modifier, 
                        "utils/config.yaml",
                        debug_container
                    )
                    print("mettre_a_jour_yaml() terminé")
                
                # Vérifier que la mise à jour a fonctionné
                print("Vérification de la mise à jour...")
                indicateurs_updated = charger_config("utils/config.yaml")
                yaml_dict_updated = {(ind['ID'], ind.get('api_nom_cube')): ind for ind in indicateurs_updated}
                print(f"Fichier rechargé, {len(yaml_dict_updated)} indicateurs trouvés")
                
                # Compter les succès
                nb_succes = 0
                for key in keys_a_modifier:
                    if key in yaml_dict_updated and key in metadonnees_api:
                        indic = yaml_dict_updated[key]
                        meta = metadonnees_api[key]
                        if (indic.get('api_nom_cube') == meta['api_nom_cube'] and
                            sorted(indic.get('type_collectivite', [])) == sorted(meta['type_collectivite']) and
                            indic.get('api_nom_axe') == meta['api_nom_axe']):
                            nb_succes += 1
                            print(f"  ✓ ID {key[0]} / cube {key[1]} vérifié et correct")
                        else:
                            print(f"  ✗ ID {key[0]} / cube {key[1]} modifié mais pas correct")
                
                print(f"Résultat: {nb_succes}/{len(keys_a_modifier)} succès")
                
                # Stocker le résultat dans session_state
                st.session_state.update_result = {
                    'success': nb_succes == len(keys_a_modifier),
                    'nb_succes': nb_succes,
                    'nb_total': len(keys_a_modifier),
                    'methode': methode,
                    'keys': keys_a_modifier,
                    'differences': differences
                }
                
                print("Stockage dans session_state terminé")
                print("Appel à st.rerun()...")
                st.rerun()
                
            except Exception as e:
                print(f"\n!!! EXCEPTION CAPTURÉE !!!")
                print(f"Type: {type(e).__name__}")
                print(f"Message: {str(e)}")
                import traceback
                print(traceback.format_exc())
                
                st.session_state.update_result = {
                    'success': False,
                    'error': str(e),
                    'traceback': traceback.format_exc()
                }
                print("Appel à st.rerun() après erreur...")
                st.rerun()
        
        # Afficher le résultat s'il existe
        if st.session_state.update_result:
            print("\n>>> Affichage du résultat depuis session_state")
            result = st.session_state.update_result
            print(f">>> Résultat: {result}")
            
            if 'error' in result:
                st.error(f"❌ Erreur lors de la mise à jour : {result['error']}")
                st.code(result['traceback'])
                if not RUAMEL_AVAILABLE:
                    st.info("💡 **Astuce :** Installez `ruamel.yaml` pour une meilleure gestion du formatage YAML : `pip install ruamel.yaml`")
            else:
                if result['success']:
                    st.success(f"🎉 **MISE À JOUR RÉUSSIE !** {result['nb_total']} indicateur(s) mis à jour dans le fichier YAML !")
                    st.info(f"📝 Méthode utilisée : {result['methode']}")
                    st.info("🔄 **Action requise :** Rechargez la page (F5) pour prendre en compte les modifications")
                else:
                    st.warning(f"⚠️ Mise à jour partielle : {result['nb_succes']}/{result['nb_total']} indicateur(s) mis à jour")
                
                st.markdown("---")
                st.markdown("### ✅ Indicateurs mis à jour:")
                for key in result['keys']:
                    id_val, cube_val = key
                    indic_info = next((ind for ind in result['differences']['a_mettre_a_jour'] 
                                      if ind['ID'] == id_val and ind['api_nom_cube'] == cube_val), None)
                    if indic_info:
                        st.markdown(f"- **ID {id_val}** (cube: `{cube_val}`) : {indic_info['nom']}")
            
            # Bouton pour réinitialiser
            if st.button("🔄 Fermer ce message", key="close_update_result"):
                st.session_state.update_result = None
                st.rerun()
    else:
        st.success("✅ Tous les indicateurs du YAML sont à jour avec l'API !")
    
    # Indicateurs nouveaux dans l'API
    if differences['manquants_yaml']:
        st.markdown("---")
        st.markdown("### 🆕 Indicateurs nouveaux dans l'API")
        st.info(f"Ces {len(differences['manquants_yaml'])} indicateur(s) sont disponibles dans l'API mais pas encore dans le YAML")
        
        indicateurs_a_afficher = [
            indic_new for indic_new in differences['manquants_yaml']
            if not (indic_new['api_nom_cube'].endswith('region') or indic_new['api_nom_cube'].endswith('dpt'))
        ]
        for indic_new in indicateurs_a_afficher:
            with st.expander(f"✨ ID {indic_new['ID']} (cube: `{indic_new['api_nom_cube']}`)"):
                meta = indic_new['meta']
                st.markdown(f"**Cube:** `{meta['api_nom_cube']}`")
                st.markdown(f"**Types de collectivité:** {', '.join(meta['type_collectivite'])}")
                st.markdown(f"**Axe API:** `{meta['api_nom_axe']}`" if meta['api_nom_axe'] else "**Axe API:** _(aucun)_")
    
    # Indicateurs manquants dans l'API
    if differences['manquants_api']:
        st.markdown("---")
        st.markdown("### 🔴 Indicateurs manquants dans l'API")
        st.warning(f"Ces {len(differences['manquants_api'])} indicateur(s) sont dans le YAML mais introuvables dans l'API")
        
        df_manquants = pd.DataFrame(differences['manquants_api'])
        st.dataframe(df_manquants, width='stretch')

st.markdown("---")
st.markdown("## 📋 Sélection des indicateurs")

# Chargement de la configuration
try:
    indicateurs = charger_config("utils/config.yaml")
    
    # Création d'un dictionnaire pour l'affichage
    options_indicateurs = {
        f"{ind['metadata']['nom_donnees']} (ID: {ind['ID']})": ind 
        for ind in indicateurs
    }
    
    # Sélection des indicateurs
    left_pad, center_col, right_pad = st.columns([1, 2, 1])
    with center_col:
        indicateurs_selectionnes = st.multiselect(
            "Choisissez un ou plusieurs indicateurs à importer",
            options=list(options_indicateurs.keys()),
            default=None,
            help="Les données seront récupérées depuis l'API data.gouv et enregistrées dans la base de données"
        )
        
        if indicateurs_selectionnes:
            st.info(f"💡 {len(indicateurs_selectionnes)} indicateur(s) sélectionné(s)")
        
        col_btn, col_toggle1, col_toggle2 = st.columns([3, 2, 2])
        with col_btn:
            lancer_import = st.button(
                "🚀 Lancer l'import",
                disabled=len(indicateurs_selectionnes) == 0,
                type="primary",
                width='stretch'
            )
        with col_toggle1:
            desactiver_filtre_siren = st.toggle(
                "🚫 Désactiver le filtrage SIREN",
                value=False,
                help=(
                    "Si activé, l'API renvoie toutes les collectivités françaises "
                    "(la jointure TET se fera ensuite côté Python). "
                    "Utile pour debug ou si le filtre SIREN ne renvoie rien."
                ),
            )
        with col_toggle2:
            desactiver_pagination_annee = st.toggle(
                "📅 Désactiver la pagination par année",
                value=False,
                help=(
                    "Si activé, on récupère commune/epci en une seule série de pages "
                    "(pagination par offset uniquement, sans découpage par année). "
                    "Utile si la pagination par année renvoie zéro ligne."
                ),
            )
    
    # Traitement de l'import
    if lancer_import:
        st.markdown("---")
        st.markdown("## 📥 Import en cours")
        
        # Récupération des collectivités TET pour filtrer les requêtes API
        engine_prod = get_engine_prod()
        cts_tet = pd.read_sql_query(
            sql=text("SELECT * FROM collectivite"),
            con=engine_prod.connect()
        )
        
        # Créer le dictionnaire de filtres pour commune et epci
        # (ignoré si l'utilisateur a désactivé le filtrage SIREN via le toggle)
        if desactiver_filtre_siren:
            ct_filter_tet = None
            st.warning(
                "🚫 Filtrage SIREN désactivé : l'API va renvoyer toutes les collectivités françaises. "
                "La jointure avec les collectivités TET se fera après la récupération."
            )
        else:
            ct_filter_tet = {
                'commune': [str(siren) for siren in cts_tet[cts_tet['type'] == 'commune']['siren'].tolist()],
                'epci': [str(siren) for siren in cts_tet[cts_tet['type'] == 'epci']['siren'].tolist()]
            }
        
        # Information sur le mode de pagination utilisé
        if desactiver_pagination_annee:
            st.warning(
                "📅 Pagination par année désactivée : pour commune/epci, on récupère tout "
                "via une simple pagination par offset (sans découpage par année)."
            )
        
        progress_bar = st.progress(0)
        
        all_data = []
        
        for i, nom_indicateur in enumerate(indicateurs_selectionnes):
            indic = options_indicateurs[nom_indicateur]
            
            # Création d'un expander pour chaque indicateur
            with st.expander(
                f"🔄 **{indic['metadata']['nom_donnees']}** (ID: {indic['ID']}) - {i+1}/{len(indicateurs_selectionnes)}", 
                expanded=True
            ):
                st.markdown(f"**📌 Indicateur :** {indic['metadata']['nom_donnees']}")
                st.markdown(f"**🆔 ID :** {indic['ID']}")
                st.markdown(f"**📦 Cube API :** {indic['api_nom_cube']}")
                st.markdown(f"**🏛️ Types de collectivités :** {', '.join(indic['type_collectivite'])}")
                
                st.markdown("---")
                st.markdown("### 📡 Récupération depuis l'API")
                
                # Container pour les détails de récupération
                detail_container = st.empty()
                
                # Récupération des données API avec affichage des détails et filtres
                df_api = recuperer_donnees_api(
                    indic,
                    detail_container,
                    ct_filter_tet,
                    paginer_par_annee=not desactiver_pagination_annee,
                )

                if st.session_state.debug_mode:
                    with st.expander("df_api 1"):
                        st.dataframe(df_api, width='stretch')
                
                if df_api.empty:
                    st.warning(f"⚠️ Aucune donnée récupérée pour cet indicateur")
                    continue
                
                st.markdown("---")
                st.markdown("### 🔗 Jointure avec les collectivités")
                
                # Jointure avec les collectivités
                with st.spinner(f"Traitement des collectivités..."):
                    df_final, df_non_correspondantes = nettoyer_et_joindre_collectivites(df_api)
                
                if df_final.empty:
                    st.warning(f"⚠️ Aucune correspondance trouvée avec les collectivités TET")
                    continue
                
                # Statistiques après jointure
                lignes_perdues = len(df_non_correspondantes)
                pourcentage_conserve = (len(df_final) / len(df_api) * 100) if len(df_api) > 0 else 0
                
                st.markdown(f"**✅ {len(df_final):,} lignes** conservées après jointure")
                
                # Compter les collectivités par type
                if 'type_collectivite' in df_final.columns and 'collectivite_id' in df_final.columns:
                    collectivites_par_type = df_final.groupby('type_collectivite')['collectivite_id'].nunique().to_dict()
                    for type_ct in sorted(collectivites_par_type.keys()):
                        st.markdown(f"  - **{type_ct}** : {collectivites_par_type[type_ct]:,} collectivité(s)")
                
                if lignes_perdues > 0:
                    st.markdown(f"**⚠️ {lignes_perdues:,} lignes** non correspondantes ({100-pourcentage_conserve:.1f}%)")
                    
                    # Afficher les lignes non correspondantes
                    with st.expander(f"👁️ Voir les {lignes_perdues:,} lignes non correspondantes"):
                        # Sélectionner les colonnes les plus pertinentes
                        cols_to_show = ['geocode', 'libelle', 'type_collectivite']
                        # Ajouter d'autres colonnes si elles existent
                        for col in df_non_correspondantes.columns:
                            if col not in cols_to_show and not col.startswith(indic['api_nom_cube']):
                                cols_to_show.append(col)
                        
                        cols_disponibles = [c for c in cols_to_show if c in df_non_correspondantes.columns]
                        st.dataframe(
                            df_non_correspondantes[cols_disponibles].drop_duplicates(),
                            width='stretch'
                        )
                
                # Ajout de l'ID de l'indicateur
                df_final['nom_indicateur'] = indic['metadata']['nom_donnees']
                
                # ===== INSERTION DANS LA BDD PRÉ-PROD =====
                st.markdown("---")
                st.markdown("### 💾 Insertion dans la base pré-prod")
                
                engine_pre_prod = get_engine_pre_prod()
                
                # Insertion ou non de la source
                with engine_pre_prod.begin() as conn:
                    # Vérifie si l'entrée avec cet ID existe déjà
                    check_query = text("""
                        SELECT 1 FROM indicateur_source WHERE id = :id
                    """)
                    result = conn.execute(check_query, {"id": indic["source"]["id"]}).first()

                    if result is None:
                        # Insertion si l'ID n'existe pas encore
                        insert_query = text("""
                            INSERT INTO indicateur_source (id, libelle, ordre_affichage)
                            VALUES (:id, :libelle, :ordre_affichage)
                        """)
                        conn.execute(insert_query, {
                            "id": indic["source"]["id"],
                            "libelle": indic["source"]["libelle"],
                            "ordre_affichage": indic["source"]["ordre_affichage"]
                        })
                        st.success(f"✅ Source '{indic['source']['id']}' insérée.")
                    else:
                        st.info(f"⏭️ Source '{indic['source']['id']}' déjà existante, pas d'insertion.")

                # Insertion de la metadata si elle n'existe pas en prenant comme clé d'unicité :
                cle = {
                    "source_id": indic["metadata"]["source_id"],
                    "nom_donnees": indic["metadata"]["nom_donnees"],
                    "diffuseur": indic["metadata"]["diffuseur"],
                    "producteur": indic["metadata"]["producteur"]
                }

                # Colonnes à mettre à jour si ligne déjà existante
                update_fields = {
                    "date_version": indic["metadata"]["date_version"],
                    "methodologie": indic["metadata"]["methodologie"],
                    "limites": indic["metadata"]["limites"]
                }

                with engine_pre_prod.begin() as conn:
                    # 1. Recherche d'une ligne existante selon la clé logique
                    result = conn.execute(text("""
                        SELECT id FROM indicateur_source_metadonnee
                        WHERE source_id = :source_id
                        AND nom_donnees = :nom_donnees
                        LIMIT 1;
                    """), cle).first()

                    if result is None:
                        # 2. Si aucune ligne existante → INSERT
                        result = conn.execute(text("""
                            INSERT INTO indicateur_source_metadonnee (
                                source_id, date_version, nom_donnees, diffuseur,
                                producteur, methodologie, limites
                            ) VALUES (
                                :source_id, :date_version, :nom_donnees, :diffuseur,
                                :producteur, :methodologie, :limites
                            ) RETURNING id;
                        """), indic["metadata"]).first()
                        id_metadonnee = result[0]
                        st.success(f"✅ Nouvelle métadonnée insérée avec id : {id_metadonnee}")
                    else:
                        # 3. Si ligne existante → UPDATE
                        id_metadonnee = result[0]
                        update_fields["id"] = id_metadonnee  # pour la clause WHERE
                        conn.execute(text("""
                            UPDATE indicateur_source_metadonnee
                            SET date_version = :date_version,
                                methodologie = :methodologie,
                                limites = :limites
                            WHERE id = :id;
                        """), update_fields)
                        st.success(f"✅ Métadonnée existante mise à jour avec id : {id_metadonnee}")

                    

                # Récupération de l'ID indicateur
                mapping_indicateurs = pd.read_sql_query(
                    sql=text("SELECT id as indicateur_id, identifiant_referentiel FROM indicateur_definition"),
                    con=engine_pre_prod.connect()
                )

                if st.session_state.debug_mode:
                    with st.expander("df_final 1"):
                        st.dataframe(df_final, width='stretch')

                # Jointure selon axe ou non
                # Si correspondance_indicateurs est un dict, on a des axes à mapper
                if isinstance(indic['correspondance_indicateurs'], dict):
                    # Construire le dict de mapping
                    nom_to_id = {v: k for k, v in indic['correspondance_indicateurs'].items()}
                    colonne_axe = f"{indic['api_nom_cube']}.{indic['api_nom_axe']}"

                    # Repérer les valeurs d'axe non couvertes par le mapping
                    valeurs = df_final[colonne_axe]
                    inconnues = set(valeurs) - set(nom_to_id.keys())
                    if inconnues:
                        st.warning(f'/!\\ Pas de match des axes pour : {inconnues}')

                    # Ne garder que les lignes mappables
                    df_final = df_final[~df_final[colonne_axe].isin(inconnues)].copy()

                    if st.session_state.debug_mode:
                        with st.expander("df_final 2"):
                            st.dataframe(df_final, width='stretch')

                    # Faire le mapping et la jointure
                    df_final['identifiant_referentiel'] = df_final[colonne_axe].map(nom_to_id)
                    df_final = df_final.merge(mapping_indicateurs,
                                        on="identifiant_referentiel",
                                        how="left")

                else:
                    # Cas sans axe : lookup direct d'après la correspondance (string simple)
                    df_final['indicateur_id'] = (
                        mapping_indicateurs
                        .loc[
                            mapping_indicateurs.identifiant_referentiel
                            == indic['correspondance_indicateurs'],
                            'indicateur_id'
                        ]
                        .iloc[0]
                    )

                    df_final['identifiant_referentiel'] = indic['correspondance_indicateurs']
                
                df_final['api_nom_cube'] = indic['api_nom_cube']

                if st.session_state.debug_mode:
                    with st.expander("df_final 3"):
                        st.dataframe(df_final, width='stretch')
                
                # Formatage au format TET v2
                date_min_str = '1990-01-01'
                df_format_tet = formater_pour_tet_v2(df_final, indic, date_min_str, id_metadonnee)
    
                all_data.append(df_format_tet)
                
                st.success(f"✅ Import terminé pour cet indicateur")
            
            # Mise à jour de la barre de progression
            progress_bar.progress((i + 1) / len(indicateurs_selectionnes))
        
        # Enregistrement dans la base
        if all_data:
            st.markdown("---")
            st.markdown("## 💾 Enregistrement sur la bdd OLAP")
            
            df_complet = pd.concat(all_data, ignore_index=True)
            
            with st.spinner("Enregistrement en cours..."):
                enregistrer_donnees(df_complet, "tous les indicateurs sélectionnés")
            
            # Statistiques par indicateur
            with st.expander("📊 Statistiques par indicateur"):
                stats = df_complet.groupby('indicateur_id').agg({
                    'collectivite_id': 'nunique',
                    'resultat': 'count',
                    'date_valeur': ['min', 'max']
                }).round(2)
                stats.columns = ['Nb collectivités', 'Nb lignes', 'Date min', 'Date max']
                st.dataframe(stats, width='stretch')
            
            # Aperçu des données
            with st.expander("👀 Aperçu des données importées (100 premières lignes)"):
                st.dataframe(df_complet.head(100), width='stretch')
        else:
            st.error("❌ Aucune donnée à enregistrer")

except Exception as e:
    st.error(f"❌ Erreur lors du chargement de la configuration : {str(e)}")
