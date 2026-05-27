import streamlit as st

# Configuration de la page en premier
st.set_page_config(
    page_title="Priorisation des actions",
    page_icon="🎯",
    layout="wide"
)

import json
import random
import time
from collections import defaultdict
from datetime import datetime
from typing import Any

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
Production Industrielle
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

LEVIERS_LIST = [l.strip() for l in LEVIERS.strip().split("\n") if l.strip()]
LEVIERS_SET = set(LEVIERS_LIST)
VALID_CATEGORIES = {1, 2, 3, 4, 5, 6}

CATEGORIES = {
    1: "Aménagement & infrastructures",
    2: "Réglementation & planification",
    3: "Financement & fiscalité",
    4: "Gouvernance & partenariats",
    5: "Exemplarité interne",
    6: "Sensibilisation & accompagnement",
}

D_MAP_SECTEUR = {
    'Résidentiel': 'cae_1.c',
    'Tertiaire': 'cae_1.d',
    'Transport ': 'cae_1.k',
    'Agriculture': 'cae_1.g',
    'Industrie': 'cae_1.i',
    'Déchets': 'cae_1.h',
    'UTCATF': 'cae_1.csc',
    'Branche énergie': 'cae_1.j',
}

# Codes INSEE région → libellés colonnes de data/leviers_sgpe_region.csv
REGION_CODE_TO_LABEL = {
    '84': 'Auvergne-Rhône-Alpes',
    '27': 'Bourgogne-Franche-Comté',
    '53': 'Bretagne',
    '24': 'Centre-Val de Loire',
    '94': 'Corse',
    '44': 'Grand Est',
    '32': 'Hauts-de-France',
    '11': 'Île-de-France',
    '28': 'Normandie',
    '75': 'Nouvelle-Aquitaine',
    '76': 'Occitanie',
    '52': 'Pays de la Loire',
    '93': "Provence-Alpes-Côte d'Azur",
}


def region_label_from_code(region_code: str | None) -> str | None:
    """Retourne le libellé région CSV à partir du region_code collectivité."""
    if region_code is None or pd.isna(region_code):
        return None
    return REGION_CODE_TO_LABEL.get(str(region_code).strip())

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
def load_ratios_csv() -> pd.DataFrame | None:
    """Charge le CSV des ratios de leviers SGPE par région."""
    try:
        return pd.read_csv('data/leviers_sgpe_region.csv', sep=';')
    except FileNotFoundError:
        return None


@st.cache_data(ttl="1h")
def load_leviers_ref():
    """Charge le référentiel leviers / secteurs depuis le CSV."""
    df = load_ratios_csv()
    if df is None:
        return None
    df_ref = df[['Secteur', 'Leviers SGPE']].copy()
    df_ref['identifiant_referentiel'] = df_ref['Secteur'].map(D_MAP_SECTEUR)
    return df_ref


def get_region_columns(df_ratios: pd.DataFrame) -> list[str]:
    """Liste les noms de région (colonnes du CSV leviers_sgpe_region)."""
    return [c for c in df_ratios.columns if c not in ('Secteur', 'Leviers SGPE')]


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
            params={"collectivite_id": collectivite_id},
        )
    return df


