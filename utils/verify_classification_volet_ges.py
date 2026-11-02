"""Reclassification GPT des fiches et comparaison avec fiche_action_volet_ges.

Lecture seule sur la base de prod (utilisateur streamlit_read_only).
Aucune écriture en base. Les sorties sont des fichiers locaux.

Le prompt est celui de pages/26_run_impact.py::build_prompt_classification
(utilisé par le run d'impact / priorisation).
"""

from __future__ import annotations

import json
import os
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse

import pandas as pd
from openai import OpenAI
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

ROOT = Path(__file__).resolve().parent.parent
SECRETS_PATH = ROOT / ".streamlit" / "secrets.toml"
OUTPUT_ROOT = ROOT / "data" / "verify_classification_volet_ges"
PROD_READONLY_USER = "streamlit_read_only"

DEFAULT_MODEL = "gpt-5.1-2025-11-13"
VALID_CATEGORIES = {1, 2, 3, 4, 5, 6}

# Aligné sur pages/26_run_impact.py
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
LEVIERS_LIST = [line.strip() for line in LEVIERS.strip().split("\n") if line.strip()]
LEVIERS_SET = set(LEVIERS_LIST)

CATEGORIES = {
    1: "Aménagement & infrastructures",
    2: "Réglementation & planification",
    3: "Financement & fiscalité",
    4: "Gouvernance & partenariats",
    5: "Exemplarité interne",
    6: "Sensibilisation & accompagnement",
}

# Enum prod levier_ges_id <-> libellé du prompt
LEVIER_ID_TO_LABEL = {
    "chaudieres_fioul_renovation_residentiel": "Changement chaudières fioul + rénovation (résidentiel)",
    "chaudieres_gaz_renovation_residentiel": "Changement chaudières gaz + rénovation (résidentiel)",
    "sobriete_batiments_residentiel": "Sobriété des bâtiments (résidentiel)",
    "chaudiere_fioul_tertiaire": "Changement de chaudière à fioul (tertiaire)",
    "chaudiere_gaz_tertiaire": "Changement de chaudière à gaz (tertiaire)",
    "sobriete_isolation_batiments_tertiaire": "Sobriété et isolation des bâtiments (tertiaire)",
    "reduction_deplacements": "Réduction des déplacements",
    "covoiturage": "Covoiturage",
    "velo_transport_commun": "Vélo et transport en commun",
    "vehicules_electriques": "Véhicules électriques",
    "efficacite_carburants_decarbones_vehicules_prives": "Efficacité et carburants décarbonés des véhicules privés",
    "bus_cars_decarbones": "Bus et cars décarbonés",
    "fret_decarbone_multimodalite": "Fret décarboné et multimodalité",
    "efficacite_sobriete_logistique": "Efficacité et sobriété logistique",
    "batiments_machines_agricoles": "Bâtiments & Machines agricoles",
    "elevage_durable": "Elevage durable",
    "pratiques_fertilisation_azotee": "Changements de pratiques de fertilisation azotée",
    "gestion_forets_produits_bois": "Gestion des forêts et produits bois",
    "pratiques_stockantes": "Pratiques stockantes",
    "gestion_haies": "Gestion des haies",
    "gestion_prairies": "Gestion des prairies",
    "sobriete_fonciere": "Sobriété foncière",
    "production_industrielle": "Production Industrielle",
    "captage_methane_isdnd": "Captage de méthane dans les ISDND",
    "prevention_dechets": "Prévention des déchets",
    "valorisation_matiere_dechets": "Valorisation matière des déchets",
    "electricite_renouvelable": "Electricité renouvelable",
    "biogaz": "Biogaz",
    "reseaux_chaleur_decarbones": "Réseaux de chaleur décarbonés",
}
LEVIER_LABEL_TO_ID = {label: levier_id for levier_id, label in LEVIER_ID_TO_LABEL.items()}

CATEGORIE_ID_TO_ENUM = {
    1: "amenagement",
    2: "planification",
    3: "financement",
    4: "gouvernance",
    5: "exemplarite",
    6: "sensibilisation",
}
CATEGORIE_ENUM_TO_ID = {name: cat_id for cat_id, name in CATEGORIE_ID_TO_ENUM.items()}

LogFn = Callable[[str], None]


def _log(message: str, log: LogFn | None = None) -> None:
    if log:
        log(message)
    else:
        print(message, flush=True)


