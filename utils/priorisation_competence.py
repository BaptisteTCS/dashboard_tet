"""Calcul automatique des volets hors compétence à partir des compétences BANATIC.

Voir spec_priorisation/SPEC.md pour la logique détaillée. En résumé, pour une
collectivité on détermine les couples (levier, catégorie) qu'elle ne peut pas
mobiliser au vu de ses compétences BANATIC, puis on écrit le complément dans
priorisation_hors_competence.

Les compétences sont lues sur la base prod en lecture seule (get_engine_prod) ;
l'écriture éventuelle se fait ailleurs, uniquement sur l'OLAP (get_engine).
"""

from __future__ import annotations

import unicodedata
from functools import lru_cache
from pathlib import Path

import pandas as pd
from sqlalchemy import text

try:
    import streamlit as st
except Exception:  # pragma: no cover - permet l'import hors contexte Streamlit
    st = None  # type: ignore

from utils.db import get_engine, get_engine_prod


# ==========================
# Constantes de l'algorithme
# ==========================

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "priorisation_competence"

# Correspondance catégorie -> tag de compétence requis (SPEC).
CATEGORIE_TAG: dict[int, str] = {1: "ope", 2: "plan", 3: "fin", 5: "patri"}
# Catégories transverses : toujours retenues hors exception A.
CATEGORIES_TRANSVERSES: tuple[int, ...] = (4, 6)
# Catégories croisées avec les tags de compétence.
CATEGORIES_TAGGEES: tuple[int, ...] = (1, 2, 3, 5)
# Règle D : ces codes rouvrent le financement (cat 3) sur tous les leviers.
CODES_FINANCEMENT_GENERIQUE: frozenset[int] = frozenset({1540, 1560, 3505, 3005})

NB_CATEGORIES = 6


def _nfc(value: object) -> str:
    """Normalisation NFC, sans strip agressif ni lowercase (accents/casse = clé)."""
    return unicodedata.normalize("NFC", str(value))


def _cache(func):
    """Cache Streamlit si dispo, sinon lru_cache pour usage hors app."""
    if st is not None:
        return st.cache_data(ttl="1h", show_spinner=False)(func)
    return lru_cache(maxsize=None)(func)


# ==========================
# Chargement des référentiels CSV (utf-8)
# ==========================


@_cache
def load_leviers() -> list[str]:
    """Les 29 leviers, libellés exacts (source de vérité pour l'orthographe)."""
    df = pd.read_csv(DATA_DIR / "leviers.csv", encoding="utf-8")
    return [str(x) for x in df["levier"].tolist()]


@_cache
def _canonical_by_nfc() -> dict[str, str]:
    """Mappe la forme NFC d'un levier vers son libellé canonique (leviers.csv)."""
    return {_nfc(levier): levier for levier in load_leviers()}


def _canonical_levier(value: object) -> str | None:
    """Renvoie le libellé canonique d'un levier, ou None s'il est inconnu."""
    return _canonical_by_nfc().get(_nfc(value))


@_cache
def load_competence_levier() -> dict[str, set[int]]:
    """levier canonique -> ensemble des competence_code qui donnent prise dessus."""
    df = pd.read_csv(DATA_DIR / "competence_levier.csv", encoding="utf-8")
    mapping: dict[str, set[int]] = {}
    for _, row in df.iterrows():
        levier = _canonical_levier(row["levier"])
        if levier is None:
            continue
        mapping.setdefault(levier, set()).add(int(row["competence_code"]))
    return mapping


@_cache
def load_competence_tags() -> dict[int, set[str]]:
    """competence_code -> ensemble des tags (format long : une ligne par tag)."""
    df = pd.read_csv(DATA_DIR / "competence_tags.csv", encoding="utf-8")
    mapping: dict[int, set[str]] = {}
    for _, row in df.iterrows():
        mapping.setdefault(int(row["competence_code"]), set()).add(str(row["tag"]))
    return mapping


@_cache
def load_exceptions_a() -> dict[str, set[int]]:
    """levier canonique -> liste blanche fermée de catégories (exception A)."""
    df = pd.read_csv(DATA_DIR / "exceptions_a_leviers_restreints.csv", encoding="utf-8")
    mapping: dict[str, set[int]] = {}
    for _, row in df.iterrows():
        levier = _canonical_levier(row["levier"])
        if levier is None:
            continue
        mapping.setdefault(levier, set()).add(int(row["categorie_id"]))
    return mapping


