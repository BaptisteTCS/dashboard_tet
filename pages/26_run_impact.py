import streamlit as st

# Configuration de la page en premier
st.set_page_config(
    page_title="Calcul impact",
    page_icon="🎯",
    layout="wide"
)

import json
import random
import re
import time
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict

import pandas as pd
from openai import OpenAI
from sqlalchemy import text

from utils.db import get_engine, get_engine_prod

# ==========================
# Configuration OpenAI
# ==========================

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ==========================
# Constantes
# ==========================

LEVIERS = """
Changement chaudières fioul + rénovation (résidentiel)
Changement chaudières gaz + rénovation (résidentiel)
Sobriété des bâtiments (résidentiel)
Changement de chaudière à fioul (tertiaire)
Changement de chaudière à gaz (tertiaire)
Sobriété et isolation des bâtiments (tertiaire)
Réduction des déplacements
Covoiturage
Vélo et transport en commun
Véhicules électriques
Efficacité et carburants décarbonés des véhicules privés
Bus et cars décarbonés
Fret décarboné et multimodalité
Efficacité et sobriété logistique
Bâtiments & Machines agricoles
Elevage durable
Changements de pratiques de fertilisation azotée
Production industrielle
Captage de méthane dans les ISDND
Prévention des déchets
Valorisation matière des déchets
Gestion des forêts et produits bois
Pratiques stockantes
Gestion des haies
Gestion des prairies
Sobriété foncière
Electricité renouvelable
Biogaz
Réseaux de chaleur décarbonés
"""

D_MAP_SECTEUR = {
    'Résidentiel': 'cae_1.c',
    'Tertiaire': 'cae_1.d',
    'Transport ': 'cae_1.k',
    'Agriculture': 'cae_1.g',
    'Industrie': 'cae_1.i',
    'Déchets': 'cae_1.h',
    'UTCATF': 'cae_1.csc',
    'Branche énergie': 'cae_1.j'
}

# ==========================
# Fonctions de chargement des données
# ==========================

@st.cache_data(ttl="1h")
def load_collectivites():
    """Charge la liste des collectivités depuis la base de prod."""
    engine = get_engine_prod()
    with engine.connect() as conn:
        df = pd.read_sql_query(
            text("""
                SELECT id, nom, population, region_code 
                FROM collectivite 
                WHERE type != 'test' 
                AND nom IS NOT NULL
                ORDER BY nom
            """),
            conn
        )
    return df


@st.cache_data(ttl="1h")
def load_ratios_csv():
    """Charge le CSV des ratios de leviers SGPE par région."""
    try:
        df = pd.read_csv('data/leviers_sgpe_region.csv', sep=';')
        return df
    except FileNotFoundError:
        return None


def get_regions_from_csv(df_ratios):
    """Extrait la liste des régions disponibles dans le CSV."""
    if df_ratios is None:
        return []
    # Les colonnes qui ne sont pas 'Secteur' ou 'Leviers SGPE' sont des régions
    exclude_cols = ['Secteur', 'Leviers SGPE', 'identifiant_referentiel']
    regions = [col for col in df_ratios.columns if col not in exclude_cols]
    return regions


def fetch_plan_actions(collectivite_id: int) -> pd.DataFrame:
    """Récupère le plan d'actions d'une collectivité."""
    engine = get_engine_prod()
    with engine.connect() as conn:

        if full_access_mode:
            df = pd.read_sql_query(
                text("""
                    SELECT DISTINCT fa.id, fa.titre, fa.description
                    FROM fiche_action fa
                    JOIN fiche_action_axe faa ON faa.fiche_id = fa.id
                    WHERE fa.collectivite_id = :collectivite_id
                """),
                conn,
                params={"collectivite_id": collectivite_id}
            )
        else:
            df = pd.read_sql_query(
                text("""
                    SELECT DISTINCT fa.id, fa.titre, fa.description
                    FROM fiche_action fa
                    JOIN fiche_action_axe faa ON faa.fiche_id = fa.id
                    WHERE fa.collectivite_id = :collectivite_id
                    AND fa.restreint = False
                """),
                conn,
                params={"collectivite_id": collectivite_id}
            )
    return df


