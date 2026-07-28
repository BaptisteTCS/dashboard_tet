import streamlit as st

st.set_page_config(
    page_title="Priorisation — choix des actions",
    page_icon="🏅",
    layout="wide",
)

import json
import re

import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy import text

from utils.collectivite_selection import (
    default_collectivite_index,
    set_selected_collectivite,
)
from utils.db import get_engine, get_engine_prod
from utils.priorisation_navigation import render_etape_3_nav

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

# Faisabilité 2 = À discuter, 3 = Prioritaire
FAISABILITE_ELIGIBLE = {2, 3}

MAX_ACTIONS_PAR_COLONNE = 3
CIBLES_PAGE_SIZE = 3
DESCRIPTION_MAX_LEN = 180

LABEL_AJOUTER = "Ajouter à ma sélection"
LABEL_SELECTIONNEE = "Sélectionnée"

SECTION_REFERENCE = "reference"
SECTION_COLLECTIVITES = "collectivites"

ORIGINE_REFERENCE = "Référence"

# Suffixe de version : les sélections stockent (fiche_action_id, reference)
SESSION_SELECTIONS = "action_selections_v2"
SESSION_COLLECTIVITE = "action_collectivite_id_v2"
SESSION_EXPANDED_CIBLES = "action_expanded_cibles"
SESSION_VISIBLE_CIBLES_COUNT = "action_visible_cibles_count"
SESSION_FLASH = "action_flash"


# ==========================
# Utilitaires texte
# ==========================


def clean_rich_text(text) -> str:
    if text is None or (isinstance(text, float) and pd.isna(text)):
        return ""
    text = str(text).strip()
    if not text:
        return ""
    text = BeautifulSoup(text, "html.parser").get_text(separator=" ")
    return re.sub(r"\s+", " ", text).strip()


def short_description(text, max_len: int = 220) -> str:
    cleaned = clean_rich_text(text)
    if len(cleaned) <= max_len:
        return cleaned
    truncated = cleaned[:max_len].rsplit(" ", 1)[0]
    return f"{truncated}…"


def is_reference_origine(origine) -> bool:
    if origine is None or (isinstance(origine, float) and pd.isna(origine)):
        return False
    return str(origine).strip().lower() in ("référence", "reference")


def origine_label(origine) -> str:
    if is_reference_origine(origine):
        return "Action de référence"
    if origine is None or (isinstance(origine, float) and pd.isna(origine)):
        return "Collectivité"
    return str(origine).strip()


