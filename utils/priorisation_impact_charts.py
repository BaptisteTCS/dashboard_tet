"""Impact Map et Impact Chart — partagés entre diagnostic (30) et synthèse (34)."""

from __future__ import annotations

from collections.abc import Callable

import pandas as pd
import streamlit as st
from streamlit_echarts import JsCode, st_echarts

CATEGORIES = {
    1: "Aménagement",
    2: "Réglementation",
    3: "Financement",
    4: "Gouvernance",
    5: "Exemplarité",
    6: "Sensibilisation",
}

NOTE_LABELS = {
    0: "Non mobilisé",
    1: "Partiellement mobilisé",
    2: "Bien mobilisé",
    3: "Pleinement mobilisé",
}

NOTE_COLORS = {
    0: "#E2E5E9",
    1: "#f5ebe0",
    2: "#5DCF69",
    3: "#389D49",
}

COLOR_ACTION_RETENUE = "#D84315"

NOTES_ENJEU_BAS = {0, 1}

LEVIER_LABELS = {
    "Captage de méthane dans les ISDND": "Captage méthane",
    "Biogaz": "Biogaz",
    "Véhicules électriques": "Véhicules électriques",
    "Efficacité et carburants décarbonés des véhicules privés": "Carburants décarbonés",
    "Sobriété des bâtiments (résidentiel)": "Sobriété bâtiments résidentiel",
    "Pratiques stockantes": "Pratiques stockantes",
    "Changement chaudières gaz + rénovation (résidentiel)": "Chaudières gaz & rénovation résidentiel",
    "Vélo et transport en commun": "Vélo & TEC",
    "Bus et cars décarbonés": "Bus et cars décarbonés",
    "Changement de chaudière à fioul (tertiaire)": "Chaudière fioul (tertiaire)",
    "Réduction des déplacements": "Réduction des déplacements",
    "Sobriété et isolation des bâtiments (tertiaire)": "Sobriété et isolation des bâtiments (tertiaire)",
    "Gestion des forêts et produits bois": "Gestion des forêts",
    "Changements de pratiques de fertilisation azotée": "Fertilisation azotée",
    "Elevage durable": "Elevage durable",
    "Bâtiments & Machines agricoles": "Bâtiments & Machines agricoles",
    "Valorisation matière des déchets": "Valorisation déchets",
    "Changement chaudières fioul + rénovation (résidentiel)": "Chaudières fioul & rénovation (résidentiel)",
    "Gestion des haies": "Gestion des haies",
    "Sobriété foncière": "Sobriété foncière",
    "Réseaux de chaleur décarbonés": "Réseaux de chaleur",
    "Prévention des déchets": "Prévention des déchets",
    "Changement de chaudière à gaz (tertiaire)": "Chaudière gaz (tertiaire)",
    "Fret décarboné et multimodalité": "Fret décarboné",
    "Electricité renouvelable": "Electricité renouvelable",
    "Efficacité et sobriété logistique": "Sobriété logistique",
    "Covoiturage": "Covoiturage",
    "Production Industrielle": "Production Industrielle",
    "Gestion des prairies": "Gestion des prairies",
}

TREEMAP_HEIGHT = 700
VUE_ENSEMBLE_CHART_HEIGHT = 700
VUE_ENSEMBLE_CHART_HEIGHT_SYNTHESE = 700

TREEMAP_CLICK_EVENTS = {
    "click": """
    function(params) {
        var d = params.data;
        if (!d || !d.levierName) return null;
        return {
            levier: d.levierName,
            categorie: d.categorieName,
            categorieId: d.categorieId,
        };
    }
    """,
}


def levier_label_court(levier: str) -> str:
    return LEVIER_LABELS.get(levier, levier)


