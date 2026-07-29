"""Loaders, writers et contexte partagé pour la page Priorisation (42)."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
import streamlit as st
from sqlalchemy import text

from utils.db import get_engine, get_engine_prod
from utils.priorisation_text import as_bool, parse_ids

# Aligné sur utils.priorisation_impact_charts.CATEGORIES
CATEGORIES = {
    1: "Aménagement",
    2: "Planification",
    3: "Financement",
    4: "Gouvernance",
    5: "Exemplarité",
    6: "Sensibilisation",
}


# ==========================
# Chargement des données
# ==========================


@st.cache_data(ttl="1h")
def load_collectivites_priorisees() -> pd.DataFrame:
    """Collectivités ayant au moins une ligne dans priorisation (OLAP)."""
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("""
                SELECT DISTINCT c.collectivite_id, c.nom
                FROM collectivite c
                INNER JOIN priorisation p ON p.collectivite_id = c.collectivite_id
                WHERE c.nom IS NOT NULL
                ORDER BY c.nom
            """),
            conn,
        )


@st.cache_data(ttl="1h")
def load_poids_categories() -> pd.DataFrame:
    """Poids catégorie × levier (référentiel statique OLAP)."""
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("SELECT * FROM priorisation_categorie_levier"),
            conn,
        )


@st.cache_data(ttl="1h")
def load_priorisation(collectivite_id: int) -> pd.DataFrame:
    """Notes et ids les plus récents par case (levier × catégorie)."""
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("""
                SELECT DISTINCT ON (levier, categorie)
                    levier, categorie, note, ids
                FROM priorisation
                WHERE collectivite_id = :collectivite_id
                ORDER BY levier, categorie, created_at DESC
            """),
            conn,
            params={"collectivite_id": collectivite_id},
        )


@st.cache_data(ttl="1h")
def load_priorisation_all(collectivite_ids: tuple[int, ...]) -> pd.DataFrame:
    """Notes et ids les plus récents par collectivité × case (levier × catégorie)."""
    if not collectivite_ids:
        return pd.DataFrame(
            columns=["collectivite_id", "levier", "categorie", "note", "ids"]
        )
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("""
                SELECT DISTINCT ON (collectivite_id, levier, categorie)
                    collectivite_id, levier, categorie, note, ids
                FROM priorisation
                WHERE collectivite_id = ANY(:ids)
                ORDER BY collectivite_id, levier, categorie, created_at DESC
            """),
            conn,
            params={"ids": list(collectivite_ids)},
        )


@st.cache_data(ttl="1h")
def load_fiches_action(collectivite_ids: tuple[int, ...]) -> pd.DataFrame:
    """Fiches action prod pour les collectivités priorisées."""
    if not collectivite_ids:
        return pd.DataFrame(columns=["id", "collectivite_id", "titre", "description"])
    engine = get_engine_prod()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("""
                SELECT id, collectivite_id, titre, description
                FROM fiche_action
                WHERE collectivite_id = ANY(:ids)
            """),
            conn,
            params={"ids": list(collectivite_ids)},
        )


@st.cache_data(ttl="1h")
def load_reductions(collectivite_id: int) -> pd.DataFrame:
    """Réductions les plus récentes par levier."""
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("""
                SELECT DISTINCT ON (levier)
                    levier, reduction
                FROM priorisation_reduction_levier
                WHERE collectivite_id = :collectivite_id
                ORDER BY levier, created_at DESC
            """),
            conn,
            params={"collectivite_id": collectivite_id},
        )


@st.cache_data(ttl="1h")
def load_hors_competence(collectivite_id: int) -> pd.DataFrame:
    """Couples levier × catégorie hors compétence pour une collectivité."""
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("""
                SELECT levier, categorie
                FROM priorisation_hors_competence
                WHERE collectivite_id = :collectivite_id
            """),
            conn,
            params={"collectivite_id": collectivite_id},
        )


@st.cache_data(ttl="1h")
def load_faisabilite(collectivite_id: int) -> pd.DataFrame:
    """Arbitrages politiques enregistrés pour une collectivité."""
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("""
                SELECT levier, categorie, faisabilite
                FROM priorisation_faisabilite
                WHERE collectivite_id = :collectivite_id
            """),
            conn,
            params={"collectivite_id": collectivite_id},
        )


@st.cache_data(ttl="1h")
def load_plans(collectivite_id: int) -> list[str]:
    """Noms des plans d'action de la collectivité (un axe racine par plan)."""
    engine = get_engine()
    with engine.connect() as conn:
        df = pd.read_sql_query(
            text("""
                SELECT DISTINCT nom
                FROM prod.axe
                WHERE collectivite_id = :collectivite_id
                  AND plan = id
                  AND nom IS NOT NULL
                  AND btrim(nom) <> ''
                ORDER BY nom
            """),
            conn,
            params={"collectivite_id": collectivite_id},
        )
    return df["nom"].tolist()