def parse_ids(value) -> list[int]:
    """Parse la colonne priorisation.ids (JSON, liste ou chaîne)."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return []
    if isinstance(value, (list, tuple, set)):
        ids: list[int] = []
        for v in value:
            try:
                ids.append(int(v))
            except (TypeError, ValueError):
                continue
        return ids
    if isinstance(value, str):
        cleaned = value.strip()
        if not cleaned:
            return []
        try:
            parsed = json.loads(cleaned)
            if isinstance(parsed, list):
                return parse_ids(parsed)
        except (json.JSONDecodeError, ValueError):
            pass
        cleaned = cleaned.strip("[]{}()")
        parts = [p.strip() for p in cleaned.split(",") if p.strip()]
        ids = []
        for p in parts:
            try:
                ids.append(int(p))
            except ValueError:
                continue
        return ids
    try:
        return [int(value)]
    except (TypeError, ValueError):
        return []


# ==========================
# Chargement des données
# ==========================


@st.cache_data(ttl="1h")
def load_collectivites_priorisees() -> pd.DataFrame:
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
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("SELECT * FROM priorisation_categorie_levier"),
            conn,
        )


@st.cache_data(ttl="1h")
def load_priorisation(collectivite_id: int) -> pd.DataFrame:
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("""
                SELECT DISTINCT ON (levier, categorie)
                    levier, categorie, note, ids
                FROM priorisation
                WHERE collectivite_id = :collectivite_id
                ORDER BY levier, categorie, created_at DESC
            """),
            conn,
            params={"collectivite_id": collectivite_id},
        )


@st.cache_data(ttl="1h")
def load_priorisation_all(collectivite_ids: tuple[int, ...]) -> pd.DataFrame:
    if not collectivite_ids:
        return pd.DataFrame(
            columns=["collectivite_id", "levier", "categorie", "note", "ids"]
        )
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("""
                SELECT DISTINCT ON (collectivite_id, levier, categorie)
                    collectivite_id, levier, categorie, note, ids
                FROM priorisation
                WHERE collectivite_id = ANY(:ids)
                ORDER BY collectivite_id, levier, categorie, created_at DESC
            """),
            conn,
            params={"ids": list(collectivite_ids)},
        )


@st.cache_data(ttl="1h")
def load_fiches_action(collectivite_ids: tuple[int, ...]) -> pd.DataFrame:
    """Fiches action prod pour les collectivités priorisées."""
    if not collectivite_ids:
        return pd.DataFrame(columns=["id", "collectivite_id", "titre", "description"])
    engine = get_engine_prod()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("""
                SELECT id, collectivite_id, titre, description
                FROM fiche_action
                WHERE collectivite_id = ANY(:ids)
            """),
            conn,
            params={"ids": list(collectivite_ids)},
        )


@st.cache_data(ttl="1h")
def load_reductions(collectivite_id: int) -> pd.DataFrame:
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
def load_actions_reference() -> pd.DataFrame:
    """Actions de référence (référentiel statique OLAP)."""
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("""
                SELECT id, levier, categorie, titre, description
                FROM priorisation_action_reference
            """),
            conn,
        )


@st.cache_data(ttl="1h")
def load_actions_choisies(collectivite_id: int) -> pd.DataFrame:
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("""
                SELECT levier, categorie, fiche_action_id, reference
                FROM priorisation_action
                WHERE collectivite_id = :collectivite_id
            """),
            conn,
            params={"collectivite_id": collectivite_id},
        )


def build_category_weights(df_poids: pd.DataFrame) -> dict[str, dict[int, float]]:
    levier_cols = [c for c in df_poids.columns if c != "categorie"]
    weights: dict[str, dict[int, float]] = {levier: {} for levier in levier_cols}
    for _, row in df_poids.iterrows():
        cat = int(row["categorie"])
        for levier in levier_cols:
            val = row[levier]
            weights[levier][cat] = 0.0 if pd.isna(val) else float(val)
    return weights


def build_notes(df_priorisation: pd.DataFrame) -> dict[tuple[str, int], int]:
    return {
        (row["levier"], int(row["categorie"])): int(row["note"])
        for _, row in df_priorisation.iterrows()
    }


def build_faisabilites(df: pd.DataFrame) -> dict[tuple[str, int], int]:
    return {
        (row["levier"], int(row["categorie"])): int(row["faisabilite"])
        for _, row in df.iterrows()
    }


def hors_competence_pairs(df: pd.DataFrame) -> set[tuple[str, int]]:
    return {(row["levier"], int(row["categorie"])) for _, row in df.iterrows()}


def as_bool(value) -> bool:
    if value is None or pd.isna(value):
        return False
    return bool(value)


def selections_from_db(
    df: pd.DataFrame,
) -> dict[tuple[str, int], set[tuple[int, bool]]]:
    result: dict[tuple[str, int], set[tuple[int, bool]]] = {}
    for _, row in df.iterrows():
        key = (row["levier"], int(row["categorie"]))
        fiche = (int(row["fiche_action_id"]), as_bool(row.get("reference")))
        result.setdefault(key, set()).add(fiche)
    return result


# ==========================
# (a) Sélection des cibles prioritaires
# ==========================


def calc_enjeu(
    levier: str,
    cat: int,
    reductions: dict[str, float],
    weights: dict[str, dict[int, float]],
) -> float:
    """Enjeu d'une cible = abs(réduction levier) × poids catégorie."""
    poids = weights.get(levier, {}).get(cat, 0.0)
    if poids <= 0 or levier not in reductions:
        return 0.0
    return abs(float(reductions[levier])) * poids


