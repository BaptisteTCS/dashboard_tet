"""Helpers pour le test de variance du prompt d'implication (page 44).

Copie volontaire du prompt / validation / override de pages/26_run_impact.py
pour ne pas importer cette page (elle exécute l'UI au chargement).
"""

from __future__ import annotations

import json
import random
import statistics
import time
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st
from openai import OpenAI
from sqlalchemy import text

from utils.db import get_engine_prod
from utils.priorisation_data import load_priorisation
from utils.priorisation_text import parse_ids

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "test_run_impact"
MODEL = "gpt-5.6-terra"
VALID_CATEGORIES = {1, 2, 3, 4, 5, 6}
FLEX_TIMEOUT_S = 900.0
DEFAULT_INPUT_PER_CALL = 6300
DEFAULT_OUTPUT_PER_CALL = 1200
PRICE_INPUT_PER_M = 2.00
PRICE_CACHED_PER_M = 0.20
PRICE_CACHE_WRITE_PER_M = 2.50
PRICE_OUTPUT_PER_M = 12.00

CATEGORIES = {
    1: "Aménagement & infrastructures",
    2: "Réglementation & planification",
    3: "Financement & fiscalité",
    4: "Gouvernance & partenariats",
    5: "Exemplarité interne",
    6: "Sensibilisation & accompagnement",
}

CATEGORIES_SHORT = {
    1: "Aménagement",
    2: "Planification",
    3: "Financement",
    4: "Gouvernance",
    5: "Exemplarité",
    6: "Sensibilisation",
}


# ==========================
# Prompt / LLM (copie 26)
# ==========================


def build_prompt_implication_prefix(
    references_par_categorie: str | None = None,
) -> str:
    """Préfixe stable (instructions) — candidat au cache entre leviers."""
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
"""


def build_prompt_implication_suffix(
    actions_par_categorie: str,
    levier: str,
    collectivite_nom: str,
    population: int,
) -> str:
    """Suffixe variable (collectivité + levier + actions)."""
    return f"""# Entrées
Collectivité : {collectivite_nom}
Population : {population}
Levier évalué : {levier}

