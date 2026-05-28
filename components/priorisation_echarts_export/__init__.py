"""Composant Streamlit : capture de deux graphiques ECharts en PNG."""

from pathlib import Path

import streamlit.components.v1 as components

_COMPONENT_DIR = Path(__file__).parent / "frontend"
_priorisation_echarts_export = components.declare_component(
    "priorisation_echarts_export",
    path=str(_COMPONENT_DIR),
)


def priorisation_echarts_export(
    treemap_option: dict,
    bar_option: dict,
    treemap_height: int,
    bar_height: int,
    key: str | None = None,
) -> dict | None:
    """Rend deux graphiques ECharts hors écran et retourne leurs PNG base64."""
    return _priorisation_echarts_export(
        treemap_option=treemap_option,
        bar_option=bar_option,
        treemap_height=treemap_height,
        bar_height=bar_height,
        key=key,
        default=None,
    )
