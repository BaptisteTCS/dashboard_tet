import streamlit as st

st.set_page_config(
    page_title="Retro Data OKRs",
    page_icon="📈",
    layout="wide",
)

import pandas as pd
from sqlalchemy import text

from utils.db import get_engine_prod, read_table
from utils.retro_charts import render_monthly_yoy_chart, render_monthly_yoy_chart_agg
from utils.retro_metrics import (
    count_row_metrics,
    distinct_metrics,
    get_retro_periods,
    mean_users_per_collectivite_metrics,
    render_comparison_metrics,
)

# ==========================
# Chargement des données
# ==========================


@st.cache_data(ttl="1h", show_spinner="Chargement des données…")
def load_retro_data(series_start: str) -> dict[str, pd.DataFrame]:
    engine_prod = get_engine_prod()
    with engine_prod.connect() as conn:
        df_fiche_action = pd.read_sql_query(
            text("""
                SELECT id, created_at, collectivite_id
                FROM fiche_action
                WHERE created_at >= :since
                  AND parent_id IS NULL
            """),
            conn,
            params={"since": series_start},
        )
        df_utilisateur_droit = pd.read_sql_query(
            text("""
                SELECT pud.created_at, pud.user_id, pud.collectivite_id
                FROM private_utilisateur_droit pud
                JOIN collectivite c ON c.id = pud.collectivite_id
                WHERE pud.created_at >= :since AND c.type != 'test'
            """),
            conn,
            params={"since": series_start},
        )

    df_pap = read_table("pap_date_passage")
    df_activite = read_table(
        "activite_semaine",
        where_sql="semaine >= :since",
        params={"since": series_start},
    )

    df_pap["passage_pap"] = pd.to_datetime(df_pap["passage_pap"], errors="coerce")
    df_activite["semaine"] = pd.to_datetime(df_activite["semaine"], errors="coerce")

    df_ct_pap = (
        df_pap.sort_values("passage_pap")
        .drop_duplicates("collectivite_id", keep="first")
        .rename(columns={"passage_pap": "created_at"})
        .copy()
    )

    df_pap_series = df_pap.rename(columns={"passage_pap": "created_at"})[
        ["plan", "created_at", "collectivite_id"]
    ].copy()

    month_start = df_activite["semaine"].dt.to_period("M").dt.to_timestamp()
    df_act_email = (
        df_activite.assign(created_at=month_start)[["created_at", "email"]]
        .drop_duplicates()
    )
    df_act_ct = (
        df_activite.assign(created_at=month_start)[["created_at", "collectivite_id"]]
        .drop_duplicates()
    )
    df_act_email_ct = (
        df_activite.assign(created_at=month_start)[
            ["created_at", "collectivite_id", "email"]
        ]
        .drop_duplicates()
    )

    return {
        "fiche_action": df_fiche_action,
        "utilisateur_droit": df_utilisateur_droit,
        "pap": df_pap,
        "pap_series": df_pap_series,
        "ct_pap": df_ct_pap,
        "activite": df_activite,
        "act_email": df_act_email,
        "act_ct": df_act_ct,
        "act_email_ct": df_act_email_ct,
    }


# ==========================
# Interface
# ==========================

periods = get_retro_periods()
data = load_retro_data(str(periods.series_start))

st.title("📈 Retro Data OKRs")
st.caption(
    f"Comparaison {periods.prev_period_label} ({periods.prev_year}) "
    f"vs {periods.cur_period_label} ({periods.cur_year})"
)
st.markdown("---")

# --- 1. Fiches action ---
st.subheader("Actions crées")

fa_cur, fa_prev = count_row_metrics(
    data["fiche_action"], "created_at", periods
)
render_comparison_metrics(
    fa_cur, fa_prev,
    count_label="Actions créées",
    periods=periods,
)
render_monthly_yoy_chart(
    data["fiche_action"],
    periods,
    chart_key="retro_fa",
    title="Créations mensuelles d'actions",
    ylabel="Nombre d'actions",
)

st.markdown("---")

# --- 2. Passages PAP ---
st.subheader("Nouveaux PAP")

pap_cur, pap_prev = count_row_metrics(
    data["pap_series"], "created_at", periods
)
render_comparison_metrics(
    pap_cur, pap_prev,
    count_label="PAP",
    periods=periods,
)
render_monthly_yoy_chart(
    data["pap_series"],
    periods,
    chart_key="retro_pap",
    title="Créations mensuelles de PAP",
    ylabel="Nombre de PAP",
)

st.markdown("---")

# --- 3. Nouvelles collectivités PAP ---
st.subheader("Nouvelles collectivités PAP")

render_monthly_yoy_chart(
    data["ct_pap"],
    periods,
    chart_key="retro_ct_pap",
    title="Nouvelles collectivités PAP",
    ylabel="Nombre de collectivités",
)

st.markdown("---")

# --- 4. Utilisateurs actifs ---
st.subheader("Utilisateurs actifs")

act_cur, act_prev = distinct_metrics(
    data["activite"], "semaine", periods, "email"
)
render_comparison_metrics(
    act_cur, act_prev,
    count_label="Utilisateurs",
    periods=periods,
)

render_monthly_yoy_chart(
    data["act_email"],
    periods,
    chart_key="retro_act_email",
    projection=False,
    title="Utilisateurs actifs par mois",
    ylabel="Emails distincts",
)
ct_cur, ct_prev = distinct_metrics(
    data["activite"], "semaine", periods, "collectivite_id"
)
render_comparison_metrics(
    ct_cur, ct_prev,
    count_label="Collectivités",
    periods=periods,
)
render_monthly_yoy_chart(
    data["act_ct"],
    periods,
    chart_key="retro_act_ct",
    projection=False,
    title="Collectivités actives par mois",
    ylabel="Collectivités distinctes",
)
mean_cur, mean_prev = mean_users_per_collectivite_metrics(
    data["activite"], "semaine", periods
)
render_comparison_metrics(
    mean_cur, mean_prev,
    count_label="Utilisateurs / collectivité",
    periods=periods,
    decimals=1,
)
render_monthly_yoy_chart_agg(
    data["act_email_ct"],
    periods,
    chart_key="retro_act_email_ct",
    agg="mean",
    projection=False,
    title="Moyenne d'utilisateurs actifs par collectivité",
    ylabel="Utilisateurs / collectivité",
)

st.markdown("---")

# --- 5. Nouveaux droits utilisateurs ---
st.subheader("Nouveaux utilisateurs")

pud_cur, pud_prev = distinct_metrics(
    data["utilisateur_droit"], "created_at", periods, "user_id"
)
render_comparison_metrics(
    pud_cur, pud_prev,
    count_label="Utilisateurs",
    periods=periods,
)
render_monthly_yoy_chart(
    data["utilisateur_droit"],
    periods,
    chart_key="retro_pud",
    title="Créations mensuelles d'utilisateurs",
    ylabel="Nombre d'utilisateurs",
)