Actions de la collectivité, regroupées par catégorie :
{actions_par_categorie}
"""


def build_prompt_implication(
    actions_par_categorie: str,
    levier: str,
    collectivite_nom: str,
    population: int,
    references_par_categorie: str | None = None,
) -> str:
    """Construit le prompt pour évaluer l'activation d'un levier, catégorie par catégorie."""
    return (
        build_prompt_implication_prefix(references_par_categorie)
        + "\n"
        + build_prompt_implication_suffix(
            actions_par_categorie,
            levier,
            collectivite_nom,
            population,
        )
    )


def strip_json_fences(text: str) -> str:
    """Enlève les ```json ... ``` si présents."""
    if not text:
        return ""
    t = text.strip()
    if t.startswith("```"):
        t = t.replace("```json", "").replace("```JSON", "").replace("```", "").strip()
    return t


def _status_write(status_container, msg: str) -> None:
    if status_container is not None and hasattr(status_container, "write"):
        status_container.write(msg)


def empty_usage() -> dict[str, int]:
    return {
        "input_tokens": 0,
        "output_tokens": 0,
        "total_tokens": 0,
        "cached_tokens": 0,
        "cache_write_tokens": 0,
    }


def _detail_int(details: Any, name: str) -> int:
    if details is None:
        return 0
    if isinstance(details, dict):
        return int(details.get(name, 0) or 0)
    return int(getattr(details, name, 0) or 0)


def extract_usage(response: Any) -> dict[str, int]:
    """Lit tokens (dont cache) depuis une réponse OpenAI Responses API."""
    usage = getattr(response, "usage", None)
    if usage is None:
        return empty_usage()
    if isinstance(usage, dict):
        input_tokens = int(usage.get("input_tokens", 0) or 0)
        output_tokens = int(usage.get("output_tokens", 0) or 0)
        total_tokens = int(usage.get("total_tokens", 0) or (input_tokens + output_tokens))
        details = usage.get("input_tokens_details")
    else:
        input_tokens = int(getattr(usage, "input_tokens", 0) or 0)
        output_tokens = int(getattr(usage, "output_tokens", 0) or 0)
        total_tokens = int(
            getattr(usage, "total_tokens", 0) or (input_tokens + output_tokens)
        )
        details = getattr(usage, "input_tokens_details", None)
    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "cached_tokens": _detail_int(details, "cached_tokens"),
        "cache_write_tokens": _detail_int(details, "cache_write_tokens"),
    }


def add_usage(left: dict[str, int], right: dict[str, int] | None) -> dict[str, int]:
    right = right or empty_usage()
    keys = (
        "input_tokens",
        "output_tokens",
        "total_tokens",
        "cached_tokens",
        "cache_write_tokens",
    )
    return {key: int(left.get(key, 0) or 0) + int(right.get(key, 0) or 0) for key in keys}


def payload_is_flex(payload: dict[str, Any] | None) -> bool:
    if not payload:
        return False
    return str(payload.get("meta", {}).get("service_tier", "")).lower() == "flex"


def token_prices_per_million(flex: bool) -> dict[str, float]:
    factor = 0.5 if flex else 1.0
    return {
        "input": PRICE_INPUT_PER_M * factor,
        "cached": PRICE_CACHED_PER_M * factor,
        "cache_write": PRICE_CACHE_WRITE_PER_M * factor,
        "output": PRICE_OUTPUT_PER_M * factor,
    }


def uncached_input_tokens(usage: dict[str, int] | None) -> int:
    usage = usage or empty_usage()
    input_tokens = int(usage.get("input_tokens", 0) or 0)
    cached = int(usage.get("cached_tokens", 0) or 0)
    writes = int(usage.get("cache_write_tokens", 0) or 0)
    return max(0, input_tokens - cached - writes)


def usage_cost_usd(usage: dict[str, int] | None, flex: bool) -> float:
    usage = usage or empty_usage()
    prices = token_prices_per_million(flex)
    return (
        uncached_input_tokens(usage) * prices["input"]
        + int(usage.get("cached_tokens", 0) or 0) * prices["cached"]
        + int(usage.get("cache_write_tokens", 0) or 0) * prices["cache_write"]
        + int(usage.get("output_tokens", 0) or 0) * prices["output"]
    ) / 1_000_000


def format_usd(amount: float) -> str:
    if amount < 0.01:
        return f"{amount:.4f} $"
    return f"{amount:.2f} $"


def format_usage_cost_line(
    usage: dict[str, int] | None,
    *,
    call_cost: float | None = None,
    total_cost: float | None = None,
) -> str:
    usage = usage or empty_usage()
    cached = int(usage.get("cached_tokens", 0) or 0)
    writes = int(usage.get("cache_write_tokens", 0) or 0)
    hit = cache_hit_pct(usage)
    hit_s = f"{hit:.0f} %" if hit is not None else "—"
    parts = [
        (
            f"Tokens — entrée {int(usage.get('input_tokens', 0)):,} "
            f"(cached {cached:,} / write {writes:,} / hit {hit_s}) "
            f"/ sortie {int(usage.get('output_tokens', 0)):,}"
        )
    ]
    if call_cost is not None:
        parts.append(f"appel {format_usd(call_cost)}")
    if total_cost is not None:
        parts.append(f"cumulé {format_usd(total_cost)}")
    return " — ".join(parts)


def cache_hit_pct(usage: dict[str, int] | None) -> float | None:
    usage = usage or empty_usage()
    input_tokens = int(usage.get("input_tokens", 0) or 0)
    if input_tokens <= 0:
        return None
    return int(usage.get("cached_tokens", 0) or 0) / input_tokens * 100


def estimate_run_costs(
    n_leviers: int,
    n_runs: int,
    avg_input: int,
    avg_output: int,
) -> dict[str, float | int]:
    """Estime le coût d'un run complet (1 écriture cache par levier, le reste en cached)."""
    n_calls = n_leviers * n_runs
    n_writes = n_leviers
    n_cached = max(0, n_calls - n_writes)

    def _cost(flex: bool, cached: bool) -> float:
        prices = token_prices_per_million(flex)
        if not cached:
            return (
                n_calls * avg_input * prices["input"]
                + n_calls * avg_output * prices["output"]
            ) / 1_000_000
        return (
            n_writes * avg_input * prices["cache_write"]
            + n_cached * avg_input * prices["cached"]
            + n_calls * avg_output * prices["output"]
        ) / 1_000_000

    return {
        "n_calls": n_calls,
        "avg_input": avg_input,
        "avg_output": avg_output,
        "standard": _cost(False, False),
        "cache": _cost(False, True),
        "flex_cache": _cost(True, True),
    }


def _is_unavailable(exc: Exception) -> bool:
    code = getattr(exc, "status_code", None)
    if code == 429:
        return True
    text = str(exc).lower()
    return "resource unavailable" in text or "429" in text


