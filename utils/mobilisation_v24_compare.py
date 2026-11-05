"""Données de la page de comparaison des notes de mobilisation (v2.4 calculée vs prod).

- Nouvelles notes : fichiers produits par scripts/mobilisation_v24.py (data/mobilisation_v2_4/).
- Notes actuelles : table collectivite_volet_ges de la prod, en lecture seule.
- Potentiels de réduction : table OLAP priorisation_reduction_levier si elle en a pour la
  collectivité, sinon l'API trajectoires SNBC de TeT (GET, lecture seule).
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import requests
import streamlit as st
from sqlalchemy import text

from utils.priorisation_data import load_reductions
from utils.verify_classification_volet_ges import (
    CATEGORIE_ENUM_TO_ID,
    LEVIER_ID_TO_LABEL,
    LEVIERS_SET,
    engine_prod_readonly,
    load_secrets,
)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "mobilisation_v2_4" / "claude-haiku-5-5"
API_LEVIER_NAME_MAP = {"Production industrielle": "Production Industrielle"}

NOTE_LABELS_V24 = {
    0: "Non mobilisé",
    1: "Amorcé",
    2: "Mobilisé",
    3: "Fortement mobilisé",
}


def load_notes_v24() -> pd.DataFrame:
    path = OUT / "notes.csv"
    if not path.exists():
        return pd.DataFrame()
    return _read_notes(str(path), path.stat().st_mtime)


@st.cache_data
def _read_notes(path: str, mtime: float) -> pd.DataFrame:  # noqa: ARG001 (mtime : clé de cache)
    """Relu dès que le fichier change (la date de modification fait partie de la clé de cache)."""
    df = pd.read_csv(path, encoding="utf-8-sig")
    for col in ("structurantes", "peu_importantes"):
        df[col] = df[col].map(json.loads)
    return df


@st.cache_data(ttl="10m")
def load_collectivites_v24() -> dict[int, dict]:
    """cid -> {nom, type_label, population, fiches: {id: titre}}."""
    out: dict[int, dict] = {}
    for d in sorted(OUT.glob("*/fiches.json")):
        data = json.loads(d.read_text(encoding="utf-8"))
        info = data["collectivite"]
        info["fiches"] = {int(f["id"]): f["titre"] for f in data["fiches"]}
        out[int(info["id"])] = info
    return out


@st.cache_data(ttl="1h")
def load_notes_prod(collectivite_id: int) -> pd.DataFrame:
    """Notes actuelles (prod, lecture seule) : levier, categorie, note, fiche_ids."""
    engine = engine_prod_readonly(load_secrets())
    with engine.connect() as conn:
        df = pd.read_sql_query(
            text(
                "SELECT levier_id::text AS levier_id, categorie::text AS categorie, note, fiche_ids "
                "FROM collectivite_volet_ges WHERE collectivite_id = :cid"
            ),
            conn,
            params={"cid": collectivite_id},
        )
    df["levier"] = df["levier_id"].map(LEVIER_ID_TO_LABEL)
    df["categorie"] = df["categorie"].map(CATEGORIE_ENUM_TO_ID).astype(int)
    df["fiche_ids"] = df["fiche_ids"].map(lambda x: list(x) if x is not None else [])
    return df[["levier", "categorie", "note", "fiche_ids"]]


@st.cache_data(ttl="1h")
def _fetch_snbc_leviers(collectivite_id: int) -> dict:
    token = st.secrets.get("api_prod_token", "")
    if not token:
        raise ValueError("api_prod_token absent de secrets.toml")
    base = st.secrets["api_prod_url"].split("/api/v1")[0]
    resp = requests.get(
        f"{base}/api/v1/trajectoires/snbc/leviers",
        headers={"Authorization": f"Bearer {token}"},
        params={"collectiviteId": collectivite_id},
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()


def load_potentiels(collectivite_id: int) -> tuple[dict[str, float], str]:
    """{levier: réduction} et la source utilisée."""
    df = load_reductions(collectivite_id)
    if not df.empty:
        return df.set_index("levier")["reduction"].astype(float).to_dict(), "OLAP (priorisation_reduction_levier)"
    data = _fetch_snbc_leviers(collectivite_id)
    out: dict[str, float] = {}
    for secteur in data.get("secteurs", []):
        for levier in secteur.get("leviers", []):
            nom = API_LEVIER_NAME_MAP.get(levier["nom"], levier["nom"])
            if nom in LEVIERS_SET and levier.get("objectifReduction") is not None:
                out[nom] = round(float(levier["objectifReduction"]), 1)
    return out, "API trajectoires SNBC de TeT (lecture)"
