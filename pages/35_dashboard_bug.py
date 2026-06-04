import streamlit as st

st.set_page_config(layout="wide")

import calendar

import pandas as pd
from sqlalchemy import text
from streamlit_elements import elements, mui, nivo

from utils.db import read_table, get_engine_prod

SEGMENT_EXCLU = "autre_mail_non_support"
_GRAPHE_START = pd.Timestamp("2025-01-01")
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


@st.cache_resource(ttl="1d")
def load_data():
    df_crisp_conversation = read_table("crisp_conversation")
    df_crisp_rating = read_table("crisp_rating")
    df_crisp_temps_reponse = read_table("crisp_temps_reponse")
    df_crisp_temps_resolution = read_table("crisp_temps_resoluton")
    df_collectivite = read_table("collectivite")
    df_user_actifs = read_table("user_actifs_ct_mois")
    df_notion_ticket = read_table("notion_ticket")

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
        "notion_ticket": df_notion_ticket,
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


def _ticket_is_bug(names: object) -> bool:
    """Vrai si 'Bugs' apparait dans epic_name.

    epic_name peut arriver sous plusieurs formes selon le driver SQL :
    liste/tuple, numpy.ndarray, ou chaine (ex. '{Bugs,...}' ou un seul nom).
    """
    if names is None:
        return False
    # NaN scalaire
    if isinstance(names, float):
        return False
    # Chaine (nom unique ou representation texte d'un tableau Postgres)
    if isinstance(names, (str, bytes)):
        return "Bugs" in (names.decode() if isinstance(names, bytes) else names)
    # Iterable (list, tuple, ndarray, pandas array)
    try:
        return any(
            "Bugs" in str(n)
            for n in names
            if n is not None and not (isinstance(n, float) and pd.isna(n))
        )
    except TypeError:
        return "Bugs" in str(names)


def _prepare_tickets(df: pd.DataFrame) -> pd.DataFrame:
    """Parse created_at et restreint aux tickets bug (epic_name contient 'Bugs')."""
    if df.empty:
        print("[bug] _prepare_tickets: notion_ticket vide en entree")
        return df
    out = df.copy()
    out["created_at"] = pd.to_datetime(out["created_at"], errors="coerce", utc=True)
    out["created_at"] = out["created_at"].dt.tz_localize(None)
    n_total = len(out)
    out = out.dropna(subset=["created_at"])
    n_after_date = len(out)
    if "epic_name" not in out.columns:
        print(
            f"[bug] _prepare_tickets: colonne 'epic_name' absente. "
            f"Colonnes={list(out.columns)}"
        )
        return out.iloc[0:0].copy()
    mask = out["epic_name"].apply(_ticket_is_bug)
    out_bug = out[mask].copy()
    _sample = out["epic_name"].dropna().head(3).tolist()
    print(
        f"[bug] _prepare_tickets: total={n_total}, apres parse date={n_after_date}, "
        f"bugs={len(out_bug)} | epic_name dtype={out['epic_name'].dtype}, "
        f"exemples={_sample!r}"
    )
    return out_bug


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


def _month_bounds(
    month_ts: pd.Timestamp, period_end: pd.Timestamp
) -> tuple[pd.Timestamp, pd.Timestamp]:
    start = pd.Timestamp(year=month_ts.year, month=month_ts.month, day=1)
    if month_ts.year == period_end.year and month_ts.month == period_end.month:
        end = period_end
    else:
        end = pd.Timestamp(
            year=month_ts.year,
            month=month_ts.month,
            day=calendar.monthrange(month_ts.year, month_ts.month)[1],
        )
    return start, end


_GRAPHE_STATS: dict[str, str] = {
    "Conversations": "conversations",
    "Taux de support": "taux_support",
    "Temps de première réponse": "temps_reponse",
    "Temps de résolution moyen": "temps_resolution",
    "Satisfaction": "satisfaction",
    "Segments": "segments",
    "Opérateurs": "operateurs",
    "Profil de ceux qui nous contacte": "profil_contact",
}


def conversations_in_period(df: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    if df.empty:
        return df
    end_inclusive = end + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1)
    return df[(df["updated_at"] >= start) & (df["updated_at"] <= end_inclusive)]


def tickets_in_period(df: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    if df.empty:
        return df
    end_inclusive = end + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1)
    return df[(df["created_at"] >= start) & (df["created_at"] <= end_inclusive)]


def count_bugs(df: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp) -> int:
    return len(tickets_in_period(df, start, end))


