"""Composant Streamlit : capture de graphiques ECharts en PNG."""

from pathlib import Path

import streamlit.components.v1 as components

_COMPONENT_DIR = Path(__file__).parent / "frontend"
_priorisation_echarts_export = components.declare_component(
    "priorisation_echarts_export",
    path=str(_COMPONENT_DIR),
)


def priorisation_echarts_export(
    charts: list[dict],
    key: str | None = None,
) -> dict | None:
    """Rend des graphiques ECharts hors écran et retourne leurs PNG base64.

    Chaque élément de ``charts`` : ``{"type": "treemap"|"bar", "option": dict, "height": int}``.
    Retourne ``{"pngs": [data_url, ...]}`` dans le même ordre.
    """
    return _priorisation_echarts_export(
        charts=charts,
        key=key,
        default=None,
    )