@_cache
def load_exemplarite_regles() -> dict[str, str]:
    """levier canonique -> règle exemplarité ('exclu' ou 'toujours_ouvert')."""
    df = pd.read_csv(DATA_DIR / "exemplarite_regles.csv", encoding="utf-8")
    mapping: dict[str, str] = {}
    for _, row in df.iterrows():
        levier = _canonical_levier(row["levier"])
        if levier is None:
            continue
        mapping[levier] = str(row["regle"])
    return mapping


# ==========================
# Cœur du calcul
# ==========================


def volets_retenus(comps: set[int]) -> set[tuple[str, int]]:
    """Ensemble des couples (levier, catégorie) retenus pour ces compétences.

    Applique l'algorithme de la SPEC dans l'ordre exact :
    1) exception A (court-circuit), 2) transverses 4/6, 3) croisement tags
    sur 1/2/3/5, 4) règle C (exemplarité toujours ouverte), 5) règle D
    (financement générique), 6) règle B (exclusion exemplarité, dernier mot).
    """
    comps = {int(c) for c in comps}
    leviers = load_leviers()
    levier_to_codes = load_competence_levier()
    code_tags = load_competence_tags()
    exceptions_a = load_exceptions_a()
    regles = load_exemplarite_regles()

    finance_generique = bool(comps & CODES_FINANCEMENT_GENERIQUE)
    retenus: set[tuple[str, int]] = set()

    for levier in leviers:
        # Étape 1 : exception A écrase tout pour ce levier.
        if levier in exceptions_a:
            for cat in exceptions_a[levier]:
                retenus.add((levier, cat))
            continue

        # Étape 2 : catégories transverses.
        for cat in CATEGORIES_TRANSVERSES:
            retenus.add((levier, cat))

        # Étape 3 : croisement standard sur les catégories taggées.
        tags_disponibles: set[str] = set()
        for code in comps & levier_to_codes.get(levier, set()):
            tags_disponibles |= code_tags.get(code, set())
        for cat in CATEGORIES_TAGGEES:
            if CATEGORIE_TAG[cat] in tags_disponibles:
                retenus.add((levier, cat))

        # Étape 4 : règle C, exemplarité toujours ouverte.
        if regles.get(levier) == "toujours_ouvert":
            retenus.add((levier, 5))

        # Étape 5 : règle D, financement générique.
        if finance_generique:
            retenus.add((levier, 3))

        # Étape 6 : règle B, exclusion exemplarité (dernier mot).
        if regles.get(levier) == "exclu":
            retenus.discard((levier, 5))

    return retenus


def univers_volets() -> set[tuple[str, int]]:
    """Les 29 leviers x 6 catégories = 174 volets possibles."""
    return {
        (levier, cat)
        for levier in load_leviers()
        for cat in range(1, NB_CATEGORIES + 1)
    }


def compute_hors_competence(comps: set[int]) -> set[tuple[str, int]]:
    """Volets hors compétence = univers complet moins volets retenus."""
    return univers_volets() - volets_retenus(comps)


# ==========================
# Accès aux compétences BANATIC (prod, lecture seule)
# ==========================


def get_siren(collectivite_id: int) -> str | None:
    """SIREN officiel de la collectivité depuis la prod (public.collectivite).

    On lit le SIREN sur la prod (source de vérité, aligné sur la SPEC) plutôt
    que le code_siren_insee de l'OLAP qui peut être un code INSEE pour les
    communes. L'identifiant est partagé entre prod et OLAP.
    """
    engine = get_engine_prod()
    with engine.connect() as conn:
        row = conn.execute(
            text("SELECT siren FROM public.collectivite WHERE id = :id"),
            {"id": int(collectivite_id)},
        ).fetchone()
    if not row or row[0] is None:
        return None
    siren = str(row[0]).strip()
    return siren or None


@_cache
def fetch_competences(collectivite_id: int) -> frozenset[int]:
    """Codes compétence BANATIC d'une collectivité (prod, via SIREN).

    Une collectivité sans SIREN exploitable ou absente de BANATIC renvoie un
    ensemble vide : elle recevra tous les volets non transverses en hors
    compétence (hors réouvertures des règles C/D), conformément à la SPEC.
    """
    siren = get_siren(collectivite_id)
    if not siren:
        return frozenset()
    engine = get_engine_prod()
    with engine.connect() as conn:
        df = pd.read_sql_query(
            text(
                """
                SELECT DISTINCT cb.competence_code
                FROM imports.competence_banatic cb
                JOIN public.banatic_competence bc ON bc.code = cb.competence_code
                WHERE cb.siren = :siren
                """
            ),
            conn,
            params={"siren": siren},
        )
    return frozenset(int(x) for x in df["competence_code"].dropna())