def count_bugs_bloquant(df: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp) -> int:
    sub = tickets_in_period(df, start, end)
    if sub.empty or "criticite" not in sub.columns:
        return 0
    return int((sub["criticite"] == "Bloquant").sum())


def monthly_bug_counts(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["mois", "value"])
    work = df.copy()
    work["mois"] = work["created_at"].dt.to_period("M").dt.to_timestamp()
    return work.groupby("mois").size().reset_index(name="value")


def monthly_bug_by_category(df: pd.DataFrame, col: str) -> pd.DataFrame:
    if df.empty or col not in df.columns:
        return pd.DataFrame(columns=["mois", col, "value"])
    work = df.copy()
    work["mois"] = work["created_at"].dt.to_period("M").dt.to_timestamp()
    work = work.dropna(subset=[col])
    if work.empty:
        return pd.DataFrame(columns=["mois", col, "value"])
    return work.groupby(["mois", col]).size().reset_index(name="value")


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


def _normalize_email(series: pd.Series) -> pd.Series:
    return series.fillna("").astype(str).str.strip().str.lower()


def _dedupe_fonction_par_user(df: pd.DataFrame) -> pd.DataFrame:
    """Une ligne par user_id : conseiller > première fonction non nulle > première ligne."""
    if df.empty or "user_id" not in df.columns:
        return pd.DataFrame(columns=["user_id", "fonction"])

    rows: list[dict] = []
    for user_id, group in df.groupby("user_id", dropna=False):
        conseiller = group[group["fonction"] == "conseiller"]
        if not conseiller.empty:
            fonction = conseiller.iloc[0]["fonction"]
        else:
            non_null = group[group["fonction"].notna()]
            fonction = (
                non_null.iloc[0]["fonction"]
                if not non_null.empty
                else group.iloc[0]["fonction"]
            )
        rows.append({"user_id": user_id, "fonction": fonction})
    return pd.DataFrame(rows)


def _build_user_fonction_lookup(
    _df_users: pd.DataFrame,
    df_droits: pd.DataFrame,
    df_membres: pd.DataFrame,
) -> pd.DataFrame:
    """private_utilisateur_droit → private_collectivite_membre (LEFT sur collectivite_id)."""
    if df_membres.empty:
        return pd.DataFrame(columns=["user_id", "fonction"])

    pcm = df_membres[["user_id", "collectivite_id", "fonction"]].copy()
    droits = df_droits[["user_id", "collectivite_id"]].drop_duplicates()

    via_droits = droits.merge(pcm, on=["user_id", "collectivite_id"], how="left")
    membres_hors_droit = pcm.merge(droits, on=["user_id", "collectivite_id"], how="left", indicator=True)
    membres_hors_droit = membres_hors_droit.loc[
        membres_hors_droit["_merge"] == "left_only", ["user_id", "fonction"]
    ]
    linked = pd.concat(
        [via_droits[["user_id", "fonction"]], membres_hors_droit],
        ignore_index=True,
    )
    return _dedupe_fonction_par_user(linked.drop_duplicates())


def _fonction_display_label(fonction: object) -> str:
    if fonction is None or (isinstance(fonction, float) and pd.isna(fonction)):
        return "Non renseigné"
    s = str(fonction).strip()
    if not s or s.lower() in ("none", "nan"):
        return "Non renseigné"
    labels = {
        "conseiller": "Conseiller",
        "partenaire": "Partenaire (BE)",
        "politique": "Élu / politique",
        "technique": "Agent technique",
    }
    return labels.get(s, s.replace("_", " ").capitalize())


def contacts_by_fonction(
    df_conv: pd.DataFrame,
    df_auth_users: pd.DataFrame,
    user_fonction_lookup: pd.DataFrame,
    start: pd.Timestamp,
    end: pd.Timestamp,
) -> pd.Series:
    """Nombre de contacts uniques (email) par fonction sur la période."""
    conv = conversations_in_period(df_conv, start, end)
    if conv.empty or "email" not in conv.columns:
        return pd.Series(dtype=int)

    contacts = (
        conv[["email"]]
        .dropna()
        .drop_duplicates()
        .assign(_email_key=lambda d: _normalize_email(d["email"]))
    )
    if contacts.empty:
        return pd.Series(dtype=int)

    users = df_auth_users.rename(columns={"id": "user_id"}).copy()
    users["_email_key"] = _normalize_email(users["email"])
    users = users.drop_duplicates(subset=["_email_key"], keep="first")

    merged = contacts.merge(
        users[["user_id", "_email_key"]],
        on="_email_key",
        how="left",
    ).merge(user_fonction_lookup, on="user_id", how="left")
    merged["fonction_label"] = merged["fonction"].apply(_fonction_display_label)
    merged.loc[merged["user_id"].isna(), "fonction_label"] = "Non identifié"

    return merged["fonction_label"].value_counts()


