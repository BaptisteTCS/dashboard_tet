import streamlit as st

st.set_page_config(
    page_title="Synthèse - Tableaux de bord",
    page_icon="🏆",
    layout="wide",
)

import json
import re
from collections.abc import Callable

import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy import text
from streamlit_echarts import JsCode, st_echarts

from utils.collectivite_selection import (
    default_collectivite_index,
    set_selected_collectivite,
)
from utils.db import get_engine, get_engine_prod
from utils.priorisation_impact_charts import (
    CATEGORIES,
    NOTE_COLORS,
    NOTE_LABELS,
    TREEMAP_CLICK_EVENTS,
    build_priorisation_cases,
    build_treemap_data,
    extract_chart_event,
    levier_label_court,
    render_impact_chart,
    render_impact_map,
)
from utils.priorisation_pareto import (
    enjeu_cible,
    render_seuil_impact_cibles_expander,
)

# ==========================
# Constantes
# ==========================

NOTE_BADGE_COLORS = {
    0: "orange",
    1: "yellow",
    2: "green",
    3: "green",
}

CARD_DESCRIPTION_MAX_LEN = 160
CARD_COLUMNS = 2

# priorisation_faisabilite : 1 = Non pertinent, 2 = À discuter avec l'élu, 3 = Pertinent
FAISABILITE_A_DISCUTER = 2


def clean_rich_text(text) -> str:
    """Convertit une description enrichie (HTML) en texte brut lisible."""
    if text is None or (isinstance(text, float) and pd.isna(text)):
        return ""
    text = str(text).strip()
    if not text:
        return ""
    text = BeautifulSoup(text, "html.parser").get_text(separator=" ")
    return re.sub(r"\s+", " ", text).strip()


def short_description(text: str, max_len: int = CARD_DESCRIPTION_MAX_LEN) -> str:
    if len(text) <= max_len:
        return text
    return f"{text[:max_len].rsplit(' ', 1)[0]}…"


def as_bool(value) -> bool:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return False
    return bool(value)


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
        return pd.read_sql_query(text("SELECT * FROM priorisation_categorie_levier"), conn)


@st.cache_data(ttl="1h")
def load_priorisation(collectivite_id: int) -> pd.DataFrame:
    """Notes et ids les plus récents par case (levier × catégorie)."""
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
    """Notes et ids les plus récents par collectivité × case (levier × catégorie)."""
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
                SELECT *
                FROM fiche_action
                WHERE collectivite_id = ANY(:ids)
            """),
            conn,
            params={"ids": list(collectivite_ids)},
        )


@st.cache_data(ttl="1h")
def load_actions_choisies(collectivite_id: int) -> pd.DataFrame:
    """Actions sauvegardées à l'étape « Choix des actions »."""
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("""
                SELECT levier, categorie, fiche_action_id, reference
                FROM priorisation_action
                WHERE collectivite_id = :collectivite_id
                ORDER BY created_at
            """),
            conn,
            params={"collectivite_id": collectivite_id},
        )


@st.cache_data(ttl="1h")
def load_faisabilite(collectivite_id: int) -> pd.DataFrame:
    """Arbitrages politiques enregistrés à l'étape « Priorisation des actions »."""
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
def load_fiches_by_ids(fiche_ids: tuple[int, ...]) -> pd.DataFrame:
    """Fiches action prod résolues depuis priorisation_action.fiche_action_id."""
    if not fiche_ids:
        return pd.DataFrame(columns=["id", "collectivite_id", "titre", "description"])
    engine = get_engine_prod()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("""
                SELECT id, collectivite_id, titre, description
                FROM fiche_action
                WHERE id = ANY(:ids)
            """),
            conn,
            params={"ids": list(fiche_ids)},
        )


@st.cache_data(ttl="1h")
def load_noms_collectivites(collectivite_ids: tuple[int, ...]) -> pd.DataFrame:
    """Noms des collectivités d'origine des fiches, priorisées ou non."""
    if not collectivite_ids:
        return pd.DataFrame(columns=["collectivite_id", "nom"])
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("""
                SELECT collectivite_id, nom
                FROM collectivite
                WHERE collectivite_id = ANY(:ids)
            """),
            conn,
            params={"ids": list(collectivite_ids)},
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


def hors_competence_pairs(df: pd.DataFrame) -> set[tuple[str, int]]:
    return {
        (row["levier"], int(row["categorie"]))
        for _, row in df.iterrows()
    }


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


