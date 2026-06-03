import streamlit as st

st.set_page_config(layout="wide")

import calendar

import pandas as pd
from sqlalchemy import text
from streamlit_elements import elements, mui, nivo

from utils.db import read_table, get_engine_prod

SEGMENT_EXCLU = "autre_mail_non_support"
_ALL_TIME_START = pd.Timestamp("2024-01-01")
_COULEUR_BAR = "#5B8FF9"
_PALETTE_SEGMENTS = [
    "#5B8FF9",
    "#5AD8A6",
    "#5D7092",
    "#F6BD16",
    "#E86452",
    "#6DC8EC",
    "#945FB9",
    "#FF9845",
]
_CATEGORY_PREFIXES: list[tuple[str, str]] = [
    ("besoin_guidage", "Besoin de guidage"),
    ("support_obligatoire", "Action support obligatoires"),
    ("amelioration", "Suggestions d'améliorations"),
    ("metier", "Questions métiers"),
    ("autre", "Autres"),
    ("bug", "Bugs"),
]
_BAR_ROW_PX = 40
_BAR_MIN_HEIGHT = 280

theme_actif = {
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

# ==========================
# Chargement des données
# ==========================


@st.cache_resource(ttl="2d")
def load_data():
    df_crisp_conversation = read_table("crisp_conversation")
    df_crisp_rating = read_table("crisp_rating")
    df_crisp_temps_reponse = read_table("crisp_temps_reponse")
    df_crisp_temps_resolution = read_table("crisp_temps_resoluton")
    df_collectivite = read_table("collectivite")
    df_user_actifs = read_table("user_actifs_ct_mois")

    engine_prod = get_engine_prod()
    with engine_prod.connect() as conn:
        df_droits = pd.read_sql_query(
            text("SELECT * FROM private_utilisateur_droit"), conn
        )
        df_membres = pd.read_sql_query(
            text("SELECT * FROM private_collectivite_membre"), conn
        )
        df_users = pd.read_sql_query(
            text("SELECT id, email FROM auth.users"), conn
        )

    return {
        "crisp_conversation": df_crisp_conversation,
        "crisp_rating": df_crisp_rating,
        "crisp_temps_reponse": df_crisp_temps_reponse,
        "crisp_temps_resolution": df_crisp_temps_resolution,
        "collectivite": df_collectivite,
        "user_actifs_ct_mois": df_user_actifs,
        "private_utilisateur_droit": df_droits,
        "private_collectivite_membre": df_membres,
        "auth_users": df_users,
    }


# ==========================
# Préparation & agrégations
# ==========================


def _mois_to_ts(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, errors="coerce").dt.to_period("M").dt.to_timestamp()


def _exclude_non_support(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty or "segments" not in df.columns:
        return df
    mask = df["segments"].fillna("").str.contains(SEGMENT_EXCLU, regex=False)
    return df.loc[~mask].copy()


def _prepare_conversations(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    out = _exclude_non_support(df)
    out["updated_at"] = pd.to_datetime(out["updated_at"], errors="coerce")
    if out["updated_at"].dt.tz is not None:
        out["updated_at"] = out["updated_at"].dt.tz_localize(None)
    return out.dropna(subset=["updated_at"])


def _prepare_user_actifs(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    out = df.copy()
    out["mois_ts"] = _mois_to_ts(out["mois"])
    return out.dropna(subset=["mois_ts"])


def _prepare_monthly_crisp(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    out = df.copy()
    out["mois_ts"] = _mois_to_ts(out["mois"])
    return out.dropna(subset=["mois_ts"])


def months_in_period(start: pd.Timestamp, end: pd.Timestamp) -> list[pd.Timestamp]:
    cursor = pd.Timestamp(year=start.year, month=start.month, day=1)
    end_month = pd.Timestamp(year=end.year, month=end.month, day=1)
    months = []
    while cursor <= end_month:
        months.append(cursor)
        cursor += pd.DateOffset(months=1)
    return months


def conversations_in_period(df: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    if df.empty:
        return df
    end_inclusive = end + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1)
    return df[(df["updated_at"] >= start) & (df["updated_at"] <= end_inclusive)]


def _weighted_avg(
    df: pd.DataFrame,
    value_col: str,
    months: list[pd.Timestamp],
    weight_col: str = "hits",
) -> float | None:
    if df.empty:
        return None
    sub = df[df["mois_ts"].isin(months)]
    if sub.empty:
        return None
    weights = sub[weight_col].fillna(0)
    if weights.sum() == 0:
        return None
    return float((sub[value_col] * weights).sum() / weights.sum())


def count_conversations(df_conv: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp) -> int:
    return len(conversations_in_period(df_conv, start, end))


def support_rate(
    df_conv: pd.DataFrame,
    df_users: pd.DataFrame,
    start: pd.Timestamp,
    end: pd.Timestamp,
) -> float | None:
    conv = conversations_in_period(df_conv, start, end)
    months = months_in_period(start, end)
    users = df_users[df_users["mois_ts"].isin(months)]
    n_support = conv["email"].dropna().nunique()
    n_actifs = users["email"].dropna().nunique()
    if n_actifs == 0:
        return None
    return n_support / n_actifs * 100


def _explode_segments(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["segment"])
    tmp = df[["segments"]].copy()
    tmp["segment"] = tmp["segments"].fillna("").str.split(",")
    exploded = tmp.explode("segment")
    exploded["segment"] = exploded["segment"].str.strip()
    return exploded[exploded["segment"] != ""]


def segment_to_category(segment: str) -> str | None:
    for prefix, label in _CATEGORY_PREFIXES:
        if segment.startswith(prefix):
            return label
    return None


def _explode_categories(df: pd.DataFrame) -> pd.DataFrame:
    exploded = _explode_segments(df)
    if exploded.empty:
        return pd.DataFrame(columns=["categorie"])
    exploded["categorie"] = exploded["segment"].map(segment_to_category)
    return exploded.dropna(subset=["categorie"])


def top_segment_counts(
    df_conv: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp, n: int = 3
) -> pd.Series:
    conv = conversations_in_period(df_conv, start, end)
    exploded = _explode_categories(conv)
    if exploded.empty:
        return pd.Series(dtype=int)
    return exploded["segment"].value_counts().head(n)


def _format_top_segments_md(counts: pd.Series) -> str:
    if counts.empty:
        return "Top 3 des segments sur cette période : *aucun*."
    parts = [f"**{seg}** ({int(nb)})" for seg, nb in counts.items()]
    return "Top 3 des segments sur cette période : " + ", ".join(parts) + "."


def category_segment_counts(
    df_conv: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp
) -> pd.DataFrame:
    conv = conversations_in_period(df_conv, start, end)
    exploded = _explode_categories(conv)
    if exploded.empty:
        return pd.DataFrame(columns=["categorie", "segment", "conversations"])
    return (
        exploded.groupby(["categorie", "segment"])
        .size()
        .reset_index(name="conversations")
    )


def monthly_category_evolution(df_conv: pd.DataFrame) -> pd.DataFrame:
    if df_conv.empty:
        return pd.DataFrame(columns=["mois", "categorie", "conversations"])
    conv = df_conv.copy()
    conv["mois"] = conv["updated_at"].dt.to_period("M").dt.to_timestamp()
    conv["segment"] = conv["segments"].fillna("").str.split(",")
    exploded = conv.explode("segment")
    exploded["segment"] = exploded["segment"].str.strip()
    exploded = exploded[exploded["segment"] != ""]
    exploded["categorie"] = exploded["segment"].map(segment_to_category)
    exploded = exploded.dropna(subset=["categorie"])
    if exploded.empty:
        return pd.DataFrame(columns=["mois", "categorie", "conversations"])
    return (
        exploded.groupby(["mois", "categorie"])
        .size()
        .reset_index(name="conversations")
    )


def operator_counts(df_conv: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp) -> pd.Series:
    conv = conversations_in_period(df_conv, start, end)
    if conv.empty or "operator" not in conv.columns:
        return pd.Series(dtype=int)
    conv = conv[conv["operator"].notna()]
    if conv.empty:
        return pd.Series(dtype=int)
    return conv["operator"].value_counts()


def monthly_operator_evolution(df_conv: pd.DataFrame) -> pd.DataFrame:
    if df_conv.empty:
        return pd.DataFrame(columns=["mois", "operator", "conversations"])
    conv = df_conv.copy()
    conv["mois"] = conv["updated_at"].dt.to_period("M").dt.to_timestamp()
    if "operator" not in conv.columns:
        return pd.DataFrame(columns=["mois", "operator", "conversations"])
    conv = conv[conv["operator"].notna()]
    if conv.empty:
        return pd.DataFrame(columns=["mois", "operator", "conversations"])
    return (
        conv.groupby(["mois", "operator"])
        .size()
        .reset_index(name="conversations")
    )


def _counts_to_nivo_bar(counts: pd.Series, index_key: str) -> list[dict]:
    """Barres horizontales : plus forte valeur en haut (comme Détail mobilisation)."""
    if counts.empty:
        return []
    df_plot = counts.reset_index()
    df_plot.columns = [index_key, "conversations"]
    df_plot = df_plot.sort_values("conversations", ascending=False)
    return df_plot.to_dict(orient="records")[::-1]


def _category_segment_to_nivo_horizontal(
    df: pd.DataFrame,
) -> tuple[list[dict], list[str], list[str]]:
    """Barre par catégorie, segments en noms (tooltip) triés du plus grand au plus petit."""
    if df.empty:
        return [], [], []
    index_key = "Catégorie"
    cat_totals = df.groupby("categorie")["conversations"].sum().sort_values(ascending=False)
    keys: list[str] = []
    seen: set[str] = set()
    bar_data = []
    n_palette = len(_PALETTE_SEGMENTS)
    segment_colors: dict[str, str] = {}

    for cat in cat_totals.index:
        sub = df[df["categorie"] == cat].sort_values("conversations", ascending=False)
        row = {index_key: cat}
        for rank, (_, r) in enumerate(sub.iterrows()):
            seg = str(r["segment"])
            count = int(r["conversations"])
            if count <= 0:
                continue
            row[seg] = count
            if seg not in seen:
                keys.append(seg)
                seen.add(seg)
                segment_colors[seg] = _PALETTE_SEGMENTS[rank % n_palette]
        bar_data.append(row)

    if not keys:
        return [], [], []
    colors = [segment_colors[seg] for seg in keys]
    return bar_data[::-1], keys, colors


def _monthly_to_nivo_lines(df: pd.DataFrame, group_col: str) -> list[dict]:
    if df.empty:
        return []
    work = df.copy()
    work["mois"] = pd.to_datetime(work["mois"])
    all_months = sorted(work["mois"].unique())
    series = []
    for grp, sub in work.groupby(group_col, sort=False):
        by_mois = sub.groupby("mois")["conversations"].sum()
        series.append({
            "id": str(grp),
            "data": [
                {"x": pd.Timestamp(m).strftime("%Y-%m"), "y": int(by_mois.get(m, 0))}
                for m in all_months
            ],
        })
    return series


def _nivo_horizontal_bar(
    counts: pd.Series,
    index_key: str,
    title: str,
    icon: str,
    color: str,
    chart_key: str,
):
    st.badge(f"{title}", icon=icon, color=color)
    bar_data = _counts_to_nivo_bar(counts, index_key)
    if not bar_data:
        st.info("Aucune donnée sur la période sélectionnée.")
        return

    max_label_len = max(len(str(row[index_key])) for row in bar_data)
    chart_height = max(_BAR_MIN_HEIGHT, len(bar_data) * _BAR_ROW_PX + 70)
    left_margin = min(320, max(100, max_label_len * 7))

    with elements(chart_key):
        with mui.Box(sx={"height": chart_height}):
            nivo.Bar(
                data=bar_data,
                keys=["conversations"],
                indexBy=index_key,
                layout="horizontal",
                margin={"top": 16, "right": 56, "bottom": 40, "left": left_margin},
                padding=0.35,
                valueScale={"type": "linear", "min": 0},
                indexScale={"type": "band", "round": True},
                colors=[_COULEUR_BAR],
                borderRadius=4,
                borderColor={"from": "color", "modifiers": [["darker", 0.4]]},
                axisTop=None,
                axisRight=None,
                axisBottom={
                    "tickSize": 5,
                    "tickPadding": 5,
                    "tickRotation": 0,
                    "legend": "Conversations",
                    "legendPosition": "middle",
                    "legendOffset": 32,
                },
                axisLeft={
                    "tickSize": 5,
                    "tickPadding": 8,
                    "tickRotation": 0,
                },
                enableLabel=True,
                labelSkipWidth=16,
                labelSkipHeight=12,
                labelTextColor="#ffffff",
                animate=True,
                motionConfig="gentle",
                theme=theme_actif,
            )


def _nivo_horizontal_stacked_bar(
    bar_data: list[dict],
    keys: list[str],
    index_key: str,
    title: str,
    icon: str,
    color: str,
    chart_key: str,
    *,
    segment_colors: list[str] | None = None,
):
    st.badge(f"{title}", icon=icon, color=color)
    if not bar_data or not keys:
        st.info("Aucune donnée sur la période sélectionnée.")
        return

    max_label_len = max(len(str(row[index_key])) for row in bar_data)
    chart_height = max(_BAR_MIN_HEIGHT, len(bar_data) * _BAR_ROW_PX + 70)
    left_margin = min(320, max(100, max_label_len * 7))

    with elements(chart_key):
        with mui.Box(sx={"height": chart_height}):
            nivo.Bar(
                data=bar_data,
                keys=keys,
                indexBy=index_key,
                layout="horizontal",
                margin={"top": 16, "right": 56, "bottom": 40, "left": left_margin},
                padding=0.35,
                groupMode="stacked",
                valueScale={"type": "linear", "min": 0},
                indexScale={"type": "band", "round": True},
                colors=segment_colors if segment_colors else [_COULEUR_BAR],
                borderRadius=4,
                borderColor={"from": "color", "modifiers": [["darker", 0.4]]},
                axisTop=None,
                axisRight=None,
                axisBottom={
                    "tickSize": 5,
                    "tickPadding": 5,
                    "tickRotation": 0,
                    "legend": "Conversations",
                    "legendPosition": "middle",
                    "legendOffset": 32,
                },
                axisLeft={
                    "tickSize": 5,
                    "tickPadding": 8,
                    "tickRotation": 0,
                },
                enableLabel=True,
                labelSkipWidth=16,
                labelSkipHeight=12,
                labelTextColor="#ffffff",
                animate=True,
                motionConfig="gentle",
                theme=theme_actif,
            )


def _nivo_multi_line(
    df: pd.DataFrame,
    group_col: str,
    title: str,
    icon: str,
    color: str,
    chart_key: str,
):
    st.badge(f"{title}", icon=icon, color=color)
    line_data = _monthly_to_nivo_lines(df, group_col)
    if not line_data:
        st.info("Aucune donnée disponible.")
        return

    with elements(chart_key):
        with mui.Box(sx={"height": 420}):
            nivo.Line(
                data=line_data,
                margin={"top": 20, "right": 130, "bottom": 60, "left": 60},
                xScale={
                    "type": "time",
                    "format": "%Y-%m",
                    "precision": "month",
                    "useUTC": False,
                },
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
                    "tickRotation": -45,
                },
                axisLeft={
                    "tickSize": 5,
                    "tickPadding": 5,
                    "tickRotation": 0,
                    "legend": "Conversations",
                    "legendPosition": "middle",
                    "legendOffset": -48,
                },
                enablePoints=True,
                pointSize=6,
                pointBorderWidth=1,
                pointBorderColor={"from": "serieColor"},
                useMesh=True,
                enableSlices="x",
                colors={"scheme": "category10"},
                legends=[
                    {
                        "anchor": "bottom-right",
                        "direction": "column",
                        "justify": False,
                        "translateX": 120,
                        "translateY": 0,
                        "itemsSpacing": 2,
                        "itemWidth": 100,
                        "itemHeight": 18,
                        "itemOpacity": 0.85,
                        "symbolSize": 10,
                        "symbolShape": "circle",
                    }
                ],
                theme=theme_actif,
            )


def format_duration_h(hours: float) -> str:
    """Heures décimales → libellé lisible (0.5 → 30min, 1.5 → 1h30)."""
    total_minutes = int(round(abs(hours) * 60))
    h, m = divmod(total_minutes, 60)
    if h == 0:
        body = f"{m}min"
    elif m == 0:
        body = f"{h}h"
    else:
        body = f"{h}h{m}"
    return f"-{body}" if hours < 0 else body


def format_duration_delta(delta_h: float) -> str:
    if delta_h == 0:
        return "0"
    if delta_h > 0:
        return f"+{format_duration_h(delta_h)}"
    return format_duration_h(delta_h)


def _metric_delta(cur, prev, *, fmt: str):
    if cur is None or prev is None:
        return None
    delta = cur - prev
    if fmt == "pct":
        return f"{delta:+.1f} pts"
    if fmt == "hours":
        return format_duration_delta(delta)
    if fmt == "rating":
        return f"{delta:+.2f}"
    return f"{delta:+.0f}"


# ==========================
# Données & période
# ==========================

data = load_data()

df_conv = _prepare_conversations(data["crisp_conversation"])
df_users = _prepare_user_actifs(data["user_actifs_ct_mois"])
df_rating = _prepare_monthly_crisp(data["crisp_rating"])
df_temps_rep = _prepare_monthly_crisp(data["crisp_temps_reponse"])
df_temps_res = _prepare_monthly_crisp(data["crisp_temps_resolution"])

st.title("🐛 Dashboard Support & Bugs")

_MOIS_FR = [
    "", "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
    "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre",
]
today = pd.Timestamp.today().normalize()

_col_seg, _col_sel, _ = st.columns(3)
with _col_seg:
    st.segmented_control(
        "Période",
        options=["Mois", "Trimestre", "All Time"],
        default="Mois",
        key="view_bug",
    )
view = st.session_state.get("view_bug", "Mois")

with _col_sel:
    if view == "Mois":
        _month_options = []
        _y, _m = 2024, 1
        while (_y, _m) <= (today.year, today.month):
            _month_options.append(f"{_y}-{_m:02d}")
            _m += 1
            if _m > 12:
                _m = 1
                _y += 1
        st.selectbox(
            "Mois",
            options=_month_options,
            index=len(_month_options) - 1,
            format_func=lambda x: f"{_MOIS_FR[int(x.split('-')[1])]} {x.split('-')[0]}",
            key="selected_month_bug",
        )
    elif view == "Trimestre":
        _quarter_options = []
        _y, _q = 2024, 1
        _cur_q = (today.month - 1) // 3 + 1
        while (_y, _q) <= (today.year, _cur_q):
            _quarter_options.append(f"T{_q} {_y}")
            _q += 1
            if _q > 4:
                _q = 1
                _y += 1
        st.selectbox(
            "Trimestre",
            options=_quarter_options,
            index=len(_quarter_options) - 1,
            key="selected_quarter_bug",
        )

is_all_time = view == "All Time"

if view == "Mois":
    _selected = st.session_state.get("selected_month_bug", f"{today.year}-{today.month:02d}")
    sel_y, sel_m = int(_selected.split("-")[0]), int(_selected.split("-")[1])
    cur_start = pd.Timestamp(year=sel_y, month=sel_m, day=1)
    cur_end = (
        today
        if sel_y == today.year and sel_m == today.month
        else pd.Timestamp(year=sel_y, month=sel_m, day=calendar.monthrange(sel_y, sel_m)[1])
    )
    prev_m = sel_m - 1 if sel_m > 1 else 12
    prev_y = sel_y if sel_m > 1 else sel_y - 1
    prev_start = pd.Timestamp(year=prev_y, month=prev_m, day=1)
    prev_end = pd.Timestamp(
        year=prev_y, month=prev_m, day=calendar.monthrange(prev_y, prev_m)[1]
    )
elif view == "Trimestre":
    _cur_q = (today.month - 1) // 3 + 1
    _default_quarter = f"T{_cur_q} {today.year}"
    _selected = st.session_state.get("selected_quarter_bug", _default_quarter)
    _q = int(_selected[1])
    sel_y = int(_selected.split(" ")[1])
    month_start = (_q - 1) * 3 + 1
    month_end = _q * 3
    cur_start = pd.Timestamp(year=sel_y, month=month_start, day=1)
    cur_end_month = pd.Timestamp(
        year=sel_y, month=month_end, day=calendar.monthrange(sel_y, month_end)[1]
    )
    cur_end = today if sel_y == today.year and _q == _cur_q else cur_end_month
    prev_q = _q - 1 if _q > 1 else 4
    prev_y = sel_y if _q > 1 else sel_y - 1
    prev_month_start = (prev_q - 1) * 3 + 1
    prev_month_end = prev_q * 3
    prev_start = pd.Timestamp(year=prev_y, month=prev_month_start, day=1)
    prev_end = pd.Timestamp(
        year=prev_y,
        month=prev_month_end,
        day=calendar.monthrange(prev_y, prev_month_end)[1],
    )
else:
    cur_start = _ALL_TIME_START
    cur_end = today
    prev_start = cur_start
    prev_end = cur_end

cur_months = months_in_period(cur_start, cur_end)
prev_months = months_in_period(prev_start, prev_end)

st.markdown("---")

# ==========================
# Section 1 : Les chiffres du support
# ==========================

st.subheader("Les chiffres du support")

nb_conv_cur = count_conversations(df_conv, cur_start, cur_end)
taux_cur = support_rate(df_conv, df_users, cur_start, cur_end)
rep_cur = _weighted_avg(df_temps_rep, "response_time_h", cur_months)
res_cur = _weighted_avg(df_temps_res, "temps_resolution_h", cur_months)
sat_cur = _weighted_avg(df_rating, "rating", cur_months)

if not is_all_time:
    nb_conv_prev = count_conversations(df_conv, prev_start, prev_end)
    taux_prev = support_rate(df_conv, df_users, prev_start, prev_end)
    rep_prev = _weighted_avg(df_temps_rep, "response_time_h", prev_months)
    res_prev = _weighted_avg(df_temps_res, "temps_resolution_h", prev_months)
    sat_prev = _weighted_avg(df_rating, "rating", prev_months)
    _d_conv = _metric_delta(nb_conv_cur, nb_conv_prev, fmt="int")
    _d_taux = _metric_delta(taux_cur, taux_prev, fmt="pct")
    _d_rep = _metric_delta(rep_cur, rep_prev, fmt="hours")
    _d_res = _metric_delta(res_cur, res_prev, fmt="hours")
    _d_sat = _metric_delta(sat_cur, sat_prev, fmt="rating")
else:
    _d_conv = _d_taux = _d_rep = _d_res = _d_sat = None

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.metric(
        label="Nombre de conversations",
        value=nb_conv_cur,
        delta=_d_conv,
    )
with c2:
    st.metric(
        label="Taux de support",
        value=f"{taux_cur:.1f} %" if taux_cur is not None else "—",
        delta=_d_taux,
        help="Nombre d'utilisateurs qui ont contacté le support sur le nombre d'utilisateurs actifs à cette période.",
    )
with c3:
    st.metric(
        label="Temps de première réponse",
        value=format_duration_h(rep_cur) if rep_cur is not None else "—",
        delta=_d_rep,
        delta_color="inverse",
    )
with c4:
    st.metric(
        label="Temps de résolution moyen",
        value=format_duration_h(res_cur) if res_cur is not None else "—",
        delta=_d_res,
        delta_color="inverse",
    )
with c5:
    st.metric(
        label="Satisfaction moyenne",
        value=f"{sat_cur:.2f}" if sat_cur is not None else "—",
        delta=_d_sat,
    )

st.markdown("---")

# ==========================
# Section 2 : Type de contact
# ==========================

st.subheader("Conversations par segment et opérateur")

chart_start = _ALL_TIME_START if is_all_time else cur_start
chart_end = today if is_all_time else cur_end
df_conv_chart = df_conv[
    (df_conv["updated_at"] >= chart_start) & (df_conv["updated_at"] <= chart_end)
] if not df_conv.empty else df_conv

_period_key = (
    "all"
    if is_all_time
    else f"{cur_start.strftime('%Y%m%d')}_{cur_end.strftime('%Y%m%d')}"
)

_top3_segments = top_segment_counts(df_conv, chart_start, chart_end, n=3)
st.markdown(_format_top_segments_md(_top3_segments))

col_seg, col_op = st.columns(2)

with col_seg:
    if is_all_time:
        _nivo_multi_line(
            monthly_category_evolution(df_conv_chart),
            group_col="categorie",
            title="Segments",
            icon=":material/bar_chart:",
            color="blue",
            chart_key=f"bug_line_category_{_period_key}",
        )
    else:
        _cat_seg_df = category_segment_counts(df_conv, cur_start, cur_end)
        _cat_data, _cat_keys, _cat_colors = _category_segment_to_nivo_horizontal(_cat_seg_df)
        _nivo_horizontal_stacked_bar(
            _cat_data,
            keys=_cat_keys,
            index_key="Catégorie",
            title="Segments",
            icon=":material/bar_chart:",
            color="blue",
            chart_key=f"bug_bar_category_{_period_key}",
            segment_colors=_cat_colors,
        )

with col_op:
    if is_all_time:
        _nivo_multi_line(
            monthly_operator_evolution(df_conv_chart),
            group_col="operator",
            title="Opérateurs",
            icon=":material/bar_chart:",
            color="blue",
            chart_key=f"bug_line_operator_{_period_key}",
        )
    else:
        _nivo_horizontal_bar(
            counts=operator_counts(df_conv, cur_start, cur_end),
            index_key="Opérateur",
            title="Opérateurs",
            icon=":material/person:",
            color="blue",
            chart_key=f"bug_bar_operator_{_period_key}",
        )