def load_secrets() -> dict[str, Any]:
    secrets: dict[str, Any] = {}
    if SECRETS_PATH.exists():
        import tomllib

        with SECRETS_PATH.open("rb") as handle:
            secrets = tomllib.load(handle)
    return secrets


def openai_api_key(secrets: dict[str, Any] | None = None) -> str:
    key = os.environ.get("OPENAI_API_KEY", "")
    if key:
        return key
    secrets = secrets if secrets is not None else load_secrets()
    key = str(secrets.get("OPENAI_API_KEY") or "")
    if not key:
        raise RuntimeError(
            "OPENAI_API_KEY absente (variable d'environnement ou .streamlit/secrets.toml)."
        )
    return key


def engine_prod_readonly(secrets: dict[str, Any] | None = None) -> Engine:
    """Connexion lecture seule à la prod. Refuse tout utilisateur autre que streamlit_read_only."""
    secrets = secrets if secrets is not None else load_secrets()
    url = os.environ.get("database_prod") or str(secrets.get("database_prod") or "")
    if not url:
        raise RuntimeError("database_prod absent (env ou secrets.toml).")
    parsed = urlparse(url)
    if parsed.username != PROD_READONLY_USER:
        raise RuntimeError(
            f"Refus de connexion prod : utilisateur {parsed.username!r} "
            f"(attendu {PROD_READONLY_USER!r}). Aucune écriture n'est autorisée."
        )
    if url.startswith("postgresql://") and "+" not in url.split("://", 1)[0]:
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)
    return create_engine(url, pool_pre_ping=True, pool_recycle=300)


def build_prompt_classification(plan_texte: str) -> str:
    """Copie du prompt de pages/26_run_impact.py — à garder aligné."""
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
Chaque action est une clé égale à son identifiant numérique (ex. "26004"), JAMAIS le titre ni un code du type "1.1.1".
Sa valeur est un objet associant chaque levier retenu à la liste (entiers, 1 à 6) de ses catégories.
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


def strip_json_fences(raw: str) -> str:
    if not raw:
        return ""
    text_value = raw.strip()
    if text_value.startswith("```"):
        text_value = (
            text_value.replace("```json", "").replace("```JSON", "").replace("```", "").strip()
        )
    return text_value


def fetch_collectivite(engine: Engine, collectivite_id: int) -> dict[str, Any]:
    with engine.connect() as conn:
        df = pd.read_sql_query(
            text("SELECT id, nom FROM collectivite WHERE id = :id"),
            conn,
            params={"id": collectivite_id},
        )
    if df.empty:
        raise ValueError(f"Collectivité {collectivite_id} introuvable en prod.")
    return {"id": int(df.iloc[0]["id"]), "nom": str(df.iloc[0]["nom"])}


def fetch_fiches_a_classifier(engine: Engine, collectivite_id: int) -> pd.DataFrame:
    """Fiches du plan (axe + parent null) ∪ fiches déjà classées en prod, non supprimées."""
    sql = text(
        """
        SELECT DISTINCT
            fa.id,
            fa.titre,
            fa.description,
            fa.collectivite_id,
            fa.restreint,
            fa.parent_id,
            (faa.fiche_id IS NOT NULL) AS dans_plan,
            (vg.fiche_id IS NOT NULL) AS classee_prod
        FROM fiche_action fa
        LEFT JOIN fiche_action_axe faa ON faa.fiche_id = fa.id
        LEFT JOIN fiche_action_volet_ges vg ON vg.fiche_id = fa.id
        WHERE fa.collectivite_id = :collectivite_id
          AND fa.parent_id IS NULL
          AND COALESCE(fa.deleted, false) = false
          AND (faa.fiche_id IS NOT NULL OR vg.fiche_id IS NOT NULL)
        ORDER BY fa.id
        """
    )
    with engine.connect() as conn:
        df = pd.read_sql_query(sql, conn, params={"collectivite_id": collectivite_id})
    if df.empty:
        return df
    df["id"] = df["id"].astype(int)
    df["titre"] = df["titre"].fillna("").astype(str)
    df["description"] = df["description"].fillna("").astype(str)
    return df.drop_duplicates(subset=["id"]).sort_values("id").reset_index(drop=True)


