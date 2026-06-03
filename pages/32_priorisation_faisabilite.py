import streamlit as st

st.set_page_config(
    page_title="Priorisation — faisabilité politique",
    page_icon="⚖️",
    layout="wide",
)

import pandas as pd
from sqlalchemy import text

from utils.db import get_engine
from utils.priorisation_navigation import render_etape_2_nav

# ==========================
# Constantes
# ==========================

CATEGORIES = {
    1: "Aménagement",
    2: "Réglementation",
    3: "Financement",
    4: "Gouvernance",
    5: "Exemplarité",
    6: "Sensibilisation",
}

FAISABILITE_OPTIONS = (
    "Hors de portée politique",
    "À discuter",
    "Prioritaire",
)

# 1 = Hors de portée, 2 = À discuter, 3 = Prioritaire
FAISABILITE_TO_INT = {label: i for i, label in enumerate(FAISABILITE_OPTIONS, start=1)}
INT_TO_FAISABILITE = {v: k for k, v in FAISABILITE_TO_INT.items()}

TOP_N_INITIAL = 5
TOP_N_MAX = 10

SESSION_FAISABILITE = "faisabilite_choices"
SESSION_COLLECTIVITE = "faisabilite_collectivite_id"
SESSION_SHOW_MORE = "faisabilite_show_more"


# ==========================
# Chargement des données
# ==========================


@st.cache_data(ttl="1h")
def load_collectivites_priorisees() -> pd.DataFrame:
    """Collectivités ayant au moins une ligne dans priorisation (OLAP)."""
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("""
                SELECT DISTINCT c.collectivite_id, c.nom
                FROM collectivite c
                INNER JOIN priorisation p ON p.collectivite_id = c.collectivite_id
                WHERE c.nom IS NOT NULL
                ORDER BY c.nom
            """),
            conn,
        )


@st.cache_data(ttl="1h")
def load_poids_categories() -> pd.DataFrame:
    """Poids catégorie × levier (référentiel statique OLAP)."""
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("SELECT * FROM priorisation_categorie_levier"),
            conn,
        )


@st.cache_data(ttl="1h")
def load_priorisation(collectivite_id: int) -> pd.DataFrame:
    """Notes les plus récentes par case (levier × catégorie)."""
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("""
                SELECT DISTINCT ON (levier, categorie)
                    levier, categorie, note
                FROM priorisation
                WHERE collectivite_id = :collectivite_id
                ORDER BY levier, categorie, created_at DESC
            """),
            conn,
            params={"collectivite_id": collectivite_id},
        )


@st.cache_data(ttl="1h")
def load_reductions(collectivite_id: int) -> pd.DataFrame:
    """Réductions les plus récentes par levier."""
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("""
                SELECT DISTINCT ON (levier)
                    levier, reduction
                FROM priorisation_reduction_levier
                WHERE collectivite_id = :collectivite_id
                ORDER BY levier, created_at DESC
            """),
            conn,
            params={"collectivite_id": collectivite_id},
        )


@st.cache_data(ttl="1h")
def load_hors_competence(collectivite_id: int) -> pd.DataFrame:
    """Couples levier × catégorie hors compétence pour une collectivité."""
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("""
                SELECT levier, categorie
                FROM priorisation_hors_competence
                WHERE collectivite_id = :collectivite_id
            """),
            conn,
            params={"collectivite_id": collectivite_id},
        )


@st.cache_data(ttl="1h")
def load_faisabilite(collectivite_id: int) -> pd.DataFrame:
    """Arbitrages politiques enregistrés pour une collectivité."""
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("""
                SELECT levier, categorie, faisabilite
                FROM priorisation_faisabilite
                WHERE collectivite_id = :collectivite_id
            """),
            conn,
            params={"collectivite_id": collectivite_id},
        )


def build_category_weights(df_poids: pd.DataFrame) -> dict[str, dict[int, float]]:
    """Retourne {levier: {categorie: poids}} depuis priorisation_categorie_levier."""
    levier_cols = [c for c in df_poids.columns if c != "categorie"]
    weights: dict[str, dict[int, float]] = {levier: {} for levier in levier_cols}
    for _, row in df_poids.iterrows():
        cat = int(row["categorie"])
        for levier in levier_cols:
            val = row[levier]
            weights[levier][cat] = 0.0 if pd.isna(val) else float(val)
    return weights


def hors_competence_pairs(df: pd.DataFrame) -> set[tuple[str, int]]:
    return {(row["levier"], int(row["categorie"])) for _, row in df.iterrows()}


def build_notes(df_priorisation: pd.DataFrame) -> dict[tuple[str, int], int]:
    return {
        (row["levier"], int(row["categorie"])): int(row["note"])
        for _, row in df_priorisation.iterrows()
    }