def is_cible_prioritaire(
    levier: str,
    cat: int,
    notes: dict[tuple[str, int], int],
    exclusions: set[tuple[str, int]],
    weights: dict[str, dict[int, float]],
    faisabilites: dict[tuple[str, int], int],
) -> bool:
    """
    Cible éligible au choix d'actions si :
    (a) dans le périmètre (absente de priorisation_hors_competence),
    (b) peu mobilisée (note 0 ou 1),
    (c) faisabilité « À discuter » (2) ou « Prioritaire » (3).
    """
    if (levier, cat) in exclusions:
        return False
    poids = weights.get(levier, {}).get(cat, 0.0)
    if poids <= 0:
        return False
    if notes.get((levier, cat), 0) not in (0, 1):
        return False
    return faisabilites.get((levier, cat)) in FAISABILITE_ELIGIBLE


def build_cibles_prioritaires(
    leviers: list[str],
    reductions: dict[str, float],
    notes: dict[tuple[str, int], int],
    exclusions: set[tuple[str, int]],
    weights: dict[str, dict[int, float]],
    faisabilites: dict[tuple[str, int], int],
) -> list[dict]:
    """Liste des cibles prioritaires triées par enjeu décroissant."""
    cibles: list[dict] = []
    for levier in leviers:
        if levier not in reductions:
            continue
        for cat in range(1, 7):
            if not is_cible_prioritaire(
                levier, cat, notes, exclusions, weights, faisabilites
            ):
                continue
            cibles.append(
                {
                    "levier": levier,
                    "categorie_id": cat,
                    "categorie": CATEGORIES[cat],
                    "enjeu": calc_enjeu(levier, cat, reductions, weights),
                }
            )
    cibles.sort(key=lambda c: c["enjeu"], reverse=True)
    return cibles


def group_cibles_by_levier(cibles: list[dict]) -> list[tuple[str, list[dict]]]:
    """Regroupe par levier ; ordre des leviers = enjeu max décroissant."""
    by_levier: dict[str, list[dict]] = {}
    for cible in cibles:
        by_levier.setdefault(cible["levier"], []).append(cible)
    ordered_leviers = sorted(
        by_levier.keys(),
        key=lambda levier: max(c["enjeu"] for c in by_levier[levier]),
        reverse=True,
    )
    return [
        (levier, sorted(by_levier[levier], key=lambda c: c["enjeu"], reverse=True))
        for levier in ordered_leviers
    ]


def fiches_reference_pour_cible(
    levier: str,
    cat: int,
    df_actions_reference: pd.DataFrame,
) -> pd.DataFrame:
    """Actions de référence disponibles pour une cible (levier × catégorie)."""
    empty = pd.DataFrame(columns=["id", "intitule", "description", "origine"])
    if df_actions_reference.empty:
        return empty

    df = df_actions_reference[
        (df_actions_reference["levier"] == levier)
        & (df_actions_reference["categorie"] == cat)
    ]
    if df.empty:
        return empty

    rows = [
        {
            "id": int(row["id"]),
            "intitule": clean_rich_text(row["titre"]) or f"Action #{int(row['id'])}",
            "description": row["description"],
            "origine": ORIGINE_REFERENCE,
        }
        for _, row in df.iterrows()
    ]
    return pd.DataFrame(rows).sort_values("intitule")


