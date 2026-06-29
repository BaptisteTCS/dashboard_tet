import streamlit as st

st.set_page_config(
    page_title="User Path",
    page_icon="🛤️",
    layout="wide",
)

from collections import Counter

import pandas as pd
from sqlalchemy import text

from utils.db import get_engine, get_engine_prod

POSTHOG_COLUMNS = [
    "email",
    "collectivite_id",
    "timestamp",
    "next_timestamp",
    "next_path_clean",
    "current_path_clean",
]


@st.cache_data(ttl="3d", show_spinner="Chargement des parcours PostHog…")
def load_posthog_next_path() -> pd.DataFrame:
    engine = get_engine()
    cols = ", ".join(POSTHOG_COLUMNS)
    query = text(f"SELECT {cols} FROM posthog_next_path")
    with engine.connect() as conn:
        df = pd.read_sql_query(query, conn)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["next_timestamp"] = pd.to_datetime(df["next_timestamp"], errors="coerce")
    return df


@st.cache_data(ttl="3d", show_spinner="Chargement des utilisateurs internes…")
def load_internal_user_emails() -> set[str]:
    engine = get_engine()
    query = text("SELECT DISTINCT email FROM internal_users")
    with engine.connect() as conn:
        df = pd.read_sql_query(query, conn)
    return set(df["email"].dropna().astype(str))


@st.cache_data(ttl="3d", show_spinner="Chargement des conseillers…")
def load_conseiller_emails() -> set[str]:
    engine = get_engine_prod()
    query = text("""
        SELECT DISTINCT u.email
        FROM private_collectivite_membre pcm
        JOIN auth.users u ON pcm.user_id = u.id
        WHERE pcm.fonction = 'conseiller'
    """)
    with engine.connect() as conn:
        df = pd.read_sql_query(query, conn)
    return set(df["email"].dropna().astype(str))


def top_sequences(
    df,
    user_col="email",
    start_path: str = "",
    depth=4,
    top_n=30,
    max_gap_minutes=30,
):
    d = df[[user_col, "current_path_clean", "timestamp"]].copy()
    d = d.sort_values([user_col, "timestamp"]).reset_index(drop=True)

    gap = d["timestamp"].diff().dt.total_seconds() / 60
    new_session = (d[user_col] != d[user_col].shift()) | (gap > max_gap_minutes)
    d["session"] = new_session.cumsum()

    counter = Counter()
    paths = d["current_path_clean"].to_numpy()
    sessions = d["session"].to_numpy()

    n = len(paths)
    for i in range(n - depth + 1):
        if sessions[i] == sessions[i + depth - 1]:
            seq = tuple(paths[i : i + depth])
            if seq[0] == start_path:
                counter[seq] += 1

    return counter.most_common(top_n)


def path_occurrence_counts(df: pd.DataFrame) -> list[tuple[str, int]]:
    counts = df["current_path_clean"].value_counts()
    return [(path, int(count)) for path, count in counts.items()]


def filter_paths(
    df: pd.DataFrame,
    segment: str,
    internal_emails: set[str],
    conseiller_emails: set[str],
) -> pd.DataFrame:
    filtered = df[~df["email"].isin(internal_emails)].copy()
    if segment == "conseiller":
        filtered = filtered[filtered["email"].isin(conseiller_emails)]
    else:
        filtered = filtered[~filtered["email"].isin(conseiller_emails)]
    return filtered


def render_top_paths(results: list[tuple[tuple, int]]) -> None:
    if not results:
        st.info("Aucun parcours trouvé pour ces critères.")
        return

    for rank, (seq, count) in enumerate(results, 1):
        path_str = " → ".join(seq)
        st.markdown(f"**#{rank}** · {count} occurrence{'s' if count > 1 else ''}")
        st.code(path_str, language=None)
        st.divider()


# ==========================
# Interface
# ==========================

st.title("🛤️ User Path")

df_paths = load_posthog_next_path()
internal_emails = load_internal_user_emails()
conseiller_emails = load_conseiller_emails()

col_seg, col_start, col_depth = st.columns([1.2, 2, 0.8])

with col_seg:
    segment = st.segmented_control(
        "Segment",
        options=["technique", "conseiller"],
        default="technique",
        key="user_path_segment",
    )

if not segment:
    segment = "technique"

df_filtered = filter_paths(df_paths, segment, internal_emails, conseiller_emails)
path_counts = path_occurrence_counts(df_filtered)

if not path_counts:
    st.warning("Aucune page disponible pour ce segment.")
    st.stop()

path_count_lookup = dict(path_counts)
start_path_options = [path for path, _ in path_counts]

with col_start:
    start_path = st.selectbox(
        "Page de départ",
        options=start_path_options,
        format_func=lambda p: f"{p} ({path_count_lookup[p]:,} occurrences)",
        help="Parcours commençant par cette page.",
    )

with col_depth:
    depth = st.number_input(
        "Profondeur",
        min_value=2,
        max_value=8,
        value=4,
        step=1,
        help="Nombre de pages consécutives dans un parcours.",
    )

nb_users = df_filtered["email"].nunique()
nb_events = len(df_filtered)

st.caption(
    f"{nb_events:,} événements · {nb_users:,} utilisateurs · segment **{segment}**"
)

st.markdown("---")
st.subheader(f"Top 15 des parcours (profondeur {depth}) depuis **{start_path}**")

results = top_sequences(df_filtered, start_path=start_path, depth=depth, top_n=15)
render_top_paths(results)