def case_color(
    levier: str,
    cat: int,
    note: int,
    cibles_actions: set[tuple[str, int]] | None,
) -> str:
    """Orange si cible peu mobilisée avec action retenue (mode synthèse)."""
    if (
        cibles_actions is not None
        and note in NOTES_ENJEU_BAS
        and (levier, cat) in cibles_actions
    ):
        return COLOR_ACTION_RETENUE
    return NOTE_COLORS.get(note, NOTE_COLORS[0])


def build_treemap_data(
    leviers: list[str],
    reductions: dict[str, float],
    notes: dict[tuple[str, int], int],
    weights: dict[str, dict[int, float]],
    exclusions: set[tuple[str, int]],
    *,
    cibles_actions: set[tuple[str, int]] | None = None,
    selected_cibles: set[tuple[str, int]] | None = None,
) -> tuple[list[dict], list[str]]:
    """Treemap : taille = enjeu relatif, couleur = mobilisation (± actions retenues)."""
    excluded_leviers: list[str] = []
    children: list[dict] = []

    for levier in sorted(leviers):
        if levier not in reductions:
            excluded_leviers.append(levier)
            continue

        reduction_abs = abs(float(reductions[levier]))
        levier_weights = weights.get(levier, {})
        cat_nodes: list[dict] = []

        for cat in range(1, 7):
            if (levier, cat) in exclusions:
                continue
            if selected_cibles is not None and (levier, cat) not in selected_cibles:
                continue
            poids = levier_weights.get(cat)
            if poids is None or pd.isna(poids) or poids == 0:
                continue

            taille = reduction_abs * float(poids)
            if taille == 0:
                continue

            note = int(notes.get((levier, cat), 0))
            categorie = CATEGORIES[cat]
            has_action = (
                cibles_actions is not None
                and (levier, cat) in cibles_actions
                and note in NOTES_ENJEU_BAS
            )
            node: dict = {
                "name": f"{levier_label_court(levier)}\n{categorie}",
                "value": round(taille, 2),
                "itemStyle": {"color": case_color(levier, cat, note, cibles_actions)},
                "levierName": levier,
                "categorieName": categorie,
                "categorieId": cat,
                "noteLevel": NOTE_LABELS.get(note, NOTE_LABELS[0]),
            }
            if cibles_actions is not None:
                node["actionRetenue"] = has_action
            cat_nodes.append(node)

        if cat_nodes:
            children.append({"name": levier, "children": cat_nodes})

    return children, excluded_leviers


def build_priorisation_cases(
    leviers: list[str],
    reductions: dict[str, float],
    notes: dict[tuple[str, int], int],
    weights: dict[str, dict[int, float]],
    exclusions: set[tuple[str, int]],
    *,
    cibles_actions: set[tuple[str, int]] | None = None,
    selected_cibles: set[tuple[str, int]] | None = None,
) -> list[dict]:
    """Cases levier × catégorie avec note et enjeu (ktCO₂e)."""
    cases: list[dict] = []
    for levier in sorted(leviers):
        if levier not in reductions:
            continue
        reduction_abs = abs(float(reductions[levier]))
        levier_weights = weights.get(levier, {})
        for cat in range(1, 7):
            if (levier, cat) in exclusions:
                continue
            if selected_cibles is not None and (levier, cat) not in selected_cibles:
                continue
            poids = levier_weights.get(cat)
            if poids is None or pd.isna(poids) or poids == 0:
                continue
            enjeu = reduction_abs * float(poids)
            if enjeu == 0:
                continue
            note = int(notes.get((levier, cat), 0))
            case: dict = {
                "levier": levier,
                "categorie": CATEGORIES[cat],
                "categorie_id": cat,
                "note": note,
                "enjeu": round(enjeu, 2),
                "label": f"{levier_label_court(levier)} · {CATEGORIES[cat]}",
            }
            if cibles_actions is not None:
                action_retenue = (
                    (levier, cat) in cibles_actions and note in NOTES_ENJEU_BAS
                )
                case["color"] = case_color(levier, cat, note, cibles_actions)
                case["action_retenue"] = action_retenue
            cases.append(case)
    return cases