def build_category_weights(df_poids: pd.DataFrame) -> dict[str, dict[int, float]]:
    """Retourne {levier: {categorie: poids}} depuis priorisation_categorie_levier."""
    levier_cols = [c for c in df_poids.columns if c != "categorie"]
    weights: dict[str, dict[int, float]] = {levier: {} for levier in levier_cols}
    for _, row in df_poids.iterrows():
        cat = int(row["categorie"])
        for levier in levier_cols:
            weights[levier][cat] = row[levier]
    return weights


def actions_par_cible(df_actions: pd.DataFrame) -> dict[tuple[str, int], int]:
    """Nombre d'actions retenues par volet (levier × catégorie)."""
    compte: dict[tuple[str, int], int] = {}
    for _, row in df_actions.iterrows():
        cle = (row["levier"], int(row["categorie"]))
        compte[cle] = compte.get(cle, 0) + 1
    return compte


def fiche_ids_non_reference(df_actions: pd.DataFrame) -> tuple[int, ...]:
    if df_actions.empty:
        return ()
    hors_reference = df_actions[~df_actions["reference"].map(as_bool)]
    return tuple(sorted({int(fid) for fid in hors_reference["fiche_action_id"]}))


def build_actions_sauvegardees(
    df_actions: pd.DataFrame,
    df_actions_reference: pd.DataFrame,
    df_fiches: pd.DataFrame,
    reductions: dict[str, float],
    weights: dict[str, dict[int, float]],
    noms_collectivites: dict[int, str],
) -> list[dict]:
    """
    Actions retenues, triées par potentiel du volet décroissant.

    `reference` distingue les deux référentiels : True renvoie vers
    priorisation_action_reference (OLAP), False vers fiche_action (prod).
    """
    if df_actions.empty:
        return []

    ref_by_id = (
        df_actions_reference.set_index("id")
        if not df_actions_reference.empty
        else pd.DataFrame()
    )
    fiches_by_id = (
        df_fiches.drop_duplicates(subset="id").set_index("id")
        if not df_fiches.empty
        else pd.DataFrame()
    )

    cartes: list[dict] = []
    for _, row in df_actions.iterrows():
        levier = row["levier"]
        cat = int(row["categorie"])
        fiche_id = int(row["fiche_action_id"])
        reference = as_bool(row.get("reference"))

        source = ref_by_id if reference else fiches_by_id
        fiche = (
            source.loc[fiche_id]
            if not source.empty and fiche_id in source.index
            else None
        )

        if fiche is None:
            titre = f"Action #{fiche_id}"
            description = ""
            origine = "Action de référence" if reference else "Origine inconnue"
        else:
            titre = clean_rich_text(fiche.get("titre")) or f"Action #{fiche_id}"
            description = clean_rich_text(fiche.get("description"))
            if reference:
                origine = "Action de référence"
            else:
                ct_id = int(fiche["collectivite_id"])
                origine = noms_collectivites.get(ct_id, f"Collectivité #{ct_id}")

        cartes.append(
            {
                "titre": titre,
                "description": description,
                "levier": levier,
                "categorie": CATEGORIES.get(cat, str(cat)),
                "enjeu": enjeu_cible(levier, cat, reductions, weights),
                "reference": reference,
                "origine": origine,
            }
        )

    cartes.sort(key=lambda c: (-c["enjeu"], c["levier"], c["titre"]))
    return cartes


def load_cartes_actions(
    collectivite_id: int,
    reductions: dict[str, float],
    weights: dict[str, dict[int, float]],
    nom_par_id: dict[int, str],
) -> list[dict]:
    """Résout les actions sauvegardées et leurs deux référentiels d'origine."""
    df_actions = load_actions_choisies(collectivite_id)
    df_fiches = load_fiches_by_ids(fiche_ids_non_reference(df_actions))

    noms_collectivites = dict(nom_par_id)
    if not df_fiches.empty:
        noms_collectivites.update(
            load_noms_collectivites(
                tuple(sorted({int(c) for c in df_fiches["collectivite_id"]}))
            )
            .set_index("collectivite_id")["nom"]
            .to_dict()
        )

    return build_actions_sauvegardees(
        df_actions,
        load_actions_reference(),
        df_fiches,
        reductions,
        weights,
        noms_collectivites,
    )