# ==========================
# Potentiel non mobilisé (cœur du calcul)
# ==========================


def _poids_angle_mort(
    levier: str,
    cat: int,
    notes: dict[tuple[str, int], int],
    exclusions: set[tuple[str, int]],
    weights: dict[str, dict[int, float]],
) -> float | None:
    """
    Poids d'une catégorie comptée dans le potentiel non mobilisé, ou None si exclue.
    Conditions : note 0 ou 1, dans le périmètre (pas hors compétence), poids > 0.
    """
    if (levier, cat) in exclusions:
        return None
    poids = weights.get(levier, {}).get(cat, 0.0)
    if poids <= 0:
        return None
    note = notes.get((levier, cat), 0)
    if note not in (0, 1):
        return None
    return poids


def angle_mort_categories(
    levier: str,
    notes: dict[tuple[str, int], int],
    exclusions: set[tuple[str, int]],
    weights: dict[str, dict[int, float]],
) -> list[int]:
    """Catégories arbitrables : angles morts (note 0/1) encore dans le périmètre."""
    return [
        cat
        for cat in range(1, 7)
        if _poids_angle_mort(levier, cat, notes, exclusions, weights) is not None
    ]


def calc_potentiel_non_mobilise(
    levier: str,
    reduction: float,
    notes: dict[tuple[str, int], int],
    exclusions: set[tuple[str, int]],
    weights: dict[str, dict[int, float]],
) -> float:
    """
    Potentiel non mobilisé d'un levier :
        abs(réduction) × Σ poids des catégories angles morts (note 0/1, dans le périmètre).

    Les catégories hors compétence sont ignorées — on n'arbitre pas ce sur quoi
    la collectivité ne peut pas agir.
    """
    somme_poids = sum(
        p
        for cat in range(1, 7)
        if (p := _poids_angle_mort(levier, cat, notes, exclusions, weights)) is not None
    )
    return abs(reduction) * somme_poids


def top_leviers_angles_morts(
    leviers: list[str],
    reductions: dict[str, float],
    notes: dict[tuple[str, int], int],
    exclusions: set[tuple[str, int]],
    weights: dict[str, dict[int, float]],
    n: int = TOP_N_MAX,
) -> list[tuple[str, float]]:
    """Top N leviers par potentiel non mobilisé décroissant."""
    scored: list[tuple[str, float]] = []
    for levier in leviers:
        if levier not in reductions:
            continue
        potentiel = calc_potentiel_non_mobilise(
            levier, reductions[levier], notes, exclusions, weights
        )
        if potentiel > 0:
            scored.append((levier, potentiel))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:n]


# ==========================
# Agrégation levier ↔ catégorie (faisabilité)
# ==========================


def levier_faisabilite_value(
    levier: str,
    faisabilites: dict[tuple[str, int], int],
    angle_mort_cats: list[int],
) -> int | None:
    """
    Agrégat levier ← catégories : renvoie 1/2/3 si toutes les catégories angles morts
    partagent la même faisabilité ; sinon None (toggle indéterminé / non sélectionné).
    """
    if not angle_mort_cats:
        return None
    values = [faisabilites.get((levier, cat)) for cat in angle_mort_cats]
    if any(v is None for v in values):
        return None
    if len(set(values)) == 1:
        return values[0]
    return None


def set_levier_faisabilite(
    levier: str,
    label: str,
    angle_mort_cats: list[int],
    faisabilites: dict[tuple[str, int], int],
) -> None:
    """Raccourci levier : applique la faisabilité à toutes les catégories angles morts."""
    val = FAISABILITE_TO_INT[label]
    for cat in angle_mort_cats:
        faisabilites[(levier, cat)] = val


def set_categorie_faisabilite(
    levier: str,
    cat: int,
    label: str,
    faisabilites: dict[tuple[str, int], int],
) -> None:
    faisabilites[(levier, cat)] = FAISABILITE_TO_INT[label]


def faisabilites_from_db(
    df: pd.DataFrame,
    notes: dict[tuple[str, int], int],
    exclusions: set[tuple[str, int]],
    weights: dict[str, dict[int, float]],
) -> dict[tuple[str, int], int]:
    """Charge les arbitrages persistés en ne gardant que les cases angles morts valides."""
    result: dict[tuple[str, int], int] = {}
    for _, row in df.iterrows():
        levier = row["levier"]
        cat = int(row["categorie"])
        fais = int(row["faisabilite"])
        if fais not in INT_TO_FAISABILITE:
            continue
        if cat not in angle_mort_categories(levier, notes, exclusions, weights):
            continue
        result[(levier, cat)] = fais
    return result