def case_sort_value(case: dict) -> float:
    """Tri décroissant : positif (vert / orange) à gauche, négatif (gris) à droite."""
    enjeu = case["enjeu"]
    if case["note"] in NOTES_ENJEU_BAS and not case.get("action_retenue"):
        return -enjeu
    return enjeu


def case_chart_value(case: dict) -> float:
    """Valeur signée pour les barres (négatif = peu mobilisé sans action retenue)."""
    if case["note"] in NOTES_ENJEU_BAS and not case.get("action_retenue"):
        return -case["enjeu"]
    return case["enjeu"]


def build_vue_ensemble_bar_options(cases: list[dict]) -> dict | None:
    """Barres verticales, couleur par note, tri par enjeu signé décroissant."""
    if not cases:
        return None

    ordered = sorted(cases, key=case_sort_value, reverse=True)
    series_data = []
    for c in ordered:
        chart_val = case_chart_value(c)
        color = c.get("color", NOTE_COLORS.get(c["note"], NOTE_COLORS[0]))
        point: dict = {
            "value": chart_val,
            "levierFull": c["levier"],
            "categorie": c["categorie"],
            "noteLevel": NOTE_LABELS.get(c["note"], NOTE_LABELS[0]),
            "itemStyle": {
                "color": color,
                "borderRadius": (
                    [6, 6, 0, 0] if chart_val >= 0 else [0, 0, 6, 6]
                ),
                "shadowColor": "rgba(0,0,0,0.06)",
                "shadowBlur": 6,
            },
        }
        if "action_retenue" in c:
            point["actionRetenue"] = c["action_retenue"]
        series_data.append(point)

    return {
        "backgroundColor": "transparent",
        "animationDuration": 600,
        "animationEasing": "cubicOut",
        "grid": {
            "left": 48,
            "right": 24,
            "top": 40,
            "bottom": 32,
            "containLabel": False,
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "shadow", "shadowStyle": {"opacity": 0.08}},
            "formatter": JsCode(
                """
                function(params) {
                    var p = params && params[0];
                    if (!p || !p.data) return '';
                    var d = p.data;
                    var val = Math.abs(Number(p.value)).toFixed(1);
                    var lines = (d.levierFull || '') + '<br/>'
                        + (d.categorie || '') + '<br/>'
                        + (d.noteLevel || '') + '<br/>'
                        + '<b>' + val + ' ktCO₂e</b>';
                    if (d.actionRetenue) {
                        lines += '<br/><b>Actions retenues</b>';
                    }
                    return lines;
                }
                """
            ),
        },
        "xAxis": {
            "type": "category",
            "data": [""] * len(ordered),
            "axisLine": {"show": False},
            "axisTick": {"show": False},
            "axisLabel": {"show": False},
        },
        "yAxis": {
            "type": "value",
            "name": "ktCO₂e",
            "nameTextStyle": {"color": "#888", "fontSize": 11},
            "axisLine": {"show": False},
            "axisTick": {"show": False},
            "axisLabel": {"color": "#888", "fontSize": 11},
            "splitLine": {"lineStyle": {"color": "#ebebeb", "type": "dashed"}},
        },
        "series": [
            {
                "type": "bar",
                "data": series_data,
                "barMaxWidth": 36,
                "emphasis": {
                    "itemStyle": {
                        "shadowColor": "rgba(0,0,0,0.12)",
                        "shadowBlur": 10,
                    }
                },
                "label": {"show": False},
            }
        ],
    }


def prepare_treemap_display_data(
    treemap_children: list[dict], *, show_labels: bool
) -> list[dict]:
    if show_labels:
        return treemap_children
    return [
        {
            **levier_node,
            "children": [{**leaf, "name": ""} for leaf in levier_node["children"]],
        }
        for levier_node in treemap_children
    ]