def _responses_input(prefix: str, suffix: str) -> list[dict[str, Any]]:
    return [
        {
            "type": "message",
            "role": "developer",
            "content": [
                {
                    "type": "input_text",
                    "text": prefix,
                    "prompt_cache_breakpoint": {"mode": "explicit"},
                }
            ],
        },
        {
            "type": "message",
            "role": "user",
            "content": [{"type": "input_text", "text": suffix}],
        },
    ]


def _create_response(
    client: OpenAI,
    kwargs: dict[str, Any],
    use_flex: bool,
    status_container,
    label: str,
) -> Any:
    """Crée une réponse, avec retry Flex 429 puis repli standard."""
    flex_now = use_flex
    last_exc: Exception | None = None
    body = dict(kwargs)
    api = client.with_options(timeout=FLEX_TIMEOUT_S)
    for attempt in range(1, 4):
        if flex_now:
            body["service_tier"] = "flex"
        else:
            body.pop("service_tier", None)
        while True:
            try:
                return api.responses.create(**body)
            except TypeError:
                stripped = False
                for key in (
                    "text",
                    "prompt_cache_options",
                    "prompt_cache_key",
                    "service_tier",
                ):
                    if key in body:
                        body.pop(key, None)
                        stripped = True
                        break
                if stripped:
                    continue
                raise
            except Exception as e:
                last_exc = e
                if not _is_unavailable(e) or attempt == 3:
                    raise
                wait = min(2**attempt, 16)
                _status_write(
                    status_container,
                    f"Flex/API saturé (429) pour {label}, retry {attempt}/3 dans {wait}s…",
                )
                time.sleep(wait)
                if attempt >= 2 and flex_now:
                    flex_now = False
                    _status_write(
                        status_container,
                        "Basculer en standard pour le dernier essai (Flex saturé).",
                    )
                break
    raise last_exc or RuntimeError(f"Échec LLM ({label})")


def call_llm_json(
    client: OpenAI,
    prefix: str,
    suffix: str,
    label: str,
    status_container,
    reasoning_low: bool,
    prompt_cache_key: str,
    use_flex: bool = True,
    max_retries: int = 3,
    max_output_tokens: int | None = None,
) -> tuple[Any, dict[str, int]]:
    """Appelle le LLM avec cache + Flex, sortie JSON forcée, retry en cas d'échec."""
    last_error = None
    usage_acc = empty_usage()

    for attempt in range(1, max_retries + 1):
        try:
            if attempt > 1:
                _status_write(
                    status_container,
                    f"Retry {attempt}/{max_retries} ({label})...",
                )

            kwargs: dict[str, Any] = {
                "model": MODEL,
                "input": _responses_input(prefix, suffix),
                "reasoning": {"effort": "low" if reasoning_low else "medium"},
                "text": {"format": {"type": "json_object"}},
                "prompt_cache_key": prompt_cache_key,
                "prompt_cache_options": {"mode": "implicit", "ttl": "30m"},
            }
            if max_output_tokens:
                kwargs["max_output_tokens"] = max_output_tokens

            response = _create_response(
                client, kwargs, use_flex, status_container, label
            )
            usage_acc = add_usage(usage_acc, extract_usage(response))
            raw_text = strip_json_fences(response.output_text or "")
            return json.loads(raw_text), usage_acc
        except json.JSONDecodeError as e:
            last_error = f"json_parse_error: {e}"
        except Exception as e:
            last_error = f"generation_error: {type(e).__name__}: {e}"

    raise RuntimeError(
        f"Échec LLM ({label}) après {max_retries} tentatives: {last_error}"
    )


def validate_activation_scores(data: Any) -> dict[int, int]:
    """Valide et normalise la sortie JSON de l'étape implication."""
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


def apply_empty_category_override(
    scores: dict[int, int],
    actions_by_cat: dict[int, list[int]],
) -> dict[int, int]:
    """Force la note à 0 pour les catégories sans action rattachée."""
    result = dict(scores)
    for cat in range(1, 7):
        if not actions_by_cat.get(cat, []):
            result[cat] = 0
    return result