def fetch_indicateurs_snbc(collectivite_id: int) -> pd.DataFrame:
    """Récupère les indicateurs SNBC pour calculer les objectifs de réduction."""
    engine = get_engine_prod()
    with engine.connect() as conn:
        df = pd.read_sql_query(
            text("""
                SELECT id.titre, id.identifiant_referentiel, iv.date_valeur, iv.objectif 
                FROM indicateur_valeur iv
                JOIN indicateur_definition id ON iv.indicateur_id = id.id
                WHERE iv.collectivite_id = :collectivite_id
                AND metadonnee_id = 17
                AND objectif IS NOT NULL
                AND date_valeur IN ('2019-01-01', '2030-01-01')
            """),
            conn,
            params={"collectivite_id": collectivite_id}
        )
    return df


# ==========================
# Fonctions de traitement LLM
# ==========================

def build_prompt_classification(plan_texte: str) -> str:
    """Construit le prompt pour classifier les actions par levier."""
    return f"""
Tu es un expert en analyse d'impact carbone des politiques publiques et en modélisation par leviers CO2.

Contexte
On te fournit deux éléments :

1 Un plan d'actions sous forme de texte structuré.
Chaque action est identifiée par un id unique et décrite par un titre et une description.

2 Une liste fermée de leviers CO2.
Chaque levier correspond à un mécanisme d'impact direct ou quasi direct sur les émissions de CO2, avec un facteur quantifiable connu en aval.

Objectif
Pour chaque action du plan, identifier les leviers CO2 auxquels elle correspond de manière SÛRE.

Règles fondamentales
• Une action peut correspondre à zéro, un ou plusieurs leviers.
• N'associe un levier à une action que si le lien est clair, direct ou très fortement plausible.
• Si le lien est trop indirect, spéculatif, dépendant d'hypothèses non explicites ou uniquement comportemental sans levier physique clair, ne pas associer.
• En cas de doute, s'abstenir. La précision est prioritaire sur l'exhaustivité.
• Ne jamais inventer de levier en dehors de la liste fournie.
• Ne pas reformuler les leviers. Utiliser exactement les libellés fournis.

Méthode attendue
Pour chaque action :
1 Analyser le titre et la description.
2 Identifier si l'action déclenche directement un ou plusieurs mécanismes d'impact CO2 connus.
3 Associer uniquement les leviers correspondant à ces mécanismes directs.

Format de sortie attendu
Tu dois répondre UNIQUEMENT avec un JSON valide, sans texte additionnel.

Le format exact est :
{{
  "id_action_1": ["levier_1", "levier_2"],
  "id_action_2": [],
  "id_action_3": ["levier_3"]
}}

Si aucune correspondance sûre n'existe pour une action, retourner une liste vide.

Entrées
Plan d'actions :
{plan_texte}

Liste des leviers CO2 :
{LEVIERS}
"""