def operator_counts(df_conv: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp) -> pd.Series:
    conv = conversations_in_period(df_conv, start, end)
    if conv.empty or "operator" not in conv.columns:
        return pd.Series(dtype=int)
    conv = conv[conv["operator"].notna()]
    if conv.empty:
        return pd.Series(dtype=int)
    return conv["operator"].value_counts()


def monthly_conversations_series(
    df_conv: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp
) -> pd.DataFrame:
    rows = []
    for m in months_in_period(start, end):
        m_start, m_end = _month_bounds(m, end)
        n = count_conversations(df_conv, m_start, m_end)
        if n > 0:
            rows.append({"mois": m, "value": n})
    return pd.DataFrame(rows)


def monthly_support_rate_series(
    df_conv: pd.DataFrame,
    df_users: pd.DataFrame,
    start: pd.Timestamp,
    end: pd.Timestamp,
) -> pd.DataFrame:
    rows = []
    for m in months_in_period(start, end):
        m_start, m_end = _month_bounds(m, end)
        taux = support_rate(df_conv, df_users, m_start, m_end)
        if taux is not None:
            rows.append({"mois": m, "value": taux})
    return pd.DataFrame(rows)


def monthly_crisp_metric_series(
    df: pd.DataFrame,
    value_col: str,
    start: pd.Timestamp,
    end: pd.Timestamp,
) -> pd.DataFrame:
    rows = []
    for m in months_in_period(start, end):
        val = _weighted_avg(df, value_col, [m])
        if val is not None:
            rows.append({"mois": m, "value": val})
    return pd.DataFrame(rows)


def monthly_fonction_evolution(
    df_conv: pd.DataFrame,
    df_auth_users: pd.DataFrame,
    user_fonction_lookup: pd.DataFrame,
    start: pd.Timestamp,
    end: pd.Timestamp,
) -> pd.DataFrame:
    rows = []
    for m in months_in_period(start, end):
        m_start, m_end = _month_bounds(m, end)
        counts = contacts_by_fonction(
            df_conv, df_auth_users, user_fonction_lookup, m_start, m_end
        )
        for fonction, nb in counts.items():
            rows.append({"mois": m, "fonction": fonction, "conversations": int(nb)})
    return pd.DataFrame(rows)


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


def _mois_label(mois) -> str:
    return pd.Timestamp(mois).strftime("%Y-%m")


def _monthly_to_nivo_lines(
    df: pd.DataFrame,
    group_col: str,
    *,
    value_col: str = "conversations",
    value_cast: type = int,
) -> list[dict]:
    if df.empty:
        return []
    work = df.copy()
    work["mois"] = pd.to_datetime(work["mois"])
    all_months = sorted(work["mois"].unique())
    series = []
    for grp, sub in work.groupby(group_col, sort=False):
        by_mois = sub.groupby("mois")[value_col].sum()
        series.append({
            "id": str(grp),
            "data": [
                {"x": _mois_label(m), "y": value_cast(by_mois.get(m, 0))}
                for m in all_months
            ],
        })
    return series


def _scalar_series_to_nivo_line(df: pd.DataFrame) -> list[dict]:
    if df.empty:
        return []
    work = df.copy()
    work["mois"] = pd.to_datetime(work["mois"])
    work = work.sort_values("mois").dropna(subset=["value"])
    if work.empty:
        return []
    return [{
        "id": "valeur",
        "data": [
            {"x": _mois_label(m), "y": float(v)}
            for m, v in zip(work["mois"], work["value"], strict=True)
            if pd.notna(v)
        ],
    }]


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