@st.cache_data(ttl="1h")
def load_nb_actions(collectivite_id: int) -> int:
    """Nombre d'actions déposées par la collectivité."""
    engine = get_engine()
    with engine.connect() as conn:
        df = pd.read_sql_query(
            text("""
                SELECT COUNT(DISTINCT id) AS nb
                FROM prod.fiche_action
                WHERE collectivite_id = :collectivite_id
            """),
            conn,
            params={"collectivite_id": collectivite_id},
        )
    return int(df["nb"].iloc[0])


@st.cache_data(ttl="1h")
def load_actions_reference() -> pd.DataFrame:
    """Actions de référence (référentiel statique OLAP)."""
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("""
                SELECT id, levier, categorie, titre, description
                FROM priorisation_action_reference
            """),
            conn,
        )


@st.cache_data(ttl="1h")
def load_actions_choisies(collectivite_id: int) -> pd.DataFrame:
    """Actions sauvegardées à l'étape « Choix des actions »."""
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("""
                SELECT levier, categorie, fiche_action_id, reference
                FROM priorisation_action
                WHERE collectivite_id = :collectivite_id
                ORDER BY created_at
            """),
            conn,
            params={"collectivite_id": collectivite_id},
        )


@st.cache_data(ttl="1h")
def load_fiches_by_ids(fiche_ids: tuple[int, ...]) -> pd.DataFrame:
    """Fiches action prod résolues depuis priorisation_action.fiche_action_id."""
    if not fiche_ids:
        return pd.DataFrame(columns=["id", "collectivite_id", "titre", "description"])
    engine = get_engine_prod()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("""
                SELECT id, collectivite_id, titre, description
                FROM fiche_action
                WHERE id = ANY(:ids)
            """),
            conn,
            params={"ids": list(fiche_ids)},
        )


@st.cache_data(ttl="1h")
def load_noms_collectivites(collectivite_ids: tuple[int, ...]) -> pd.DataFrame:
    """Noms des collectivités d'origine des fiches, priorisées ou non."""
    if not collectivite_ids:
        return pd.DataFrame(columns=["collectivite_id", "nom"])
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("""
                SELECT collectivite_id, nom
                FROM collectivite
                WHERE collectivite_id = ANY(:ids)
            """),
            conn,
            params={"ids": list(collectivite_ids)},
        )


# ==========================
# Builders
# ==========================


def build_category_weights(df_poids: pd.DataFrame) -> dict[str, dict[int, float]]:
    """Retourne {levier: {categorie: poids}} depuis priorisation_categorie_levier."""
    levier_cols = [c for c in df_poids.columns if c != "categorie"]
    weights: dict[str, dict[int, float]] = {levier: {} for levier in levier_cols}
    for _, row in df_poids.iterrows():
        cat = int(row["categorie"])
        for levier in levier_cols:
            val = row[levier]
            weights[levier][cat] = 0.0 if pd.isna(val) else float(val)
    return weights


def build_notes(df_priorisation: pd.DataFrame) -> dict[tuple[str, int], int]:
    return {
        (row["levier"], int(row["categorie"])): int(row["note"])
        for _, row in df_priorisation.iterrows()
    }


def build_faisabilites(df: pd.DataFrame) -> dict[tuple[str, int], int]:
    return {
        (row["levier"], int(row["categorie"])): int(row["faisabilite"])
        for _, row in df.iterrows()
    }


def hors_competence_pairs(df: pd.DataFrame) -> set[tuple[str, int]]:
    return {(row["levier"], int(row["categorie"])) for _, row in df.iterrows()}


def selections_from_db(
    df: pd.DataFrame,
) -> dict[tuple[str, int], set[tuple[int, bool]]]:
    result: dict[tuple[str, int], set[tuple[int, bool]]] = {}
    for _, row in df.iterrows():
        key = (row["levier"], int(row["categorie"]))
        fiche = (int(row["fiche_action_id"]), as_bool(row.get("reference")))
        result.setdefault(key, set()).add(fiche)
    return result


def actions_par_cible(df_actions: pd.DataFrame) -> dict[tuple[str, int], int]:
    """Nombre d'actions retenues par volet (levier × catégorie)."""
    compte: dict[tuple[str, int], int] = {}
    for _, row in df_actions.iterrows():
        cle = (row["levier"], int(row["categorie"]))
        compte[cle] = compte.get(cle, 0) + 1
    return compte


