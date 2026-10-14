"""Client HogQL (API PostHog) utilise par l'assistant IA."""

import logging
import os
from typing import Optional

import pandas as pd
import requests
import streamlit as st
from dateutil.relativedelta import relativedelta
from sqlalchemy import text

from utils.db import get_engine

logger = logging.getLogger(__name__)

POSTHOG_HOST = "https://eu.posthog.com"
POSTHOG_PROJECT_ID = 12975
REQUEST_TIMEOUT = 120

HOGQL_WINDOW_LIMIT = 50000  # LIMIT max par requete HogQL
MAX_WINDOWS = 24
MAX_TOTAL_ROWS = 200_000

START_PLACEHOLDER = "{start}"
END_PLACEHOLDER = "{end}"


def _get_api_key() -> str:
    for key in ("posthog_api_key", "POSTHOG_API_KEY"):
        try:
            value = st.secrets.get(key)
        except Exception:  # noqa: BLE001
            value = None
        if value:
            return str(value)
    return os.getenv("POSTHOG_API_KEY", "")


@st.cache_data(ttl="1h", show_spinner=False)
def load_internal_emails() -> set[str]:
    """Emails des utilisateurs internes (public.internal_users), en minuscules."""
    engine = get_engine()
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                "SELECT DISTINCT lower(trim(email)) FROM public.internal_users "
                "WHERE email IS NOT NULL"
            )
        ).scalars().all()
    return set(rows)


def _to_utc(value: str) -> pd.Timestamp:
    ts = pd.Timestamp(value)
    return ts.tz_localize("UTC") if ts.tzinfo is None else ts.tz_convert("UTC")


def _post_hogql(query: str) -> tuple[Optional[list], Optional[list], bool, Optional[str]]:
    """Execute une requete HogQL. Retourne (columns, results, has_more, erreur)."""
    api_key = _get_api_key()
    if not api_key:
        return None, None, False, "Cle API PostHog absente (secret 'posthog_api_key')."

    url = f"{POSTHOG_HOST}/api/projects/{POSTHOG_PROJECT_ID}/query/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    payload = {"query": {"kind": "HogQLQuery", "query": query}}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=REQUEST_TIMEOUT)
    except requests.RequestException as exc:
        return None, None, False, f"Erreur reseau PostHog : {exc}"

    try:
        data = response.json()
    except ValueError:
        return None, None, False, (
            f"Reponse PostHog non JSON (HTTP {response.status_code}) : {response.text[:500]}"
        )

    if response.status_code != 200 or "results" not in data:
        detail = data.get("detail") or data.get("error") or data
        return None, None, False, f"Erreur PostHog (HTTP {response.status_code}) : {str(detail)[:1000]}"

    return data.get("columns") or [], data["results"] or [], bool(data.get("hasMore")), None


def _build_windows(date_from: str, date_to: Optional[str]) -> list[tuple[str, str]]:
    start = _to_utc(date_from)
    end = _to_utc(date_to) if date_to else pd.Timestamp.now(tz="UTC")
    windows = []
    window_start = start
    while window_start < end:
        window_end = min(window_start + relativedelta(months=1), end)
        windows.append(
            (
                window_start.strftime("%Y-%m-%d %H:%M:%S"),
                window_end.strftime("%Y-%m-%d %H:%M:%S"),
            )
        )
        window_start = window_end
    return windows


def _remove_internal_users(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    email_cols = [c for c in df.columns if str(c).lower() == "email"]
    if not email_cols or df.empty:
        return df, 0
    internal = load_internal_emails()
    mask = pd.Series(False, index=df.index)
    for col in email_cols:
        mask |= df[col].fillna("").astype(str).str.strip().str.lower().isin(internal)
    return df[~mask].reset_index(drop=True), int(mask.sum())


def run_hogql(
    hogql: str,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
) -> tuple[Optional[pd.DataFrame], dict, Optional[str]]:
    """
    Execute une requete HogQL, eventuellement decoupee en fenetres mensuelles.

    Si la requete contient {start} et {end} et que date_from est fourni, elle est
    executee une fois par mois entre date_from et date_to (defaut : maintenant),
    les marqueurs etant remplaces par 'YYYY-MM-DD HH:MM:SS'. Les resultats sont
    concatenes puis dedoublonnes. Les utilisateurs internes sont retires si une
    colonne email est presente.

    Retourne (dataframe, meta, None) en cas de succes, (None, meta, erreur) sinon.
    """
    meta: dict = {"windows": 0, "truncated_windows": []}
    if not hogql or not hogql.strip():
        return None, meta, "Requete HogQL vide."

    has_placeholders = START_PLACEHOLDER in hogql and END_PLACEHOLDER in hogql
    if has_placeholders and not date_from:
        return None, meta, "La requete contient {start}/{end} : date_from est obligatoire."

    if has_placeholders:
        try:
            windows = _build_windows(date_from, date_to)
        except (ValueError, TypeError) as exc:
            return None, meta, f"Dates invalides : {exc}"
        if not windows:
            return None, meta, "Plage de dates vide (date_from >= date_to)."
        if len(windows) > MAX_WINDOWS:
            return None, meta, (
                f"Plage trop longue : {len(windows)} mois (maximum {MAX_WINDOWS}). Reduis la periode."
            )
    else:
        windows = [(None, None)]
        if date_from or date_to:
            meta["note_dates"] = (
                "date_from/date_to ignores : la requete ne contient pas les marqueurs {start}/{end}."
            )

    frames: list[pd.DataFrame] = []
    columns: list = []
    total_rows = 0
    for window_start, window_end in windows:
        query = hogql
        if window_start is not None:
            query = query.replace(START_PLACEHOLDER, window_start).replace(END_PLACEHOLDER, window_end)

        cols, results, has_more, err = _post_hogql(query)
        meta["windows"] += 1
        if err:
            if window_start is not None:
                err = f"[fenetre {window_start} -> {window_end}] {err}"
            return None, meta, err

        columns = cols or columns
        if results:
            frames.append(pd.DataFrame(results, columns=cols or None))
            total_rows += len(results)
        if has_more or len(results) >= HOGQL_WINDOW_LIMIT:
            label = f"{window_start} -> {window_end}" if window_start else "requete unique"
            meta["truncated_windows"].append(label)
        if total_rows >= MAX_TOTAL_ROWS:
            meta["row_cap_reached"] = True
            break

    if frames:
        df = pd.concat(frames, ignore_index=True)
    else:
        df = pd.DataFrame(columns=columns)

    if len(windows) > 1:
        try:
            df = df.drop_duplicates().reset_index(drop=True)
        except TypeError:
            # Colonnes non hashables (tableaux, objets JSON) : pas de dedoublonnage.
            pass

    df = df.head(MAX_TOTAL_ROWS)
    df, removed = _remove_internal_users(df)
    meta["internal_rows_removed"] = removed
    return df, meta, None