def _nivo_line_chart(
    line_data: list[dict],
    chart_key: str,
    *,
    y_legend: str = "Valeur",
    show_legend: bool = False,
):
    if not line_data:
        st.info("Aucune donnée disponible.")
        return

    n_series = len(line_data)
    if show_legend and n_series > 1:
        chart_colors = _PALETTE_SEGMENTS[:n_series]
        if n_series > len(_PALETTE_SEGMENTS):
            chart_colors = [
                _PALETTE_SEGMENTS[i % len(_PALETTE_SEGMENTS)] for i in range(n_series)
            ]
    else:
        chart_colors = [_COULEUR_BAR]

    legends = []
    if show_legend and n_series > 1:
        legends = [
            {
                "anchor": "bottom-right",
                "direction": "column",
                "justify": False,
                "translateX": 120,
                "translateY": 0,
                "itemsSpacing": 2,
                "itemDirection": "left-to-right",
                "itemWidth": 100,
                "itemHeight": 20,
                "symbolSize": 12,
                "symbolShape": "circle",
            }
        ]

    with elements(chart_key):
        with mui.Box(sx={"height": 550}):
            nivo.Line(
                data=line_data,
                margin={
                    "top": 20,
                    "right": 180 if show_legend else 30,
                    "bottom": 50,
                    "left": 90,
                },
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
                    "tickRotation": -45,
                },
                axisLeft={
                    "tickSize": 5,
                    "tickPadding": 5,
                    "tickRotation": 0,
                    "legend": y_legend,
                    "legendPosition": "middle",
                    "legendOffset": -60,
                },
                enableArea=False,
                enablePoints=False,
                useMesh=True,
                enableSlices="x",
                colors=chart_colors,
                legends=legends,
                theme=theme_actif,
            )


def _nivo_multi_line(
    df: pd.DataFrame,
    group_col: str,
    title: str,
    icon: str,
    color: str,
    chart_key: str,
    *,
    y_legend: str = "Conversations",
    value_col: str = "conversations",
    value_cast: type = int,
):
    st.badge(f"{title}", icon=icon, color=color)
    line_data = _monthly_to_nivo_lines(
        df, group_col, value_col=value_col, value_cast=value_cast
    )
    _nivo_line_chart(
        line_data,
        chart_key,
        y_legend=y_legend,
        show_legend=True,
    )


def _value_counts_to_nivo_pie(counts: pd.Series) -> list[dict]:
    if counts.empty:
        return []
    return [
        {"id": str(k), "label": str(k), "value": int(v)}
        for k, v in counts.items()
    ]


def _nivo_pie(
    counts: pd.Series,
    title: str,
    icon: str,
    color: str,
    chart_key: str,
):
    st.badge(f"{title}", icon=icon, color=color)
    data = _value_counts_to_nivo_pie(counts)
    if not data:
        st.info("Aucune donnée sur la période sélectionnée.")
        return

    with elements(chart_key):
        with mui.Box(sx={"height": 360}):
            nivo.Pie(
                data=data,
                margin={"top": 20, "right": 80, "bottom": 60, "left": 80},
                innerRadius=0.5,
                padAngle=0.7,
                cornerRadius=3,
                activeOuterRadiusOffset=8,
                colors=_PALETTE_SEGMENTS,
                borderWidth=1,
                borderColor={"from": "color", "modifiers": [["darker", 0.2]]},
                arcLinkLabelsSkipAngle=10,
                arcLinkLabelsTextColor="#31333F",
                arcLinkLabelsThickness=2,
                arcLinkLabelsColor={"from": "color"},
                arcLabelsSkipAngle=10,
                arcLabelsTextColor="#ffffff",
                animate=True,
                motionConfig="gentle",
                theme=theme_actif,
            )


def _monthly_long_to_stacked(
    df: pd.DataFrame, cat_col: str, *, value_col: str = "value"
) -> tuple[list[dict], list[str]]:
    """df long {mois, cat_col, value_col} -> (bar_data indexBy mois, keys cat triées par total)."""
    if df.empty:
        return [], []
    work = df.copy()
    work["mois"] = pd.to_datetime(work["mois"])
    months = sorted(work["mois"].unique())
    cat_totals = work.groupby(cat_col)[value_col].sum().sort_values(ascending=False)
    keys = [str(c) for c in cat_totals.index]
    bar_data = []
    for m in months:
        row = {"mois": _mois_label(m)}
        sub = work[work["mois"] == m]
        for cat in cat_totals.index:
            row[str(cat)] = int(sub[sub[cat_col] == cat][value_col].sum())
        bar_data.append(row)
    return bar_data, keys