def fetch_classification_prod(engine: Engine, collectivite_id: int) -> pd.DataFrame:
    sql = text(
        """
        SELECT
            vg.fiche_id,
            vg.levier_id::text AS levier_id,
            vg.categorie::text AS categorie,
            vg.created_at
        FROM fiche_action_volet_ges vg
        JOIN fiche_action fa ON fa.id = vg.fiche_id
        WHERE fa.collectivite_id = :collectivite_id
        ORDER BY vg.fiche_id, vg.levier_id, vg.categorie
        """
    )
    with engine.connect() as conn:
        df = pd.read_sql_query(sql, conn, params={"collectivite_id": collectivite_id})
    if not df.empty:
        df["fiche_id"] = df["fiche_id"].astype(int)
    return df


def build_plan_texte(plan: pd.DataFrame) -> str:
    """Format plus explicite que `id:titre` (les titres du type 1.1.1 trompaient le JSON)."""
    blocks = []
    for _, row in plan.iterrows():
        titre = str(row.titre or "").replace("\n", " ").strip()
        description = str(row.description or "").replace("\n", " ").strip()
        blocks.append(f"[id={int(row.id)}] {titre} : {description}")
    return "\n\n".join(blocks)


def _parse_action_id(action_key: Any, known_action_ids: set[int]) -> int:
    raw = str(action_key).strip()
    try:
        action_id = int(raw)
    except (ValueError, TypeError):
        match = re.match(r"^(\d+)", raw)
        if not match:
            raise ValueError(f"Identifiant d'action invalide: {action_key}")
        action_id = int(match.group(1))
    if action_id not in known_action_ids:
        raise ValueError(f"Action inconnue: {action_id} (clé {action_key!r})")
    return action_id


def validate_classification(
    data: Any,
    known_action_ids: set[int],
    known_leviers: set[str],
) -> dict[int, dict[str, list[int]]]:
    if not isinstance(data, dict):
        raise ValueError("La classification doit être un objet JSON")

    result: dict[int, dict[str, list[int]]] = {}
    for action_key, leviers_map in data.items():
        action_id = _parse_action_id(action_key, known_action_ids)

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
                    raise ValueError(f"Catégorie invalide {cat} pour l'action {action_id}")
                cats.append(cat_int)
            parsed_leviers[levier] = sorted(set(cats))

        result[action_id] = parsed_leviers

    for action_id in known_action_ids:
        result.setdefault(action_id, {})
    return result


def _call_llm_json(
    client: OpenAI,
    prompt: str,
    model: str,
    reasoning_low: bool,
    max_output_tokens: int,
    max_retries: int = 3,
    log: LogFn | None = None,
) -> Any:
    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            if attempt > 1:
                _log(f"  retry LLM {attempt}/{max_retries}", log)
            kwargs: dict[str, Any] = {
                "model": model,
                "input": prompt,
                "reasoning": {"effort": "low" if reasoning_low else "medium"},
                "text": {"format": {"type": "json_object"}},
                "max_output_tokens": max_output_tokens,
            }
            try:
                response = client.responses.create(**kwargs)
            except TypeError:
                kwargs.pop("text", None)
                response = client.responses.create(**kwargs)
            raw_text = strip_json_fences(getattr(response, "output_text", None) or "")
            return json.loads(raw_text)
        except json.JSONDecodeError as e:
            last_error = f"json_parse_error: {e}"
        except Exception as e:
            last_error = f"generation_error: {type(e).__name__}: {e}"
    raise RuntimeError(f"Échec LLM après {max_retries} tentatives: {last_error}")