def collect_faisabilites_to_save(
    faisabilites: dict[tuple[str, int], int],
    notes: dict[tuple[str, int], int],
    exclusions: set[tuple[str, int]],
    weights: dict[str, dict[int, float]],
) -> list[tuple[str, int, int]]:
    """Liste triée des arbitrages valides à persister (catégories renseignées uniquement)."""
    rows: list[tuple[str, int, int]] = []
    for (levier, cat), fais in faisabilites.items():
        if fais not in INT_TO_FAISABILITE:
            continue
        if cat not in angle_mort_categories(levier, notes, exclusions, weights):
            continue
        rows.append((levier, cat, fais))
    return sorted(rows, key=lambda x: (x[0], x[1]))


def init_session_faisabilite(
    collectivite_id: int,
    notes: dict[tuple[str, int], int],
    exclusions: set[tuple[str, int]],
    weights: dict[str, dict[int, float]],
) -> None:
    if st.session_state.get(SESSION_COLLECTIVITE) == collectivite_id:
        return
    df = load_faisabilite(collectivite_id)
    st.session_state[SESSION_FAISABILITE] = faisabilites_from_db(
        df, notes, exclusions, weights
    )
    st.session_state[SESSION_COLLECTIVITE] = collectivite_id
    st.session_state.pop(SESSION_SHOW_MORE, None)


def sync_segmented_key(key: str, label: str | None) -> None:
    """Synchronise un segmented control : sélectionné ou indéterminé (default=None)."""
    if label is not None:
        st.session_state[key] = label
    elif key in st.session_state:
        del st.session_state[key]


def save_faisabilite(
    collectivite_id: int,
    rows: list[tuple[str, int, int]],
) -> None:
    """Remplacement complet des arbitrages pour la collectivité (une transaction)."""
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(
            text(
                "DELETE FROM priorisation_faisabilite "
                "WHERE collectivite_id = :collectivite_id"
            ),
            {"collectivite_id": collectivite_id},
        )
        if rows:
            conn.execute(
                text("""
                    INSERT INTO priorisation_faisabilite
                        (collectivite_id, levier, categorie, faisabilite)
                    VALUES (:collectivite_id, :levier, :categorie, :faisabilite)
                """),
                [
                    {
                        "collectivite_id": collectivite_id,
                        "levier": levier,
                        "categorie": cat,
                        "faisabilite": fais,
                    }
                    for levier, cat, fais in rows
                ],
            )


# ==========================
# Callbacks widgets
# ==========================


def _on_levier_change(levier: str, angle_mort_cats: list[int]) -> None:
    key = f"faisabilite_levier_{levier}"
    label = st.session_state[key]
    faisabilites = st.session_state[SESSION_FAISABILITE]
    set_levier_faisabilite(levier, label, angle_mort_cats, faisabilites)


def _on_categorie_change(levier: str, cat: int) -> None:
    key = f"faisabilite_cat_{levier}_{cat}"
    label = st.session_state[key]
    faisabilites = st.session_state[SESSION_FAISABILITE]
    set_categorie_faisabilite(levier, cat, label, faisabilites)


# ==========================
# Interface
# ==========================

st.title("⚖️ Faisabilité politique")

st.markdown(
    "Après le diagnostic, cette étape sert à **arbitrer politiquement** les leviers "
    "à fort **potentiel non mobilisé**, les **angles morts** où des actions restent "
    "non ou partiellement mobilisées. Pour chaque levier, indiquez s'il est "
    "**hors de portée politique**, **à discuter** ou **prioritaire**. "
    "Rien n'est sélectionné par défaut : l'arbitrage reste volontaire."
)

df_collectivites = load_collectivites_priorisees()
if df_collectivites.empty:
    st.warning("Aucune collectivité avec des données de priorisation disponible.")
    st.stop()

nom_par_id = df_collectivites.set_index("collectivite_id")["nom"].to_dict()
collectivite_ids = df_collectivites["collectivite_id"].tolist()

default_index = 0
qp_id = st.query_params.get("collectivite_id")
if qp_id is not None:
    try:
        qp_id_int = int(qp_id)
        if qp_id_int in collectivite_ids:
            default_index = collectivite_ids.index(qp_id_int)
    except (TypeError, ValueError):
        pass

collectivite_id = st.selectbox(
    "Collectivité",
    options=collectivite_ids,
    index=default_index,
    format_func=lambda cid: nom_par_id[cid],
    key="faisabilite_select_collectivite",
)

st.markdown("---")

df_priorisation = load_priorisation(collectivite_id)
df_reductions = load_reductions(collectivite_id)
df_poids = load_poids_categories()

notes = build_notes(df_priorisation)
reductions = df_reductions.set_index("levier")["reduction"].to_dict()
exclusions = hors_competence_pairs(load_hors_competence(collectivite_id))
weights = build_category_weights(df_poids)