def _nivo_monthly_stacked_bar(
    bar_data: list[dict],
    keys: list[str],
    title: str,
    icon: str,
    color: str,
    chart_key: str,
    *,
    y_legend: str = "Tickets",
):
    st.badge(f"{title}", icon=icon, color=color)
    if not bar_data or not keys:
        st.info("Aucune donnée disponible.")
        return

    n_keys = len(keys)
    colors = [_PALETTE_SEGMENTS[i % len(_PALETTE_SEGMENTS)] for i in range(n_keys)]

    with elements(chart_key):
        with mui.Box(sx={"height": 550}):
            nivo.Bar(
                data=bar_data,
                keys=keys,
                indexBy="mois",
                layout="vertical",
                groupMode="stacked",
                margin={"top": 20, "right": 180, "bottom": 80, "left": 70},
                padding=0.3,
                valueScale={"type": "linear", "min": 0},
                indexScale={"type": "band", "round": True},
                colors=colors,
                borderRadius=2,
                borderColor={"from": "color", "modifiers": [["darker", 0.4]]},
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
                    "legend": y_legend,
                    "legendPosition": "middle",
                    "legendOffset": -55,
                },
                enableLabel=True,
                labelSkipWidth=16,
                labelSkipHeight=12,
                labelTextColor="#ffffff",
                legends=[
                    {
                        "dataFrom": "keys",
                        "anchor": "bottom-right",
                        "direction": "column",
                        "justify": False,
                        "translateX": 170,
                        "translateY": 0,
                        "itemsSpacing": 2,
                        "itemWidth": 160,
                        "itemHeight": 20,
                        "itemDirection": "left-to-right",
                        "symbolSize": 12,
                        "symbolShape": "circle",
                    }
                ],
                animate=True,
                motionConfig="gentle",
                theme=theme_actif,
            )


def _graphe_mean(series: pd.DataFrame) -> float | None:
    """Moyenne sur les mois présents dans la série (sans imputer 0 aux mois absents)."""
    if series.empty or "value" not in series.columns:
        return None
    vals = series["value"].dropna()
    if vals.empty:
        return None
    return float(vals.mean())


def _format_graphe_average(stat_id: str, series: pd.DataFrame) -> str:
    avg = _graphe_mean(series)
    if avg is None:
        return "—"
    if stat_id == "taux_support":
        return f"{avg:.1f} %"
    if stat_id in ("temps_reponse", "temps_resolution"):
        return format_duration_h(avg)
    if stat_id == "satisfaction":
        return f"{avg:.2f}"
    return f"{avg:.0f}"


def _first_mois_with_positive_value(series: pd.DataFrame) -> pd.Timestamp | None:
    if series.empty or "value" not in series.columns:
        return None
    work = series.copy()
    work["mois"] = pd.to_datetime(work["mois"])
    pos = work[work["value"] > 0]
    if pos.empty:
        return None
    return pd.Timestamp(year=pos["mois"].min().year, month=pos["mois"].min().month, day=1)


def _first_mois_with_positive_total(
    df: pd.DataFrame, value_col: str = "conversations"
) -> pd.Timestamp | None:
    if df.empty:
        return None
    work = df.copy()
    work["mois"] = pd.to_datetime(work["mois"])
    monthly = work.groupby("mois")[value_col].sum()
    monthly = monthly[monthly > 0]
    if monthly.empty:
        return None
    first = monthly.index.min()
    return pd.Timestamp(year=first.year, month=first.month, day=1)


def _effective_graphe_start(first_mois: pd.Timestamp | None) -> pd.Timestamp:
    if first_mois is None:
        return _GRAPHE_START
    first = pd.Timestamp(year=first_mois.year, month=first_mois.month, day=1)
    return max(_GRAPHE_START, first)


def _clip_from_start(df: pd.DataFrame, start: pd.Timestamp) -> pd.DataFrame:
    if df.empty or "mois" not in df.columns:
        return df
    out = df.copy()
    out["mois"] = pd.to_datetime(out["mois"])
    return out[out["mois"] >= start].copy()


