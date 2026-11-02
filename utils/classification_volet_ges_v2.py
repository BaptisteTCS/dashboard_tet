"""Classification volet GES, prompt v2 : une fiche par appel, codes de leviers, JSON contraint.

Le prompt système est dans prompts/classification_volet_ges_v2.md. Il est envoyé tel quel
en premier, pour être mis en cache d'un appel à l'autre ; seule la fiche (message
utilisateur) change.

Modèles pris en charge (voir MODELS) :
- Mistral (mistral-large-4, mistral-small-2603) : chat/completions compatible OpenAI,
  JSON contraint par `response_format=json_schema`, cache automatique ;
- Claude (claude-haiku-5-5) : SDK Anthropic, réponse forcée via un outil dont le schéma
  est celui du JSON attendu, cache explicite (`cache_control`) sur le prompt système.

Lecture seule : ce module n'écrit rien en base.
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any

import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

from utils.verify_classification_volet_ges import (
    LEVIER_ID_TO_LABEL,
    VALID_CATEGORIES,
    strip_json_fences,
)

ROOT = Path(__file__).resolve().parent.parent
PROMPT_PATH = ROOT / "prompts" / "classification_volet_ges_v2.md"
MISTRAL_BASE_URL = "https://api.mistral.ai/v1"
MAX_LEVIERS = 3
LEVIER_CODES = list(LEVIER_ID_TO_LABEL)

# Prix en USD par million de tokens.
# Mistral : grille de utils/test_run_impact.py (Large 4 au tarif promo ; la page publique
# de Mistral ne donne pas de prix pour Small 4). Claude : page tarifs Anthropic, prompts
# de moins de 100 000 tokens, cache 5 minutes.
MODELS: dict[str, dict[str, Any]] = {
    "mistral-large-4": {
        "provider": "mistral",
        "reasoning_effort": "low",
        "max_tokens": 16000,
        "prices": {"input": 0.68, "cached": 0.07, "cache_write": 0.68, "output": 2.09},
    },
    "mistral-small-2603": {
        "provider": "mistral",
        "reasoning_effort": "none",  # ce modèle n'accepte que "none" ou "high"
        "max_tokens": 16000,
        "prices": {"input": 0.15, "cached": 0.15, "cache_write": 0.15, "output": 0.60},
    },
    "claude-haiku-5-5": {
        "provider": "anthropic",
        "reasoning_effort": None,  # pas d'extended thinking
        "max_tokens": 1024,
        "prices": {"input": 0.10, "cached": 0.01, "cache_write": 0.125, "output": 0.50},
    },
}
DEFAULT_MODEL = "mistral-large-4"
# Compatibilité avec l'ancien code.
MODEL = DEFAULT_MODEL
REASONING_EFFORT = MODELS[DEFAULT_MODEL]["reasoning_effort"]

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "leviers": {
            "type": "array",
            "maxItems": MAX_LEVIERS,
            "items": {
                "type": "object",
                "properties": {
                    "levier": {"type": "string", "enum": LEVIER_CODES},
                    "categories": {
                        "type": "array",
                        "minItems": 1,
                        "items": {"type": "integer", "enum": sorted(VALID_CATEGORIES)},
                    },
                },
                "required": ["levier", "categories"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["leviers"],
    "additionalProperties": False,
}
TOOL_NAME = "classer_fiche"
# Le mode strict d'Anthropic refuse maxItems sur les tableaux.
ANTHROPIC_SCHEMA = json.loads(json.dumps(RESPONSE_SCHEMA))
ANTHROPIC_SCHEMA["properties"]["leviers"].pop("maxItems")


def load_system_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


def make_client(model: str, secrets: dict[str, Any]) -> Any:
    provider = MODELS[model]["provider"]
    if provider == "anthropic":
        import anthropic

        key = os.environ.get("ANTHROPIC_API_KEY") or str(secrets.get("ANTHROPIC_API_KEY") or "")
        if not key:
            raise RuntimeError("ANTHROPIC_API_KEY absente (env ou .streamlit/secrets.toml).")
        return anthropic.Anthropic(api_key=key, timeout=300.0)
    from openai import OpenAI

    key = (
        os.environ.get("MISTRAL_API_KEY")
        or os.environ.get("mistral_api_key")
        or str(secrets.get("mistral_api_key") or "")
    )
    if not key:
        raise RuntimeError("mistral_api_key absente (env ou .streamlit/secrets.toml).")
    return OpenAI(base_url=MISTRAL_BASE_URL, api_key=key, timeout=900.0)


def fetch_contexte_axes(engine: Engine, collectivite_id: int) -> dict[int, str]:
    """fiche_id -> « Plan > Axe > Sous-axe » (plusieurs rattachements séparés par « | »)."""
    sql = text(
        """
        WITH RECURSIVE chaine AS (
            SELECT faa.fiche_id, a.id AS depart, a.nom, a.parent, 0 AS profondeur
            FROM fiche_action_axe faa
            JOIN axe a ON a.id = faa.axe_id
            JOIN fiche_action fa ON fa.id = faa.fiche_id
            WHERE fa.collectivite_id = :cid
            UNION ALL
            SELECT c.fiche_id, c.depart, p.nom, p.parent, c.profondeur + 1
            FROM chaine c
            JOIN axe p ON p.id = c.parent
            WHERE c.profondeur < 10
        )
        SELECT fiche_id, depart,
               string_agg(COALESCE(NULLIF(trim(nom), ''), '(sans nom)'), ' > '
                          ORDER BY profondeur DESC) AS chemin
        FROM chaine
        GROUP BY fiche_id, depart
        """
    )
    with engine.connect() as conn:
        df = pd.read_sql_query(sql, conn, params={"cid": collectivite_id})
    out: dict[int, str] = {}
    for fid, grp in df.groupby("fiche_id"):
        out[int(fid)] = " | ".join(sorted(set(grp["chemin"])))
    return out


def build_user_message(titre: str, description: str, contexte: str | None) -> str:
    titre = " ".join(str(titre or "").split()) or "(sans titre)"
    description = " ".join(str(description or "").split()) or "aucune"
    if description.lower() == "nan":
        description = "aucune"
    return (
        f"Contexte : {contexte or 'non renseigné'}\n"
        f"Titre : {titre}\n"
        f"Description : {description}"
    )


def validate(data: Any) -> dict[str, list[int]]:
    """Réponse du modèle -> {libellé v1 du levier: catégories}. Lève ValueError si invalide."""
    if not isinstance(data, dict) or not isinstance(data.get("leviers"), list):
        raise ValueError("JSON attendu : {\"leviers\": [...]}")
    out: dict[str, set[int]] = {}
    for item in data["leviers"]:
        code = item.get("levier") if isinstance(item, dict) else None
        if code not in LEVIER_ID_TO_LABEL:
            raise ValueError(f"Levier inconnu : {code!r}")
        cats = item.get("categories")
        if not isinstance(cats, list) or not cats:
            raise ValueError(f"Catégories vides pour {code}")
        parsed = {int(c) for c in cats}
        if not parsed <= VALID_CATEGORIES:
            raise ValueError(f"Catégorie invalide pour {code} : {cats}")
        out.setdefault(LEVIER_ID_TO_LABEL[code], set()).update(parsed)
    if len(out) > MAX_LEVIERS:
        raise ValueError(f"{len(out)} leviers (maximum {MAX_LEVIERS})")
    return {label: sorted(cats) for label, cats in out.items()}


def cost_usd(tokens: dict[str, int], model: str = DEFAULT_MODEL) -> float:
    """tokens : input (total, cache compris), cached (lus en cache), cache_write, output."""
    p = MODELS.get(model, MODELS[DEFAULT_MODEL])["prices"]
    cached = tokens.get("cached", 0)
    write = tokens.get("cache_write", 0)
    plain = tokens.get("input", 0) - cached - write
    return (
        plain * p["input"]
        + cached * p["cached"]
        + write * p["cache_write"]
        + tokens.get("output", 0) * p["output"]
    ) / 1_000_000


# ---------------------------------------------------------------- appels


def _mistral_text(response: Any) -> str:
    content = response.choices[0].message.content
    if isinstance(content, list):
        parts = []
        for part in content:
            get = part.get if isinstance(part, dict) else (lambda k, p=part: getattr(p, k, None))
            if get("type") == "text":
                parts.append(str(get("text") or ""))
        return "".join(parts)
    return str(content or "")


def _call_mistral(client: Any, model: str, system_prompt: str, user_message: str) -> tuple[Any, dict[str, int]]:
    cfg = MODELS[model]
    body: dict[str, Any] = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {"name": "classification", "schema": RESPONSE_SCHEMA, "strict": True},
        },
        "max_tokens": cfg["max_tokens"],
    }
    if cfg["reasoning_effort"]:
        body["extra_body"] = {"reasoning_effort": cfg["reasoning_effort"]}
    response = client.chat.completions.create(**body)
    usage = getattr(response, "usage", None)
    details = getattr(usage, "prompt_tokens_details", None)
    tokens = {
        "input": int(getattr(usage, "prompt_tokens", 0) or 0),
        "cached": int(getattr(details, "cached_tokens", 0) or 0),
        "cache_write": 0,
        "output": int(getattr(usage, "completion_tokens", 0) or 0),
    }
    return json.loads(strip_json_fences(_mistral_text(response))), tokens


def _call_anthropic(client: Any, model: str, system_prompt: str, user_message: str) -> tuple[Any, dict[str, int]]:
    response = client.messages.create(
        model=model,
        max_tokens=MODELS[model]["max_tokens"],
        system=[{"type": "text", "text": system_prompt, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": user_message}],
        tools=[
            {
                "name": TOOL_NAME,
                "description": "Renvoie la classification de la fiche action.",
                "input_schema": ANTHROPIC_SCHEMA,
                # Mode strict : les codes de leviers et les catégories hors liste sont
                # impossibles. Il refuse maxItems : la limite de 3 leviers est appliquée après.
                "strict": True,
            }
        ],
        tool_choice={"type": "tool", "name": TOOL_NAME},
    )
    u = response.usage
    read = int(getattr(u, "cache_read_input_tokens", 0) or 0)
    write = int(getattr(u, "cache_creation_input_tokens", 0) or 0)
    tokens = {
        # input_tokens d'Anthropic exclut le cache : on additionne pour avoir le total.
        "input": int(u.input_tokens or 0) + read + write,
        "cached": read,
        "cache_write": write,
        "output": int(u.output_tokens or 0),
    }
    for block in response.content:
        if getattr(block, "type", None) == "tool_use":
            data = dict(block.input)
            if isinstance(data.get("leviers"), list) and len(data["leviers"]) > MAX_LEVIERS:
                # Équivalent du maxItems de Mistral : on garde les 3 premiers (les plus directs).
                data["leviers"] = data["leviers"][:MAX_LEVIERS]
                tokens["tronque"] = 1
            return data, tokens
    raise json.JSONDecodeError("pas d'appel d'outil dans la réponse", "", 0)


def _is_unavailable(exc: Exception) -> bool:
    msg = str(exc).lower()
    status = getattr(exc, "status_code", None)
    return status in (429, 500, 502, 503, 529) or any(
        k in msg for k in ("429", "rate", "overloaded", "502", "503", "timeout", "timed out")
    )


def classify_fiche(
    client: Any,
    system_prompt: str,
    user_message: str,
    log=print,
    label: str = "",
    model: str = DEFAULT_MODEL,
) -> tuple[dict[str, list[int]], dict[str, Any]]:
    """Une fiche, un appel. Rejoue jusqu'à 3 fois une réponse invalide ; attend sur 429/5xx."""
    call = _call_anthropic if MODELS[model]["provider"] == "anthropic" else _call_mistral
    tokens = {"input": 0, "cached": 0, "cache_write": 0, "output": 0}
    errors: list[str] = []
    essais = 0
    attentes = 0
    while essais < 3:
        try:
            data, tk = call(client, model, system_prompt, user_message)
        except json.JSONDecodeError as e:
            essais += 1
            errors.append(f"JSONDecodeError: {e}")
            log(f"  {label} réponse illisible, essai {essais}/3 : {e}")
            continue
        except Exception as e:
            if _is_unavailable(e) and attentes < 20:
                attentes += 1
                log(f"    {label} API indisponible ({type(e).__name__}), nouvel essai dans 10 s")
                time.sleep(10)
                continue
            raise
        essais += 1
        for k, v in tk.items():
            tokens[k] = tokens.get(k, 0) + v
        try:
            parsed = validate(data)
            return parsed, {"essais": essais, "erreurs": errors, "tokens": tokens}
        except ValueError as e:
            errors.append(f"ValueError: {e}")
            log(f"  {label} réponse invalide, essai {essais}/3 : {e}")
    raise RuntimeError(f"{label} : 3 réponses invalides : {errors}")
