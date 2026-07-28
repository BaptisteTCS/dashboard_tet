import streamlit as st

st.set_page_config(
    page_title="Priorisation",
    page_icon="🥇",
    layout="wide",
)

import pandas as pd
from sqlalchemy import text

from utils.collectivite_selection import (
    default_collectivite_index,
    set_selected_collectivite,
)
from utils.db import get_engine
from utils.priorisation_navigation import render_etape_2_nav

# ==========================
# Constantes
# ==========================

CATEGORIES = {
    1: "Aménagement",
    2: "Planification",
    3: "Financement",
    4: "Gouvernance",
    5: "Exemplarité",
    6: "Sensibilisation",
}

FAISABILITE_OPTIONS = (
    "Non pertinent",
    "A discuter avec l'élu",
    "Pertinent",
)

# Notes de mobilisation : 0 = non mobilisé, 1 = partiellement, 2 = bien, 3 = pleinement
NOTES_SOUS_MOBILISEES = (0, 1)

# 1 = Non pertinent, 2 = A discuter avec l'élu, 3 = Pertinent
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


@st.cache_data(ttl="1h")
def load_plans(collectivite_id: int) -> list[str]:
    """Noms des plans d'action de la collectivité (un axe racine par plan)."""
    engine = get_engine()
    with engine.connect() as conn:
        df = pd.read_sql_query(
            text("""
                SELECT DISTINCT nom
                FROM prod.axe
                WHERE collectivite_id = :collectivite_id
                  AND plan = id
                  AND nom IS NOT NULL
                  AND btrim(nom) <> ''
                ORDER BY nom
            """),
            conn,
            params={"collectivite_id": collectivite_id},
        )
    return df["nom"].tolist()


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


def volet_dans_perimetre(
    levier: str,
    cat: int,
    exclusions: set[tuple[str, int]],
    weights: dict[str, dict[int, float]],
) -> bool:
    """Volet sur lequel la collectivité peut agir : pas hors compétence et poids > 0."""
    if (levier, cat) in exclusions:
        return False
    return weights.get(levier, {}).get(cat, 0.0) > 0


def volet_est_mobilise(
    levier: str,
    cat: int,
    notes: dict[tuple[str, int], int],
) -> bool:
    """Volet bien (2) ou pleinement (3) mobilisé : plus rien à arbitrer dessus."""
    return notes.get((levier, cat), 0) not in NOTES_SOUS_MOBILISEES


def potentiel_volet(
    levier: str,
    cat: int,
    reduction: float,
    notes: dict[tuple[str, int], int],
    exclusions: set[tuple[str, int]],
    weights: dict[str, dict[int, float]],
) -> float:
    """
    Potentiel d'un volet (levier × catégorie) : abs(réduction du levier) × poids
    de la catégorie. Nul si le volet est déjà mobilisé ou hors du périmètre.
    """
    if not volet_dans_perimetre(levier, cat, exclusions, weights):
        return 0.0
    if volet_est_mobilise(levier, cat, notes):
        return 0.0
    return abs(reduction) * weights[levier][cat]


def volets_perimetre(
    levier: str,
    exclusions: set[tuple[str, int]],
    weights: dict[str, dict[int, float]],
) -> list[int]:
    """Volets du levier sur lesquels la collectivité peut agir."""
    return [
        cat
        for cat in range(1, 7)
        if volet_dans_perimetre(levier, cat, exclusions, weights)
    ]


def volets_sous_mobilises(
    levier: str,
    notes: dict[tuple[str, int], int],
    exclusions: set[tuple[str, int]],
    weights: dict[str, dict[int, float]],
) -> list[int]:
    """Volets arbitrables : non ou partiellement mobilisés, dans le périmètre."""
    return [
        cat
        for cat in volets_perimetre(levier, exclusions, weights)
        if not volet_est_mobilise(levier, cat, notes)
    ]