def build_prompt_implication(actions: str, levier: str, collectivite_nom: str, population: int) -> str:
    """Construit le prompt pour évaluer l'implication sur un levier."""
    return f"""
Tu es un expert en politiques publiques locales et en évaluation qualitative d'impact climat.

Contexte
On te fournit :
1 Le nom d'une collectivité et sa population.
2 Un levier d'action précis (ex : « Co-voiturage »).
3 Une liste d'actions mises en œuvre par la collectivité concernant ce levier

Objectif
Évaluer à quel point la collectivité exploite le levier donné, au regard de ce qu'une collectivité de taille comparable pourrait raisonnablement faire aujourd'hui.

IMPORTANT – usage du score
Le score que tu produis sera utilisé directement comme un coefficient d'activation du potentiel de réduction de CO2 du levier.

Par exemple :
• un score de 25% signifie que la collectivité ne mobilise qu'environ 25 % du potentiel théorique du levier
• un score de 75% signifie que la majorité du potentiel du levier est effectivement mobilisée
• un score de 100% signifie que le potentiel est exploité au maximum raisonnablement atteignable

Tu dois donc positionner la note en te demandant explicitement :
« Quelle part du potentiel de réduction CO2 de ce levier est réellement activée par les actions observées ? »

Il ne s'agit pas de mesurer un impact chiffré réel, mais d'estimer la fraction du potentiel du levier effectivement mobilisée.

Échelle d'évaluation
Tu dois retourner une valeur entière parmis [0, 25, 50, 75, 100], selon la logique suivante :

• 0 %  
Les actions entreprises ne permettent pas d'activer de manière crédible le potentiel de réduction CO2 du levier.

• 25 %  
Actions ponctuelles, symboliques ou très limitées, activant seulement une faible part du potentiel du levier.

• 50 %  
Actions réelles mais partielles. Le levier est activé sur une part significative mais incomplète de son potentiel
(par exemple en couverture, en intensité, en population touchée ou en durée).

• 75 %  
Effort important, structuré et cohérent. La majorité du potentiel du levier est activée, même si des marges de progression existent encore.

• 100 %  
Mobilisation maximale et systémique du levier. Le potentiel est exploité au niveau le plus élevé raisonnablement atteignable pour une collectivité de cette taille.

Principes d'évaluation
• Toujours raisonner relativement à la taille de la collectivité et à sa population.
• Toujours raisonner en termes d'activation du potentiel du levier, et non en valeur absolue des actions.
• Privilégier les actions structurantes, durables et à large portée.
• Ne pas surévaluer des actions uniquement incitatives, communicationnelles ou expérimentales.
• En cas de doute, adopter une approche prudente.
• La note doit être cohérente avec la justification fournie.

Méthode attendue
1 Évaluer la part du potentiel du levier qu'elles permettent d'activer (couverture, intensité, durée).
2 Positionner la collectivité sur l'échelle 0–100 de manière argumentée.

Format de sortie attendu
Tu dois répondre UNIQUEMENT avec un JSON valide, sans texte additionnel.

Format exact :
{{
  "score": <entier entre 0 et 100 parmis [0, 25, 50, 75, 100]>,
  "justification": "<quelques phrases claires expliquant le score>"
}}

Entrées
Collectivité : {collectivite_nom}
Population : {population}
Levier évalué : {levier}

Actions mises en œuvre :
{actions}
"""


def invert_actions_by_lever(response_text: str) -> Dict[str, list]:
    """
    Transforme un texte JSON de la forme:
    { "id": ["levier1", "levier2"], ... }
    en:
    { "levier1": [id1, id2], ... }
    avec id en int
    """
    if not response_text or not response_text.strip():
        return {}

    txt = response_text.strip()

    # Gère les blocs ```json ... ```
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", txt, flags=re.IGNORECASE)
    if fence:
        txt = fence.group(1).strip()

    data = json.loads(txt)
    inverted = defaultdict(list)

    for action_id, leviers in data.items():
        try:
            action_id_int = int(action_id)
        except (ValueError, TypeError):
            continue

        for levier in leviers or []:
            inverted[levier].append(action_id_int)

    return dict(inverted)


def build_actions_text(plan: pd.DataFrame, ids: list) -> str:
    """
    Construit un texte d'actions à partir de plan (colonnes: id, titre, description)
    pour une liste d'ids (int).
    """
    df = plan[plan["id"].isin(ids)].copy()
    if df.empty:
        return ""

    df["titre"] = df["titre"].fillna("").astype(str)
    df["description"] = df["description"].fillna("").astype(str)

    return "\n\n".join(
        f"{row.id} | {row.titre} : {row.description}".strip()
        for _, row in df.iterrows()
    ).strip()


def strip_json_fences(text: str) -> str:
    """Enlève les ```json ... ``` si présents."""
    if not text:
        return ""
    t = text.strip()
    if t.startswith("```"):
        t = t.replace("```json", "").replace("```JSON", "").replace("```", "").strip()
    return t