def compute_hors_competence_for_collectivite(
    collectivite_id: int,
) -> set[tuple[str, int]]:
    """Raccourci : récupère les compétences BANATIC puis calcule le hors compétence."""
    comps = set(fetch_competences(collectivite_id))
    return compute_hors_competence(comps)


def save_hors_competence(
    collectivite_id: int,
    exclusions: set[tuple[str, int]] | list[tuple[str, int]],
) -> int:
    """Remplace les exclusions d'une collectivité sur l'OLAP (une transaction).

    Recalcul complet et idempotent : suppression des lignes existantes puis
    insertion des nouvelles. Écriture uniquement sur l'OLAP (get_engine),
    conformément aux règles du projet. Renvoie le nombre de lignes insérées.
    """
    rows = sorted(exclusions, key=lambda x: (x[0], x[1]))
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(
            text(
                "DELETE FROM priorisation_hors_competence "
                "WHERE collectivite_id = :collectivite_id"
            ),
            {"collectivite_id": int(collectivite_id)},
        )
        if rows:
            conn.execute(
                text(
                    """
                    INSERT INTO priorisation_hors_competence
                        (collectivite_id, levier, categorie)
                    VALUES (:collectivite_id, :levier, :categorie)
                    """
                ),
                [
                    {
                        "collectivite_id": int(collectivite_id),
                        "levier": levier,
                        "categorie": int(cat),
                    }
                    for levier, cat in rows
                ],
            )
    return len(rows)


# ==========================
# Non-régression (valeurs figées, cf. SPEC.md § Contrôles)
# ==========================

# Volets retenus pour un ensemble de compétences vide (invariant #5).
EMPTY_BASELINE_RETENUS = 75
# Volets fermés structurellement par les règles A et B, quelles que soient les
# compétences détenues (invariant #6) : catégories hors liste blanche des
# leviers de la règle A + catégorie 5 des leviers `exclu` hors règle A.
STRUCTURAL_CLOSURES_COUNT = 20


def count_empty_baseline_retenus() -> int:
    """Nombre de volets retenus pour une collectivité sans aucune compétence."""
    return len(univers_volets()) - len(compute_hors_competence(set()))


def count_structural_closures() -> int:
    """Volets universellement inexistants, fermés par les règles A et B.

    - Règle A : pour chaque levier de la liste A, les catégories hors de sa
      liste blanche ne sont jamais retenues (NB_CATEGORIES - taille liste blanche).
    - Règle B : la catégorie 5 des leviers `exclu` qui ne sont pas en règle A est
      systématiquement retirée à l'étape 6, donc jamais retenue.
    """
    exceptions_a = load_exceptions_a()
    regles = load_exemplarite_regles()

    total = sum(NB_CATEGORIES - len(cats) for cats in exceptions_a.values())
    for levier in load_leviers():
        if regles.get(levier) == "exclu" and levier not in exceptions_a:
            total += 1
    return total


# ==========================
# Contrôles / invariants (SPEC)
# ==========================


def check_invariants(hors: set[tuple[str, int]]) -> list[str]:
    """Vérifie les invariants de la SPEC, renvoie la liste des anomalies."""
    anomalies: list[str] = []
    leviers = set(load_leviers())
    exceptions_a = load_exceptions_a()
    regles = load_exemplarite_regles()
    retenus = univers_volets() - hors

    # 1. Pas de catégorie 4/6 hors compétence pour un levier absent de A.
    for levier, cat in hors:
        if cat in CATEGORIES_TRANSVERSES and levier not in exceptions_a:
            anomalies.append(
                f"Catégorie transverse {cat} hors compétence sur '{levier}' (hors liste A)"
            )

    # 2. Aucun levier B présent avec une catégorie 5 dans les volets retenus.
    for levier, regle in regles.items():
        if regle == "exclu" and (levier, 5) in retenus:
            anomalies.append(f"Levier B '{levier}' retenu en catégorie 5")

    # 3. Nombre de volets retenus entre 0 et 174.
    if not 0 <= len(retenus) <= len(leviers) * NB_CATEGORIES:
        anomalies.append(f"Nombre de volets retenus hors bornes : {len(retenus)}")

    # 4. Tous les libellés écrits appartiennent aux 29 leviers.
    for levier, _cat in hors:
        if levier not in leviers:
            anomalies.append(f"Levier inconnu écrit : '{levier}'")

    return anomalies