def build_actions_text(plan: pd.DataFrame, ids: list[int]) -> str:
    """Construit un texte d'actions pour une liste d'ids."""
    if not ids:
        return ""

    known = set(plan["id"].astype(int)) if not plan.empty else set()
    lines: list[str] = []
    plan_by_id = (
        {int(row.id): row for _, row in plan.iterrows()} if not plan.empty else {}
    )

    for action_id in ids:
        if action_id in known:
            row = plan_by_id[action_id]
            titre = "" if pd.isna(row.titre) else str(row.titre)
            description = "" if pd.isna(row.description) else str(row.description)
            lines.append(f"{action_id} | {titre} : {description}".strip())
        else:
            lines.append(f"{action_id} | (fiche introuvable)")

    return "\n\n".join(lines).strip()


def format_actions_by_category(
    plan: pd.DataFrame,
    actions_by_cat: dict[int, list[int]],
) -> str:
    """Formate les actions regroupées par catégorie pour le prompt."""
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


def score_one_lever(
    client: OpenAI,
    plan: pd.DataFrame,
    levier: str,
    actions_by_cat: dict[int, list[int]],
    collectivite_nom: str,
    population: int,
    status_container,
    reasoning_low: bool,
    prompt_cache_key: str,
    use_flex: bool = True,
) -> tuple[dict[int, int], dict[str, int]]:
    """Note un levier (6 catégories) avec cache prefix/suffix et Flex optionnel."""
    actions_par_categorie = format_actions_by_category(plan, actions_by_cat)
    prefix = build_prompt_implication_prefix()
    suffix = build_prompt_implication_suffix(
        actions_par_categorie,
        levier,
        collectivite_nom,
        population,
    )
    usage_acc = empty_usage()

    for attempt in range(1, 4):
        try:
            data, usage = call_llm_json(
                client,
                prefix,
                suffix,
                f"activation_{levier}",
                status_container,
                reasoning_low=reasoning_low,
                prompt_cache_key=prompt_cache_key,
                use_flex=use_flex,
                max_retries=1,
            )
            usage_acc = add_usage(usage_acc, usage)
            scores = validate_activation_scores(data)
            return apply_empty_category_override(scores, actions_by_cat), usage_acc
        except (ValueError, RuntimeError) as e:
            if attempt == 3:
                raise RuntimeError(f"Notation impossible pour « {levier} »: {e}") from e
            _status_write(
                status_container,
                f"Validation échouée, retry {attempt + 1}/3: {e}",
            )

    raise RuntimeError(f"Notation impossible pour « {levier} »")


def score_one_lever_mock(
    actions_by_cat: dict[int, list[int]],
) -> tuple[dict[int, int], dict[str, int]]:
    """Version mock — notes aléatoires 0-3, override catégories vides."""
    scores = {cat: random.randint(0, 3) for cat in range(1, 7)}
    return apply_empty_category_override(scores, actions_by_cat), empty_usage()


# ==========================
# Données OLAP / prod
# ==========================


@st.cache_data(ttl="1h")
def load_collectivite_prod(collectivite_id: int) -> dict[str, Any]:
    """Nom et population depuis la base prod (lecture seule)."""
    engine = get_engine_prod()
    with engine.connect() as conn:
        df = pd.read_sql_query(
            text(
                """
                SELECT id, nom, population
                FROM collectivite
                WHERE id = :id
                """
            ),
            conn,
            params={"id": collectivite_id},
        )
    if df.empty:
        raise ValueError(f"Collectivité {collectivite_id} introuvable en prod")
    row = df.iloc[0]
    population = int(row["population"]) if pd.notna(row["population"]) else 0
    return {
        "id": int(row["id"]),
        "nom": str(row["nom"]) if pd.notna(row["nom"]) else "",
        "population": population,
    }


def load_fiches_by_ids(ids: list[int]) -> pd.DataFrame:
    """Fiches action prod pour les ids classifiés."""
    return _load_fiches_by_ids_cached(tuple(int(i) for i in ids))


@st.cache_data(ttl="1h")
def _load_fiches_by_ids_cached(ids: tuple[int, ...]) -> pd.DataFrame:
    if not ids:
        return pd.DataFrame(columns=["id", "titre", "description"])
    engine = get_engine_prod()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text(
                """
                SELECT id, titre, description
                FROM fiche_action
                WHERE id = ANY(:ids)
                """
            ),
            conn,
            params={"ids": list(ids)},
        )