def fiches_autres_collectivites(
    levier: str,
    cat: int,
    collectivite_id: int,
    df_priorisation_all: pd.DataFrame,
    df_fiches_action: pd.DataFrame,
    nom_par_id: dict[int, str],
) -> pd.DataFrame:
    """
    Fiches disponibles pour une cible : ids des autres collectivités dans
    priorisation (OLAP), résolues via fiche_action (prod).
    """
    rows: list[dict] = []
    df_autres = df_priorisation_all[
        (df_priorisation_all["levier"] == levier)
        & (df_priorisation_all["categorie"] == cat)
        & (df_priorisation_all["collectivite_id"] != collectivite_id)
    ]
    seen: set[tuple[int, int]] = set()

    for _, row in df_autres.iterrows():
        ct_id = int(row["collectivite_id"])
        ct_nom = nom_par_id.get(ct_id, f"Collectivité #{ct_id}")
        for aid in parse_ids(row["ids"]):
            dedupe = (ct_id, aid)
            if dedupe in seen:
                continue
            seen.add(dedupe)

            df_f = df_fiches_action[
                (df_fiches_action["id"] == aid)
                & (df_fiches_action["collectivite_id"] == ct_id)
            ]
            if df_f.empty:
                continue

            fiche = df_f.iloc[0]
            rows.append(
                {
                    "id": aid,
                    "intitule": fiche.get("titre") or f"Fiche #{aid}",
                    "description": fiche.get("description"),
                    "origine": ct_nom,
                }
            )

    if not rows:
        return pd.DataFrame(columns=["id", "intitule", "description", "origine"])

    return pd.DataFrame(rows).sort_values(
        ["origine", "intitule"], ascending=[True, True]
    )