def _write_gpt_checkpoint(
    path: Path | None, classification: dict[int, dict[str, list[int]]]
) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(classification_to_jsonable(classification), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def classify_actions(
    plan: pd.DataFrame,
    client: OpenAI,
    *,
    model: str = DEFAULT_MODEL,
    batch_size: int = 25,
    reasoning_low: bool = False,
    max_output_tokens: int = 16000,
    existing: dict[int, dict[str, list[int]]] | None = None,
    checkpoint_path: Path | None = None,
    log: LogFn | None = None,
) -> dict[int, dict[str, list[int]]]:
    if plan.empty:
        return dict(existing or {})

    merged: dict[int, dict[str, list[int]]] = dict(existing or {})
    remaining = plan[~plan["id"].astype(int).isin(merged)].copy()
    if remaining.empty:
        _log("  toutes les fiches déjà présentes dans le checkpoint GPT", log)
        return merged
    if merged:
        _log(f"  reprise : {len(merged)} fiches déjà classées, {len(remaining)} restantes", log)

    n_batches = (len(remaining) + batch_size - 1) // batch_size
    for batch_idx, start in enumerate(range(0, len(remaining), batch_size), start=1):
        batch = remaining.iloc[start : start + batch_size]
        known_ids = set(batch["id"].astype(int))
        _log(
            f"  lot {batch_idx}/{n_batches} — {len(batch)} fiches "
            f"(ids {int(batch['id'].min())}–{int(batch['id'].max())})",
            log,
        )
        prompt = build_prompt_classification(build_plan_texte(batch))
        last_error: Exception | None = None
        for attempt in range(1, 4):
            try:
                data = _call_llm_json(
                    client,
                    prompt,
                    model=model,
                    reasoning_low=reasoning_low,
                    max_output_tokens=max_output_tokens,
                    max_retries=1,
                    log=log,
                )
                merged.update(validate_classification(data, known_ids, LEVIERS_SET))
                _write_gpt_checkpoint(checkpoint_path, merged)
                last_error = None
                break
            except (ValueError, RuntimeError) as e:
                last_error = e
                _log(f"  validation échouée, retry {attempt}/3: {e}", log)
        if last_error is not None:
            _write_gpt_checkpoint(checkpoint_path, merged)
            raise RuntimeError(f"Classification impossible pour le lot {batch_idx}: {last_error}")
    return merged


def classification_to_pairs(
    classification: dict[int, dict[str, list[int]]],
) -> dict[int, set[tuple[str, str]]]:
    """fiche_id -> {(levier_id, categorie_enum)}."""
    result: dict[int, set[tuple[str, str]]] = {}
    for fiche_id, leviers_map in classification.items():
        pairs: set[tuple[str, str]] = set()
        for label, cats in leviers_map.items():
            levier_id = LEVIER_LABEL_TO_ID.get(label)
            if levier_id is None:
                continue
            for cat in cats:
                pairs.add((levier_id, CATEGORIE_ID_TO_ENUM[cat]))
        result[int(fiche_id)] = pairs
    return result


def prod_df_to_pairs(df: pd.DataFrame) -> dict[int, set[tuple[str, str]]]:
    result: dict[int, set[tuple[str, str]]] = defaultdict(set)
    for _, row in df.iterrows():
        result[int(row["fiche_id"])].add((str(row["levier_id"]), str(row["categorie"])))
    return dict(result)


def format_pairs(pairs: set[tuple[str, str]]) -> str:
    if not pairs:
        return "(aucune)"
    parts = []
    for levier_id, categorie in sorted(pairs):
        label = LEVIER_ID_TO_LABEL.get(levier_id, levier_id)
        cat_id = CATEGORIE_ENUM_TO_ID.get(categorie)
        cat_label = CATEGORIES.get(cat_id, categorie) if cat_id else categorie
        parts.append(f"{label} × {cat_id or '?'} {cat_label}")
    return " | ".join(parts)


def _truncate(text_value: str, limit: int = 600) -> str:
    text_value = re.sub(r"\s+", " ", (text_value or "")).strip()
    if len(text_value) <= limit:
        return text_value
    return text_value[: limit - 1] + "…"


def compare_classifications(
    collectivite: dict[str, Any],
    fiches: pd.DataFrame,
    gpt: dict[int, dict[str, list[int]]],
    prod_df: pd.DataFrame,
) -> pd.DataFrame:
    gpt_pairs = classification_to_pairs(gpt)
    prod_pairs = prod_df_to_pairs(prod_df)
    fiche_ids = set(fiches["id"].astype(int)) | set(prod_pairs) | set(gpt_pairs)
    info = fiches.set_index("id") if not fiches.empty else pd.DataFrame()

    rows: list[dict[str, Any]] = []
    for fiche_id in sorted(fiche_ids):
        prod = prod_pairs.get(fiche_id, set())
        gpt_set = gpt_pairs.get(fiche_id, set())
        only_prod = prod - gpt_set
        only_gpt = gpt_set - prod
        if prod == gpt_set:
            if prod:
                type_diff = "accord"
            else:
                type_diff = "aucun_levier"
        elif not prod and gpt_set:
            type_diff = "seulement_gpt"
        elif prod and not gpt_set:
            type_diff = "seulement_prod"
        else:
            type_diff = "divergence"

        titre = ""
        description = ""
        dans_plan = None
        if fiche_id in info.index:
            titre = str(info.at[fiche_id, "titre"] or "")
            description = str(info.at[fiche_id, "description"] or "")
            dans_plan = bool(info.at[fiche_id, "dans_plan"]) if "dans_plan" in info.columns else None

        rows.append(
            {
                "collectivite_id": collectivite["id"],
                "collectivite_nom": collectivite["nom"],
                "fiche_id": fiche_id,
                "titre": titre,
                "description": description,
                "dans_plan": dans_plan,
                "type_diff": type_diff,
                "prod": format_pairs(prod),
                "gpt": format_pairs(gpt_set),
                "seulement_prod": format_pairs(only_prod) if only_prod else "",
                "seulement_gpt": format_pairs(only_gpt) if only_gpt else "",
                "n_paires_prod": len(prod),
                "n_paires_gpt": len(gpt_set),
                "n_paires_communes": len(prod & gpt_set),
            }
        )
    return pd.DataFrame(rows)


def write_rapport_markdown(df: pd.DataFrame, collectivite: dict[str, Any], path: Path) -> None:
    nom = collectivite["nom"]
    cid = collectivite["id"]
    counts = df["type_diff"].value_counts().to_dict()
    n = len(df)
    n_accord = int(counts.get("accord", 0) + counts.get("aucun_levier", 0))
    n_diff = n - n_accord

    lines = [
        f"# Vérification classification — {nom} ({cid})",
        "",
        f"Comparaison de `fiche_action_volet_ges` (prod, lecture seule) avec une reclassification GPT.",
        f"Prompt : `pages/26_run_impact.py` (classification levier × catégorie).",
        "",
        "## Synthèse",
        "",
        f"- Fiches comparées : **{n}**",
        f"- Accords (y compris aucun levier des deux côtés) : **{n_accord}**",
        f"- Différences : **{n_diff}**",
        f"- Accords stricts (mêmes paires) : **{counts.get('accord', 0)}**",
        f"- Aucun levier des deux côtés : **{counts.get('aucun_levier', 0)}**",
        f"- Seulement prod : **{counts.get('seulement_prod', 0)}**",
        f"- Seulement GPT : **{counts.get('seulement_gpt', 0)}**",
        f"- Divergences (paires différentes) : **{counts.get('divergence', 0)}**",
        "",
    ]

    order = ["divergence", "seulement_prod", "seulement_gpt", "accord", "aucun_levier"]
    titles = {
        "divergence": "Divergences (prod et GPT classent, mais pas pareil)",
        "seulement_prod": "Classées en prod, pas par GPT",
        "seulement_gpt": "Classées par GPT, absentes de la prod",
        "accord": "Accords",
        "aucun_levier": "Aucun levier (prod et GPT)",
    }

    for type_diff in order:
        subset = df[df["type_diff"] == type_diff]
        if subset.empty:
            continue
        lines.append(f"## {titles[type_diff]} ({len(subset)})")
        lines.append("")
        for _, row in subset.iterrows():
            lines.append(f"### Fiche {row['fiche_id']} — {row['titre'] or '(sans titre)'}")
            lines.append("")
            lines.append(f"- **Prod :** {row['prod']}")
            lines.append(f"- **GPT :** {row['gpt']}")
            if row["seulement_prod"]:
                lines.append(f"- **Seulement prod :** {row['seulement_prod']}")
            if row["seulement_gpt"]:
                lines.append(f"- **Seulement GPT :** {row['seulement_gpt']}")
            if row["dans_plan"] is False:
                lines.append("- Hors plan (pas d'axe) mais classée en prod.")
            description = _truncate(str(row["description"] or ""), 800)
            if description:
                lines.append("")
                lines.append(f"> {description}")
            lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def classification_to_jsonable(classification: dict[int, dict[str, list[int]]]) -> dict[str, Any]:
    return {
        str(fiche_id): leviers_map
        for fiche_id, leviers_map in sorted(classification.items())
    }


def run_verification(
    collectivite_ids: list[int],
    *,
    model: str = DEFAULT_MODEL,
    batch_size: int = 25,
    reasoning_low: bool = False,
    skip_llm: bool = False,
    limit: int | None = None,
    from_json: dict[int, Path] | None = None,
    resume: bool = False,
    output_dir: Path | None = None,
    log: LogFn | None = None,
) -> Path:
    secrets = load_secrets()
    engine = engine_prod_readonly(secrets)
    output_dir = output_dir or (
        OUTPUT_ROOT / datetime.now().strftime("%Y-%m-%d_%Hh%M")
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    client: OpenAI | None = None
    if not skip_llm:
        client = OpenAI(api_key=openai_api_key(secrets), timeout=600.0)

    synthese_rows: list[str] = [
        "# Synthèse vérification classification volet GES",
        "",
        "Lecture seule sur la prod. Aucune écriture en base.",
        f"Modèle : `{model}`",
        "",
    ]

    all_diffs: list[pd.DataFrame] = []

    for collectivite_id in collectivite_ids:
        collectivite = fetch_collectivite(engine, collectivite_id)
        _log(f"=== {collectivite['nom']} ({collectivite_id}) ===", log)

        fiches = fetch_fiches_a_classifier(engine, collectivite_id)
        if limit is not None:
            fiches = fiches.head(limit).copy()
            _log(f"Limite --limit {limit} appliquée", log)
        prod_df = fetch_classification_prod(engine, collectivite_id)
        if limit is not None and not prod_df.empty:
            keep_ids = set(fiches["id"].astype(int))
            prod_df = prod_df[prod_df["fiche_id"].isin(keep_ids)].copy()
        _log(
            f"{len(fiches)} fiches à classifier, "
            f"{prod_df['fiche_id'].nunique() if not prod_df.empty else 0} fiches déjà classées en prod "
            f"({len(prod_df)} lignes)",
            log,
        )

        fiches.to_csv(output_dir / f"{collectivite_id}_fiches.csv", index=False, encoding="utf-8")
        prod_df.to_csv(
            output_dir / f"{collectivite_id}_classification_prod.csv",
            index=False,
            encoding="utf-8",
        )

        gpt_path = output_dir / f"{collectivite_id}_classification_gpt.json"
        json_path = (from_json or {}).get(collectivite_id)
        if json_path is None and resume and gpt_path.exists():
            json_path = gpt_path

        gpt: dict[int, dict[str, list[int]]] = {}
        if json_path:
            _log(f"Reprise GPT depuis {json_path}", log)
            raw = json.loads(Path(json_path).read_text(encoding="utf-8"))
            gpt = {int(k): v for k, v in raw.items()}

        if skip_llm:
            for fid in fiches["id"].tolist():
                gpt.setdefault(int(fid), {})
            _log("skip-llm : pas d'appel GPT", log)
        else:
            assert client is not None
            gpt = classify_actions(
                fiches,
                client,
                model=model,
                batch_size=batch_size,
                reasoning_low=reasoning_low,
                existing=gpt,
                checkpoint_path=gpt_path,
                log=log,
            )

        _write_gpt_checkpoint(gpt_path, gpt)

        df_diff = compare_classifications(collectivite, fiches, gpt, prod_df)
        all_diffs.append(df_diff)
        csv_path = output_dir / f"{collectivite_id}_differences.csv"
        df_diff.to_csv(csv_path, index=False, encoding="utf-8")
        md_path = output_dir / f"{collectivite_id}_rapport.md"
        write_rapport_markdown(df_diff, collectivite, md_path)

        counts = df_diff["type_diff"].value_counts().to_dict()
        n_diff = int(
            counts.get("divergence", 0)
            + counts.get("seulement_prod", 0)
            + counts.get("seulement_gpt", 0)
        )
        synthese_rows.extend(
            [
                f"## {collectivite['nom']} ({collectivite_id})",
                "",
                f"- Fiches comparées : {len(df_diff)}",
                f"- Accords : {counts.get('accord', 0)}",
                f"- Aucun levier : {counts.get('aucun_levier', 0)}",
                f"- Divergences : {counts.get('divergence', 0)}",
                f"- Seulement prod : {counts.get('seulement_prod', 0)}",
                f"- Seulement GPT : {counts.get('seulement_gpt', 0)}",
                f"- **Différences à relire : {n_diff}**",
                f"- Rapport : `{md_path.name}`",
                "",
            ]
        )
        _log(f"Rapport : {md_path}", log)

    if all_diffs:
        pd.concat(all_diffs, ignore_index=True).to_csv(
            output_dir / "differences.csv", index=False, encoding="utf-8"
        )
    (output_dir / "synthese.md").write_text("\n".join(synthese_rows), encoding="utf-8")
    _log(f"Sortie : {output_dir}", log)
    return output_dir
