"""Helpers pour les métriques YoY de la page Retro Data."""

from __future__ import annotations

import calendar
from dataclasses import dataclass
from datetime import date, timedelta

import pandas as pd
import streamlit as st


@dataclass(frozen=True)
class RetroPeriods:
    today: date
    prev_year: int
    cur_year: int
    series_start: date
    prev_year_start: date
    prev_yoy_end: date
    cur_year_start: date

    @property
    def prev_period_label(self) -> str:
        end_inclusive = self.prev_yoy_end - timedelta(days=1)
        return (
            f"Du {self.prev_year_start.strftime('%d/%m/%Y')} "
            f"au {end_inclusive.strftime('%d/%m/%Y')}"
        )

    @property
    def cur_period_label(self) -> str:
        return (
            f"Du {self.cur_year_start.strftime('%d/%m/%Y')} "
            f"au {self.today.strftime('%d/%m/%Y')}"
        )


def get_retro_periods(today: date | None = None) -> RetroPeriods:
    """Calcule les bornes de comparaison YoY à partir de la date du jour."""
    today = today or date.today()
    prev_year = today.year - 1
    cur_year = today.year
    max_day = calendar.monthrange(prev_year, today.month)[1]
    prev_yoy_end = date(prev_year, today.month, min(today.day, max_day))
    year_start = date(prev_year, 1, 1)
    return RetroPeriods(
        today=today,
        prev_year=prev_year,
        cur_year=cur_year,
        series_start=year_start,
        prev_year_start=year_start,
        prev_yoy_end=prev_yoy_end,
        cur_year_start=date(cur_year, 1, 1),
    )


def _to_ts(series: pd.Series) -> pd.Series:
    dates = pd.to_datetime(series, errors="coerce")
    if getattr(dates.dt, "tz", None) is not None:
        dates = dates.dt.tz_localize(None)
    return dates


def _period_ts(d: date) -> pd.Timestamp:
    return pd.Timestamp(d)


def filter_yoy_prev(df: pd.DataFrame, date_col: str, periods: RetroPeriods) -> pd.DataFrame:
    dates = _to_ts(df[date_col])
    return df[
        (dates > _period_ts(periods.prev_year_start))
        & (dates < _period_ts(periods.prev_yoy_end))
    ]


def filter_yoy_cur(df: pd.DataFrame, date_col: str, periods: RetroPeriods) -> pd.DataFrame:
    dates = _to_ts(df[date_col])
    end_of_today = _period_ts(periods.today) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
    return df[
        (dates > _period_ts(periods.cur_year_start))
        & (dates <= end_of_today)
    ]


def count_row_metrics(
    df: pd.DataFrame,
    date_col: str,
    periods: RetroPeriods,
) -> tuple[int, int]:
    """Retourne (count_cur, count_prev)."""
    cur = filter_yoy_cur(df, date_col, periods)
    prev = filter_yoy_prev(df, date_col, periods)
    return len(cur), len(prev)


def distinct_metrics(
    df: pd.DataFrame,
    date_col: str,
    periods: RetroPeriods,
    primary_col: str,
) -> tuple[int, int]:
    """Compte les distinct primary_col sur chaque période YoY."""
    cur = filter_yoy_cur(df, date_col, periods)
    prev = filter_yoy_prev(df, date_col, periods)
    return int(cur[primary_col].nunique()), int(prev[primary_col].nunique())


def _mean_users_per_collectivite(df: pd.DataFrame) -> float:
    """Moyenne d'emails distincts par collectivité sur toute la période filtrée."""
    if df.empty:
        return 0.0
    per_ct = df.groupby("collectivite_id")["email"].nunique()
    return float(per_ct.mean()) if len(per_ct) > 0 else 0.0


def mean_users_per_collectivite_metrics(
    df: pd.DataFrame,
    date_col: str,
    periods: RetroPeriods,
) -> tuple[float, float]:
    """Moyenne d'utilisateurs actifs par collectivité sur chaque période YoY."""
    cur = filter_yoy_cur(df, date_col, periods)
    prev = filter_yoy_prev(df, date_col, periods)
    return _mean_users_per_collectivite(cur), _mean_users_per_collectivite(prev)


def _format_metric_value(value: float, decimals: int) -> str:
    if decimals == 0:
        return f"{int(round(value)):,}".replace(",", " ")
    return f"{value:.{decimals}f}".replace(".", ",")


def render_comparison_metrics(
    count_cur: float,
    count_prev: float,
    *,
    count_label: str = "Volume",
    periods: RetroPeriods,
    decimals: int = 0,
) -> None:
    """Affiche 2 métriques : période N-1 et période N avec delta YoY."""
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            f"{count_label} ({periods.prev_year})",
            _format_metric_value(count_prev, decimals),
        )
    with col2:
        delta = count_cur - count_prev
        if decimals == 0:
            delta_str = f"{int(round(delta)):+,}".replace(",", " ")
        else:
            delta_str = f"{delta:+.{decimals}f}".replace(".", ",")
        st.metric(
            f"{count_label} ({periods.cur_year})",
            _format_metric_value(count_cur, decimals),
            delta=delta_str,
        )