def calculate_reductions_by_lever(
    df_ratios: pd.DataFrame,
    region: str,
    df_indicateurs: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calcule la réduction de CO2 par levier (potentiel brut, sans score d'implication).

    Réduction par levier = (objectif 2030 − objectif 2019 du secteur) × ratio régional / 100.
    """
    df_ct = df_ratios[['Secteur', 'Leviers SGPE']].copy()
    df_ct['identifiant_referentiel'] = df_ct['Secteur'].map(D_MAP_SECTEUR)
    df_ct[region] = df_ratios[region]

    dic_reduction: dict[str, float] = {}
    for ref in df_indicateurs['identifiant_referentiel'].unique():
        df_filtered = df_indicateurs[df_indicateurs['identifiant_referentiel'] == ref]

        if len(df_filtered) >= 2:
            df_filtered = df_filtered.copy()
            df_filtered['date_str'] = df_filtered['date_valeur'].astype(str)

            df_2030 = df_filtered[df_filtered['date_str'].str.startswith('2030')]
            val_2030 = df_2030['objectif'].iloc[0] if len(df_2030) > 0 else 0

            df_2019 = df_filtered[df_filtered['date_str'].str.startswith('2019')]
            val_2019 = df_2019['objectif'].iloc[0] if len(df_2019) > 0 else 0

            dic_reduction[ref] = float(val_2030 - val_2019)

    df_ct['reduction_secteur'] = df_ct['identifiant_referentiel'].map(dic_reduction)
    df_ct['reduction'] = (df_ct['reduction_secteur'] * df_ct[region] / 100).round(1)

    df_result = df_ct[['Leviers SGPE', 'reduction']].rename(
        columns={'Leviers SGPE': 'levier'}
    )
    return df_result.dropna(subset=['reduction']).reset_index(drop=True)


def save_reductions_by_lever(df: pd.DataFrame, collectivite_id: int):
    """Sauvegarde les réductions par levier dans priorisation_reduction_levier (OLAP)."""
    df_to_save = df[['levier', 'reduction']].copy()
    df_to_save['collectivite_id'] = collectivite_id
    df_to_save = df_to_save[['collectivite_id', 'levier', 'reduction']]

    if debug_mode:
        st.info("Mode débogage — réductions par levier non sauvegardées.")
        st.dataframe(df_to_save, use_container_width=True)
        return

    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(
            text(
                "DELETE FROM priorisation_reduction_levier "
                "WHERE collectivite_id = :id"
            ),
            {"id": collectivite_id},
        )
        df_to_save.to_sql(
            'priorisation_reduction_levier',
            con=conn,
            if_exists='append',
            index=False,
        )


def run_reductions_by_lever(
    collectivite_id: int,
    region: str,
    df_ratios: pd.DataFrame,
) -> pd.DataFrame:
    """Calcule et enregistre les réductions potentielles par levier."""
    if region not in get_region_columns(df_ratios):
        raise ValueError(f"Région invalide : {region}")
    df_indicateurs = fetch_indicateurs_snbc(collectivite_id)
    df_result = calculate_reductions_by_lever(
        df_ratios=df_ratios,
        region=region,
        df_indicateurs=df_indicateurs,
    )
    save_reductions_by_lever(df_result, collectivite_id)
    return df_result


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
                    WHERE fa.collectivite_id = :collectivite_id and parent_id is null
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
                    WHERE fa.collectivite_id = :collectivite_id and parent_id is null
                    AND fa.restreint = False
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

# Contexte
On te fournit trois éléments :

1. Un plan d'actions sous forme de texte structuré. Chaque action est identifiée par un id unique et décrite par un titre et une description.

2. Une liste fermée de leviers CO2. Chaque levier correspond à un mécanisme d'impact direct ou quasi direct sur les émissions de CO2.

3. Une liste fermée de 6 catégories de TYPE D'ACTION. La catégorie ne décrit pas l'impact carbone mais le MOYEN par lequel la collectivité agit.

# Les 6 catégories
1. Aménagement & infrastructures — Actions physiques sur le territoire à destination des habitants et des acteurs économiques : urbanisme, mobilités douces, espaces verts, réseaux (eau, chaleur, assainissement), renaturation, équipements publics ouverts au public.
2. Réglementation & planification — Documents cadres et actes juridiques qui orientent l'action du territoire : PLU/PLUi, PCAET, SCoT, règlements locaux, zones à faibles émissions, arrêtés municipaux.
3. Financement & fiscalité — Orientation des flux économiques : subventions aux particuliers et entreprises, tarification incitative, budgets participatifs écologiques, fiscalité locale verte.
4. Gouvernance & partenariats — Pilotage de la politique de transition : élu référent, service dédié, stratégie et feuille de route, coopération intercommunale, partenariats privés/associatifs, concertation citoyenne, suivi-évaluation.
5. Exemplarité interne — Transition écologique appliquée au fonctionnement PROPRE de la collectivité : rénovation du patrimoine bâti public, flotte de véhicules, restauration collective, achats et commande publique responsables, numérique responsable, formation des agents.
6. Sensibilisation & accompagnement — Information, éducation et conseil aux habitants, entreprises et associations : guichet unique rénovation, animations scolaires, ateliers, communication, accompagnement de projets citoyens.

# Distinctions à respecter impérativement
- Catégorie 1 vs 5 : une action sur un bâtiment ou un véhicule relève de la 5 si elle porte sur le patrimoine ou les moyens PROPRES de la collectivité, et de la 1 seulement si l'équipement est destiné aux habitants/acteurs du territoire.
- Catégorie 2 vs 4 : la 2 concerne l'acte juridique ou le document opposable lui-même ; la 4 concerne la manière de piloter, décider et coopérer. Adopter un PLU = 2. Créer un comité de suivi = 4.
- Catégorie 3 vs 6 : verser une subvention = 3 ; informer, orienter ou accompagner sans flux financier = 6.
- Une action peut relever de plusieurs catégories AU SEIN d'un même levier si elle agit réellement par plusieurs de ces mécanismes (ex : créer une piste cyclable + la subventionner). N'attribue une catégorie que si l'action agit CONCRÈTEMENT par ce mécanisme, pas si elle l'évoque seulement.

# Objectif
Pour chaque action, identifier de manière SÛRE :
- les leviers CO2 auxquels elle correspond ;
- pour chaque levier retenu, la ou les catégories de type d'action correspondantes.

# Règles fondamentales
- Une action peut correspondre à zéro, un ou plusieurs leviers.
- N'associe un levier que si le lien avec un mécanisme d'impact CO2 est clair, direct ou très fortement plausible.
- Si le lien est trop indirect, spéculatif ou dépend d'hypothèses non explicites, ne pas associer le levier.
- En cas de doute sur un levier, s'abstenir : la précision prime sur l'exhaustivité.
- Pour chaque levier retenu, il doit y avoir AU MOINS une catégorie. Une liste de catégories vide pour un levier retenu est interdite.
- Ne jamais inventer de levier hors de la liste fournie. Ne pas reformuler les leviers : utiliser exactement les libellés fournis.
- Les catégories sont des entiers de 1 à 6 uniquement.

# Format de sortie attendu
Réponds UNIQUEMENT avec un JSON valide, sans texte ni balise additionnels.
Chaque action est une clé. Sa valeur est un objet associant chaque levier retenu à la liste (entiers, 1 à 6) de ses catégories.
Si aucun levier sûr n'existe pour une action, la valeur est un objet vide {{}}.

Exemple de format :
{{
  "id_action_1": {{ "levier_A": [1, 3], "levier_B": [4] }},
  "id_action_2": {{}},
  "id_action_3": {{ "levier_C": [2] }}
}}

# Entrées
Plan d'actions :
{plan_texte}

Liste des leviers CO2 :
{LEVIERS}
"""


def build_prompt_implication(
    actions_par_categorie: str,
    levier: str,
    collectivite_nom: str,
    population: int,
    references_par_categorie: str | None = None,
) -> str:
    """Construit le prompt pour évaluer l'activation d'un levier, catégorie par catégorie.

    `actions_par_categorie` : actions de la collectivité regroupées par catégorie (1 à 6).
        Une catégorie sans action doit apparaître explicitement comme vide.
    `references_par_categorie` : actions de référence par catégorie, si disponibles.
    """
    bloc_reference = (
        f"\n# Actions de référence par catégorie\n"
        f"Pour chaque catégorie, voici à quoi ressemblerait une mobilisation exemplaire. "
        f"Sers-t'en comme étalon du niveau 3.\n{references_par_categorie}\n"
        if references_par_categorie
        else "\n# Référentiel\nAucune liste de référence fournie : pour chaque catégorie, "
        "raisonne à partir de ce qu'une collectivité comparable et volontariste ferait.\n"
    )

    return f"""Tu es un expert en politiques publiques locales et en évaluation qualitative d'impact climat.

# Contexte
On te fournit :
1. Le nom d'une collectivité et sa population.
2. UN levier d'action climat (ex : « Co-voiturage »).
3. Les actions de la collectivité rattachées à ce levier, déjà regroupées par catégorie de type d'action.

# Les 6 catégories de type d'action
La catégorie ne décrit pas l'impact carbone mais le MOYEN par lequel la collectivité agit.
1. Aménagement & infrastructures — Actions physiques sur le territoire à destination des habitants et acteurs économiques : urbanisme, mobilités douces, espaces verts, réseaux, renaturation, équipements publics ouverts au public.
2. Réglementation & planification — Documents cadres et actes juridiques : PLU/PLUi, PCAET, SCoT, règlements locaux, zones à faibles émissions, arrêtés.
3. Financement & fiscalité — Orientation des flux économiques : subventions, tarification incitative, budgets participatifs écologiques, fiscalité locale verte.
4. Gouvernance & partenariats — Pilotage de la transition : élu référent, service dédié, stratégie et feuille de route, coopération intercommunale, partenariats, concertation, suivi-évaluation.
5. Exemplarité interne — Transition appliquée au fonctionnement propre de la collectivité : patrimoine bâti public, flotte, restauration collective, commande publique responsable, numérique responsable, formation des agents.
6. Sensibilisation & accompagnement — Information, éducation et conseil aux habitants, entreprises et associations : guichet unique rénovation, animations, ateliers, communication, accompagnement de projets citoyens.

# Objectif
Pour CHACUNE des 6 catégories, évaluer à quel point la collectivité mobilise ce type d'action SUR CE levier,
comparé à ce qui serait raisonnablement attendu d'une collectivité de taille comparable.

# Cadrage important
Tu évalues 6 cases « levier x catégorie », une note par catégorie.
Tu n'évalues pas le levier dans son ensemble, ni un impact CO2 chiffré.
Une catégorie seule ne peut pas activer tout le potentiel d'un levier — ce n'est pas la question.
La question, pour chaque catégorie, est : sur ce type précis d'action, la collectivité fait-elle peu,
ou fait-elle ce qu'on peut raisonnablement attendre de mieux ?
{bloc_reference}
# Échelle d'évaluation — 4 niveaux
Pour chaque catégorie, un entier parmi [0, 1, 2, 3] :

- 0 — non couvert : aucune action crédible sur cette case, ou actions hors sujet.
- 1 — amorcé : actions ponctuelles, symboliques ou expérimentales ; intention visible mais portée très limitée.
- 2 — partiel : actions réelles et concrètes mais incomplètes ; une part significative de l'attendu est faite, des pans importants manquent.
- 3 — pleinement activé : mobilisation structurée, cohérente et à large portée ; l'essentiel de l'attendu est fait.

# Principes d'évaluation
- Raisonner relativement à la taille et à la population de la collectivité.
- Juger la portée réelle (couverture, intensité, durée, public touché), pas le nombre d'actions ni leur formulation.
- Une catégorie sans aucune action rattachée reçoit obligatoirement 0.
- Ne pas surévaluer les actions purement incitatives, communicationnelles ou expérimentales — SAUF pour la catégorie 6 (Sensibilisation & accompagnement), où ces actions sont précisément le cœur du sujet.
- Une action seulement annoncée, non financée ou non engagée, ne peut pas porter un niveau 3.
- En cas de doute entre deux niveaux, retenir le plus bas.

# Méthode attendue
Pour chaque catégorie, raisonne en interne (portée réelle vs attendu) puis fixe la note.
Ne fais PAS apparaître ce raisonnement dans la réponse : la sortie ne contient que les notes.

# Format de sortie attendu
Réponds UNIQUEMENT avec un JSON valide, sans texte ni balise additionnels.
Les 6 catégories doivent toutes être présentes, clés "1" à "6", même si la note est 0.
Format exact :
{{
  "1": <0-3>,
  "2": <0-3>,
  "3": <0-3>,
  "4": <0-3>,
  "5": <0-3>,
  "6": <0-3>
}}

# Entrées
Collectivité : {collectivite_nom}
Population : {population}
Levier évalué : {levier}

Actions de la collectivité, regroupées par catégorie :
{actions_par_categorie}
"""


def strip_json_fences(text: str) -> str:
    """Enlève les ```json ... ``` si présents."""
    if not text:
        return ""
    t = text.strip()
    if t.startswith("```"):
        t = t.replace("```json", "").replace("```JSON", "").replace("```", "").strip()
    return t


def _call_llm_json(
    prompt: str,
    label: str,
    status_container,
    max_retries: int = 3,
    max_output_tokens: int | None = None,
) -> Any:
    """Appelle le LLM avec sortie JSON forcée, parse et retry en cas d'échec."""
    last_error = None

    for attempt in range(1, max_retries + 1):
        try:
            if attempt > 1:
                status_container.write(f"🔄 Retry {attempt}/{max_retries} ({label})...")

            kwargs: dict[str, Any] = {
                "model": "gpt-5.1-2025-11-13",
                "input": prompt,
                "reasoning": {"effort": "low" if reasoning_mode else "medium"},
                "text": {"format": {"type": "json_object"}},
            }
            if max_output_tokens:
                kwargs["max_output_tokens"] = max_output_tokens

            try:
                response = client.responses.create(**kwargs)
            except TypeError:
                kwargs.pop("text", None)
                response = client.responses.create(**kwargs)

            raw_text = strip_json_fences(response.output_text or "")
            return json.loads(raw_text)
        except json.JSONDecodeError as e:
            last_error = f"json_parse_error: {e}"
        except Exception as e:
            last_error = f"generation_error: {type(e).__name__}: {e}"

    raise RuntimeError(f"Échec LLM ({label}) après {max_retries} tentatives: {last_error}")


def validate_classification(
    data: Any,
    known_action_ids: set[int],
    known_leviers: set[str],
) -> dict[int, dict[str, list[int]]]:
    """Valide et normalise la sortie JSON de l'étape 1."""
    if not isinstance(data, dict):
        raise ValueError("La classification doit être un objet JSON")

    result: dict[int, dict[str, list[int]]] = {}
    for action_key, leviers_map in data.items():
        try:
            action_id = int(action_key)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Identifiant d'action invalide: {action_key}") from e

        if action_id not in known_action_ids:
            raise ValueError(f"Action inconnue: {action_id}")

        if not leviers_map:
            result[action_id] = {}
            continue

        if not isinstance(leviers_map, dict):
            raise ValueError(f"Valeur invalide pour l'action {action_id}")

        parsed_leviers: dict[str, list[int]] = {}
        for levier, categories in leviers_map.items():
            if levier not in known_leviers:
                raise ValueError(f"Levier inconnu: {levier}")
            if not isinstance(categories, list) or len(categories) == 0:
                raise ValueError(
                    f"Catégories vides pour le levier « {levier} » (action {action_id})"
                )
            cats: list[int] = []
            for cat in categories:
                cat_int = int(cat)
                if cat_int not in VALID_CATEGORIES:
                    raise ValueError(
                        f"Catégorie invalide {cat} pour l'action {action_id}"
                    )
                cats.append(cat_int)
            parsed_leviers[levier] = sorted(set(cats))

        result[action_id] = parsed_leviers

    return result


def validate_activation_scores(data: Any) -> dict[int, int]:
    """Valide et normalise la sortie JSON de l'étape 2."""
    if not isinstance(data, dict):
        raise ValueError("Les scores d'activation doivent être un objet JSON")

    scores: dict[int, int] = {}
    for cat_key in ("1", "2", "3", "4", "5", "6"):
        if cat_key not in data:
            raise ValueError(f"Catégorie manquante: {cat_key}")
        note = int(data[cat_key])
        if note not in {0, 1, 2, 3}:
            raise ValueError(f"Note invalide pour la catégorie {cat_key}: {note}")
        scores[int(cat_key)] = note

    return scores


def build_actions_text(plan: pd.DataFrame, ids: list) -> str:
    """Construit un texte d'actions pour une liste d'ids."""
    df = plan[plan["id"].isin(ids)].copy()
    if df.empty:
        return ""

    df["titre"] = df["titre"].fillna("").astype(str)
    df["description"] = df["description"].fillna("").astype(str)

    return "\n\n".join(
        f"{row.id} | {row.titre} : {row.description}".strip()
        for _, row in df.iterrows()
    ).strip()


def group_actions_by_lever_and_category(
    classification: dict[int, dict[str, list[int]]],
) -> dict[str, dict[int, list[int]]]:
    """Regroupe les actions classées par levier puis par catégorie."""
    grouped: dict[str, dict[int, list[int]]] = defaultdict(
        lambda: {cat: [] for cat in range(1, 7)}
    )

    for action_id, leviers_map in classification.items():
        for levier, categories in leviers_map.items():
            for cat in categories:
                grouped[levier][cat].append(action_id)

    result: dict[str, dict[int, list[int]]] = {}
    for levier, actions_by_cat in grouped.items():
        result[levier] = {
            cat: sorted(set(actions_by_cat[cat])) for cat in range(1, 7)
        }

    return result


def format_actions_by_category(
    plan: pd.DataFrame,
    actions_by_cat: dict[int, list[int]],
) -> str:
    """Formate les actions regroupées par catégorie pour le prompt étape 2."""
    blocks: list[str] = []
    for cat in range(1, 7):
        label = CATEGORIES[cat]
        blocks.append(f"Catégorie {cat} — {label} :")
        ids = actions_by_cat.get(cat, [])
        if ids:
            blocks.append(build_actions_text(plan, ids))
        else:
            blocks.append("(aucune action)")
        blocks.append("")
    return "\n".join(blocks).strip()


def classify_actions(
    plan: pd.DataFrame,
    status_container,
) -> dict[int, dict[str, list[int]]]:
    """Appelle l'API OpenAI pour classifier les actions (étape 1)."""
    plan_texte = "{" + ", ".join(
        f"{row.id}:{row.titre} - {row.description}"
        for _, row in plan.iterrows()
    ) + "}"

    prompt = build_prompt_classification(plan_texte)
    status_container.write("🤖 Classification des actions (étape 1)...")

    known_ids = set(plan["id"].astype(int))
    for attempt in range(1, 4):
        try:
            data = _call_llm_json(
                prompt,
                "classification",
                status_container,
                max_retries=1,
                max_output_tokens=120000,
            )
            return validate_classification(data, known_ids, LEVIERS_SET)
        except (ValueError, RuntimeError) as e:
            if attempt == 3:
                raise
            status_container.write(f"🔄 Validation échouée, retry {attempt + 1}/3: {e}")

    raise RuntimeError("Classification impossible")


def classify_actions_mock(
    plan: pd.DataFrame,
    status_container,
) -> dict[int, dict[str, list[int]]]:
    """Version mock — classification aléatoire levier × catégorie."""
    status_container.write("🎲 Mode débogage — Classification aléatoire...")

    result: dict[int, dict[str, list[int]]] = {}
    for _, row in plan.iterrows():
        num_leviers = random.randint(0, min(3, len(LEVIERS_LIST)))
        if num_leviers == 0:
            result[int(row.id)] = {}
        else:
            mapping: dict[str, list[int]] = {}
            for levier in random.sample(LEVIERS_LIST, num_leviers):
                num_cats = random.randint(1, 3)
                mapping[levier] = sorted(random.sample(list(range(1, 7)), num_cats))
            result[int(row.id)] = mapping

    return result


def _apply_empty_category_override(
    scores: dict[int, int],
    actions_by_cat: dict[int, list[int]],
) -> dict[int, int]:
    """Force la note à 0 pour les catégories sans action rattachée."""
    result = dict(scores)
    for cat in range(1, 7):
        if not actions_by_cat.get(cat, []):
            result[cat] = 0
    return result


def score_all_levers(
    plan: pd.DataFrame,
    lever_category_actions: dict[str, dict[int, list[int]]],
    collectivite_nom: str,
    population: int,
    status_container,
) -> dict[str, dict[int, int]]:
    """Évalue l'activation catégorie par catégorie pour chaque levier actif (étape 2)."""
    lever_scores: dict[str, dict[int, int]] = {}
    total_leviers = len(lever_category_actions)

    for idx, (levier, actions_by_cat) in enumerate(lever_category_actions.items(), 1):
        status_container.write(
            f"📊 Notation ({idx}/{total_leviers}): {levier}"
        )

        actions_par_categorie = format_actions_by_category(plan, actions_by_cat)
        prompt = build_prompt_implication(
            actions_par_categorie,
            levier,
            collectivite_nom,
            population,
        )

        for attempt in range(1, 4):
            try:
                data = _call_llm_json(prompt, f"activation_{levier}", status_container, max_retries=1)
                scores = validate_activation_scores(data)
                lever_scores[levier] = _apply_empty_category_override(scores, actions_by_cat)
                break
            except (ValueError, RuntimeError) as e:
                if attempt == 3:
                    raise RuntimeError(f"Notation impossible pour « {levier} »: {e}") from e
                status_container.write(f"🔄 Validation échouée, retry {attempt + 1}/3: {e}")

        time.sleep(0.2)

    return lever_scores


def score_all_levers_mock(
    plan: pd.DataFrame,
    lever_category_actions: dict[str, dict[int, list[int]]],
    collectivite_nom: str,
    population: int,
    status_container,
) -> dict[str, dict[int, int]]:
    """Version mock — notes aléatoires 0-3 par catégorie."""
    lever_scores: dict[str, dict[int, int]] = {}
    total_leviers = len(lever_category_actions)

    for idx, (levier, actions_by_cat) in enumerate(lever_category_actions.items(), 1):
        status_container.write(
            f"🎲 Notation aléatoire ({idx}/{total_leviers}): {levier}"
        )
        scores = {cat: random.randint(0, 3) for cat in range(1, 7)}
        lever_scores[levier] = _apply_empty_category_override(scores, actions_by_cat)
        time.sleep(0.05)

    return lever_scores


def build_priorisation_dataframe(
    collectivite_id: int,
    df_leviers_ref: pd.DataFrame,
    lever_scores: dict[str, dict[int, int]],
    lever_category_actions: dict[str, dict[int, list[int]]],
) -> pd.DataFrame:
    """Construit le dataframe final : une ligne par case levier × catégorie."""
    rows: list[dict[str, Any]] = []
    created_at = datetime.now()
    zero_scores = {cat: 0 for cat in range(1, 7)}
    empty_actions = {cat: [] for cat in range(1, 7)}

    for _, row in df_leviers_ref.iterrows():
        levier = row["Leviers SGPE"]
        scores = lever_scores.get(levier, zero_scores)
        actions = lever_category_actions.get(levier, empty_actions)

        for cat in range(1, 7):
            rows.append({
                "collectivite_id": collectivite_id,
                "secteur": row["Secteur"],
                "identifiant_referentiel": row["identifiant_referentiel"],
                "levier": levier,
                "categorie": cat,
                "note": scores.get(cat, 0),
                "ids": actions.get(cat, []),
                "created_at": created_at,
            })

    return pd.DataFrame(rows)


def save_to_database(df: pd.DataFrame, collectivite_id: int):
    """Sauvegarde les résultats dans la table priorisation sur OLAP (replace)."""
    df_to_save = df.copy()

    if "ids" in df_to_save.columns:
        df_to_save["ids"] = df_to_save["ids"].apply(
            lambda x: json.dumps(x) if isinstance(x, list) else x
        )

    if debug_mode:
        st.info("Debug mode activé, on ne sauvegarde pas en base.")
        st.dataframe(df_to_save, use_container_width=True)
        return

    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(
            text("DELETE FROM priorisation WHERE collectivite_id = :id"),
            {"id": collectivite_id},
        )
        df_to_save.to_sql("priorisation", con=conn, if_exists="append", index=False)


# ==========================
# Interface Streamlit
# ==========================

st.title("🎯 Priorisation des actions")
st.markdown(
    "Analyse qualitative du plan d'actions d'une collectivité : "
    "classification par levier × catégorie et notation d'activation (0–3)."
)

st.markdown("---")

df_collectivites = load_collectivites()
df_ratios = load_ratios_csv()
df_leviers_ref = load_leviers_ref()

if df_ratios is None or df_leviers_ref is None:
    st.error(
        "❌ Le fichier `data/leviers_sgpe_region.csv` est introuvable. "
        "Veuillez l'ajouter au projet."
    )
    st.stop()

selected_nom = st.selectbox(
    "🏛️ Sélectionner une collectivité",
    options=df_collectivites["nom"].tolist(),
    index=None,
    placeholder="Rechercher une collectivité...",
)

selected_region: str | None = None

if selected_nom:
    collectivite_info = df_collectivites[df_collectivites["nom"] == selected_nom].iloc[0]
    selected_id = collectivite_info["id"]
    population = (
        collectivite_info["population"]
        if pd.notna(collectivite_info["population"])
        else 0
    )
    selected_region = region_label_from_code(collectivite_info["region_code"])
    region_info = (
        f" — Région : **{selected_region}**"
        if selected_region
        else " — ⚠️ Région inconnue (region_code absent ou non mappé)"
    )
    st.info(
        f"**Collectivité sélectionnée:** {selected_nom} (ID: {selected_id}) "
        f"— Population: {population:,}{region_info}"
    )

st.markdown("---")

debug_mode = st.toggle(
    "🐛 Mode débogage (classification et notation aléatoires, sans appels API)",
    value=False,
)

full_access_mode = st.toggle(
    "🔓 Accès à toutes les fiches actions (y compris restreintes)",
    value=False,
)

reasoning_mode = st.toggle(
    "😴 Low reasoning (Medium par défaut)",
    value=False,
)

if debug_mode:
    st.warning("⚠️ Mode débogage activé — les résultats seront générés aléatoirement")

can_run = bool(selected_nom and selected_region)

if st.button("🚀 Lancer l'exécution", type="primary", disabled=not can_run):

    with st.status("⏳ Exécution en cours...", expanded=True) as status:

        st.write("📋 Récupération du plan d'actions...")
        plan = fetch_plan_actions(selected_id)

        if plan.empty:
            status.update(label="❌ Erreur", state="error")
            st.error(f"Aucune action trouvée pour la collectivité {selected_nom}")
            st.stop()

        st.write(f"✅ {len(plan)} actions récupérées")
        st.dataframe(plan, use_container_width=True)

        st.write("📉 Calcul des réductions par levier (SNBC × ratios région)...")
        try:
            st.write(f"✅ Région utilisée : **{selected_region}**")
            df_reductions = run_reductions_by_lever(
                collectivite_id=selected_id,
                region=selected_region,
                df_ratios=df_ratios,
            )
            st.write(f"✅ {len(df_reductions)} leviers avec réduction calculée")
            if not df_reductions.empty:
                st.dataframe(df_reductions, use_container_width=True)
            if not debug_mode:
                st.write(
                    "✅ Réductions sauvegardées dans "
                    "`priorisation_reduction_levier` (OLAP)"
                )
        except Exception as e:
            status.update(label="❌ Erreur", state="error")
            st.error(f"Erreur lors du calcul des réductions par levier : {e}")
            st.stop()

        st.write("🔍 Classification des actions par levier × catégorie (étape 1)...")
        try:
            if debug_mode:
                classification = classify_actions_mock(plan, st)
            else:
                classification = classify_actions(plan, st)

            lever_category_actions = group_actions_by_lever_and_category(classification)
            st.write(f"✅ {len(lever_category_actions)} leviers identifiés avec des actions")

            df_classif_debug = pd.DataFrame([
                {
                    "Levier": levier,
                    "Catégorie": cat,
                    "Nb actions": len(ids),
                    "IDs": str(ids),
                }
                for levier, cats in lever_category_actions.items()
                for cat, ids in cats.items()
                if ids
            ])
            if not df_classif_debug.empty:
                st.dataframe(df_classif_debug, use_container_width=True)
            else:
                st.warning("Aucune action classée sur un levier.")
        except Exception as e:
            status.update(label="❌ Erreur", state="error")
            st.error(f"Erreur lors de la classification: {e}")
            st.stop()

        st.write("📈 Notation de l'activation par levier (étape 2)...")
        try:
            if debug_mode:
                lever_scores = score_all_levers_mock(
                    plan=plan,
                    lever_category_actions=lever_category_actions,
                    collectivite_nom=selected_nom,
                    population=int(population),
                    status_container=st,
                )
            else:
                lever_scores = score_all_levers(
                    plan=plan,
                    lever_category_actions=lever_category_actions,
                    collectivite_nom=selected_nom,
                    population=int(population),
                    status_container=st,
                )
            st.write(f"✅ {len(lever_scores)} leviers notés")

            df_scores_debug = pd.DataFrame([
                {
                    "Levier": levier,
                    **{CATEGORIES[cat]: scores.get(cat, 0) for cat in range(1, 7)},
                }
                for levier, scores in lever_scores.items()
            ])
            st.dataframe(df_scores_debug, use_container_width=True)
        except Exception as e:
            status.update(label="❌ Erreur", state="error")
            st.error(f"Erreur lors de la notation: {e}")
            st.stop()

        st.write("📦 Construction du résultat priorisation...")
        try:
            df_results = build_priorisation_dataframe(
                collectivite_id=selected_id,
                df_leviers_ref=df_leviers_ref,
                lever_scores=lever_scores,
                lever_category_actions=lever_category_actions,
            )
            st.write(f"✅ {len(df_results)} cases levier × catégorie générées")
        except Exception as e:
            status.update(label="❌ Erreur", state="error")
            st.error(f"Erreur lors de la construction du résultat: {e}")
            st.stop()

        st.write("💾 Sauvegarde dans la base de données OLAP...")
        try:
            save_to_database(df_results, selected_id)
            if not debug_mode:
                st.write("✅ Données sauvegardées dans `priorisation` (OLAP)")
        except Exception as e:
            status.update(label="❌ Erreur", state="error")
            st.error(f"Erreur lors de la sauvegarde: {e}")
            st.stop()

        status.update(label="✅ Exécution terminée avec succès!", state="complete")

    st.success(f"🎉 Priorisation terminée pour **{selected_nom}**!")

    st.subheader("📊 Aperçu des résultats")

    cases_activees = (df_results["note"] > 0).sum()
    leviers_couverts = df_results.loc[df_results["note"] > 0, "levier"].nunique()
    note_counts = df_results["note"].value_counts().sort_index().to_dict()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Cases activées (note > 0)", cases_activees)
    with col2:
        st.metric("Leviers couverts", leviers_couverts)
    with col3:
        st.metric("Cases totales", len(df_results))

    st.caption(f"Répartition des notes : {note_counts}")

    df_display = df_results.copy()
    df_display["categorie_libelle"] = df_display["categorie"].map(CATEGORIES)
    df_display["nb_actions"] = df_display["ids"].apply(
        lambda x: len(x) if isinstance(x, list) else 0
    )

    st.dataframe(
        df_display[
            ["secteur", "levier", "categorie_libelle", "note", "nb_actions"]
        ].rename(columns={
            "secteur": "Secteur",
            "levier": "Levier",
            "categorie_libelle": "Catégorie",
            "note": "Note",
            "nb_actions": "Nb actions",
        }),
        use_container_width=True,
        hide_index=True,
    )

else:
    st.info(
        "👆 Sélectionnez une **collectivité**, "
        "puis cliquez sur **Lancer l'exécution**."
    )