if SESSION_FAISABILITE not in st.session_state:
    st.session_state[SESSION_FAISABILITE] = {}

init_session_faisabilite(collectivite_id, notes, exclusions, weights)
faisabilites: dict[tuple[str, int], int] = st.session_state[SESSION_FAISABILITE]

leviers = sorted(reductions.keys())

top = top_leviers_angles_morts(leviers, reductions, notes, exclusions, weights)

if not top:
    st.info(
        "Aucun angle mort identifié pour cette collectivité "
        "(toutes les cibles dans le périmètre sont bien mobilisées, "
        "ou aucune réduction disponible)."
    )
    st.markdown("---")
    render_etape_2_nav(
        collectivite_id,
        back_key=f"nav_fais_retour_empty_{collectivite_id}",
        forward_key=f"nav_fais_suivant_empty_{collectivite_id}",
    )
    st.stop()

max_potentiel = top[0][1]

show_more = st.session_state.get(SESSION_SHOW_MORE, False)
n_visible = TOP_N_MAX if show_more else TOP_N_INITIAL
visible_top = top[:n_visible]

st.subheader(f"Top {len(visible_top)} des leviers sous mobilisés")

for rank, (levier, potentiel) in enumerate(visible_top, start=1):
    angle_mort_cats = angle_mort_categories(levier, notes, exclusions, weights)
    levier_key = f"faisabilite_levier_{levier}"

    # Agrégation levier ← catégories avant rendu du toggle
    levier_val = levier_faisabilite_value(levier, faisabilites, angle_mort_cats)
    levier_label = INT_TO_FAISABILITE.get(levier_val) if levier_val else None
    sync_segmented_key(levier_key, levier_label)

    col_rank, col_bar, col_toggle = st.columns([2, 1, 3])
    with col_rank:
        st.markdown(f"**{rank}. {levier}**")
    with col_bar:
        st.caption(f"Potentiel non mobilisé : **{potentiel:.0f}** ktCO₂e")
        st.progress(min(potentiel / max_potentiel, 1.0) if max_potentiel > 0 else 0.0)
    with col_toggle:
        st.segmented_control(
            "Faisabilité",
            options=list(FAISABILITE_OPTIONS),
            key=levier_key,
            default=None,
            label_visibility="collapsed",
            on_change=_on_levier_change,
            args=(levier, angle_mort_cats),
        )

    with st.expander("Affiner par type d'action"):
        for cat in angle_mort_cats:
            cat_key = f"faisabilite_cat_{levier}_{cat}"
            cat_val = faisabilites.get((levier, cat))
            cat_label = INT_TO_FAISABILITE.get(cat_val) if cat_val else None
            sync_segmented_key(cat_key, cat_label)

            c1, c2, c3 = st.columns([1, 2, 2])
            with c1:
                st.caption(CATEGORIES[cat])
            with c2:
                st.segmented_control(
                    CATEGORIES[cat],
                    options=list(FAISABILITE_OPTIONS),
                    key=cat_key,
                    default=None,
                    label_visibility="collapsed",
                    on_change=_on_categorie_change,
                    args=(levier, cat),
                )

    st.markdown("")

if len(top) > TOP_N_INITIAL and not show_more:
    if st.button("Afficher plus", type="secondary"):
        st.session_state[SESSION_SHOW_MORE] = True
        st.rerun()
elif len(top) > TOP_N_INITIAL and show_more:
    if st.button("Afficher moins", type="secondary"):
        st.session_state[SESSION_SHOW_MORE] = False
        st.rerun()

st.markdown("---")

if st.button("Sauvegarder", type="primary"):
    to_save = collect_faisabilites_to_save(faisabilites, notes, exclusions, weights)
    try:
        save_faisabilite(collectivite_id, to_save)
        load_faisabilite.clear()
        n = len(to_save)
        if n == 0:
            st.success(
                f"Arbitrage enregistré pour **{nom_par_id[collectivite_id]}** "
                "(aucune catégorie renseignée)."
            )
        elif n == 1:
            st.success(
                f"Arbitrage enregistré pour **{nom_par_id[collectivite_id]}** "
                f"({n} catégorie)."
            )
        else:
            st.success(
                f"Arbitrage enregistré pour **{nom_par_id[collectivite_id]}** "
                f"({n} catégories)."
            )
    except Exception as e:
        st.error(f"Erreur lors de l'enregistrement : {e}")

st.markdown("---")
render_etape_2_nav(
    collectivite_id,
    back_key=f"nav_fais_retour_{collectivite_id}",
    forward_key=f"nav_fais_suivant_{collectivite_id}",
)