def classify_actions(plan: pd.DataFrame, status_container) -> str:
    """Appelle l'API OpenAI pour classifier les actions par levier."""
    plan_texte = "{" + ", ".join(
        f"{row.id}:{row.titre} - {row.description}"
        for _, row in plan.iterrows()
    ) + "}"
    
    prompt = build_prompt_classification(plan_texte)
    
    status_container.write("🤖 Appel à l'API OpenAI pour classification...")
    
    response = client.responses.create(
        model="gpt-5.1-2025-11-13",
        input=prompt,
        reasoning={"effort": "medium"},
        max_output_tokens=120000
    )
    
    return response.output_text


def classify_actions_mock(plan: pd.DataFrame, status_container) -> str:
    """Version mock pour le débogage - classifie aléatoirement les actions."""
    status_container.write("🎲 Mode débogage - Classification aléatoire...")
    
    # Liste des leviers disponibles
    leviers_list = [l.strip() for l in LEVIERS.strip().split('\n') if l.strip()]
    
    # Pour chaque action, assigner aléatoirement 0 à 3 leviers
    result = {}
    for _, row in plan.iterrows():
        num_leviers = random.randint(0, min(3, len(leviers_list)))
        if num_leviers > 0:
            result[str(row.id)] = random.sample(leviers_list, num_leviers)
        else:
            result[str(row.id)] = []
    
    return json.dumps(result)


def score_all_levers(
    plan: pd.DataFrame,
    dic_leviers: Dict[str, list],
    collectivite_nom: str,
    population: int,
    status_container
) -> Dict[str, Any]:
    """
    Boucle sur tous les leviers pour évaluer l'implication.
    """
    results: Dict[str, Any] = {}
    total_leviers = len(dic_leviers)
    
    for idx, (levier, ids) in enumerate(dic_leviers.items(), 1):
        actions_text = build_actions_text(plan, ids)
        prompt = build_prompt_implication(actions_text, levier, collectivite_nom, population)
        
        status_container.write(f"📊 Évaluation du levier ({idx}/{total_leviers}): {levier}")
        
        try:
            resp = client.responses.create(
                model="gpt-5.1-2025-11-13",
                input=prompt,
                reasoning={"effort": "medium"}
            )
            raw_text = resp.output_text
        except Exception as e:
            results[levier] = {
                "ids": ids,
                "raw_text": "",
                "parsed": None,
                "error": f"generation_error: {type(e).__name__}: {e}",
            }
            continue

        raw_text_clean = strip_json_fences(raw_text)

        parsed = None
        parse_error = None
        try:
            parsed = json.loads(raw_text_clean)
        except Exception as e:
            parse_error = f"json_parse_error: {type(e).__name__}: {e}"

        results[levier] = {
            "ids": ids,
            "raw_text": raw_text,
            "parsed": parsed,
            "error": parse_error,
        }
        
        # Petite pause pour ne pas surcharger l'API
        time.sleep(0.2)

    return results


def score_all_levers_mock(
    plan: pd.DataFrame,
    dic_leviers: Dict[str, list],
    collectivite_nom: str,
    population: int,
    status_container
) -> Dict[str, Any]:
    """
    Version mock pour le débogage - génère des scores aléatoires.
    """
    results: Dict[str, Any] = {}
    total_leviers = len(dic_leviers)
    scores_possibles = [0, 25, 50, 75, 100]
    
    justifications = {
        0: "Aucune action concrète identifiée pour ce levier. (Mode débogage)",
        25: "Actions ponctuelles et limitées identifiées. (Mode débogage)",
        50: "Actions partielles mais significatives mises en œuvre. (Mode débogage)",
        75: "Effort important et structuré observé. (Mode débogage)",
        100: "Mobilisation maximale du potentiel du levier. (Mode débogage)"
    }
    
    for idx, (levier, ids) in enumerate(dic_leviers.items(), 1):
        status_container.write(f"🎲 Évaluation aléatoire du levier ({idx}/{total_leviers}): {levier}")
        
        score = random.choice(scores_possibles)
        
        results[levier] = {
            "ids": ids,
            "raw_text": f'{{"score": {score}, "justification": "{justifications[score]}"}}',
            "parsed": {
                "score": score,
                "justification": justifications[score]
            },
            "error": None,
        }
        
        # Petite pause pour simuler le traitement
        time.sleep(0.05)

    return results