def render_action_card(carte: dict) -> None:
    """Card d'une action retenue : volet, origine, titre et potentiel du volet."""
    with st.container(border=True, height="stretch"):
        col_volet, col_origine = st.columns([3, 2], vertical_alignment="center")
        with col_volet:
            st.badge(
                f"{levier_label_court(carte['levier'])} · {carte['categorie']}",
                icon=":material/category:",
                color="green",
            )
        with col_origine:
            if carte["reference"]:
                st.badge(
                    "Action de référence",
                    icon=":material/cards_star:",
                    color="orange",
                )
            else:
                st.badge(
                    carte["origine"],
                    icon=":material/location_city:",
                    color="blue",
                )

        st.markdown(f"**{carte['titre']}**")

        description = carte["description"]
        if description:
            st.caption(short_description(description))
            if len(description) > CARD_DESCRIPTION_MAX_LEN:
                with st.popover(
                    "Lire la description complète",
                    icon=":material/description:",
                ):
                    st.markdown(f"**{carte['titre']}**")
                    st.caption(f"{carte['levier']} · {carte['categorie']}")
                    st.write(description)
        else:
            st.caption("Aucune description disponible.")

        st.caption(f"Potentiel du volet : **{carte['enjeu']:.0f}** ktCO₂e")


def build_volets_a_discuter(
    df_faisabilite: pd.DataFrame,
    reductions: dict[str, float],
    weights: dict[str, dict[int, float]],
    hors_competence: set[tuple[str, int]],
    compte_actions: dict[tuple[str, int], int],
) -> list[dict]:
    """Volets arbitrés « À discuter avec l'élu », par potentiel décroissant."""
    if df_faisabilite.empty:
        return []

    volets: list[dict] = []
    for _, row in df_faisabilite.iterrows():
        if int(row["faisabilite"]) != FAISABILITE_A_DISCUTER:
            continue
        levier = row["levier"]
        cat = int(row["categorie"])
        if (levier, cat) in hors_competence:
            continue
        volets.append(
            {
                "levier": levier,
                "categorie": CATEGORIES.get(cat, str(cat)),
                "enjeu": enjeu_cible(levier, cat, reductions, weights),
                "n_actions": compte_actions.get((levier, cat), 0),
            }
        )

    volets.sort(key=lambda v: (-v["enjeu"], v["levier"], v["categorie"]))
    return volets


def render_volet_card(volet: dict) -> None:
    """Card d'un volet à arbitrer : intitulé, potentiel et actions déjà retenues."""
    with st.container(border=True, height="stretch"):
        col_volet, col_actions = st.columns([3, 2], vertical_alignment="center")
        with col_volet:
            st.badge(
                "À discuter avec l'élu",
                icon=":material/forum:",
                color="orange",
            )
        with col_actions:
            n_actions = volet["n_actions"]
            if n_actions:
                st.badge(
                    f"{n_actions} action{'s' if n_actions > 1 else ''} "
                    f"sauvegardée{'s' if n_actions > 1 else ''}",
                    icon=":material/bookmark:",
                    color="green",
                )
            else:
                st.badge(
                    "Aucune action retenue",
                    icon=":material/bookmark_border:",
                    color="grey",
                )

        st.markdown(f"**{volet['levier']} · {volet['categorie']}**")
        st.caption(f"Potentiel du volet : **{volet['enjeu']:.0f}** ktCO₂e")


def render_cards_grid(items: list[dict], renderer: Callable[[dict], None]) -> None:
    """Grille de cards sur deux colonnes, du potentiel le plus fort au plus faible."""
    for start in range(0, len(items), CARD_COLUMNS):
        colonnes = st.columns(CARD_COLUMNS, gap="medium")
        for colonne, item in zip(colonnes, items[start : start + CARD_COLUMNS]):
            with colonne:
                renderer(item)


