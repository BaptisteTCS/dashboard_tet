import streamlit as st

st.set_page_config(
    page_title="Priorisation — treemap",
    page_icon="🧭",
    layout="wide",
)

import json
import re

import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy import text
from streamlit_echarts import JsCode, st_echarts

from utils.db import get_engine, get_engine_prod
from utils.priorisation_impact_charts import (
    CATEGORIES,
    NOTE_COLORS,
    NOTE_LABELS,
    TREEMAP_CLICK_EVENTS,
    build_priorisation_cases,
    build_treemap_data,
    extract_chart_event,
    render_impact_chart,
    render_impact_map,
)
from utils.priorisation_navigation import render_etape_1_suivant
from utils.priorisation_pareto import render_seuil_impact_cibles_expander

# ==========================
# Constantes
# ==========================

NOTE_BADGE_COLORS = {
    0: "orange",
    1: "yellow",
    2: "green",
    3: "green",
}


def clean_rich_text(text) -> str:
    """Convertit une description enrichie (HTML) en texte brut lisible."""
    if text is None or (isinstance(text, float) and pd.isna(text)):
        return ""
    text = str(text).strip()
    if not text:
        return ""
    text = BeautifulSoup(text, "html.parser").get_text(separator=" ")
    return re.sub(r"\s+", " ", text).strip()


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

st.title("💡 Visualisation de l'impact des actions de votre collectivité")

st.markdown(
    """Visualisez l'impact potentiel des actions de votre collectivité au regard des leviers de la transition écologique. Vos actions ont été regroupées par volet. Pour en savoir plus, cliquez sur l'introduction ci-dessous."""
)

with st.expander("Introduction à l'outil"):
    st.info("""Cet outil a pour objectif de mettre en perspective les actions de votre PCAET au regard des leviers de la TE et de leur potentiel d'impact.

Le SGPE structure la réduction des émissions de GES autour de grands leviers de la transition écologique (Vélo, Rénovation des bâtiments, Alimentation...). Chaque levier se décline en volets, qui correspondent aux types d'actions mobilisables (Sensibilisation, Investissement, Réglementation...).

- Identifiez quels sont les volets que votre PCAET couvre et ceux qu'il ne couvre pas
- Pour les volets couverts, visualisez le potentiel d'impact de vos actions sur les émissions de GES
- Pour les volets non couverts, découvrez des actions éprouvées que vous pourriez décider de mettre en place

Cet outil a pour but de proposer une réflexion et non une solution toute faite. Il peut servir de base d'échange tangible avec vos élus.""")

df_collectivites = load_collectivites_priorisees()

if df_collectivites.empty:
    st.warning("Aucune collectivité avec des données de priorisation disponible.")
    st.stop()

nom_par_id = df_collectivites.set_index("collectivite_id")["nom"].to_dict()
collectivite_ids = df_collectivites["collectivite_id"].tolist()
df_fiches_action = load_fiches_action(tuple(collectivite_ids))

default_index = 0
qp_id = st.query_params.get("collectivite_id")
if qp_id is not None:
    try:
        qp_id_int = int(qp_id)
        if qp_id_int in collectivite_ids:
            default_index = collectivite_ids.index(qp_id_int)
    except (TypeError, ValueError):
        pass

selected_id = st.selectbox(
    "Collectivité",
    options=collectivite_ids,
    index=default_index,
    format_func=lambda cid: nom_par_id[cid],
    key="diag_select_collectivite",
)

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
    selected_cibles=selected_cibles,
)

treemap_children, _ = build_treemap_data(
    leviers,
    reductions,
    notes,
    weights,
    hors_competence,
    selected_cibles=selected_cibles,
)
excluded_leviers = [levier for levier in leviers if levier not in reductions]

tabs = st.tabs(["Carte de l'impact", "Graphique de l'impact"])

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
        labels_toggle_key=f"diag_treemap_labels_{selected_id}",
        labels_toggle_default=True,
        click_events=TREEMAP_CLICK_EVENTS,
        before_chart=_before_treemap_chart if treemap_children else None,
        palette_selector_key=f"diag_palette_{selected_id}",
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


# with tabs[2]:
#     note_options = [NOTE_LABELS[i] for i in range(4)]
#     selected_note_label = st.segmented_control(
#         "État de mobilisation",
#         options=note_options,
#         default=note_options[0],
#         key=f"mobilisation_note_{selected_id}",
#     )
#     selected_note = next(
#         note for note, label in NOTE_LABELS.items() if label == selected_note_label
#     )
#     note_badge_color = NOTE_BADGE_COLORS.get(selected_note, "orange")

#     st.caption(
#         f"Leviers **{selected_note_label.lower()}**, "
#         "classés par potentiel de réduction décroissant."
#     )

#     bar_options = build_mobilisation_bar_options(
#         priorisation_cases, selected_note
#     )
#     if bar_options is None:
#         st.info(
#             f"Aucun levier × catégorie en état « {selected_note_label} » "
#             "pour cette collectivité."
#         )
#     else:
#         n_bars = len([c for c in priorisation_cases if c["note"] == selected_note])
#         chart_height = max(
#             MOBILISATION_BAR_MIN_HEIGHT,
#             n_bars * MOBILISATION_BAR_ROW_PX + 80,
#         )
#         st.markdown(
#             f"### :{note_badge_color}-badge[{selected_note_label}]"
#         )
#         st_echarts(
#             options=bar_options,
#             height=f"{chart_height}px",
#             key=f"mobilisation_bar_{selected_id}_{selected_note}_{threshold_pct}",
#         )

with tabs[1]:
    render_impact_chart(
        priorisation_cases,
        chart_key=f"vue_ensemble_{selected_id}_{threshold_pct}",
    )

st.markdown("---")
render_etape_1_suivant(selected_id, key=f"nav_diag_suivant_{selected_id}")
