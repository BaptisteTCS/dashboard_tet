"""Helpers texte partagés entre les onglets de priorisation."""

from __future__ import annotations

import json
import re

import pandas as pd
from bs4 import BeautifulSoup


def clean_rich_text(text) -> str:
    """Convertit une description enrichie (HTML) en texte brut lisible."""
    if text is None or (isinstance(text, float) and pd.isna(text)):
        return ""
    text = str(text).strip()
    if not text:
        return ""
    text = BeautifulSoup(text, "html.parser").get_text(separator=" ")
    return re.sub(r"\s+", " ", text).strip()


def short_description(text, max_len: int = 220) -> str:
    cleaned = clean_rich_text(text) if not isinstance(text, str) else text
    if len(cleaned) <= max_len:
        return cleaned
    truncated = cleaned[:max_len].rsplit(" ", 1)[0]
    return f"{truncated}…"


def as_bool(value) -> bool:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return False
    return bool(value)


def parse_ids(value) -> list[int]:
    """Parse la colonne priorisation.ids (JSON, liste ou chaîne)."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return []
    if isinstance(value, (list, tuple, set)):
        ids: list[int] = []
        for v in value:
            try:
                ids.append(int(v))
            except (TypeError, ValueError):
                continue
        return ids
    if isinstance(value, str):
        cleaned = value.strip()
        if not cleaned:
            return []
        try:
            parsed = json.loads(cleaned)
            if isinstance(parsed, list):
                return parse_ids(parsed)
        except (json.JSONDecodeError, ValueError):
            pass
        cleaned = cleaned.strip("[]{}()")
        parts = [p.strip() for p in cleaned.split(",") if p.strip()]
        ids = []
        for p in parts:
            try:
                ids.append(int(p))
            except ValueError:
                continue
        return ids
    try:
        return [int(value)]
    except (TypeError, ValueError):
        return []


def is_reference_origine(origine) -> bool:
    if origine is None or (isinstance(origine, float) and pd.isna(origine)):
        return False
    return str(origine).strip().lower() in ("référence", "reference")


def origine_label(origine) -> str:
    if is_reference_origine(origine):
        return "Action de référence"
    if origine is None or (isinstance(origine, float) and pd.isna(origine)):
        return "Collectivité"
    return str(origine).strip()