def rebuild_classification(
    df_priorisation: pd.DataFrame,
) -> tuple[dict[str, dict[int, list[int]]], dict[tuple[str, int], int]]:
    """Reconstruit levier → catégorie → ids, et les notes OLAP de référence."""
    grouped: dict[str, dict[int, list[int]]] = defaultdict(
        lambda: {cat: [] for cat in range(1, 7)}
    )
    olap_notes: dict[tuple[str, int], int] = {}

    for _, row in df_priorisation.iterrows():
        levier = str(row["levier"])
        cat = int(row["categorie"])
        if cat not in VALID_CATEGORIES:
            continue
        ids = parse_ids(row["ids"])
        grouped[levier][cat] = ids
        note = int(row["note"]) if pd.notna(row["note"]) else 0
        olap_notes[(levier, cat)] = note

    lever_category_actions: dict[str, dict[int, list[int]]] = {}
    for levier, cats in grouped.items():
        if any(cats[c] for c in range(1, 7)):
            lever_category_actions[levier] = {
                cat: list(cats[cat]) for cat in range(1, 7)
            }

    return lever_category_actions, olap_notes


def count_volets_with_actions(
    lever_category_actions: dict[str, dict[int, list[int]]],
) -> int:
    return sum(
        1
        for cats in lever_category_actions.values()
        for ids in cats.values()
        if ids
    )


def collect_action_ids(
    lever_category_actions: dict[str, dict[int, list[int]]],
) -> list[int]:
    seen: set[int] = set()
    ordered: list[int] = []
    for cats in lever_category_actions.values():
        for ids in cats.values():
            for action_id in ids:
                if action_id not in seen:
                    seen.add(action_id)
                    ordered.append(action_id)
    return ordered


def load_run_inputs(collectivite_id: int) -> dict[str, Any]:
    """Charge classification OLAP, notes, fiches et infos collectivité."""
    info = load_collectivite_prod(collectivite_id)
    df_priorisation = load_priorisation(collectivite_id)
    if df_priorisation.empty:
        raise ValueError("Aucune classification trouvée en OLAP pour cette collectivité")

    lever_category_actions, olap_notes = rebuild_classification(df_priorisation)
    if not lever_category_actions:
        raise ValueError("Aucun levier avec des actions classifiées")

    action_ids = collect_action_ids(lever_category_actions)
    plan = load_fiches_by_ids(action_ids)
    return {
        "collectivite_id": collectivite_id,
        "collectivite_nom": info["nom"],
        "population": info["population"],
        "lever_category_actions": lever_category_actions,
        "olap_notes": olap_notes,
        "plan": plan,
        "n_leviers": len(lever_category_actions),
        "n_volets": count_volets_with_actions(lever_category_actions),
        "n_actions": len(action_ids),
    }


# ==========================
# JSON checkpoint
# ==========================


def classification_to_json(
    lever_category_actions: dict[str, dict[int, list[int]]],
) -> dict[str, dict[str, list[int]]]:
    return {
        levier: {str(cat): ids for cat, ids in cats.items()}
        for levier, cats in lever_category_actions.items()
    }


def classification_from_json(
    raw: dict[str, dict[str, list[int]]],
) -> dict[str, dict[int, list[int]]]:
    return {
        levier: {int(cat): [int(i) for i in ids] for cat, ids in cats.items()}
        for levier, cats in raw.items()
    }


def olap_notes_to_json(
    olap_notes: dict[tuple[str, int], int],
) -> dict[str, dict[str, int]]:
    nested: dict[str, dict[str, int]] = defaultdict(dict)
    for (levier, cat), note in olap_notes.items():
        nested[levier][str(cat)] = note
    return dict(nested)


def olap_notes_from_json(
    raw: dict[str, dict[str, int]],
) -> dict[tuple[str, int], int]:
    result: dict[tuple[str, int], int] = {}
    for levier, cats in raw.items():
        for cat, note in cats.items():
            result[(levier, int(cat))] = int(note)
    return result


def new_run_path(collectivite_id: int) -> Path:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return DATA_DIR / f"{collectivite_id}_{ts}.json"


