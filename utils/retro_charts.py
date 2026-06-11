"""Graphiques mensuels YoY Nivo pour la page Retro Data."""

from __future__ import annotations

import streamlit as st
from streamlit_elements import elements, mui, nivo

import pandas as pd

from utils.retro_metrics import RetroPeriods

MONTH_LABELS = [
    "Jan", "Fév", "Mar", "Avr", "Mai", "Juin",
    "Juil", "Aoû", "Sep", "Oct", "Nov", "Déc",
]

COLOR_PREV = "#4380f5"
COLOR_CUR = "#F0806A"

THEME_NIVO = {
    "text": {
        "fontFamily": "Source Sans Pro, sans-serif",
        "fontSize": 13,
        "fill": "#31333F",
    },
    "labels": {
        "text": {
            "fontFamily": "Source Sans Pro, sans-serif",
            "fontSize": 12,
            "fill": "#333333",
        }
    },
    "tooltip": {
        "container": {
            "background": "rgba(255, 255, 255, 0.95)",
            "color": "#31333F",
            "fontSize": "13px",
            "fontFamily": "Source Sans Pro, sans-serif",
            "borderRadius": "4px",
            "boxShadow": "0 2px 8px rgba(0,0,0,0.15)",
            "padding": "8px 12px",
            "border": "1px solid rgba(0, 0, 0, 0.1)",
        }
    },
}


def _monthly_pivot_simple(df: pd.DataFrame) -> pd.DataFrame:
    work = df.copy()
    work["created_at"] = pd.to_datetime(work["created_at"], errors="coerce")
    if getattr(work["created_at"].dt, "tz", None) is not None:
        work["created_at"] = work["created_at"].dt.tz_localize(None)
    work["year"] = work["created_at"].dt.year
    work["month"] = work["created_at"].dt.month
    monthly = (
        work.groupby(["year", "month"])
        .size()
        .reset_index(name="value")
    )
    pivot = monthly.pivot(index="month", columns="year", values="value")
    return pivot.reindex(range(1, 13))


def _monthly_pivot_agg(
    df: pd.DataFrame,
    agg: str,
) -> pd.DataFrame:
    work = df.copy()
    work["created_at"] = pd.to_datetime(work["created_at"], errors="coerce")
    if getattr(work["created_at"].dt, "tz", None) is not None:
        work["created_at"] = work["created_at"].dt.tz_localize(None)
    work["year"] = work["created_at"].dt.year
    work["month"] = work["created_at"].dt.month

    counts = (
        work.groupby(["year", "month", "collectivite_id"])["email"]
        .nunique()
        .reset_index(name="nb_emails")
    )

    if agg == "mean":
        monthly = (
            counts.groupby(["year", "month"])["nb_emails"]
            .mean()
            .reset_index(name="value")
        )
    elif agg == "intensity":
        emails = counts.groupby(["year", "month"])["nb_emails"].sum()
        collectivites = counts.groupby(["year", "month"])["collectivite_id"].nunique()
        monthly = (emails / collectivites).reset_index(name="value")
    else:
        monthly = (
            counts.groupby(["year", "month"])["nb_emails"]
            .sum()
            .reset_index(name="value")
        )

    pivot = monthly.pivot(index="month", columns="year", values="value")
    return pivot.reindex(range(1, 13))


def _pivot_to_nivo_lines(
    df_pivot: pd.DataFrame,
    periods: RetroPeriods,
) -> list[dict]:
    series = []
    year_colors = [
        (periods.prev_year, COLOR_PREV),
        (periods.cur_year, COLOR_CUR),
    ]

    for year, _color in year_colors:
        if year not in df_pivot.columns:
            continue

        data = []
        for month in range(1, 13):
            value = df_pivot.loc[month, year]
            if pd.isna(value):
                continue
            data.append({
                "x": MONTH_LABELS[month - 1],
                "y": float(value),
            })

        if data:
            series.append({"id": str(year), "data": data})

    return series


def _render_nivo_yoy_line(
    line_data: list[dict],
    periods: RetroPeriods,
    chart_key: str,
    *,
    y_legend: str | None = None,
) -> None:
    if not line_data:
        st.info("Aucune donnée disponible pour ce graphique.")
        return

    color_by_year = {
        str(periods.prev_year): COLOR_PREV,
        str(periods.cur_year): COLOR_CUR,
    }
    colors = [color_by_year.get(s["id"], COLOR_PREV) for s in line_data]

    with elements(chart_key):
        with mui.Box(sx={"height": 420}):
            nivo.Line(
                data=line_data,
                margin={"top": 20, "right": 120, "bottom": 50, "left": 90},
                xScale={"type": "point"},
                yScale={
                    "type": "linear",
                    "min": 0,
                    "max": "auto",
                    "stacked": False,
                    "reverse": False,
                },
                curve="monotoneX",
                axisTop=None,
                axisRight=None,
                axisBottom={
                    "tickSize": 5,
                    "tickPadding": 5,
                    "tickRotation": 0,
                },
                axisLeft={
                    "tickSize": 5,
                    "tickPadding": 5,
                    "tickRotation": 0,
                    "legend": y_legend or "",
                    "legendPosition": "middle",
                    "legendOffset": -60,
                },
                enableArea=False,
                enablePoints=False,
                useMesh=True,
                enableSlices="x",
                colors=colors,
                legends=[
                    {
                        "anchor": "bottom-right",
                        "direction": "column",
                        "justify": False,
                        "translateX": 100,
                        "translateY": 0,
                        "itemsSpacing": 2,
                        "itemDirection": "left-to-right",
                        "itemWidth": 80,
                        "itemHeight": 20,
                        "symbolSize": 12,
                        "symbolShape": "circle",
                    }
                ],
                theme=THEME_NIVO,
            )


def render_monthly_yoy_chart(
    df: pd.DataFrame,
    periods: RetroPeriods,
    *,
    chart_key: str,
    title: str | None = None,
    ylabel: str | None = None,
    projection: bool = True,  # noqa: ARG001 — conservé pour compatibilité API
) -> None:
    if df is None or df.empty:
        st.info("Aucune donnée disponible pour ce graphique.")
        return

    if title:
        st.markdown(f"**{title}**")

    pivot = _monthly_pivot_simple(df)
    line_data = _pivot_to_nivo_lines(pivot, periods)
    _render_nivo_yoy_line(line_data, periods, chart_key, y_legend=ylabel)


def render_monthly_yoy_chart_agg(
    df: pd.DataFrame,
    periods: RetroPeriods,
    *,
    chart_key: str,
    agg: str = "mean",
    title: str | None = None,
    ylabel: str | None = None,
    projection: bool = True,  # noqa: ARG001
) -> None:
    if df is None or df.empty:
        st.info("Aucune donnée disponible pour ce graphique.")
        return

    if title:
        st.markdown(f"**{title}**")

    pivot = _monthly_pivot_agg(df, agg=agg)
    line_data = _pivot_to_nivo_lines(pivot, periods)
    _render_nivo_yoy_line(line_data, periods, chart_key, y_legend=ylabel)