def _render_graphe_view(
    stat_label: str,
    *,
    df_conv: pd.DataFrame,
    df_users: pd.DataFrame,
    df_rating: pd.DataFrame,
    df_temps_rep: pd.DataFrame,
    df_temps_res: pd.DataFrame,
    df_auth_users: pd.DataFrame,
    user_fonction_lookup: pd.DataFrame,
    graphe_end: pd.Timestamp,
):
    stat_id = _GRAPHE_STATS[stat_label]
    scan_start = _GRAPHE_START
    df_conv_scan = df_conv[
        (df_conv["updated_at"] >= scan_start) & (df_conv["updated_at"] <= graphe_end)
    ] if not df_conv.empty else df_conv

    series: pd.DataFrame | None = None
    evo: pd.DataFrame | None = None
    group_col: str | None = None
    y_legend = "Valeur"

    if stat_id == "conversations":
        series = monthly_conversations_series(df_conv, scan_start, graphe_end)
        y_legend = "Conversations"
    elif stat_id == "taux_support":
        series = monthly_support_rate_series(df_conv, df_users, scan_start, graphe_end)
        y_legend = "Taux (%)"
    elif stat_id == "temps_reponse":
        series = monthly_crisp_metric_series(
            df_temps_rep, "response_time_h", scan_start, graphe_end
        )
        y_legend = "Heures"
    elif stat_id == "temps_resolution":
        series = monthly_crisp_metric_series(
            df_temps_res, "temps_resolution_h", scan_start, graphe_end
        )
        y_legend = "Heures"
    elif stat_id == "satisfaction":
        series = monthly_crisp_metric_series(df_rating, "rating", scan_start, graphe_end)
        y_legend = "Note"
    elif stat_id == "segments":
        evo = monthly_category_evolution(df_conv_scan)
        group_col = "categorie"
        y_legend = "Conversations"
    elif stat_id == "operateurs":
        evo = monthly_operator_evolution(df_conv_scan)
        group_col = "operator"
        y_legend = "Conversations"
    else:
        evo = monthly_fonction_evolution(
            df_conv, df_auth_users, user_fonction_lookup, scan_start, graphe_end
        )
        group_col = "fonction"
        y_legend = "Contacts"

    _multi_stat = stat_id in ("segments", "operateurs", "profil_contact")
    avg_value = "—"

    if _multi_stat and evo is not None and group_col is not None:
        chart_start = _effective_graphe_start(_first_mois_with_positive_total(evo))
        evo = _clip_from_start(evo, chart_start)
        bar_data, keys = _monthly_long_to_stacked(
            evo, group_col, value_col="conversations"
        )
        _nivo_monthly_stacked_bar(
            bar_data,
            keys=keys,
            title=stat_label,
            icon=":material/bar_chart:",
            color="blue",
            chart_key="bug_graphe",
            y_legend=y_legend,
        )
        return

    if series is not None:
        chart_start = _effective_graphe_start(_first_mois_with_positive_value(series))
        series = _clip_from_start(series, chart_start)
        line_data = _scalar_series_to_nivo_line(series)
        avg_value = _format_graphe_average(stat_id, series)
    else:
        line_data = []

    st.metric(label=f"{stat_label} (moyenne)", value=avg_value)
    st.badge(stat_label, icon=":material/show_chart:", color="blue")
    _nivo_line_chart(
        line_data,
        "bug_graphe",
        y_legend=y_legend,
        show_legend=False,
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

@st.cache_resource(ttl="1d")
def get_prepared_data():
    """Charge ET prépare les données une seule fois (évite de recalculer à chaque rerun).

    La préparation (notamment la construction du lookup user→fonction qui boucle
    en Python) est coûteuse : la mettre en cache évite de la rejouer à chaque
    interaction avec un sélecteur.
    """
    raw = load_data()
    return {
        "df_conv": _prepare_conversations(raw["crisp_conversation"]),
        "df_users": _prepare_user_actifs(raw["user_actifs_ct_mois"]),
        "user_fonction_lookup": _build_user_fonction_lookup(
            raw["auth_users"],
            raw["private_utilisateur_droit"],
            raw["private_collectivite_membre"],
        ),
        "df_rating": _prepare_monthly_crisp(raw["crisp_rating"]),
        "df_temps_rep": _prepare_monthly_crisp(raw["crisp_temps_reponse"]),
        "df_temps_res": _prepare_monthly_crisp(raw["crisp_temps_resolution"]),
        "auth_users": raw["auth_users"],
        "df_tickets": _prepare_tickets(raw["notion_ticket"]),
        "df_tickets_raw": raw["notion_ticket"],
    }


_prepared = get_prepared_data()

df_conv = _prepared["df_conv"]
df_users = _prepared["df_users"]
_user_fonction_lookup = _prepared["user_fonction_lookup"]
df_rating = _prepared["df_rating"]
df_temps_rep = _prepared["df_temps_rep"]
df_temps_res = _prepared["df_temps_res"]
df_tickets = _prepared["df_tickets"]
df_tickets_raw = _prepared["df_tickets_raw"]

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
        options=["Mois", "Trimestre", "Graphe"],
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

is_graphe = view == "Graphe"
graphe_start = _GRAPHE_START
graphe_end = today

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
elif is_graphe:
    cur_start = graphe_start
    cur_end = graphe_end
    prev_start = cur_start
    prev_end = cur_end

cur_months = months_in_period(cur_start, cur_end)
prev_months = months_in_period(prev_start, prev_end)

st.markdown("---")

tab_support, tab_bug = st.tabs(["Support", "Bug"])


# ==========================
# Onglet Support (vue actuelle)
# ==========================

with tab_support:
    if is_graphe:
        st.selectbox(
            "Statistique",
            options=list(_GRAPHE_STATS.keys()),
            key="graphe_stat_bug",
        )
        st.subheader("Graphe")
        _render_graphe_view(
            st.session_state.get("graphe_stat_bug", list(_GRAPHE_STATS.keys())[0]),
            df_conv=df_conv,
            df_users=df_users,
            df_rating=df_rating,
            df_temps_rep=df_temps_rep,
            df_temps_res=df_temps_res,
            df_auth_users=_prepared["auth_users"],
            user_fonction_lookup=_user_fonction_lookup,
            graphe_end=graphe_end,
        )
    else:
        # ----- Section 1 : Les chiffres du support -----
        st.subheader("Les chiffres du support")

        nb_conv_cur = count_conversations(df_conv, cur_start, cur_end)
        taux_cur = support_rate(df_conv, df_users, cur_start, cur_end)
        rep_cur = _weighted_avg(df_temps_rep, "response_time_h", cur_months)
        res_cur = _weighted_avg(df_temps_res, "temps_resolution_h", cur_months)
        sat_cur = _weighted_avg(df_rating, "rating", cur_months)

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

        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            st.metric(
                label="Nombre de conversations",
                value=nb_conv_cur,
                delta=_d_conv,
                delta_color="inverse",
            )
        with c2:
            st.metric(
                label="Taux de support",
                value=f"{taux_cur:.1f} %" if taux_cur is not None else "—",
                delta=_d_taux,
                delta_color="inverse",
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

        # ----- Section 2 : Type de contact -----
        st.subheader("Conversations par segment et opérateur")

        _top3_segments = top_segment_counts(df_conv, cur_start, cur_end, n=3)
        st.markdown(_format_top_segments_md(_top3_segments))

        col_seg, col_op = st.columns(2)

        with col_seg:
            _cat_seg_df = category_segment_counts(df_conv, cur_start, cur_end)
            _cat_data, _cat_keys, _cat_colors = _category_segment_to_nivo_horizontal(_cat_seg_df)
            _nivo_horizontal_stacked_bar(
                _cat_data,
                keys=_cat_keys,
                index_key="Catégorie",
                title="Segments",
                icon=":material/bar_chart:",
                color="blue",
                chart_key="bug_bar_category",
                segment_colors=_cat_colors,
            )

        with col_op:
            _nivo_horizontal_bar(
                counts=operator_counts(df_conv, cur_start, cur_end),
                index_key="Opérateur",
                title="Opérateurs",
                icon=":material/person:",
                color="blue",
                chart_key="bug_bar_operator",
            )

        st.markdown("---")

        # ----- Section 3 : Profil des contacteurs -----
        st.subheader("Profil de ceux qui nous contacte")

        _fonction_counts = contacts_by_fonction(
            df_conv,
            _prepared["auth_users"],
            _user_fonction_lookup,
            cur_start,
            cur_end,
        )

        _nivo_horizontal_bar(
            counts=_fonction_counts,
            index_key="Fonction",
            title="Contacts par fonction",
            icon=":material/groups:",
            color="green",
            chart_key="bug_bar_fonction",
        )


# ==========================
# Onglet Bug (notion_ticket)
# ==========================

with tab_bug:
    if df_tickets.empty:
        with st.expander("⚠️ Diagnostic : aucun ticket bug trouvé", expanded=True):
            st.write(
                f"notion_ticket brut : {len(df_tickets_raw)} lignes, "
                f"df_tickets (filtré bugs) : {len(df_tickets)} lignes."
            )
            if not df_tickets_raw.empty:
                st.write("Colonnes :", list(df_tickets_raw.columns))
                if "epic_name" in df_tickets_raw.columns:
                    _ep = df_tickets_raw["epic_name"]
                    st.write(
                        f"epic_name → dtype={_ep.dtype}, "
                        f"type d'une cellule={type(_ep.dropna().iloc[0]).__name__ if _ep.notna().any() else 'aucune valeur'}"
                    )
                    st.write("Exemples epic_name :", _ep.dropna().head(10).tolist())
                else:
                    st.warning("La colonne 'epic_name' est absente de notion_ticket.")
                st.dataframe(df_tickets_raw.head(50))
            else:
                st.warning("La table notion_ticket est vide côté base.")

    if is_graphe:
        st.subheader("Évolution des bugs")

        _bug_monthly = monthly_bug_counts(df_tickets)
        _bug_monthly = _clip_from_start(_bug_monthly, _GRAPHE_START)
        st.badge("Tickets bugs par mois", icon=":material/show_chart:", color="red")
        _nivo_line_chart(
            _scalar_series_to_nivo_line(_bug_monthly),
            "bug_tab_line",
            y_legend="Tickets",
            show_legend=False,
        )

        st.markdown("---")

        _them_monthly = monthly_bug_by_category(df_tickets, "thematique")
        _them_monthly = _clip_from_start(_them_monthly, _GRAPHE_START)
        _them_data, _them_keys = _monthly_long_to_stacked(_them_monthly, "thematique")
        _nivo_monthly_stacked_bar(
            _them_data,
            keys=_them_keys,
            title="Bugs par thématique (mensuel)",
            icon=":material/bar_chart:",
            color="red",
            chart_key="bug_tab_stacked_thematique",
        )

        st.markdown("---")

        _crit_monthly = monthly_bug_by_category(df_tickets, "criticite")
        _crit_monthly = _clip_from_start(_crit_monthly, _GRAPHE_START)
        _crit_data, _crit_keys = _monthly_long_to_stacked(_crit_monthly, "criticite")
        _nivo_monthly_stacked_bar(
            _crit_data,
            keys=_crit_keys,
            title="Bugs par criticité (mensuel)",
            icon=":material/bar_chart:",
            color="red",
            chart_key="bug_tab_stacked_criticite",
        )
    else:
        st.subheader("Les chiffres des bugs")

        nb_bug_cur = count_bugs(df_tickets, cur_start, cur_end)
        nb_bug_prev = count_bugs(df_tickets, prev_start, prev_end)
        nb_bloq_cur = count_bugs_bloquant(df_tickets, cur_start, cur_end)
        nb_bloq_prev = count_bugs_bloquant(df_tickets, prev_start, prev_end)
        _d_bug = _metric_delta(nb_bug_cur, nb_bug_prev, fmt="int")
        _d_bloq = _metric_delta(nb_bloq_cur, nb_bloq_prev, fmt="int")

        m1, m2 = st.columns(2)
        with m1:
            st.metric(
                label="Nombre de tickets bugs",
                value=nb_bug_cur,
                delta=_d_bug,
                delta_color="inverse",
            )
        with m2:
            st.metric(
                label="Bugs bloquants",
                value=nb_bloq_cur,
                delta=_d_bloq,
                delta_color="inverse",
            )

        st.markdown("---")

        st.subheader("Répartition des bugs")

        _bug_period = tickets_in_period(df_tickets, cur_start, cur_end)

        p1, p2 = st.columns(2)
        with p1:
            _statut_counts = (
                _bug_period["statut"].dropna().value_counts()
                if not _bug_period.empty and "statut" in _bug_period.columns
                else pd.Series(dtype=int)
            )
            _nivo_pie(
                _statut_counts,
                title="Statut",
                icon=":material/donut_large:",
                color="red",
                chart_key="bug_tab_pie_statut",
            )
        with p2:
            _them_counts = (
                _bug_period["thematique"].dropna().value_counts()
                if not _bug_period.empty and "thematique" in _bug_period.columns
                else pd.Series(dtype=int)
            )
            _nivo_pie(
                _them_counts,
                title="Thématique",
                icon=":material/donut_large:",
                color="red",
                chart_key="bug_tab_pie_thematique",
            )

        p3, _p4 = st.columns(2)
        with p3:
            _crit_counts = (
                _bug_period["criticite"].dropna().value_counts()
                if not _bug_period.empty and "criticite" in _bug_period.columns
                else pd.Series(dtype=int)
            )
            _nivo_pie(
                _crit_counts,
                title="Criticité",
                icon=":material/donut_large:",
                color="red",
                chart_key="bug_tab_pie_criticite",
            )