def save_payload(path: Path, payload: dict[str, Any]) -> None:
    """Écriture atomique (temp + replace) pour ne pas corrompre le JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload["meta"]["updated_at"] = datetime.now().isoformat(timespec="seconds")
    tmp = path.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    tmp.replace(path)


def load_payload(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def init_payload(
    inputs: dict[str, Any],
    n_runs: int,
    reasoning_low: bool,
    debug: bool,
    use_flex: bool = True,
) -> dict[str, Any]:
    now = datetime.now().isoformat(timespec="seconds")
    return {
        "meta": {
            "collectivite_id": inputs["collectivite_id"],
            "collectivite_nom": inputs["collectivite_nom"],
            "population": inputs["population"],
            "model": MODEL,
            "reasoning": "low" if reasoning_low else "medium",
            "service_tier": "flex" if use_flex else "standard",
            "prompt_cache_key": f"test-run-impact:{inputs['collectivite_id']}",
            "n_runs": n_runs,
            "debug": debug,
            "started_at": now,
            "updated_at": now,
            "status": "running",
            "tokens": empty_usage(),
            "cost_usd": 0.0,
        },
        "classification": classification_to_json(inputs["lever_category_actions"]),
        "olap_notes": olap_notes_to_json(inputs["olap_notes"]),
        "results": [],
    }


def completed_pairs(payload: dict[str, Any]) -> set[tuple[int, str]]:
    return {
        (int(row["run"]), str(row["levier"]))
        for row in payload.get("results", [])
    }


def pending_work(payload: dict[str, Any]) -> list[tuple[int, str]]:
    """Levier d'abord, puis run : N appels identiques se suivent pour le cache."""
    n_runs = int(payload["meta"]["n_runs"])
    leviers = list(payload.get("classification", {}).keys())
    done = completed_pairs(payload)
    pending: list[tuple[int, str]] = []
    for levier in leviers:
        for run in range(1, n_runs + 1):
            if (run, levier) not in done:
                pending.append((run, levier))
    return pending


def append_result(
    payload: dict[str, Any],
    run: int,
    levier: str,
    scores: dict[int, int],
    usage: dict[str, int] | None = None,
) -> None:
    usage = add_usage(empty_usage(), usage)
    flex = payload_is_flex(payload)
    cost = usage_cost_usd(usage, flex)
    payload["results"].append(
        {
            "run": run,
            "levier": levier,
            "scores": {str(cat): scores[cat] for cat in range(1, 7)},
            "usage": usage,
            "cost_usd": cost,
            "at": datetime.now().isoformat(timespec="seconds"),
        }
    )
    meta = payload.setdefault("meta", {})
    meta["tokens"] = add_usage(meta.get("tokens") or empty_usage(), usage)
    meta["cost_usd"] = float(meta.get("cost_usd") or 0) + cost


def payload_token_totals(payload: dict[str, Any]) -> dict[str, int]:
    """Totaux tokens : meta si présent, sinon somme des résultats (JSON anciens)."""
    meta_tokens = payload.get("meta", {}).get("tokens")
    if meta_tokens and int(meta_tokens.get("total_tokens", 0) or 0) > 0:
        return add_usage(empty_usage(), meta_tokens)
    acc = empty_usage()
    for row in payload.get("results", []):
        acc = add_usage(acc, row.get("usage"))
    return acc


def payload_cost_usd(payload: dict[str, Any]) -> float:
    meta_cost = payload.get("meta", {}).get("cost_usd")
    if meta_cost is not None:
        return float(meta_cost)
    flex = payload_is_flex(payload)
    return sum(
        usage_cost_usd(row.get("usage"), flex) for row in payload.get("results", [])
    )


def typical_tokens_per_call(collectivite_id: int | None = None) -> tuple[int, int]:
    """Moyenne observée sur les JSON existants, sinon heuristique."""
    inputs: list[int] = []
    outputs: list[int] = []
    for path in list_run_files(collectivite_id)[:15]:
        try:
            payload = load_payload(path)
        except (json.JSONDecodeError, OSError):
            continue
        for row in payload.get("results", []):
            usage = row.get("usage") or {}
            inp = int(usage.get("input_tokens", 0) or 0)
            if inp <= 0:
                continue
            inputs.append(inp)
            outputs.append(int(usage.get("output_tokens", 0) or 0))
    if inputs:
        return int(statistics.mean(inputs)), int(statistics.mean(outputs))
    return DEFAULT_INPUT_PER_CALL, DEFAULT_OUTPUT_PER_CALL


