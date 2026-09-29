"""Matrice d'impact des leviers — mobilisation OLAP × potentiel CO₂ (données BDD)."""

from __future__ import annotations

import statistics
from typing import Any

import pandas as pd

QUADRANT_LABELS = {
    "angles_morts": "Angles morts",
    "bien_couvert": "Bien couvert",
    "faible_enjeu": "Faible enjeu",
    "bien_investi": "Bien investi",
}

QUADRANT_TITLES = {
    "angles_morts": "ANGLES MORTS : FORT IMPACT, PEU MOBILISÉ",
    "bien_couvert": "BIEN COUVERT",
    "faible_enjeu": "FAIBLE ENJEU",
    "bien_investi": "BIEN INVESTI : IMPACT LIMITÉ",
}

MATRICE_COLUMNS = [
    "levier",
    "mobilisation_pct",
    "potentiel_ktco2e",
    "quadrant",
    "quadrant_label",
    "y_seuil",
]

X_SEUIL_DEFAULT = 50.0
COLOR_ANGLES_MORTS = "#FFF8E1"
COLOR_POINT = "#4A90D9"
COLOR_POINT_ANGLES_MORTS = "#1565C0"
CHART_HEIGHT = 600


def mobilisation_levier_pct(
    levier: str,
    notes: dict[tuple[str, int], int],
    weights: dict[str, dict[int, float]],
    exclusions: set[tuple[str, int]],
) -> float | None:
    """Moyenne pondérée des notes volet (0–3) du levier → pourcentage (3/3 = 100 %)."""
    weighted_sum = 0.0
    weight_sum = 0.0
    for cat in range(1, 7):
        if (levier, cat) in exclusions:
            continue
        poids = weights.get(levier, {}).get(cat, 0.0)
        if poids is None or pd.isna(poids) or poids <= 0:
            continue
        note = notes.get((levier, cat))
        if note is None:
            continue
        weighted_sum += int(note) * float(poids)
        weight_sum += float(poids)
    if weight_sum <= 0:
        return None
    return (weighted_sum / weight_sum) / 3.0 * 100.0


def _quadrant_key(mobilisation_pct: float, potentiel: float, y_seuil: float) -> str:
    high_impact = potentiel >= y_seuil
    high_mob = mobilisation_pct >= X_SEUIL_DEFAULT
    if high_impact and not high_mob:
        return "angles_morts"
    if high_impact:
        return "bien_couvert"
    if not high_mob:
        return "faible_enjeu"
    return "bien_investi"


def build_matrice_leviers(
    leviers: list[str],
    notes: dict[tuple[str, int], int],
    weights: dict[str, dict[int, float]],
    reductions: dict[str, float],
    exclusions: set[tuple[str, int]],
) -> tuple[pd.DataFrame, list[str]]:
    """Croise mobilisation OLAP et potentiel de réduction pour chaque levier."""
    rows: list[dict[str, Any]] = []
    excluded: list[str] = []

    for levier in leviers:
        if levier not in reductions:
            excluded.append(f"{levier} (potentiel CO₂ absent)")
            continue
        pct = mobilisation_levier_pct(levier, notes, weights, exclusions)
        if pct is None:
            excluded.append(f"{levier} (aucune note dans le périmètre)")
            continue
        rows.append(
            {
                "levier": levier,
                "mobilisation_pct": pct,
                "potentiel_ktco2e": abs(float(reductions[levier])),
            }
        )

    if not rows:
        return pd.DataFrame(columns=MATRICE_COLUMNS), excluded

    return _assign_quadrants(pd.DataFrame(rows)), excluded


def _assign_quadrants(df: pd.DataFrame) -> pd.DataFrame:
    """Recalcule médiane Y et quadrants sur le DataFrame courant."""
    if df.empty:
        return df
    y_seuil = float(statistics.median(df["potentiel_ktco2e"]))
    df = df.copy()
    df["quadrant"] = df.apply(
        lambda r: _quadrant_key(r["mobilisation_pct"], r["potentiel_ktco2e"], y_seuil),
        axis=1,
    )
    df["quadrant_label"] = df["quadrant"].map(QUADRANT_LABELS)
    df["y_seuil"] = y_seuil
    return df.sort_values("potentiel_ktco2e", ascending=False).reset_index(drop=True)


def filter_matrice_by_potentiel_min(
    df: pd.DataFrame,
    min_ktco2e: float,
) -> pd.DataFrame:
    """Exclut les leviers dont le potentiel est strictement inférieur au seuil."""
    if df.empty or min_ktco2e <= 0:
        return _assign_quadrants(df)
    filtered = df[df["potentiel_ktco2e"] >= min_ktco2e].copy()
    return _assign_quadrants(filtered)


