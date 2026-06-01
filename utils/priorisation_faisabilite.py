"""Calculs faisabilité politique — angles morts et top leviers sous-mobilisés."""

from __future__ import annotations

from utils.priorisation_impact_charts import CATEGORIES

FAISABILITE_LABELS = {
    1: "Hors de portée politique",
    2: "À discuter",
    3: "Prioritaire",
}

TOP_N = 10


def _poids_angle_mort(
    levier: str,
    cat: int,
    notes: dict[tuple[str, int], int],
    exclusions: set[tuple[str, int]],
    weights: dict[str, dict[int, float]],
) -> float | None:
    if (levier, cat) in exclusions:
        return None
    poids = weights.get(levier, {}).get(cat, 0.0)
    if poids <= 0:
        return None
    note = notes.get((levier, cat), 0)
    if note not in (0, 1):
        return None
    return poids


def angle_mort_categories(
    levier: str,
    notes: dict[tuple[str, int], int],
    exclusions: set[tuple[str, int]],
    weights: dict[str, dict[int, float]],
) -> list[int]:
    return [
        cat
        for cat in range(1, 7)
        if _poids_angle_mort(levier, cat, notes, exclusions, weights) is not None
    ]


def calc_potentiel_non_mobilise(
    levier: str,
    reduction: float,
    notes: dict[tuple[str, int], int],
    exclusions: set[tuple[str, int]],
    weights: dict[str, dict[int, float]],
) -> float:
    somme_poids = sum(
        p
        for cat in range(1, 7)
        if (p := _poids_angle_mort(levier, cat, notes, exclusions, weights)) is not None
    )
    return abs(reduction) * somme_poids


def top_leviers_angles_morts(
    leviers: list[str],
    reductions: dict[str, float],
    notes: dict[tuple[str, int], int],
    exclusions: set[tuple[str, int]],
    weights: dict[str, dict[int, float]],
    n: int = TOP_N,
) -> list[tuple[str, float]]:
    scored: list[tuple[str, float]] = []
    for levier in leviers:
        if levier not in reductions:
            continue
        potentiel = calc_potentiel_non_mobilise(
            levier, reductions[levier], notes, exclusions, weights
        )
        if potentiel > 0:
            scored.append((levier, potentiel))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:n]


def build_top_leviers_faisabilite_pdf(
    leviers: list[str],
    reductions: dict[str, float],
    notes: dict[tuple[str, int], int],
    exclusions: set[tuple[str, int]],
    weights: dict[str, dict[int, float]],
    faisabilites: dict[tuple[str, int], int],
) -> list[dict]:
    """Top 10 leviers sous-mobilisés avec arbitrages faisabilité par catégorie."""
    entries: list[dict] = []
    for rank, (levier, potentiel) in enumerate(
        top_leviers_angles_morts(
            leviers, reductions, notes, exclusions, weights
        ),
        start=1,
    ):
        categories = []
        for cat in angle_mort_categories(levier, notes, exclusions, weights):
            fais = faisabilites.get((levier, cat))
            categories.append(
                {
                    "categorie": CATEGORIES[cat],
                    "faisabilite": FAISABILITE_LABELS.get(fais, "Non renseigné"),
                }
            )
        entries.append(
            {
                "rank": rank,
                "levier": levier,
                "potentiel": potentiel,
                "categories": categories,
            }
        )
    return entries


def faisabilites_from_rows(
    rows: list[tuple[str, int, int]],
    notes: dict[tuple[str, int], int],
    exclusions: set[tuple[str, int]],
    weights: dict[str, dict[int, float]],
) -> dict[tuple[str, int], int]:
    result: dict[tuple[str, int], int] = {}
    for levier, cat, fais in rows:
        if fais not in FAISABILITE_LABELS:
            continue
        if cat not in angle_mort_categories(levier, notes, exclusions, weights):
            continue
        result[(levier, cat)] = fais
    return result