# ==========================
# Writers
# ==========================


def save_faisabilite(
    collectivite_id: int,
    rows: list[tuple[str, int, int]],
) -> None:
    """Remplacement complet des arbitrages pour la collectivité (une transaction)."""
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(
            text(
                "DELETE FROM priorisation_faisabilite "
                "WHERE collectivite_id = :collectivite_id"
            ),
            {"collectivite_id": collectivite_id},
        )
        if rows:
            conn.execute(
                text("""
                    INSERT INTO priorisation_faisabilite
                        (collectivite_id, levier, categorie, faisabilite)
                    VALUES (:collectivite_id, :levier, :categorie, :faisabilite)
                """),
                [
                    {
                        "collectivite_id": collectivite_id,
                        "levier": levier,
                        "categorie": cat,
                        "faisabilite": fais,
                    }
                    for levier, cat, fais in rows
                ],
            )


def save_priorisation_action(
    collectivite_id: int,
    rows: list[tuple[str, int, int, bool]],
) -> None:
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(
            text(
                "DELETE FROM priorisation_action "
                "WHERE collectivite_id = :collectivite_id"
            ),
            {"collectivite_id": collectivite_id},
        )
        if rows:
            conn.execute(
                text("""
                    INSERT INTO priorisation_action
                        (collectivite_id, levier, categorie, fiche_action_id,
                         reference)
                    VALUES (:collectivite_id, :levier, :categorie,
                            :fiche_action_id, :reference)
                """),
                [
                    {
                        "collectivite_id": collectivite_id,
                        "levier": levier,
                        "categorie": cat,
                        "fiche_action_id": fiche_id,
                        "reference": reference,
                    }
                    for levier, cat, fiche_id, reference in rows
                ],
            )


# ==========================
# Contexte partagé
# ==========================


@dataclass
class PriorisationContext:
    collectivite_id: int
    nom: str
    nom_par_id: dict[int, str]
    collectivite_ids: list[int]
    df_priorisation: pd.DataFrame
    df_priorisation_all: pd.DataFrame
    df_fiches_action: pd.DataFrame
    df_actions_reference: pd.DataFrame
    notes: dict[tuple[str, int], int]
    notes_perimetre: dict[tuple[str, int], int]
    ids_by_case: dict[tuple[str, int], list[int]]
    reductions: dict[str, float]
    weights: dict[str, dict[int, float]]
    exclusions: set[tuple[str, int]]
    faisabilites: dict[tuple[str, int], int]
    leviers_reduction: list[str]
    leviers_notes: list[str]


def build_priorisation_context(
    collectivite_id: int,
    nom_par_id: dict[int, str],
    collectivite_ids: list[int],
) -> PriorisationContext:
    """Charge et assemble le contexte partagé une fois par run."""
    df_priorisation = load_priorisation(collectivite_id)
    df_priorisation_all = load_priorisation_all(tuple(collectivite_ids))
    df_reductions = load_reductions(collectivite_id)
    df_poids = load_poids_categories()
    exclusions = hors_competence_pairs(load_hors_competence(collectivite_id))

    notes = build_notes(df_priorisation)
    notes_perimetre = {
        key: note for key, note in notes.items() if key not in exclusions
    }
    ids_by_case = {
        (row["levier"], int(row["categorie"])): parse_ids(row["ids"])
        for _, row in df_priorisation.iterrows()
        if (row["levier"], int(row["categorie"])) not in exclusions
    }
    reductions = df_reductions.set_index("levier")["reduction"].to_dict()
    weights = build_category_weights(df_poids)
    faisabilites = build_faisabilites(load_faisabilite(collectivite_id))

    return PriorisationContext(
        collectivite_id=collectivite_id,
        nom=nom_par_id[collectivite_id],
        nom_par_id=nom_par_id,
        collectivite_ids=collectivite_ids,
        df_priorisation=df_priorisation,
        df_priorisation_all=df_priorisation_all,
        df_fiches_action=load_fiches_action(tuple(collectivite_ids)),
        df_actions_reference=load_actions_reference(),
        notes=notes,
        notes_perimetre=notes_perimetre,
        ids_by_case=ids_by_case,
        reductions=reductions,
        weights=weights,
        exclusions=exclusions,
        faisabilites=faisabilites,
        leviers_reduction=sorted(reductions.keys()),
        leviers_notes=sorted(df_priorisation["levier"].unique().tolist()),
    )