def build_matrice_echarts_options(
    df: pd.DataFrame,
    *,
    x_seuil: float = X_SEUIL_DEFAULT,
    show_all_labels: bool = False,
) -> dict[str, Any] | None:
    """Options ECharts : scatter + quadrants (markArea / markLine / annotations)."""
    from streamlit_echarts import JsCode

    if df.empty:
        return None

    y_seuil = float(df["y_seuil"].iloc[0])
    y_axis_max = max(float(df["potentiel_ktco2e"].max()) * 1.15, y_seuil * 1.5, 1.0)

    scatter_data = []
    for _, row in df.iterrows():
        angle_mort = row["quadrant"] == "angles_morts"
        scatter_data.append(
            {
                "value": [
                    round(float(row["mobilisation_pct"]), 2),
                    round(float(row["potentiel_ktco2e"]), 2),
                ],
                "levier": str(row["levier"]),
                "quadrant": str(row["quadrant_label"]),
                "symbolSize": 14 if angle_mort else 10,
                "label": {
                    "show": bool(angle_mort or show_all_labels),
                    "formatter": str(row["levier"]),
                    "position": "right",
                    "fontSize": 11,
                    "color": "#444",
                },
                "itemStyle": {
                    "color": COLOR_POINT_ANGLES_MORTS if angle_mort else COLOR_POINT,
                },
            }
        )

    return {
        "backgroundColor": "transparent",
        "grid": {"left": 70, "right": 60, "top": 50, "bottom": 70},
        "tooltip": {
            "trigger": "item",
            "formatter": JsCode(
                """
                function(params) {
                    var d = params.data;
                    if (!d || !d.levier) return '';
                    return '<b>' + d.levier + '</b><br/>'
                        + 'Mobilisation : ' + Number(d.value[0]).toFixed(1) + ' %<br/>'
                        + 'Potentiel : ' + Number(d.value[1]).toFixed(1) + ' ktCO₂e<br/>'
                        + d.quadrant;
                }
                """
            ),
        },
        "xAxis": {
            "type": "value",
            "min": 0,
            "max": 100,
            "name": "Mobilisation du levier (%) →",
            "nameLocation": "middle",
            "nameGap": 40,
            "nameTextStyle": {"color": "#666", "fontSize": 12},
            "axisLine": {"lineStyle": {"color": "#ccc"}},
            "axisTick": {"show": False},
            "axisLabel": {"color": "#888", "fontSize": 11, "formatter": "{value} %"},
            "splitLine": {"show": False},
        },
        "yAxis": {
            "type": "value",
            "min": 0,
            "max": round(y_axis_max, 2),
            "name": "Potentiel de réduction (ktCO₂e) →",
            "nameLocation": "middle",
            "nameGap": 50,
            "nameTextStyle": {"color": "#666", "fontSize": 12},
            "axisLine": {"lineStyle": {"color": "#ccc"}},
            "axisTick": {"show": False},
            "axisLabel": {"color": "#888", "fontSize": 11},
            "splitLine": {"show": False},
        },
        "graphic": [
            {
                "type": "text",
                "left": "10%",
                "top": "7%",
                "style": {
                    "text": QUADRANT_TITLES["angles_morts"],
                    "fill": "#C47A00",
                    "fontSize": 11,
                    "fontWeight": "bold",
                },
            },
            {
                "type": "text",
                "right": "6%",
                "top": "7%",
                "style": {
                    "text": QUADRANT_TITLES["bien_couvert"],
                    "fill": "#aaa",
                    "fontSize": 11,
                    "fontWeight": "bold",
                },
            },
            {
                "type": "text",
                "left": "10%",
                "bottom": "12%",
                "style": {
                    "text": QUADRANT_TITLES["faible_enjeu"],
                    "fill": "#aaa",
                    "fontSize": 11,
                    "fontWeight": "bold",
                },
            },
            {
                "type": "text",
                "right": "6%",
                "bottom": "12%",
                "style": {
                    "text": QUADRANT_TITLES["bien_investi"],
                    "fill": "#aaa",
                    "fontSize": 11,
                    "fontWeight": "bold",
                },
            },
        ],
        "series": [
            {
                "type": "scatter",
                "data": scatter_data,
                "markArea": {
                    "silent": True,
                    "itemStyle": {"color": COLOR_ANGLES_MORTS},
                    "data": [
                        [
                            {"coord": [0, y_seuil]},
                            {"coord": [x_seuil, y_axis_max]},
                        ],
                    ],
                },
                "markLine": {
                    "silent": True,
                    "symbol": "none",
                    "lineStyle": {"type": "dashed", "color": "#ccc", "width": 1},
                    "label": {"show": False},
                    "data": [{"xAxis": x_seuil}, {"yAxis": y_seuil}],
                },
            }
        ],
    }