def calc_potentiel_non_mobilise(
    levier: str,
    reduction: float,
    notes: dict[tuple[str, int], int],
    exclusions: set[tuple[str, int]],
    weights: dict[str, dict[int, float]],
) -> float:
    """Somme des potentiels des volets non ou partiellement mobilisés du levier."""
    return sum(
        potentiel_volet(levier, cat, reduction, notes, exclusions, weights)
        for cat in range(1, 7)
    )


def top_leviers_sous_mobilises(
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
# Arbitrages de faisabilité (par volet)
# ==========================


def set_categorie_faisabilite(
    levier: str,
    cat: int,
    label: str,
    faisabilites: dict[tuple[str, int], int],
) -> None:
    faisabilites[(levier, cat)] = FAISABILITE_TO_INT[label]


def faisabilite_commune(
    levier: str,
    cats: tuple[int, ...],
    faisabilites: dict[tuple[str, int], int],
) -> str | None:
    """Label partagé par tous les volets du levier, None si les choix diffèrent."""
    valeurs = {faisabilites.get((levier, cat)) for cat in cats}
    if len(valeurs) != 1:
        return None
    (valeur,) = valeurs
    return INT_TO_FAISABILITE.get(valeur) if valeur else None


def faisabilites_from_db(
    df: pd.DataFrame,
    notes: dict[tuple[str, int], int],
    exclusions: set[tuple[str, int]],
    weights: dict[str, dict[int, float]],
) -> dict[tuple[str, int], int]:
    """Charge les arbitrages persistés en ne gardant que les volets encore arbitrables."""
    result: dict[tuple[str, int], int] = {}
    for _, row in df.iterrows():
        levier = row["levier"]
        cat = int(row["categorie"])
        fais = int(row["faisabilite"])
        if fais not in INT_TO_FAISABILITE:
            continue
        if cat not in volets_sous_mobilises(levier, notes, exclusions, weights):
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
        if cat not in volets_sous_mobilises(levier, notes, exclusions, weights):
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


def _on_categorie_change(levier: str, cat: int) -> None:
    key = f"faisabilite_cat_{levier}_{cat}"
    label = st.session_state[key]
    faisabilites = st.session_state[SESSION_FAISABILITE]
    set_categorie_faisabilite(levier, cat, label, faisabilites)


def _on_tout_change(levier: str, cats: tuple[int, ...]) -> None:
    label = st.session_state[f"faisabilite_tout_{levier}"]
    if label is None:
        return
    faisabilites = st.session_state[SESSION_FAISABILITE]
    for cat in cats:
        set_categorie_faisabilite(levier, cat, label, faisabilites)


# ==========================
# Interface
# ==========================

st.title("🥇 Priorisation des actions")

st.warning(
    """
**Vos actions, regroupées par volet.**

Toutes les actions de vos plans d'actions déposés sur Territoires en Transitions ont été regroupées par volet, soit le croisement entre :
- **un levier** : vélo, rénovation, véhicule électrique, etc.
- **une catégorie** : aménagement, planification, financement, gouvernance, exemplarité, sensibilisation.

Le potentiel de réduction des émissions de GES de chaque volet a été estimé à partir de la Stratégie nationale bas carbone (SNBC) et des Mondrians de la transition écologique.

Les volets que votre collectivité mobilise déjà sont notés **"Mobilisé"**. Pour les autres, indiquez la pertinence d'agir au regard de vos contraintes et de vos priorités politiques :
- **Non pertinent** : ce volet n'entre pas dans vos priorités actuelles
- **Pertinent** : ce volet correspond à une priorité pour votre collectivité
- **À discuter avec l'élu** : la décision nécessite un arbitrage politique

Nous vous proposerons ensuite des **actions de référence**, et vous pourrez explorer **les actions menées par d'autres collectivités**.
""",
    icon=":material/tips_and_updates:",
)

df_collectivites = load_collectivites_priorisees()
if df_collectivites.empty:
    st.warning(
        "Aucune collectivité avec des données de priorisation disponible.",
        icon=":material/domain_disabled:",
    )
    st.stop()

nom_par_id = df_collectivites.set_index("collectivite_id")["nom"].to_dict()
collectivite_ids = df_collectivites["collectivite_id"].tolist()

collectivite_id = st.selectbox(
    "Collectivité",
    options=collectivite_ids,
    index=default_collectivite_index(collectivite_ids),
    format_func=lambda cid: nom_par_id[cid],
    key="faisabilite_select_collectivite",
)

set_selected_collectivite(collectivite_id)

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

top = top_leviers_sous_mobilises(leviers, reductions, notes, exclusions, weights)

if not top:
    st.info(
        "Aucun levier sous mobilisé identifié pour cette collectivité "
        "(tous les volets dans le périmètre sont bien mobilisés, "
        "ou aucune réduction disponible).",
        icon=":material/task_alt:",
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

st.subheader(f"Les {len(visible_top)} leviers au plus fort potentiel de réduction GES pour votre collectivité")

plans = load_plans(collectivite_id)
if plans:
    st.markdown(f"Les plans concernés sont : {', '.join(plans)}.")

for rank, (levier, potentiel) in enumerate(visible_top, start=1):
    with st.container(border=True):
        col_titre, col_bar = st.columns([3, 2], vertical_alignment="center")
        with col_titre:
            st.markdown(f"**{rank}. {levier}**")
        with col_bar:
            st.caption(f"Potentiel non mobilisé : **{potentiel:.0f}** ktCO₂e")
            st.progress(
                min(potentiel / max_potentiel, 1.0) if max_potentiel > 0 else 0.0
            )

        for cat in volets_perimetre(levier, exclusions, weights):
            c1, c2 = st.columns([1, 4], vertical_alignment="center")
            with c1:
                st.caption(CATEGORIES[cat])
            with c2:
                if volet_est_mobilise(levier, cat, notes):
                    st.badge(
                        "Mobilisé", icon=":material/check_circle:", color="green"
                    )
                    continue

                cat_key = f"faisabilite_cat_{levier}_{cat}"
                cat_val = faisabilites.get((levier, cat))
                cat_label = INT_TO_FAISABILITE.get(cat_val) if cat_val else None
                sync_segmented_key(cat_key, cat_label)

                st.segmented_control(
                    CATEGORIES[cat],
                    options=list(FAISABILITE_OPTIONS),
                    key=cat_key,
                    default=None,
                    label_visibility="collapsed",
                    on_change=_on_categorie_change,
                    args=(levier, cat),
                )

        cats_arbitrables = tuple(
            volets_sous_mobilises(levier, notes, exclusions, weights)
        )
        if len(cats_arbitrables) > 1:
            c1, c2 = st.columns([1, 4], vertical_alignment="center")
            with c1:
                st.caption("**Tout**")
            with c2:
                tout_key = f"faisabilite_tout_{levier}"
                sync_segmented_key(
                    tout_key,
                    faisabilite_commune(levier, cats_arbitrables, faisabilites),
                )

                st.segmented_control(
                    f"Tout - {levier}",
                    options=list(FAISABILITE_OPTIONS),
                    key=tout_key,
                    default=None,
                    label_visibility="collapsed",
                    on_change=_on_tout_change,
                    args=(levier, cats_arbitrables),
                )

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
                "(aucune catégorie renseignée).",
                icon=":material/save:",
            )
        elif n == 1:
            st.success(
                f"Arbitrage enregistré pour **{nom_par_id[collectivite_id]}** "
                f"({n} catégorie).",
                icon=":material/save:",
            )
        else:
            st.success(
                f"Arbitrage enregistré pour **{nom_par_id[collectivite_id]}** "
                f"({n} catégories).",
                icon=":material/save:",
            )
    except Exception as e:
        st.error(
            f"Erreur lors de l'enregistrement : {e}",
            icon=":material/error:",
        )
