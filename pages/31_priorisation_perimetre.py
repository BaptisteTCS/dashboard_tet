import streamlit as st

st.set_page_config(
    page_title="Priorisation — périmètre d'action",
    page_icon="📍",
    layout="wide",
)

import pandas as pd
from sqlalchemy import text

from utils.db import get_engine, get_engine_prod

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

EXCLUDABLE_CATEGORIES = (1, 2, 3)

PERIMETRE_OPTIONS = ("Dans mon périmètre", "Hors compétence")

SECTEUR_ORDER = [
    "Résidentiel",
    "Tertiaire",
    "Transport ",
    "Agriculture",
    "Industrie",
    "Déchets",
    "Branche énergie",
    "UTCATF",
]

SESSION_EXCLUSIONS = "perimetre_exclusions"
SESSION_COLLECTIVITE = "perimetre_collectivite_id"


# ==========================
# Chargement des données
# ==========================


@st.cache_data(ttl="1h")
def load_collectivites() -> pd.DataFrame:
    """Liste des collectivités (prod), hors type test."""
    engine = get_engine_prod()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("""
                SELECT id, nom
                FROM collectivite
                WHERE type != 'test' AND nom IS NOT NULL
                ORDER BY nom
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
def load_leviers_par_secteur() -> dict[str, list[str]]:
    """Leviers groupés par secteur, dans l'ordre du CSV référentiel."""
    df = pd.read_csv("data/leviers_sgpe_region.csv", sep=";")
    df = df[["Secteur", "Leviers SGPE"]].rename(
        columns={"Leviers SGPE": "levier"}
    )
    par_secteur: dict[str, list[str]] = {s: [] for s in SECTEUR_ORDER}
    for _, row in df.iterrows():
        secteur = row["Secteur"]
        levier = row["levier"]
        if secteur in par_secteur and levier not in par_secteur[secteur]:
            par_secteur[secteur].append(levier)
    return par_secteur


@st.cache_data(ttl="1h")
def load_hors_competence(collectivite_id: int) -> pd.DataFrame:
    """Exclusions enregistrées pour une collectivité."""
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


# ==========================
# Logique périmètre / compétence
# ==========================


def excludable_categories(
    levier: str, weights: dict[str, dict[int, float]]
) -> list[int]:
    """Catégories 1–3 à poids strictement positif pour ce levier."""
    levier_weights = weights.get(levier, {})
    return [
        cat
        for cat in EXCLUDABLE_CATEGORIES
        if levier_weights.get(cat, 0) > 0
    ]


def is_hors_competence(
    levier: str,
    cat: int,
    exclusions: set[tuple[str, int]],
) -> bool:
    return (levier, cat) in exclusions


def levier_perimetre_label(
    levier: str,
    exclusions: set[tuple[str, int]],
    weights: dict[str, dict[int, float]],
) -> str:
    """
    Agrégat levier ← catégories : « Hors compétence » si toutes les catégories
    excluables (1–3, poids > 0) sont exclues ; sinon « Dans mon périmètre ».
    """
    cats = excludable_categories(levier, weights)
    if not cats:
        return PERIMETRE_OPTIONS[0]
    if all((levier, c) in exclusions for c in cats):
        return PERIMETRE_OPTIONS[1]
    return PERIMETRE_OPTIONS[0]


def categorie_perimetre_label(
    levier: str, cat: int, exclusions: set[tuple[str, int]]
) -> str:
    return (
        PERIMETRE_OPTIONS[1]
        if is_hors_competence(levier, cat, exclusions)
        else PERIMETRE_OPTIONS[0]
    )


def set_levier_perimetre(
    levier: str,
    label: str,
    exclusions: set[tuple[str, int]],
    weights: dict[str, dict[int, float]],
) -> None:
    """Raccourci levier : inclut ou exclut toutes les catégories excluables."""
    for cat in excludable_categories(levier, weights):
        if label == PERIMETRE_OPTIONS[1]:
            exclusions.add((levier, cat))
        else:
            exclusions.discard((levier, cat))


def set_categorie_perimetre(
    levier: str,
    cat: int,
    label: str,
    exclusions: set[tuple[str, int]],
) -> None:
    if label == PERIMETRE_OPTIONS[1]:
        exclusions.add((levier, cat))
    else:
        exclusions.discard((levier, cat))


def exclusions_from_db(
    df: pd.DataFrame,
    weights: dict[str, dict[int, float]],
) -> set[tuple[str, int]]:
    """Charge les exclusions persistées en ne gardant que les cases valides."""
    result: set[tuple[str, int]] = set()
    for _, row in df.iterrows():
        levier = row["levier"]
        cat = int(row["categorie"])
        if cat not in EXCLUDABLE_CATEGORIES:
            continue
        if cat not in excludable_categories(levier, weights):
            continue
        result.add((levier, cat))
    return result


def collect_exclusions_to_save(
    exclusions: set[tuple[str, int]],
    weights: dict[str, dict[int, float]],
) -> list[tuple[str, int]]:
    """Liste triée des exclusions valides à persister."""
    valid = [
        (levier, cat)
        for levier, cat in exclusions
        if cat in excludable_categories(levier, weights)
    ]
    return sorted(valid, key=lambda x: (x[0], x[1]))


def init_session_exclusions(collectivite_id: int, weights: dict[str, dict[int, float]]) -> None:
    if st.session_state.get(SESSION_COLLECTIVITE) == collectivite_id:
        return
    df = load_hors_competence(collectivite_id)
    st.session_state[SESSION_EXCLUSIONS] = exclusions_from_db(df, weights)
    st.session_state[SESSION_COLLECTIVITE] = collectivite_id


def save_hors_competence(
    collectivite_id: int,
    exclusions: list[tuple[str, int]],
) -> None:
    """Remplacement complet des exclusions pour la collectivité (une transaction)."""
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(
            text(
                "DELETE FROM priorisation_hors_competence "
                "WHERE collectivite_id = :collectivite_id"
            ),
            {"collectivite_id": collectivite_id},
        )
        if exclusions:
            conn.execute(
                text("""
                    INSERT INTO priorisation_hors_competence
                        (collectivite_id, levier, categorie)
                    VALUES (:collectivite_id, :levier, :categorie)
                """),
                [
                    {
                        "collectivite_id": collectivite_id,
                        "levier": levier,
                        "categorie": cat,
                    }
                    for levier, cat in exclusions
                ],
            )


# ==========================
# Callbacks widgets (agrégation levier ↔ catégorie)
# ==========================


def _on_levier_change(levier: str, weights: dict[str, dict[int, float]]) -> None:
    key = f"perimetre_levier_{levier}"
    label = st.session_state[key]
    exclusions = st.session_state[SESSION_EXCLUSIONS]
    set_levier_perimetre(levier, label, exclusions, weights)


def _on_categorie_change(levier: str, cat: int) -> None:
    key = f"perimetre_cat_{levier}_{cat}"
    label = st.session_state[key]
    exclusions = st.session_state[SESSION_EXCLUSIONS]
    set_categorie_perimetre(levier, cat, label, exclusions)


# ==========================
# Interface
# ==========================

st.title("🔧 Définition du périmètre d'action")

st.markdown(
    "Cette étape permet d'écarter les leviers sur lesquels votre collectivité "
    "**n'a pas la compétence d'agir**. Tout est **dans le périmètre** par défaut : "
    "seules les exclusions sont enregistrées. Les actions de **gouvernance**, "
    "**exemplarité** et **sensibilisation** restent toujours mobilisables, "
    "y compris sur un levier hors compétence, vous pourrez agir indirectement "
    "(partenariats, sensibilisation, etc.)."
)

df_collectivites = load_collectivites()
if df_collectivites.empty:
    st.warning("Aucune collectivité disponible.")
    st.stop()

nom_par_id = df_collectivites.set_index("id")["nom"].to_dict()
ids = df_collectivites["id"].tolist()

# Paramètre optionnel ?collectivite_id= pour pré-sélection
default_index = 0
qp_id = st.query_params.get("collectivite_id")
if qp_id is not None:
    try:
        qp_id_int = int(qp_id)
        if qp_id_int in ids:
            default_index = ids.index(qp_id_int)
    except (TypeError, ValueError):
        pass

collectivite_id = st.selectbox(
    "Collectivité",
    options=ids,
    index=default_index,
    format_func=lambda cid: nom_par_id[cid],
    key="perimetre_select_collectivite",
)

st.markdown("---")

df_poids = load_poids_categories()
weights = build_category_weights(df_poids)
leviers_par_secteur = load_leviers_par_secteur()

if SESSION_EXCLUSIONS not in st.session_state:
    st.session_state[SESSION_EXCLUSIONS] = set()

init_session_exclusions(collectivite_id, weights)
exclusions: set[tuple[str, int]] = st.session_state[SESSION_EXCLUSIONS]

for secteur in SECTEUR_ORDER:
    leviers = leviers_par_secteur.get(secteur, [])
    if not leviers:
        continue

    st.subheader(secteur.strip())

    for levier in leviers:
        cats_excluables = excludable_categories(levier, weights)
        levier_key = f"perimetre_levier_{levier}"

        # Synchroniser le segmented control levier avec l'agrégat des catégories
        st.session_state[levier_key] = levier_perimetre_label(
            levier, exclusions, weights
        )

        col_nom, col_toggle = st.columns([3, 2])
        with col_nom:
            st.markdown(f"**{levier}**")
        with col_toggle:
            st.segmented_control(
                "Périmètre",
                options=list(PERIMETRE_OPTIONS),
                key=levier_key,
                label_visibility="collapsed",
                on_change=_on_levier_change,
                args=(levier, weights),
            )

        if cats_excluables:
            with st.expander("Affiner par type d'action"):
                for cat in cats_excluables:
                    cat_key = f"perimetre_cat_{levier}_{cat}"
                    st.session_state[cat_key] = categorie_perimetre_label(
                        levier, cat, exclusions
                    )
                    c1, c2 = st.columns([1, 1])
                    with c1:
                        st.caption(CATEGORIES[cat])
                    with c2:
                        st.segmented_control(
                            CATEGORIES[cat],
                            options=list(PERIMETRE_OPTIONS),
                            key=cat_key,
                            label_visibility="collapsed",
                            on_change=_on_categorie_change,
                            args=(levier, cat),
                        )

    st.markdown("")

st.markdown("---")

if st.button("Sauvegarder", type="primary"):
    to_save = collect_exclusions_to_save(exclusions, weights)
    try:
        save_hors_competence(collectivite_id, to_save)
        load_hors_competence.clear()
        if len(to_save) > 1:
            st.success(
                f"Périmètre enregistré pour **{nom_par_id[collectivite_id]}** "
                f"({len(to_save)} exclusions)."
            )
        else:
            st.success(
                f"Périmètre enregistré pour **{nom_par_id[collectivite_id]}** "
                f"({len(to_save)} exclusion)."
            )
    except Exception as e:
        st.error(f"Erreur lors de l'enregistrement : {e}")