def calculate_reductions(
    df_ratios: pd.DataFrame,
    region: str,
    dic_leviers: Dict[str, Any],
    results_scores: Dict[str, Any],
    df_indicateurs: pd.DataFrame
) -> pd.DataFrame:
    """Calcule les réductions de CO2 par levier."""
    
    # Ajouter le mapping identifiant_referentiel
    df_ct = df_ratios[['Secteur', 'Leviers SGPE']].copy()
    df_ct['identifiant_referentiel'] = df_ct['Secteur'].map(D_MAP_SECTEUR)
    df_ct[region] = df_ratios[region]
    st.write("📊 Étape 1: Dataframe initial avec mapping secteur")
    st.dataframe(df_ct.head(10), use_container_width=True)
    
    # Calculer les réductions objectives par secteur
    st.write("🔍 DEBUG: Analyse des dates dans df_indicateurs")
    st.write(f"Type de date_valeur: {df_indicateurs['date_valeur'].dtype}")
    st.write(f"Valeurs uniques de date_valeur: {df_indicateurs['date_valeur'].unique()}")
    st.dataframe(df_indicateurs[['identifiant_referentiel', 'date_valeur', 'objectif']].head(10))
    
    dic_reduction = {}
    for ids in df_indicateurs.identifiant_referentiel.unique():
        df_filtered = df_indicateurs[df_indicateurs.identifiant_referentiel == ids]
        
        if len(df_filtered) >= 2:
            # Convertir date_valeur en string si nécessaire pour la comparaison
            df_filtered['date_str'] = df_filtered['date_valeur'].astype(str)
            
            # Filtrer pour 2030
            df_2030 = df_filtered[df_filtered['date_str'].str.startswith('2030')]
            val_2030 = df_2030['objectif'].iloc[0] if len(df_2030) > 0 else 0
            
            # Filtrer pour 2019
            df_2019 = df_filtered[df_filtered['date_str'].str.startswith('2019')]
            val_2019 = df_2019['objectif'].iloc[0] if len(df_2019) > 0 else 0
            
            dic_reduction[ids] = float(val_2030 - val_2019)
    
    st.write("📊 Étape 2: Dictionnaire des réductions par secteur")
    st.write(dic_reduction)
    
    df_ct['reduction'] = df_ct['identifiant_referentiel'].map(dic_reduction)
    df_ct['reduction_leveir'] = (df_ct['reduction'] * df_ct[region] / 100).round(1)
    st.write("📊 Étape 3: Après calcul des réductions par levier")
    st.dataframe(df_ct.head(10), use_container_width=True)
    
    # Extraire les scores d'implication
    ct_levier = {}
    dic_justification = {}
    dic_ids_fa = {}
    
    for levier, data in results_scores.items():
        if data.get('parsed'):
            ct_levier[levier] = data['parsed'].get('score', 0)
            dic_justification[levier] = data['parsed'].get('justification', '')
        else:
            ct_levier[levier] = 0
            dic_justification[levier] = ''
        dic_ids_fa[levier] = data.get('ids', [])
    
    df_ct['implication'] = df_ct['Leviers SGPE'].map(ct_levier).fillna(0)
    df_ct['reduction_theorique'] = (df_ct['reduction_leveir'] * df_ct['implication'] / 100).round(1)
    df_ct['justification'] = df_ct['Leviers SGPE'].map(dic_justification)
    df_ct['ids'] = df_ct['Leviers SGPE'].map(dic_ids_fa)
    st.write("📊 Étape 4: Dataframe final avec implication et réduction théorique")
    st.dataframe(df_ct, use_container_width=True)
    
    return df_ct