def build_mobilisation_bar_options(
    cases: list[dict], selected_note: int
) -> dict | None:
    """Barres horizontales ECharts, tri décroissant (plus fort enjeu en haut)."""
    filtered = [c for c in cases if c["note"] == selected_note]
    if not filtered:
        return None

    filtered.sort(key=lambda c: c["enjeu"], reverse=True)
    labels = [c["label"] for c in filtered]
    color = NOTE_COLORS.get(selected_note, NOTE_COLORS[0])

    return {
        "backgroundColor": "transparent",
        "animationDuration": 600,
        "animationEasing": "cubicOut",
        "grid": {"left": 24, "right": 72, "top": 16, "bottom": 28, "containLabel": True},
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "shadow", "shadowStyle": {"opacity": 0.08}},
            "formatter": JsCode(
                """
                function(params) {
                    var p = params && params[0];
                    if (!p || !p.data) return '';
                    var d = p.data;
                    return (d.levierFull || '') + '<br/>'
                        + (d.categorie || '') + '<br/>'
                        + '<b>' + Number(p.value).toFixed(1) + ' ktCO₂e</b>';
                }
                """
            ),
        },
        "xAxis": {
            "type": "value",
            "name": "ktCO₂e",
            "nameTextStyle": {"color": "#888", "fontSize": 11},
            "axisLine": {"show": False},
            "axisTick": {"show": False},
            "axisLabel": {"color": "#888", "fontSize": 11},
            "splitLine": {"lineStyle": {"color": "#ebebeb", "type": "dashed"}},
        },
        "yAxis": {
            "type": "category",
            "data": labels,
            "inverse": True,
            "axisLine": {"show": False},
            "axisTick": {"show": False},
            "axisLabel": {
                "fontSize": 12,
                "color": "#333",
                "width": 400,
                "overflow": "break",
                "lineHeight": 16,
            },
        },
        "series": [
            {
                "type": "bar",
                "data": [
                    {
                        "value": c["enjeu"],
                        "levierFull": c["levier"],
                        "categorie": c["categorie"],
                        "itemStyle": {
                            "color": color,
                            "borderRadius": [0, 8, 8, 0],
                            "shadowColor": "rgba(0,0,0,0.06)",
                            "shadowBlur": 6,
                            "shadowOffsetY": 2,
                        },
                    }
                    for c in filtered
                ],
                "barMaxWidth": 26,
                "emphasis": {
                    "itemStyle": {
                        "shadowColor": "rgba(0,0,0,0.12)",
                        "shadowBlur": 10,
                    }
                },
                "label": {
                    "show": True,
                    "position": "right",
                    "distance": 8,
                    "formatter": JsCode(
                        "function(p) { return Number(p.value).toFixed(1) + ' kt'; }"
                    ),
                    "fontSize": 11,
                    "color": "#555",
                },
            }
        ],
    }


MOBILISATION_BAR_ROW_PX = 40
MOBILISATION_BAR_MIN_HEIGHT = 280


# ==========================
# Interface
# ==========================

st.title("🏆 Priorisation - Tableaux de bord")