def _treemap_series_config(display_data: list[dict]) -> list[dict]:
    return [
        {
            "type": "treemap",
            "roam": False,
            "nodeClick": False,
            "left": 0,
            "top": 0,
            "right": 0,
            "bottom": 0,
            "breadcrumb": {"show": False},
            "levels": [
                {
                    "itemStyle": {
                        "borderColor": "#444",
                        "borderWidth": 1,
                        "gapWidth": 1,
                    },
                    "upperLabel": {"show": False},
                    "label": {"show": False},
                },
                {
                    "itemStyle": {
                        "borderColor": "#fff",
                        "borderWidth": 1,
                        "gapWidth": 1,
                    },
                    "label": {
                        "show": True,
                        "fontSize": 10,
                        "lineHeight": 14,
                        "color": "#333",
                        "overflow": "break",
                        "width": 80,
                    },
                    "upperLabel": {"show": False},
                },
            ],
            "data": display_data,
        }
    ]


def build_echarts_options(
    treemap_children: list[dict], *, show_labels: bool = True
) -> dict:
    display_data = prepare_treemap_display_data(
        treemap_children, show_labels=show_labels
    )
    return {
        "backgroundColor": "transparent",
        "tooltip": {
            "formatter": JsCode(
                """
                function(params) {
                    var d = params.data;
                    if (!d || !d.levierName) return '';
                    var taille = Number(d.value).toFixed(1);
                    var lines = d.levierName + '<br/>'
                        + d.categorieName + '<br/>'
                        + 'Note : ' + d.noteLevel + '<br/>'
                        + 'Taille : ' + taille + ' ktCO2';
                    if (d.actionRetenue) {
                        lines += '<br/><b>Actions retenues</b>';
                    }
                    return lines;
                }
                """
            ),
        },
        "series": _treemap_series_config(display_data),
    }


def build_bar_export_options(cases: list[dict]) -> dict | None:
    """Options bar chart sérialisables (sans JsCode) pour export PNG / PDF."""
    if not cases:
        return None

    ordered = sorted(cases, key=case_sort_value, reverse=True)
    series_data = []
    for c in ordered:
        chart_val = case_chart_value(c)
        color = c.get("color", NOTE_COLORS.get(c["note"], NOTE_COLORS[0]))
        point: dict = {
            "value": chart_val,
            "itemStyle": {
                "color": color,
                "borderRadius": (
                    [6, 6, 0, 0] if chart_val >= 0 else [0, 0, 6, 6]
                ),
                "shadowColor": "rgba(0,0,0,0.06)",
                "shadowBlur": 6,
            },
        }
        series_data.append(point)

    return {
        "backgroundColor": "#ffffff",
        "animation": False,
        "tooltip": {"show": False},
        "grid": {
            "left": 48,
            "right": 24,
            "top": 40,
            "bottom": 32,
            "containLabel": False,
        },
        "xAxis": {
            "type": "category",
            "data": [""] * len(ordered),
            "axisLine": {"show": False},
            "axisTick": {"show": False},
            "axisLabel": {"show": False},
        },
        "yAxis": {
            "type": "value",
            "name": "ktCO₂e",
            "nameTextStyle": {"color": "#888", "fontSize": 11},
            "axisLine": {"show": False},
            "axisTick": {"show": False},
            "axisLabel": {"color": "#888", "fontSize": 11},
            "splitLine": {"lineStyle": {"color": "#ebebeb", "type": "dashed"}},
        },
        "series": [
            {
                "type": "bar",
                "data": series_data,
                "barMaxWidth": 36,
                "label": {"show": False},
            }
        ],
    }


def build_treemap_export_options(
    treemap_children: list[dict], *, show_labels: bool = True
) -> dict:
    """Options ECharts sérialisables (sans JsCode) pour export PNG / PDF."""
    display_data = prepare_treemap_display_data(
        treemap_children, show_labels=show_labels
    )
    return {
        "backgroundColor": "#ffffff",
        "tooltip": {"show": False},
        "series": _treemap_series_config(display_data),
    }