def save_to_database(df: pd.DataFrame, collectivite_id: int):
    """Sauvegarde les résultats dans la table modelisation_impact sur OLAP."""
    df_to_save = df.copy()
    df_to_save['collectivite_id'] = collectivite_id
    df_to_save['created_at'] = datetime.now()
    
    # Convertir les listes en JSON string pour le stockage
    if 'ids' in df_to_save.columns:
        df_to_save['ids'] = df_to_save['ids'].apply(lambda x: json.dumps(x) if isinstance(x, list) else x)
    
    # ⚠️ IMPORTANT: On écrit sur OLAP, jamais en prod !
    engine = get_engine()
    df_to_save.to_sql('modelisation_impact', con=engine, if_exists='append', index=False)


# ==========================
# Interface Streamlit
# ==========================

st.title("🎯 Calcul de modélisation d'impact")
st.markdown("Exécutez la modélisation d'impact CO2 pour une collectivité à partir de son plan d'actions.")

st.markdown("---")

# Chargement des données
df_collectivites = load_collectivites()
df_ratios = load_ratios_csv()

# Vérification du fichier CSV
if df_ratios is None:
    st.error("❌ Le fichier `data/leviers_sgpe_region.csv` est introuvable. Veuillez l'ajouter au projet.")
    st.stop()

regions = get_regions_from_csv(df_ratios)

if not regions:
    st.error("❌ Aucune région trouvée dans le fichier CSV.")
    st.stop()

# Sélecteurs
col1, col2 = st.columns(2)

with col1:
    # Créer une liste pour le selectbox avec nom et id
    collectivite_options = df_collectivites['nom'].tolist()
    selected_nom = st.selectbox(
        "🏛️ Sélectionner une collectivité",
        options=collectivite_options,
        index=None,
        placeholder="Rechercher une collectivité..."
    )

with col2:
    selected_region = st.selectbox(
        "🗺️ Sélectionner une région",
        options=regions,
        index=0
    )

# Afficher les infos de la collectivité sélectionnée
if selected_nom:
    collectivite_info = df_collectivites[df_collectivites['nom'] == selected_nom].iloc[0]
    selected_id = collectivite_info['id']
    population = collectivite_info['population'] if pd.notna(collectivite_info['population']) else 0
    
    st.info(f"**Collectivité sélectionnée:** {selected_nom} (ID: {selected_id}) — Population: {population:,}")

st.markdown("---")

# Mode débogage
debug_mode = st.toggle(
    "🐛 Mode débogage (classification et notation aléatoires, sans appels API)",
    value=False
)

full_access_mode = st.toggle(
    "🔓 Accès à toutes les fiches actions (y compris restreintes)",
    value=False
)

if debug_mode:
    st.warning("⚠️ Mode débogage activé - Les résultats seront générés aléatoirement")