st.warning(
    """
**Tableau de bord de la priorisation des actions**

Vous retrouvez ici :
- les **actions que vous avez sélectionnées** pour chaque volet prioritaire
- les **volets que vous avez jugés à discuter** avec vos élus

Plus bas, la carte et le graphique des volets vous donnent une vue d'ensemble sur les domaines où agissent vos plans d'actions.
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
df_fiches_action = load_fiches_action(tuple(collectivite_ids))

selected_id = st.selectbox(
    "Collectivité",
    options=collectivite_ids,
    index=default_collectivite_index(collectivite_ids),
    format_func=lambda cid: nom_par_id[cid],
    key="diag_select_collectivite",
)

set_selected_collectivite(selected_id)

st.markdown("---")

df_priorisation = load_priorisation(selected_id)
df_priorisation_all = load_priorisation_all(tuple(collectivite_ids))
df_reductions = load_reductions(selected_id)
df_poids = load_poids_categories()
hors_competence = hors_competence_pairs(load_hors_competence(selected_id))

leviers = sorted(df_priorisation["levier"].unique().tolist())
reductions = df_reductions.set_index("levier")["reduction"].to_dict()
notes = {
    (row["levier"], int(row["categorie"])): int(row["note"])
    for _, row in df_priorisation.iterrows()
    if (row["levier"], int(row["categorie"])) not in hors_competence
}
ids_by_case = {
    (row["levier"], int(row["categorie"])): parse_ids(row["ids"])
    for _, row in df_priorisation.iterrows()
    if (row["levier"], int(row["categorie"])) not in hors_competence
}
weights = build_category_weights(df_poids)
compte_actions = actions_par_cible(load_actions_choisies(selected_id))
cibles_actions = set(compte_actions)

# ==========================
# Actions sauvegardées
# ==========================

st.subheader("🎯 Vos actions sauvegardées")

cartes_actions = load_cartes_actions(selected_id, reductions, weights, nom_par_id)

if not cartes_actions:
    st.info(
        "Aucune action sauvegardée pour cette collectivité. "
        "Rendez-vous à l'étape « Actions de référence » pour constituer "
        "votre sélection.",
        icon=":material/bookmark_add:",
    )
else:
    n_volets = len({(c["levier"], c["categorie"]) for c in cartes_actions})

    col_total, col_volets, _ = st.columns(3)
    col_total.metric("Actions sauvegardées", len(cartes_actions))
    col_volets.metric("Volets couverts", n_volets)

    render_cards_grid(cartes_actions, render_action_card)

st.markdown("---")

# ==========================
# Volets à discuter avec l'élu
# ==========================

st.subheader("🗣️ Volets à discuter avec vos élus")

volets_a_discuter = build_volets_a_discuter(
    load_faisabilite(selected_id),
    reductions,
    weights,
    hors_competence,
    compte_actions,
)

if not volets_a_discuter:
    st.info(
        "Aucun volet marqué « À discuter avec l'élu ». Vous pouvez revenir à "
        "l'étape « Priorisation des actions » pour signaler les volets qui "
        "demandent un arbitrage politique.",
        icon=":material/forum:",
    )
else:
    st.caption(
        "Ces volets peu mobilisés attendent une décision politique. "
        "Ils sont classés du potentiel de réduction le plus fort au plus faible."
    )
    render_cards_grid(volets_a_discuter, render_volet_card)

st.markdown("---")

st.info(
    """
**Vue d'ensemble de vos plans d'actions**

Visualisez comment l'ensemble de vos plans se répartit sur les volets, et repérez d'un coup d'œil les volets à fort potentiel que vous ne mobilisez pas encore. Les volets en orange sont ceux sur lesquelles vous avez retenu des actions.
""",
    icon=":material/travel_explore:",
)

# Les onglets sont réservés avant l'expander pour que le seuil s'affiche en dessous,
# alors que ses valeurs sont nécessaires en amont pour construire les graphiques.
tabs_slot = st.container()

threshold_pct, selected_cibles = render_seuil_impact_cibles_expander(
    leviers,
    reductions,
    weights,
    hors_competence,
    key_prefix=f"vue_ensemble_{selected_id}",
)

priorisation_cases = build_priorisation_cases(
    leviers,
    reductions,
    notes,
    weights,
    hors_competence,
    cibles_actions=cibles_actions,
    selected_cibles=selected_cibles,
)

treemap_children, _ = build_treemap_data(
    leviers,
    reductions,
    notes,
    weights,
    hors_competence,
    cibles_actions=cibles_actions,
    selected_cibles=selected_cibles,
)
excluded_leviers = [levier for levier in leviers if levier not in reductions]

with tabs_slot:
    tabs = st.tabs(["Carte des volets", "Graphique des volets"])

_detail_slot_holder: dict = {}


def _before_treemap_chart() -> None:
    if st.session_state.get("treemap_collectivite_id") != selected_id:
        st.session_state.pop("treemap_selection", None)
    st.session_state["treemap_collectivite_id"] = selected_id

    treemap_selection = st.session_state.get("treemap_selection")
    if treemap_selection and treemap_selection.get("levier") not in leviers:
        st.session_state.pop("treemap_selection", None)

    _detail_slot_holder["slot"] = st.empty()


with tabs[0]:
    _, click = render_impact_map(
        treemap_children,
        excluded_leviers,
        chart_key_prefix=f"treemap_{selected_id}",
        threshold_pct=threshold_pct,
        labels_toggle_default=True,
        show_labels_toggle=False,
        show_actions_retenues=True,
        click_events=TREEMAP_CLICK_EVENTS,
        before_chart=_before_treemap_chart if treemap_children else None,
        cibles_actions=cibles_actions,
    )

    if treemap_children:
        click_event = extract_chart_event(click)
        if click_event and click_event.get("levier"):
            st.session_state["treemap_selection"] = click_event

        selection = st.session_state.get("treemap_selection")
        with _detail_slot_holder["slot"].container():
            if selection:
                levier = selection["levier"]
                cat_id = selection.get("categorieId")
                if cat_id is not None:
                    try:
                        cat_id = int(cat_id)
                    except (TypeError, ValueError):
                        cat_id = None
                if cat_id is None:
                    cat_id = next(
                        (
                            k
                            for k, v in CATEGORIES.items()
                            if v == selection.get("categorie")
                        ),
                        None,
                    )
                cat_label = CATEGORIES.get(cat_id, selection.get("categorie", ""))
                action_ids = (
                    ids_by_case.get((levier, int(cat_id)), [])
                    if cat_id is not None
                    else []
                )
                note = (
                    int(notes.get((levier, int(cat_id)), 0))
                    if cat_id is not None
                    else 0
                )
                note_label = NOTE_LABELS.get(note, NOTE_LABELS[0])
                note_badge_color = NOTE_BADGE_COLORS.get(note, "orange")

                st.subheader(
                    f"{levier} · {cat_label} :{note_badge_color}-badge[{note_label}]"
                )
                st.badge("Actions associées", icon=":material/add_notes:", color="blue")

                if not action_ids:
                    st.info(f"Aucune action associée à : {levier} · {cat_label}.")
                else:
                    df_fiches_case = df_fiches_action[
                        df_fiches_action["id"].isin(action_ids)
                        & (df_fiches_action["collectivite_id"] == selected_id)
                    ]
                    if df_fiches_case.empty:
                        st.info(
                            "Aucune fiche action trouvée pour les identifiants associés."
                        )
                    else:
                        for _, fiche in df_fiches_case.iterrows():
                            titre = fiche.get("titre") or f"Fiche #{fiche['id']}"
                            with st.expander(titre):
                                description = clean_rich_text(fiche.get("description"))
                                if description:
                                    st.write(description)
                                else:
                                    st.caption("Aucune description.")

                st.badge(
                    "Actions de référence",
                    icon=":material/cards_star:",
                    color="yellow",
                )
                st.warning("Aucune action de référence pour le moment.")

                st.badge("Actions des autres collectivités", icon=":material/search_check:", color="yellow")

                with st.expander("Voir les actions des autres collectivités"):
                    if cat_id is None:
                        st.info(
                            f"Aucune action d'autres collectivités associée à : "
                            f"{levier} · {cat_label}."
                        )
                    else:
                        df_priorisation_autres = df_priorisation_all[
                            (df_priorisation_all["levier"] == levier)
                            & (df_priorisation_all["categorie"] == int(cat_id))
                            & (df_priorisation_all["collectivite_id"] != selected_id)
                        ]
                        collectivites_avec_actions: list[tuple[int, list[int]]] = []
                        for _, row in df_priorisation_autres.iterrows():
                            ct_ids = parse_ids(row["ids"])
                            if ct_ids:
                                collectivites_avec_actions.append(
                                    (int(row["collectivite_id"]), ct_ids)
                                )

                        if not collectivites_avec_actions:
                            st.info(
                                f"Aucune action d'autres collectivités pour : "
                                f"{levier} · {cat_label}."
                            )
                        else:
                            collectivites_avec_actions.sort(
                                key=lambda item: nom_par_id.get(item[0], "").lower()
                            )
                            affiche = False
                            for ct_id, ct_action_ids in collectivites_avec_actions:
                                df_fiches_ct = df_fiches_action[
                                    df_fiches_action["id"].isin(ct_action_ids)
                                    & (df_fiches_action["collectivite_id"] == ct_id)
                                ]
                                if df_fiches_ct.empty:
                                    continue

                                affiche = True
                                collectivite_nom = nom_par_id.get(
                                    ct_id, f"Collectivité #{ct_id}"
                                )
                                st.markdown(f"**{collectivite_nom}**")
                                id_order = {
                                    aid: i for i, aid in enumerate(ct_action_ids)
                                }
                                df_fiches_ct = df_fiches_ct.assign(
                                    _ord=df_fiches_ct["id"].map(id_order)
                                ).sort_values("_ord")

                                for _, fiche in df_fiches_ct.iterrows():
                                    titre = fiche.get("titre") or f"Fiche #{fiche['id']}"
                                    with st.expander(titre):
                                        description = clean_rich_text(
                                            fiche.get("description")
                                        )
                                        if description:
                                            st.write(description)
                                        else:
                                            st.caption("Aucune description.")

                            if not affiche:
                                st.info(
                                    "Des identifiants sont enregistrés pour d'autres "
                                    "collectivités, mais aucune fiche action correspondante "
                                    "n'a été trouvée."
                                )

with tabs[1]:
    render_impact_chart(
        priorisation_cases,
        chart_key=f"vue_ensemble_{selected_id}_{threshold_pct}",
        show_actions_retenues=True,
    )
