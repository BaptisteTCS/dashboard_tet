"""Espace de travail DuckDB par conversation pour l'assistant IA.

Les dataframes (resultats SQL Postgres ou HogQL PostHog) sont stockes dans
st.session_state sous un nom, puis interrogeables en SQL via DuckDB en memoire.
"""

import re
from typing import Optional

import pandas as pd
import streamlit as st

WORKSPACE_KEY = "workspace"
MAX_WORKSPACE_TABLES = 20
DUCKDB_MEMORY_LIMIT = "1GB"

_NAME_REGEX = re.compile(r"^[a-z_][a-z0-9_]{0,40}$")

FORBIDDEN = (
    "insert",
    "update",
    "delete",
    "drop",
    "alter",
    "create",
    "truncate",
    "grant",
    "revoke",
)
_FORBIDDEN_REGEX = re.compile(r"\b(" + "|".join(FORBIDDEN) + r")\b", re.IGNORECASE)

_DUCKDB_FORBIDDEN = (
    "attach",
    "detach",
    "copy",
    "install",
    "load",
    "pragma",
    "export",
    "import",
    "checkpoint",
)
_DUCKDB_FORBIDDEN_REGEX = re.compile(
    r"\b(" + "|".join(_DUCKDB_FORBIDDEN) + r")\b"
    r"|\bread_\w+\s*\("
    r"|\b(glob|parquet_scan|csv_scan|json_scan|sniff_csv)\s*\(",
    re.IGNORECASE,
)


def validate_select_sql(
    sql: str, forbidden_regex: re.Pattern = _FORBIDDEN_REGEX
) -> tuple[Optional[str], Optional[str]]:
    """
    Valide une requete en lecture seule et la nettoie.

    - Retire un eventuel formatage markdown et le ';' final.
    - Une seule instruction, commencant par SELECT ou WITH.
    - Aucun mot-cle de forbidden_regex (detection par word-boundary).

    Retourne (sql_nettoye, None) ou (None, message_erreur).
    """
    if not sql or not sql.strip():
        return None, "Requete SQL vide."

    cleaned = sql.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```[a-zA-Z]*", "", cleaned).strip()
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3].strip()

    cleaned = cleaned.rstrip().rstrip(";").rstrip()

    if ";" in cleaned:
        return None, "Plusieurs instructions SQL detectees : une seule requete SELECT est autorisee."

    if not re.match(r"^\s*(select|with)\b", cleaned, re.IGNORECASE):
        return None, "Seules les requetes SELECT (ou WITH ... SELECT) sont autorisees."

    match = forbidden_regex.search(cleaned)
    if match:
        return None, (
            f"Requete refusee : commande de modification non autorisee ({match.group(1).upper()})."
        )

    return cleaned, None


def get_workspace() -> dict[str, pd.DataFrame]:
    if WORKSPACE_KEY not in st.session_state:
        st.session_state[WORKSPACE_KEY] = {}
    return st.session_state[WORKSPACE_KEY]


def reset_workspace() -> None:
    st.session_state[WORKSPACE_KEY] = {}


def save(name: str, df: pd.DataFrame) -> Optional[str]:
    """Enregistre df sous name. Retourne un message d'erreur ou None."""
    if not name or not _NAME_REGEX.match(name):
        return (
            f"Nom de table invalide '{name}' : minuscules, chiffres et '_' uniquement, "
            "commencant par une lettre ou '_' (41 caracteres max)."
        )
    workspace = get_workspace()
    if name not in workspace and len(workspace) >= MAX_WORKSPACE_TABLES:
        return f"Workspace plein ({MAX_WORKSPACE_TABLES} tables max) : reutilise un nom existant."
    workspace[name] = df.reset_index(drop=True)
    return None


def describe() -> list[dict]:
    """Liste des tables du workspace avec colonnes, types et nombre de lignes."""
    return [
        {
            "table": name,
            "row_count": len(df),
            "columns": {str(col): str(dtype) for col, dtype in df.dtypes.items()},
        }
        for name, df in get_workspace().items()
    ]


def run_workspace_sql(sql: str, limit: int) -> tuple[Optional[pd.DataFrame], Optional[str]]:
    """
    Execute une requete SELECT DuckDB sur les dataframes du workspace.

    DuckDB est isole : base en memoire, acces fichiers/reseau desactive, pas de
    lecture des variables Python par nom, configuration verrouillee.
    """
    workspace = get_workspace()
    if not workspace:
        return None, (
            "Le workspace est vide : enregistre d'abord des donnees avec save_as "
            "(run_hogql_query ou run_sql_query)."
        )

    cleaned, err = validate_select_sql(sql)
    if err:
        return None, err
    match = _DUCKDB_FORBIDDEN_REGEX.search(cleaned)
    if match:
        return None, f"Requete refusee : instruction DuckDB non autorisee ({match.group(0).strip()})."

    import duckdb

    con = duckdb.connect(
        ":memory:",
        config={
            "enable_external_access": False,
            "python_enable_replacements": False,
            "memory_limit": DUCKDB_MEMORY_LIMIT,
        },
    )
    try:
        for name, df in workspace.items():
            con.register(name, df)
        con.execute("SET lock_configuration = true")
        wrapped = f"SELECT * FROM (\n{cleaned}\n) AS _sub LIMIT {int(limit)}"
        return con.execute(wrapped).df(), None
    except Exception as exc:  # noqa: BLE001
        return None, f"Erreur DuckDB : {exc}"
    finally:
        con.close()


def count_workspace_rows(sql: str) -> Optional[int]:
    """Nombre total de lignes d'une requete workspace (best-effort)."""
    df, err = run_workspace_sql(f"SELECT count(*) AS n FROM (\n{sql.strip().rstrip(';')}\n) AS _c", 1)
    if err or df is None or df.empty:
        return None
    return int(df.iloc[0]["n"])
