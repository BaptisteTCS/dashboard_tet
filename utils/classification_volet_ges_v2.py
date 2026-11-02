"""Classification volet GES, prompt v2 : une fiche par appel, codes de leviers, JSON contraint.

Le prompt système est dans prompts/classification_volet_ges_v2.md. Il est envoyé tel quel
en premier message, pour que Mistral le mette en cache d'un appel à l'autre ; seule la
fiche (message utilisateur) change.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import pandas as pd
from openai import OpenAI
from sqlalchemy import text
from sqlalchemy.engine import Engine

from utils.verify_classification_volet_ges import (
    LEVIER_ID_TO_LABEL,
    VALID_CATEGORIES,
    strip_json_fences,
)

ROOT = Path(__file__).resolve().parent.parent
PROMPT_PATH = ROOT / "prompts" / "classification_volet_ges_v2.md"
MODEL = "mistral-large-4"
REASONING_EFFORT = "low"
# Le raisonnement compte dans max_tokens : une limite basse renvoie une réponse vide.
MAX_TOKENS = 16000
MAX_LEVIERS = 3
LEVIER_CODES = list(LEVIER_ID_TO_LABEL)

# USD par million de tokens (grille utilisée dans utils/test_run_impact.py).
PRICE_INPUT = 0.68
PRICE_CACHED = 0.07
PRICE_OUTPUT = 2.09

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


def load_system_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


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
    return (
        f"Contexte : {contexte or 'non renseigné'}\n"
        f"Titre : {titre}\n"
        f"Description : {description}"
    )


def _message_text(response: Any) -> str:
    content = response.choices[0].message.content
    if isinstance(content, list):
        parts = []
        for part in content:
            get = part.get if isinstance(part, dict) else (lambda k, p=part: getattr(p, k, None))
            if get("type") == "text":
                parts.append(str(get("text") or ""))
        return "".join(parts)
    return str(content or "")


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


def _usage(response: Any) -> dict[str, int]:
    usage = getattr(response, "usage", None)
    details = getattr(usage, "prompt_tokens_details", None)
    return {
        "input": int(getattr(usage, "prompt_tokens", 0) or 0),
        "cached": int(getattr(details, "cached_tokens", 0) or 0),
        "output": int(getattr(usage, "completion_tokens", 0) or 0),
    }


def cost_usd(tokens: dict[str, int]) -> float:
    non_cached = tokens.get("input", 0) - tokens.get("cached", 0)
    return (
        non_cached * PRICE_INPUT
        + tokens.get("cached", 0) * PRICE_CACHED
        + tokens.get("output", 0) * PRICE_OUTPUT
    ) / 1_000_000


def classify_fiche(
    client: OpenAI,
    system_prompt: str,
    user_message: str,
    log=print,
    label: str = "",
) -> tuple[dict[str, list[int]], dict[str, Any]]:
    """Une fiche, un appel. Rejoue jusqu'à 3 fois une réponse invalide ; backoff sur 429/5xx."""
    body: dict[str, Any] = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {"name": "classification", "schema": RESPONSE_SCHEMA, "strict": True},
        },
        "max_tokens": MAX_TOKENS,
        "extra_body": {"reasoning_effort": REASONING_EFFORT},
    }
    tokens = {"input": 0, "cached": 0, "output": 0}
    errors: list[str] = []
    essais = 0
    while essais < 3:
        try:
            response = client.chat.completions.create(**body)
        except Exception as e:  # 429 / 5xx / timeout : on attend, sans compter un essai
            msg = str(e).lower()
            if any(k in msg for k in ("429", "rate", "502", "503", "timeout", "timed out")):
                log(f"    {label} Mistral indisponible ({type(e).__name__}), nouvel essai dans 10 s")
                time.sleep(10)
                continue
            raise
        essais += 1
        for k, v in _usage(response).items():
            tokens[k] += v
        try:
            parsed = validate(json.loads(strip_json_fences(_message_text(response))))
            return parsed, {"essais": essais, "erreurs": errors, "tokens": tokens}
        except (ValueError, json.JSONDecodeError) as e:
            errors.append(f"{type(e).__name__}: {e}")
            log(f"  {label} réponse invalide, essai {essais}/3 : {e}")
    raise RuntimeError(f"{label} : 3 réponses invalides : {errors}")
