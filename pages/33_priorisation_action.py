import streamlit as st

st.set_page_config(
    page_title="Priorisation — choix des actions",
    page_icon="🎯",
    layout="wide",
)

import json
import re

import pandas as pd
from bs4 import BeautifulSoup
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

NOTE_LABELS = {
    0: "Non mobilisé",
    1: "Partiellement mobilisé",
    2: "Bien mobilisé",
    3: "Pleinement mobilisé",
}

NOTE_BADGE_COLORS = {
    0: "orange",
    1: "yellow",
    2: "green",
    3: "green",
}

# Faisabilité 2 = À discuter, 3 = Prioritaire
FAISABILITE_ELIGIBLE = {2, 3}

SESSION_SELECTIONS = "action_selections"
SESSION_COLLECTIVITE = "action_collectivite_id"


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
def load_actions_choisies(collectivite_id: int) -> pd.DataFrame:
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("""
                SELECT levier, categorie, fiche_action_id
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


def selections_from_db(df: pd.DataFrame) -> dict[tuple[str, int], set[int]]:
    result: dict[tuple[str, int], set[int]] = {}
    for _, row in df.iterrows():
        key = (row["levier"], int(row["categorie"]))
        result.setdefault(key, set()).add(int(row["fiche_action_id"]))
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
                    "note": notes.get((levier, cat), 0),
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


def fiches_reference_pour_cible() -> pd.DataFrame:
    """Actions de référence — non disponibles pour le moment (cf. page diagnostic)."""
    return pd.DataFrame(columns=["id", "intitule", "description", "origine"])


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


def checkbox_key(levier: str, cat: int, fiche_id: int) -> str:
    return f"sel_action_{levier}_{cat}_{fiche_id}"


def clear_checkbox_keys() -> None:
    for key in list(st.session_state.keys()):
        if str(key).startswith("sel_action_"):
            del st.session_state[key]


def init_session_selections(collectivite_id: int, saved: dict[tuple[str, int], set[int]]) -> None:
    if st.session_state.get(SESSION_COLLECTIVITE) == collectivite_id:
        return
    clear_checkbox_keys()
    st.session_state[SESSION_SELECTIONS] = {
        key: set(ids) for key, ids in saved.items()
    }
    st.session_state[SESSION_COLLECTIVITE] = collectivite_id


def collect_selections_from_widgets(
    cibles: list[dict],
    collectivite_id: int,
    df_priorisation_all: pd.DataFrame,
    df_fiches_action: pd.DataFrame,
    nom_par_id: dict[int, str],
) -> list[tuple[str, int, int]]:
    rows: list[tuple[str, int, int]] = []
    for cible in cibles:
        levier = cible["levier"]
        cat = cible["categorie_id"]
        df_ref = fiches_reference_pour_cible()
        df_autres = fiches_autres_collectivites(
            levier,
            cat,
            collectivite_id,
            df_priorisation_all,
            df_fiches_action,
            nom_par_id,
        )
        for _, fiche in pd.concat([df_ref, df_autres], ignore_index=True).iterrows():
            fid = int(fiche["id"])
            if st.session_state.get(checkbox_key(levier, cat, fid), False):
                rows.append((levier, cat, fid))
    return sorted(rows, key=lambda x: (x[0], x[1], x[2]))


def save_priorisation_action(
    collectivite_id: int,
    rows: list[tuple[str, int, int]],
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
                        (collectivite_id, levier, categorie, fiche_action_id)
                    VALUES (:collectivite_id, :levier, :categorie, :fiche_action_id)
                """),
                [
                    {
                        "collectivite_id": collectivite_id,
                        "levier": levier,
                        "categorie": cat,
                        "fiche_action_id": fiche_id,
                    }
                    for levier, cat, fiche_id in rows
                ],
            )


def render_fiche_checkbox(
    fiche: pd.Series,
    levier: str,
    cat: int,
    saved_ids: set[int],
    *,
    reference: bool,
) -> None:
    fid = int(fiche["id"])
    key = checkbox_key(levier, cat, fid)
    if key not in st.session_state:
        st.session_state[key] = fid in saved_ids

    badge = origine_label(fiche.get("origine"))
    titre = fiche.get("intitule") or f"Fiche #{fid}"
    desc = short_description(fiche.get("description"))

    col_check, col_content = st.columns([0.06, 0.94])
    with col_check:
        st.checkbox(
            titre,
            key=key,
            label_visibility="collapsed",
        )
    with col_content:
        st.markdown(f"**{titre}**")
        if reference:
            st.badge(badge, icon=":material/cards_star:", color="yellow")
        else:
            st.badge(badge, icon=":material/location_city:", color="blue")
        if desc:
            st.caption(desc)
        else:
            st.caption("Aucune description.")