# Bouton d'exécution
if st.button("🚀 Lancer l'exécution", type="primary", disabled=not selected_nom):
    
    with st.status("⏳ Exécution en cours...", expanded=True) as status:
        
        # Étape 1: Récupération du plan d'actions
        st.write("📋 Récupération du plan d'actions...")
        plan = fetch_plan_actions(selected_id)
        
        if plan.empty:
            status.update(label="❌ Erreur", state="error")
            st.error(f"Aucune action trouvée pour la collectivité {selected_nom}")
            st.stop()
        
        st.write(f"✅ {len(plan)} actions récupérées")
        st.dataframe(plan, use_container_width=True)
        
        # Étape 2: Récupération des indicateurs SNBC
        st.write("📊 Récupération des indicateurs SNBC...")
        df_indicateurs = fetch_indicateurs_snbc(selected_id)
        st.write(f"✅ {len(df_indicateurs)} indicateurs récupérés")
        st.dataframe(df_indicateurs, use_container_width=True)
        
        # Étape 3: Classification des actions par levier
        st.write("🔍 Classification des actions par levier CO2...")
        try:
            if debug_mode:
                classification_response = classify_actions_mock(plan, st)
            else:
                classification_response = classify_actions(plan, st)
            dic_leviers = invert_actions_by_lever(classification_response)
            st.write(f"✅ {len(dic_leviers)} leviers identifiés avec des actions")
            # Afficher le dictionnaire des leviers
            df_leviers_debug = pd.DataFrame([
                {"Levier": levier, "Nombre d'actions": len(ids), "IDs actions": str(ids)}
                for levier, ids in dic_leviers.items()
            ])
            st.dataframe(df_leviers_debug, use_container_width=True)
        except Exception as e:
            status.update(label="❌ Erreur", state="error")
            st.error(f"Erreur lors de la classification: {e}")
            st.stop()
        
        # Étape 4: Évaluation de l'implication par levier
        st.write("📈 Évaluation de l'implication par levier...")
        try:
            if debug_mode:
                results_scores = score_all_levers_mock(
                    plan=plan,
                    dic_leviers=dic_leviers,
                    collectivite_nom=selected_nom,
                    population=int(population),
                    status_container=st
                )
            else:
                results_scores = score_all_levers(
                    plan=plan,
                    dic_leviers=dic_leviers,
                    collectivite_nom=selected_nom,
                    population=int(population),
                    status_container=st
                )
            st.write(f"✅ {len(results_scores)} leviers évalués")
            # Afficher les scores
            df_scores_debug = pd.DataFrame([
                {
                    "Levier": levier,
                    "Score": data.get('parsed', {}).get('score', 0) if data.get('parsed') else 0,
                    "Justification": data.get('parsed', {}).get('justification', '') if data.get('parsed') else '',
                    "Erreur": data.get('error', '')
                }
                for levier, data in results_scores.items()
            ])
            st.dataframe(df_scores_debug, use_container_width=True)
        except Exception as e:
            status.update(label="❌ Erreur", state="error")
            st.error(f"Erreur lors de l'évaluation: {e}")
            st.stop()
        
        # Étape 5: Calcul des réductions
        st.write("🧮 Calcul des réductions de CO2...")
        try:
            df_results = calculate_reductions(
                df_ratios=df_ratios,
                region=selected_region,
                dic_leviers=dic_leviers,
                results_scores=results_scores,
                df_indicateurs=df_indicateurs
            )
            st.write(f"✅ Calculs terminés pour {len(df_results)} leviers")
            st.write("📊 Résultats finaux du calcul")
            st.dataframe(df_results, use_container_width=True)
        except Exception as e:
            status.update(label="❌ Erreur", state="error")
            st.error(f"Erreur lors du calcul: {e}")
            st.stop()
        
        # Étape 6: Sauvegarde en base OLAP
        st.write("💾 Sauvegarde dans la base de données OLAP...")
        try:
            save_to_database(df_results, selected_id)
            st.write("✅ Données sauvegardées dans `modelisation_impact` (OLAP)")
        except Exception as e:
            status.update(label="❌ Erreur", state="error")
            st.error(f"Erreur lors de la sauvegarde: {e}")
            st.stop()
        
        status.update(label="✅ Exécution terminée avec succès!", state="complete")
    
    # Afficher un résumé des résultats
    st.success(f"🎉 Modélisation terminée pour **{selected_nom}**!")
    
    # Afficher un aperçu des résultats
    st.subheader("📊 Aperçu des résultats")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        reduction_totale = df_results['reduction_theorique'].sum()
        st.metric("Réduction modélisée", f"{abs(reduction_totale):.0f} kt CO₂eq")
    with col2:
        potentiel_total = df_results['reduction_leveir'].sum()
        st.metric("Potentiel total", f"{abs(potentiel_total):.0f} kt CO₂eq")
    with col3:
        pct = (abs(reduction_totale) / abs(potentiel_total) * 100) if potentiel_total != 0 else 0
        st.metric("% du potentiel activé", f"{pct:.0f}%")
    
    # Tableau des résultats
    st.dataframe(
        df_results[['Secteur', 'Leviers SGPE', 'implication', 'reduction_theorique', 'justification']].rename(columns={
            'Leviers SGPE': 'Levier',
            'implication': 'Implication (%)',
            'reduction_theorique': 'Réduction (kt)',
            'justification': 'Justification'
        }),
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("👆 Sélectionnez une collectivité et une région, puis cliquez sur **Lancer l'exécution**.")