def render_note_color_legend(*, show_actions_retenues: bool = False) -> None:
    items = "".join(
        f'<span style="display:inline-flex;align-items:center;margin-right:1.5rem;">'
        f'<span style="display:inline-block;width:14px;height:14px;border-radius:3px;'
        f"background:{NOTE_COLORS[note]};border:1px solid rgba(0,0,0,0.12);"
        f'margin-right:0.45rem;flex-shrink:0;"></span>'
        f'<span style="font-size:0.875rem;color:#333;">{NOTE_LABELS[note]}</span>'
        f"</span>"
        for note in range(4)
    )
    if show_actions_retenues:
        items += (
            f'<span style="display:inline-flex;align-items:center;margin-right:1.5rem;">'
            f'<span style="display:inline-block;width:14px;height:14px;border-radius:3px;'
            f"background:{COLOR_ACTION_RETENUE};border:1px solid rgba(0,0,0,0.12);"
            f'margin-right:0.45rem;flex-shrink:0;"></span>'
            f'<span style="font-size:0.875rem;color:#333;">Actions retenues</span>'
            f"</span>"
        )
    st.markdown(
        f'<div style="display:flex;flex-wrap:wrap;align-items:center;'
        f'margin-bottom:0.75rem;">{items}</div>',
        unsafe_allow_html=True,
    )


def extract_chart_event(component_value) -> dict | None:
    """Extrait l'événement JS depuis la valeur retournée par st_echarts v0.6+."""
    if component_value is None:
        return None
    if hasattr(component_value, "chart_event"):
        event = component_value.chart_event
        return event if isinstance(event, dict) else None
    if isinstance(component_value, dict):
        if "chart_event" in component_value:
            event = component_value["chart_event"]
            return event if isinstance(event, dict) else None
        if component_value.get("levier"):
            return component_value
    return None


def render_impact_map(
    treemap_children: list[dict],
    excluded_leviers: list[str],
    *,
    chart_key_prefix: str,
    threshold_pct: int,
    labels_toggle_key: str | None = None,
    show_actions_retenues: bool = False,
    click_events: dict | None = None,
    height: int = TREEMAP_HEIGHT,
    before_chart: Callable[[], None] | None = None,
) -> tuple[bool, object | None]:
    """Affiche l'onglet Impact Map. Retourne (show_labels, valeur st_echarts ou None)."""
    toggle_kwargs: dict = {"label": "Libellés", "value": False}
    if labels_toggle_key is not None:
        toggle_kwargs["key"] = labels_toggle_key
    show_labels = st.toggle(**toggle_kwargs)

    for levier in excluded_leviers:
        st.warning(
            f"Le levier **{levier}** est présent dans la priorisation "
            f"mais sans réduction CO₂ — il est exclu de la treemap."
        )

    if not treemap_children:
        st.info("Aucune case à afficher pour cette collectivité.")
        return show_labels, None

    if before_chart is not None:
        before_chart()

    render_note_color_legend(show_actions_retenues=show_actions_retenues)
    options = build_echarts_options(treemap_children, show_labels=show_labels)
    chart_key = f"{chart_key_prefix}_{threshold_pct}_labels_{int(show_labels)}"
    echarts_kwargs: dict = {
        "options": options,
        "height": f"{height}px",
        "key": chart_key,
    }
    if click_events is not None:
        echarts_kwargs["events"] = click_events
    click = st_echarts(**echarts_kwargs)
    return show_labels, click


def render_impact_chart(
    priorisation_cases: list[dict],
    *,
    chart_key: str,
    show_actions_retenues: bool = False,
    height: int = VUE_ENSEMBLE_CHART_HEIGHT,
) -> None:
    """Affiche l'onglet Impact Chart."""
    vue_options = build_vue_ensemble_bar_options(priorisation_cases)
    if vue_options is None:
        st.info("Aucune case à afficher pour ce seuil.")
        return
    render_note_color_legend(show_actions_retenues=show_actions_retenues)
    st_echarts(
        options=vue_options,
        height=f"{height}px",
        key=chart_key,
    )