# ==========================
# Interface
# ==========================

st.title("🏅 Choix des actions")

st.markdown(
    "Après l'arbitrage politique, cette étape sert à **choisir**, parmi des actions "
    "**éprouvées** (fiches de référence et actions d'autres collectivités), celles que "
    "votre collectivité souhaite **engager** sur ses **cibles prioritaires** — les "
    "angles morts retenus à l'étape précédente."
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
    key="action_select_collectivite",
)

st.markdown("---")

df_priorisation = load_priorisation(collectivite_id)
df_priorisation_all = load_priorisation_all(tuple(collectivite_ids))
df_reductions = load_reductions(collectivite_id)
df_poids = load_poids_categories()
df_fiches_action = load_fiches_action(tuple(collectivite_ids))
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
        "Aucune cible prioritaire pour cette collectivité. Vérifiez le diagnostic, "
        "le périmètre et l'arbitrage politique (faisabilité « À discuter » ou "
        "« Prioritaire » sur des cibles peu mobilisées)."
    )
    st.stop()

st.caption(
    f"**{len(cibles)}** cibles prioritaires classées par impact décroissant."
)

for levier, cibles_levier in group_cibles_by_levier(cibles):
    for cible in cibles_levier:
        cat = cible["categorie_id"]
        cat_label = cible["categorie"]
        saved_ids = saved.get((levier, cat), set())
        note = cible["note"]
        note_label = NOTE_LABELS.get(note, NOTE_LABELS[0])
        note_badge_color = NOTE_BADGE_COLORS.get(note, "orange")

        st.subheader(f"{levier} - {cat_label} :{note_badge_color}-badge[{note_label}]")

        df_ref = fiches_reference_pour_cible()
        df_autres = fiches_autres_collectivites(
            levier,
            cat,
            collectivite_id,
            df_priorisation_all,
            df_fiches_action,
            nom_par_id,
        )

        if df_ref.empty and df_autres.empty:
            st.info("Aucune fiche action disponible pour cette cible.")
            st.markdown("")
            continue

        st.badge(
            "Actions de référence",
            icon=":material/cards_star:",
            color="green",
        )
        if df_ref.empty:
            st.caption("Aucune action de référence pour le moment.")
        else:
            for _, fiche in df_ref.iterrows():
                render_fiche_checkbox(
                    fiche, levier, cat, saved_ids, reference=True
                )

        st.badge(
            "Actions des autres collectivités",
            icon=":material/search_check:",
            color="green",
        )
        if df_autres.empty:
            st.caption("Aucune action d'autres collectivités pour cette cible.")
        else:
            for _, fiche in df_autres.iterrows():
                render_fiche_checkbox(
                    fiche, levier, cat, saved_ids, reference=False
                )

        st.markdown("")

st.markdown("---")

if st.button("Sauvegarder", type="primary"):
    to_save = collect_selections_from_widgets(
        cibles,
        collectivite_id,
        df_priorisation_all,
        df_fiches_action,
        nom_par_id,
    )
    try:
        save_priorisation_action(collectivite_id, to_save)
        load_actions_choisies.clear()
        clear_checkbox_keys()
        st.session_state.pop(SESSION_COLLECTIVITE, None)
        init_session_selections(
            collectivite_id, selections_from_db(load_actions_choisies(collectivite_id))
        )
        n = len(to_save)
        if n == 0:
            st.success(
                f"Choix enregistrés pour **{nom_par_id[collectivite_id]}** "
                "(aucune action sélectionnée)."
            )
        elif n == 1:
            st.success(
                f"Choix enregistrés pour **{nom_par_id[collectivite_id]}** "
                f"({n} action)."
            )
        else:
            st.success(
                f"Choix enregistrés pour **{nom_par_id[collectivite_id]}** "
                f"({n} actions)."
            )
    except Exception as e:
        st.error(f"Erreur lors de l'enregistrement : {e}")