def list_run_files(collectivite_id: int | None = None) -> list[Path]:
    if not DATA_DIR.exists():
        return []
    files = sorted(DATA_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    if collectivite_id is None:
        return files
    prefix = f"{collectivite_id}_"
    return [p for p in files if p.name.startswith(prefix)]


def find_incomplete_runs(collectivite_id: int) -> list[Path]:
    incomplete: list[Path] = []
    for path in list_run_files(collectivite_id):
        try:
            payload = load_payload(path)
        except (json.JSONDecodeError, OSError):
            continue
        status = payload.get("meta", {}).get("status")
        if status != "complete" and pending_work(payload):
            incomplete.append(path)
    return incomplete


def file_label(path: Path) -> str:
    try:
        payload = load_payload(path)
        meta = payload.get("meta", {})
        nom = meta.get("collectivite_nom", "?")
        status = meta.get("status", "?")
        n_runs = meta.get("n_runs", "?")
        n_results = len(payload.get("results", []))
        started = meta.get("started_at", "")
        return f"{nom} — {started} — {status} — {n_results} résultats / {n_runs} runs — {path.name}"
    except (json.JSONDecodeError, OSError):
        return f"{path.name} (illisible)"


# ==========================
# Stats
# ==========================


def _mean_or_none(values: list[float]) -> float | None:
    if not values:
        return None
    return float(statistics.mean(values))


def compute_stats(
    payload: dict[str, Any],
    accord_cutoff: float = 100.0,
) -> dict[str, Any]:
    """Calcule les indicateurs de variance à partir d'un JSON de run.

    Un volet n'est instable que s'il a au moins 2 notes distinctes ET un
    accord majoritaire strictement inférieur à ``accord_cutoff`` (0–100).
    """
    classification = classification_from_json(payload.get("classification", {}))
    olap_notes = olap_notes_from_json(payload.get("olap_notes", {}))
    n_runs_expected = int(payload.get("meta", {}).get("n_runs", 0))
    pending = pending_work(payload)
    incomplete = bool(pending) or payload.get("meta", {}).get("status") != "complete"

    scores_by_volet: dict[tuple[str, int], list[int]] = {}
    for levier, cats in classification.items():
        for cat, ids in cats.items():
            if ids:
                scores_by_volet[(levier, cat)] = []

    for row in payload.get("results", []):
        levier = str(row["levier"])
        scores = {int(k): int(v) for k, v in row.get("scores", {}).items()}
        for cat in range(1, 7):
            key = (levier, cat)
            if key in scores_by_volet and cat in scores:
                scores_by_volet[key].append(scores[cat])

    volet_rows: list[dict[str, Any]] = []
    for (levier, cat), notes in scores_by_volet.items():
        n = len(notes)
        ids = classification.get(levier, {}).get(cat, [])
        counts = Counter(notes)
        n_distinct = len(set(notes)) if notes else 0
        mode_note = counts.most_common(1)[0][0] if notes else None
        accord = (counts[mode_note] / n * 100) if n and mode_note is not None else None
        vmin = min(notes) if notes else None
        vmax = max(notes) if notes else None
        etendue = (vmax - vmin) if vmin is not None and vmax is not None else None
        moyenne = float(statistics.mean(notes)) if notes else None
        variance = float(statistics.variance(notes)) if n >= 2 else None
        stdev = float(statistics.stdev(notes)) if n >= 2 else None
        olap_note = olap_notes.get((levier, cat))
        volet_rows.append(
            {
                "levier": levier,
                "categorie": cat,
                "categorie_libelle": CATEGORIES_SHORT[cat],
                "nb_actions": len(ids),
                "nb_runs": n,
                "scores": notes,
                "scores_str": ", ".join(str(s) for s in notes),
                "effectifs": ", ".join(
                    f"{k}:{counts[k]}" for k in sorted(counts)
                ),
                "mode": mode_note,
                "n_distinct": n_distinct,
                "min": vmin,
                "max": vmax,
                "etendue": etendue,
                "moyenne": moyenne,
                "variance": variance,
                "stdev": stdev,
                "accord_pct": accord,
                "instable": bool(
                    n_distinct > 1
                    and (accord is None or accord < accord_cutoff)
                ),
                "note_olap": olap_note,
                "mode_eq_olap": (
                    mode_note == olap_note
                    if mode_note is not None and olap_note is not None
                    else None
                ),
                "ecart_olap": (
                    abs(mode_note - olap_note)
                    if mode_note is not None and olap_note is not None
                    else None
                ),
            }
        )

    df_volets = pd.DataFrame(volet_rows)
    if df_volets.empty:
        empty = pd.DataFrame()
        return {
            "incomplete": incomplete,
            "n_runs_expected": n_runs_expected,
            "n_pending": len(pending),
            "n_leviers": len(classification),
            "n_volets": 0,
            "n_unstable": 0,
            "pct_unstable": None,
            "pct_stable": None,
            "mean_variance_global": None,
            "mean_stdev_global": None,
            "max_range": None,
            "max_range_row": None,
            "df_volets": empty,
            "df_unstable": empty,
            "df_leviers": empty,
            "df_heatmap": empty,
            "olap_match_rate": None,
            "olap_mean_abs_diff": None,
            "n_comparable": 0,
        }

    usable = df_volets[df_volets["nb_runs"] >= 2]
    n_volets = len(df_volets)
    n_unstable = int(usable["instable"].sum()) if not usable.empty else 0
    n_stable = int((usable["n_distinct"] == 1).sum()) if not usable.empty else 0
    n_usable = len(usable)

    variances = [v for v in usable["variance"].tolist() if v is not None]
    stdevs = [v for v in usable["stdev"].tolist() if v is not None]

    max_range_row = None
    max_range = None
    if not usable.empty and usable["etendue"].notna().any():
        idx = usable.sort_values(
            ["etendue", "n_distinct", "variance"],
            ascending=False,
        ).index[0]
        max_range_row = df_volets.loc[idx].to_dict()
        max_range = int(max_range_row["etendue"])

    df_unstable = (
        usable[usable["instable"]]
        .sort_values(["n_distinct", "etendue", "variance"], ascending=False)
        .reset_index(drop=True)
        if not usable.empty
        else pd.DataFrame()
    )

    levier_rows: list[dict[str, Any]] = []
    for levier, grp in df_volets.groupby("levier", sort=False):
        grp_usable = grp[grp["nb_runs"] >= 2]
        levier_vars = [v for v in grp_usable["variance"].tolist() if v is not None]
        levier_rows.append(
            {
                "levier": levier,
                "nb_volets": len(grp),
                "nb_instables": int(grp_usable["instable"].sum()) if not grp_usable.empty else 0,
                "variance_moyenne": _mean_or_none(levier_vars),
                "stdev_moyen": _mean_or_none(
                    [v for v in grp_usable["stdev"].tolist() if v is not None]
                ),
                "etendue_max": (
                    int(grp_usable["etendue"].max())
                    if not grp_usable.empty and grp_usable["etendue"].notna().any()
                    else 0
                ),
                "accord_moyen_pct": _mean_or_none(
                    [v for v in grp_usable["accord_pct"].tolist() if v is not None]
                ),
            }
        )
    df_leviers = pd.DataFrame(levier_rows)
    if not df_leviers.empty:
        df_leviers = df_leviers.sort_values(
            ["nb_instables", "variance_moyenne", "etendue_max"],
            ascending=False,
            na_position="last",
        ).reset_index(drop=True)

    heat = df_volets.pivot_table(
        index="levier",
        columns="categorie_libelle",
        values="etendue",
        aggfunc="first",
    )
    ordered_cols = [
        CATEGORIES_SHORT[c]
        for c in range(1, 7)
        if CATEGORIES_SHORT[c] in heat.columns
    ]
    df_heatmap = heat.reindex(columns=ordered_cols)

    comparable = df_volets[df_volets["mode_eq_olap"].notna()]
    n_comparable = len(comparable)
    olap_match_rate = (
        float(comparable["mode_eq_olap"].mean() * 100) if n_comparable else None
    )
    olap_mean_abs_diff = (
        float(comparable["ecart_olap"].mean()) if n_comparable else None
    )

    return {
        "incomplete": incomplete,
        "n_runs_expected": n_runs_expected,
        "n_pending": len(pending),
        "n_leviers": len(classification),
        "n_volets": n_volets,
        "n_unstable": n_unstable,
        "n_stable": n_stable,
        "n_usable": n_usable,
        "pct_unstable": (n_unstable / n_usable * 100) if n_usable else None,
        "pct_stable": (n_stable / n_usable * 100) if n_usable else None,
        "mean_variance_global": _mean_or_none(variances),
        "mean_stdev_global": _mean_or_none(stdevs),
        "mean_variance_per_levier": _mean_or_none(
            [v for v in df_leviers["variance_moyenne"].tolist() if v is not None]
            if not df_leviers.empty
            else []
        ),
        "max_range": max_range,
        "max_range_row": max_range_row,
        "df_volets": df_volets.sort_values(
            ["n_distinct", "etendue", "variance"],
            ascending=False,
            na_position="last",
        ).reset_index(drop=True),
        "df_unstable": df_unstable,
        "df_leviers": df_leviers,
        "df_heatmap": df_heatmap,
        "olap_match_rate": olap_match_rate,
        "olap_mean_abs_diff": olap_mean_abs_diff,
        "n_comparable": n_comparable,
    }


def pause_between_calls(debug: bool) -> None:
    time.sleep(0.05 if debug else 0.2)
