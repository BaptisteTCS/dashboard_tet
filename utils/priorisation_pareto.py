"""Seuil Pareto sur les volets (levier × catégorie) — partagé entre pages priorisation."""

from __future__ import annotations

import pandas as pd
import streamlit as st

CibleKey = tuple[str, int]

VUE_ENSEMBLE_THRESHOLDS = [50, 60, 70, 80, 90, 100]

SLIDER_LABEL = (
    "Seuil d'impact des volets (%)"
)
SLIDER_HELP = (
    "Conserve le minimum de volets (levier × levier d'action) les plus contributrices "
    "dont le potentiel cumulé atteint ce seuil. "
    "Ex. : 80 % = les volets les plus impactantes qui représentent au moins 80 % "
    "du potentiel total affiché sur la cartographie."
)


def enjeu_cible(
    levier: str,
    cat: int,
    reductions: dict[str, float],
    weights: dict[str, dict[int, float]],
) -> float:
    if levier not in reductions:
        return 0.0
    poids = weights.get(levier, {}).get(cat)
    if poids is None or pd.isna(poids) or poids == 0:
        return 0.0
    return abs(float(reductions[levier])) * float(poids)


def list_cibles_enjeu(
    leviers: list[str],
    reductions: dict[str, float],
    weights: dict[str, dict[int, float]],
    exclusions: set[CibleKey],
) -> list[tuple[CibleKey, float]]:
    contributions: list[tuple[CibleKey, float]] = []
    for levier in leviers:
        if levier not in reductions:
            continue
        for cat in range(1, 7):
            if (levier, cat) in exclusions:
                continue
            enjeu = enjeu_cible(levier, cat, reductions, weights)
            if enjeu > 0:
                contributions.append(((levier, cat), enjeu))
    return contributions


def select_cibles_pareto(
    leviers: list[str],
    reductions: dict[str, float],
    weights: dict[str, dict[int, float]],
    exclusions: set[CibleKey],
    threshold_pct: int,
) -> set[CibleKey]:
    """Plus petit ensemble de cibles couvrant au moins threshold_pct % du potentiel total."""
    contributions = list_cibles_enjeu(leviers, reductions, weights, exclusions)
    if not contributions:
        return set()

    total = sum(value for _, value in contributions)
    if total == 0:
        return set()

    contributions.sort(key=lambda item: item[1], reverse=True)
    target = total * threshold_pct / 100
    selected: set[CibleKey] = set()
    cumul = 0.0
    for key, value in contributions:
        selected.add(key)
        cumul += value
        if cumul >= target:
            break
    return selected


def render_seuil_impact_cibles_expander(
    leviers: list[str],
    reductions: dict[str, float],
    weights: dict[str, dict[int, float]],
    exclusions: set[CibleKey],
    *,
    key_prefix: str,
    default_threshold: int = 80,
    expander_label: str = "Seuil d'impact",
) -> tuple[int, set[CibleKey]]:
    """Affiche l'expander Pareto et retourne (seuil %, volet retenues)."""
    with st.expander(expander_label):
        threshold_pct = st.select_slider(
            SLIDER_LABEL,
            options=VUE_ENSEMBLE_THRESHOLDS,
            value=default_threshold,
            key=f"{key_prefix}_threshold",
            help=SLIDER_HELP,
        )
        selected_cibles = select_cibles_pareto(
            leviers, reductions, weights, exclusions, threshold_pct
        )
        n_cibles_total = len(
            list_cibles_enjeu(leviers, reductions, weights, exclusions)
        )
        st.caption(
            f"**{len(selected_cibles)}** volets retenues sur {n_cibles_total}"
        )
        st.info("""Pour faciliter la lecture et porter l'effort sur les actions à plus fort impact, 
        nous recommandons un seuil de **80 %** : vous voyez directement les volets qui concentrent 
        **80 % du potentiel total de réduction** des émissions de GES. Le reste est masqué, mais le 
        curseur reste **ajustable** selon vos besoins.""")
    return threshold_pct, selected_cibles