def fiches_pour_cible(
    levier: str,
    cat: int,
    collectivite_id: int,
    df_priorisation_all: pd.DataFrame,
    df_fiches_action: pd.DataFrame,
    df_actions_reference: pd.DataFrame,
    nom_par_id: dict[int, str],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    df_ref = fiches_reference_pour_cible(levier, cat, df_actions_reference)
    df_autres = fiches_autres_collectivites(
        levier,
        cat,
        collectivite_id,
        df_priorisation_all,
        df_fiches_action,
        nom_par_id,
    )
    return df_ref, df_autres


# ==========================
# État de sélection (source de vérité : st.session_state)
# ==========================


def selections() -> dict[tuple[str, int], set[tuple[int, bool]]]:
    """Sélections par cible ; une action = (fiche_action_id, action de référence)."""
    return st.session_state.setdefault(SESSION_SELECTIONS, {})


def is_fiche_selected(levier: str, cat: int, fiche_id: int, reference: bool) -> bool:
    return (fiche_id, reference) in selections().get((levier, cat), set())


def toggle_fiche_selection(
    levier: str, cat: int, fiche_id: int, reference: bool
) -> None:
    current = selections()
    ids = current.setdefault((levier, cat), set())
    fiche = (fiche_id, reference)
    if fiche in ids:
        ids.discard(fiche)
    else:
        ids.add(fiche)
    if not ids:
        current.pop((levier, cat), None)


def nb_selections_cible(levier: str, cat: int) -> int:
    return len(selections().get((levier, cat), set()))


def selections_to_rows() -> list[tuple[str, int, int, bool]]:
    return saved_to_rows(selections())


def saved_to_rows(
    saved: dict[tuple[str, int], set[tuple[int, bool]]],
) -> list[tuple[str, int, int, bool]]:
    rows = [
        (levier, cat, fiche_id, reference)
        for (levier, cat), ids in saved.items()
        for fiche_id, reference in ids
    ]
    return sorted(rows, key=lambda x: (x[0], x[1], x[2], x[3]))


def is_section_expanded(levier: str, cat: int, section: str) -> bool:
    expanded: set[tuple[str, int, str]] = st.session_state.get(
        SESSION_EXPANDED_CIBLES, set()
    )
    return (levier, cat, section) in expanded


def toggle_section_expanded(levier: str, cat: int, section: str) -> None:
    expanded = st.session_state.setdefault(SESSION_EXPANDED_CIBLES, set())
    key = (levier, cat, section)
    if key in expanded:
        expanded.discard(key)
    else:
        expanded.add(key)


def show_more_cibles(total: int) -> None:
    current = st.session_state.get(SESSION_VISIBLE_CIBLES_COUNT, CIBLES_PAGE_SIZE)
    st.session_state[SESSION_VISIBLE_CIBLES_COUNT] = min(
        current + CIBLES_PAGE_SIZE, total
    )


def init_session_selections(
    collectivite_id: int,
    saved: dict[tuple[str, int], set[tuple[int, bool]]],
    *,
    reset_pagination: bool = True,
) -> None:
    if (
        st.session_state.get(SESSION_COLLECTIVITE) == collectivite_id
        and SESSION_SELECTIONS in st.session_state
    ):
        return
    st.session_state[SESSION_SELECTIONS] = {
        key: set(ids) for key, ids in saved.items()
    }
    st.session_state[SESSION_COLLECTIVITE] = collectivite_id
    if reset_pagination:
        st.session_state[SESSION_EXPANDED_CIBLES] = set()
        st.session_state[SESSION_VISIBLE_CIBLES_COUNT] = CIBLES_PAGE_SIZE


def message_sauvegarde(nom_collectivite: str, n: int) -> str:
    if n == 0:
        return (
            f"Choix enregistrés pour **{nom_collectivite}** "
            "(aucune action sélectionnée)."
        )
    return (
        f"Choix enregistrés pour **{nom_collectivite}** "
        f"({n} action{'s' if n > 1 else ''})."
    )


def save_priorisation_action(
    collectivite_id: int,
    rows: list[tuple[str, int, int, bool]],
) -> None:
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(
            text(
                "DELETE FROM priorisation_action "
                "WHERE collectivite_id = :collectivite_id"
            ),
            {"collectivite_id": collectivite_id},
        )
        if rows:
            conn.execute(
                text("""
                    INSERT INTO priorisation_action
                        (collectivite_id, levier, categorie, fiche_action_id,
                         reference)
                    VALUES (:collectivite_id, :levier, :categorie,
                            :fiche_action_id, :reference)
                """),
                [
                    {
                        "collectivite_id": collectivite_id,
                        "levier": levier,
                        "categorie": cat,
                        "fiche_action_id": fiche_id,
                        "reference": reference,
                    }
                    for levier, cat, fiche_id, reference in rows
                ],
            )


# ==========================
# Rendu
# ==========================


def render_action_card(
    fiche: pd.Series,
    levier: str,
    cat: int,
    *,
    reference: bool,
) -> None:
    """Card d'une action : origine, titre, description et bouton de sélection."""
    fid = int(fiche["id"])
    section = SECTION_REFERENCE if reference else SECTION_COLLECTIVITES
    selected = is_fiche_selected(levier, cat, fid, reference)

    titre = fiche.get("intitule") or f"Action #{fid}"
    description = clean_rich_text(fiche.get("description"))

    with st.container(border=True):
        col_origine, col_etat = st.columns([3, 2], vertical_alignment="center")
        with col_origine:
            if reference:
                st.badge(
                    "Action de référence",
                    icon=":material/cards_star:",
                    color="orange",
                )
            else:
                st.badge(
                    origine_label(fiche.get("origine")),
                    icon=":material/location_city:",
                    color="blue",
                )
        with col_etat:
            if selected:
                st.badge(
                    "Sélectionnée", icon=":material/check_circle:", color="green"
                )

        st.markdown(f"**{titre}**")

        if description:
            st.caption(short_description(description, DESCRIPTION_MAX_LEN))
            if len(description) > DESCRIPTION_MAX_LEN:
                with st.popover(
                    "Lire la description complète",
                    icon=":material/description:",
                ):
                    st.markdown(f"**{titre}**")
                    st.write(description)
        else:
            st.caption("Aucune description disponible.")

        st.button(
            LABEL_SELECTIONNEE if selected else LABEL_AJOUTER,
            key=f"card_{section}_{levier}_{cat}_{fid}",
            type="primary" if selected else "secondary",
            icon=":material/check:" if selected else ":material/add:",
            width="stretch",
            on_click=toggle_fiche_selection,
            args=(levier, cat, fid, reference),
            help="Cliquez à nouveau pour retirer l'action de votre sélection."
            if selected
            else None,
        )


def render_colonne_actions(
    df: pd.DataFrame,
    levier: str,
    cat: int,
    *,
    reference: bool,
) -> None:
    """Une colonne d'actions (référence ou autres collectivités), paginée."""
    section = SECTION_REFERENCE if reference else SECTION_COLLECTIVITES
    if reference:
        st.badge(
            f"Actions de référence ({len(df)})",
            icon=":material/cards_star:",
            color="orange",
        )
        message_vide = "Aucune action de référence pour ce volet."
    else:
        st.badge(
            f"Actions d'autres collectivités ({len(df)})",
            icon=":material/location_city:",
            color="blue",
        )
        message_vide = "Aucune action d'autre collectivité pour ce volet."

    if df.empty:
        st.caption(message_vide)
        return

    expanded = is_section_expanded(levier, cat, section)
    visible = df if expanded else df.head(MAX_ACTIONS_PAR_COLONNE)

    for _, fiche in visible.iterrows():
        render_action_card(fiche, levier, cat, reference=reference)

    reste = len(df) - len(visible)
    if reste > 0:
        st.button(
            f"Afficher {reste} action{'s' if reste > 1 else ''} de plus",
            key=f"more_{section}_{levier}_{cat}",
            icon=":material/expand_more:",
            width="stretch",
            on_click=toggle_section_expanded,
            args=(levier, cat, section),
        )
    elif expanded:
        st.button(
            "Afficher moins",
            key=f"less_{section}_{levier}_{cat}",
            icon=":material/expand_less:",
            width="stretch",
            on_click=toggle_section_expanded,
            args=(levier, cat, section),
        )


# ==========================
# Interface
# ==========================

st.title("🏅 Actions de référence")

st.warning(
    """
**Les actions à explorer pour vos volets prioritaires.**

Pour chaque volet que vous avez jugé pertinent ou à discuter avec vos élus, vous retrouverez :
- **Actions de référence** : actions recommandées par l'Ademe
- **Actions des autres collectivités** : actions menées par d'autres collectivités

Cliquez sur **"Ajouter à ma sélection"** pour constituer votre ensemble d'actions. Elles vous serviront de ressources pour vos prochaines planifications et vos discussions avec vos élus, vos comités, etc.

Une fois votre sélection terminée, cliquez sur **"Sauvegarder"** en bas de page pour la valider. Vous retrouverez ensuite vos actions sur votre tableau de bord de synthèse.
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
    key="action_select_collectivite",
)

set_selected_collectivite(collectivite_id)


df_priorisation = load_priorisation(collectivite_id)
df_priorisation_all = load_priorisation_all(tuple(collectivite_ids))
df_reductions = load_reductions(collectivite_id)
df_poids = load_poids_categories()
df_fiches_action = load_fiches_action(tuple(collectivite_ids))
df_actions_reference = load_actions_reference()
saved_df = load_actions_choisies(collectivite_id)

notes = build_notes(df_priorisation)
reductions = df_reductions.set_index("levier")["reduction"].to_dict()
exclusions = hors_competence_pairs(load_hors_competence(collectivite_id))
faisabilites = build_faisabilites(load_faisabilite(collectivite_id))
weights = build_category_weights(df_poids)
saved = selections_from_db(saved_df)

init_session_selections(collectivite_id, saved)

leviers = sorted(reductions.keys())
cibles = build_cibles_prioritaires(
    leviers, reductions, notes, exclusions, weights, faisabilites
)

if not cibles:
    st.info(
        "Aucun levier prioritaire pour cette collectivité. Vérifiez le diagnostic, "
        "le périmètre et l'arbitrage politique (faisabilité « À discuter » ou "
        "« Prioritaire » sur des leviers peu mobilisés).",
        icon=":material/filter_alt_off:",
    )

    render_etape_3_nav(
        collectivite_id,
        back_key=f"nav_action_retour_empty_{collectivite_id}",
        forward_key=f"nav_action_suivant_empty_{collectivite_id}",
    )
    st.stop()

n_visible_cibles = st.session_state.get(SESSION_VISIBLE_CIBLES_COUNT, CIBLES_PAGE_SIZE)
visible_cibles = cibles[:n_visible_cibles]

max_enjeu = max(cible["enjeu"] for cible in cibles)

for rank, cible in enumerate(visible_cibles, start=1):
    levier = cible["levier"]
    cat = cible["categorie_id"]
    cat_label = cible["categorie"]
    enjeu = cible["enjeu"]

    st.divider()
    col_titre, col_bar = st.columns([3, 2], vertical_alignment="center")
    with col_titre:
        st.subheader(f"{rank}. {levier} — {cat_label}")
        nb_cible = nb_selections_cible(levier, cat)
        if nb_cible:
            st.caption(
                f"**{nb_cible}** action{'s' if nb_cible > 1 else ''} "
                f"sélectionnée{'s' if nb_cible > 1 else ''}"
            )
    with col_bar:
        st.caption(f"Potentiel du volet : **{enjeu:.0f}** ktCO₂e")
        st.progress(min(enjeu / max_enjeu, 1.0) if max_enjeu > 0 else 0.0)

    df_ref, df_autres = fiches_pour_cible(
        levier,
        cat,
        collectivite_id,
        df_priorisation_all,
        df_fiches_action,
        df_actions_reference,
        nom_par_id,
    )

    if df_ref.empty and df_autres.empty:
        st.info(
            "Aucune action disponible pour ce volet.",
            icon=":material/search_off:",
        )
        continue

    col_reference, col_collectivites = st.columns(2, gap="medium")
    with col_reference:
        render_colonne_actions(df_ref, levier, cat, reference=True)
    with col_collectivites:
        render_colonne_actions(df_autres, levier, cat, reference=False)

if len(cibles) > n_visible_cibles:
    restants = len(cibles) - n_visible_cibles
    st.button(
        f"Afficher plus de volets ({restants} restant{'s' if restants > 1 else ''})",
        key="action_show_more_cibles",
        icon=":material/expand_more:",
        width="stretch",
        on_click=show_more_cibles,
        args=(len(cibles),),
    )

st.divider()

to_save = selections_to_rows()
modifie = to_save != saved_to_rows(saved)

col_resume, col_save = st.columns([3, 1], vertical_alignment="center")
with col_resume:
    if modifie:
        st.warning(
            "Modifications non enregistrées.", icon=":material/pending_actions:"
        )
    else:
        st.caption("Votre sélection est à jour.")
with col_save:
    sauvegarder = st.button(
        "Sauvegarder",
        type="primary",
        icon=":material/save:",
        width="stretch",
    )

if sauvegarder:
    try:
        save_priorisation_action(collectivite_id, to_save)
        load_actions_choisies.clear()
        st.session_state.pop(SESSION_COLLECTIVITE, None)
        init_session_selections(
            collectivite_id,
            selections_from_db(load_actions_choisies(collectivite_id)),
            reset_pagination=False,
        )
        st.session_state[SESSION_FLASH] = (
            "success",
            message_sauvegarde(nom_par_id[collectivite_id], len(to_save)),
        )
    except Exception as e:
        st.session_state[SESSION_FLASH] = (
            "error",
            f"Erreur lors de l'enregistrement : {e}",
        )
    st.rerun()

flash = st.session_state.pop(SESSION_FLASH, None)
if flash is not None:
    niveau, message = flash
    if niveau == "success":
        st.success(message, icon=":material/save:")
    else:
        st.error(message, icon=":material/error:")