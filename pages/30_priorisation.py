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
from utils.priorisation_pareto import render_seuil_impact_cibles_expander

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

COLOR_grey = {
    0: "#ADADAD",
    1: "#E8E8E8",
    2: "#B5D96A",
    3: "#4CAF7D",
}

COLOR_yellow = {
    0: "#FBE8CE",
    1: "#E4DFB5",
    2: "#C3CC9B",
    3: "#9AB17A",
}

COLOR_mobilisation = {
    0: "#E8E8E8",
    1: "#F5E170",
    2: "#B5D96A",
    3: "#4CAF7D",
}

COLOR_green = {
    0: "#f2e8cf",
    1: "#a7c957",
    2: "#6a994e",
    3: "#386641",
}

COLOR_green_2 = {
    0: "#E8E8E8",
    1: "#D0F0C0",
    2: "#74C365",
    3: "#018749",
}

COLOR_green_3 = {
    0: "#E2E5E9",
    1: "#f5ebe0",
    2: "#5DCF69",
    3: "#389D49",
}

NOTE_COLORS = COLOR_green_3


# Couleurs st.badge (proches de NOTE_COLORS ; 2 et 3 en vert)
NOTE_BADGE_COLORS = {
    0: "orange",
    1: "yellow",
    2: "green",
    3: "green",
}

# Libellés courts des leviers — affichage treemap uniquement (tooltip = nom complet)
LEVIER_LABELS = {
    "Captage de méthane dans les ISDND": "Captage méthane",
    "Biogaz": "Biogaz",
    "Véhicules électriques": "Véhicules électriques",
    "Efficacité et carburants décarbonés des véhicules privés": "Carburants décarbonés",
    "Sobriété des bâtiments (résidentiel)": "Sobriété bâtiments résidentiel",
    "Pratiques stockantes": "Pratiques stockantes",
    "Changement chaudières gaz + rénovation (résidentiel)": "Chaudières gaz & rénovation résidentiel",
    "Vélo et transport en commun": "Vélo & TEC",
    "Bus et cars décarbonés": "Bus et cars décarbonés",
    "Changement de chaudière à fioul (tertiaire)": "Chaudière fioul (tertiaire)",
    "Réduction des déplacements": "Réduction des déplacements",
    "Sobriété et isolation des bâtiments (tertiaire)": "Sobriété et isolation des bâtiments (tertiaire)",
    "Gestion des forêts et produits bois": "Gestion des forêts",
    "Changements de pratiques de fertilisation azotée": "Fertilisation azotée",
    "Elevage durable": "Elevage durable",
    "Bâtiments & Machines agricoles": "Bâtiments & Machines agricoles",
    "Valorisation matière des déchets": "Valorisation déchets",
    "Changement chaudières fioul + rénovation (résidentiel)": "Chaudières fioul & rénovation (résidentiel)",
    "Gestion des haies": "Gestion des haies",
    "Sobriété foncière": "Sobriété foncière",
    "Réseaux de chaleur décarbonés": "Réseaux de chaleur",
    "Prévention des déchets": "Prévention des déchets",
    "Changement de chaudière à gaz (tertiaire)": "Chaudière gaz (tertiaire)",
    "Fret décarboné et multimodalité": "Fret décarboné",
    "Electricité renouvelable": "Electricité renouvelable",
    "Efficacité et sobriété logistique": "Sobriété logistique",
    "Covoiturage": "Covoiturage",
    "Production Industrielle": "Production Industrielle",
    "Gestion des prairies": "Gestion des prairies",
}


def levier_label_court(levier: str) -> str:
    """Libellé court pour l'affichage sur les cases de la treemap."""
    return LEVIER_LABELS.get(levier, levier)


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


def build_treemap_data(
    leviers: list[str],
    reductions: dict[str, float],
    notes: dict[tuple[str, int], int],
    weights: dict[str, dict[int, float]],
    exclusions: set[tuple[str, int]] | None = None,
    selected_cibles: set[tuple[str, int]] | None = None,
) -> tuple[list[dict], list[str]]:
    """Construit la structure ECharts et retourne les leviers exclus (sans réduction)."""
    excluded_leviers: list[str] = []
    children: list[dict] = []
    exclusions = exclusions or set()

    for levier in sorted(leviers):
        if levier not in reductions:
            excluded_leviers.append(levier)
            continue

        reduction_abs = abs(reductions[levier])
        levier_weights = weights.get(levier, {})
        cat_nodes: list[dict] = []

        for cat in range(1, 7):
            if (levier, cat) in exclusions:
                continue
            if selected_cibles is not None and (levier, cat) not in selected_cibles:
                continue
            poids = levier_weights.get(cat)
            if poids is None or pd.isna(poids) or poids == 0:
                continue

            taille = reduction_abs * float(poids)
            if taille == 0:
                continue

            note = int(notes.get((levier, cat), 0))
            categorie = CATEGORIES[cat]
            cat_nodes.append(
                {
                    "name": f"{levier_label_court(levier)}\n{categorie}",
               
                    "value": round(taille, 2),
                    "itemStyle": {"color": NOTE_COLORS.get(note, NOTE_COLORS[0])},
                    "levierName": levier,
                    "categorieName": categorie,
                    "categorieId": cat,
                    "noteLevel": NOTE_LABELS.get(note, NOTE_LABELS[0]),
                }
            )

        if cat_nodes:
            children.append({"name": levier, "children": cat_nodes})

    return children, excluded_leviers


def build_priorisation_cases(
    leviers: list[str],
    reductions: dict[str, float],
    notes: dict[tuple[str, int], int],
    weights: dict[str, dict[int, float]],
    exclusions: set[tuple[str, int]] | None = None,
    selected_cibles: set[tuple[str, int]] | None = None,
) -> list[dict]:
    """Cases levier × catégorie avec note et potentiel de réduction (ktCO₂e)."""
    cases: list[dict] = []
    exclusions = exclusions or set()
    for levier in sorted(leviers):
        if levier not in reductions:
            continue
        reduction_abs = abs(reductions[levier])
        levier_weights = weights.get(levier, {})
        for cat in range(1, 7):
            if (levier, cat) in exclusions:
                continue
            if selected_cibles is not None and (levier, cat) not in selected_cibles:
                continue
            poids = levier_weights.get(cat)
            if poids is None or pd.isna(poids) or poids == 0:
                continue
            potentiel = reduction_abs * float(poids)
            if potentiel == 0:
                continue
            note = int(notes.get((levier, cat), 0))
            categorie = CATEGORIES[cat]
            cases.append(
                {
                    "levier": levier,
                    "categorie": categorie,
                    "categorie_id": cat,
                    "note": note,
                    "potentiel": round(potentiel, 2),
                    "label": f"{levier_label_court(levier)} · {categorie}",
                }
            )
    return cases


def build_mobilisation_bar_options(
    cases: list[dict], selected_note: int
) -> dict | None:
    """Barres horizontales ECharts, tri décroissant (plus fort enjeu en haut)."""
    filtered = [c for c in cases if c["note"] == selected_note]
    if not filtered:
        return None

    filtered.sort(key=lambda c: c["potentiel"], reverse=True)
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
                        "value": c["potentiel"],
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

VUE_ENSEMBLE_CHART_HEIGHT = 1000
NOTES_ENJEU_BAS = {0, 1}

TREEMAP_HEIGHT = 800


def case_sort_value(case: dict) -> float:
    """Valeur de tri : négative pour non/partiellement mobilisé, positive sinon."""
    potentiel = case["potentiel"]
    if case["note"] in NOTES_ENJEU_BAS:
        return -potentiel
    return potentiel


def case_chart_value(case: dict) -> float:
    """Valeur affichée dans le graphique (signée pour les barres orange/jaune)."""
    if case["note"] in NOTES_ENJEU_BAS:
        return -case["potentiel"]
    return case["potentiel"]


def build_vue_ensemble_bar_options(cases: list[dict]) -> dict | None:
    """Barres verticales, couleur par note, tri par potentiel signé décroissant."""
    if not cases:
        return None

    ordered = sorted(cases, key=case_sort_value, reverse=True)
    series_data = []
    for c in ordered:
        chart_val = case_chart_value(c)
        series_data.append(
            {
                "value": chart_val,
                "levierFull": c["levier"],
                "categorie": c["categorie"],
                "noteLevel": NOTE_LABELS.get(c["note"], NOTE_LABELS[0]),
                "itemStyle": {
                    "color": NOTE_COLORS.get(c["note"], NOTE_COLORS[0]),
                    "borderRadius": (
                        [6, 6, 0, 0] if chart_val >= 0 else [0, 0, 6, 6]
                    ),
                    "shadowColor": "rgba(0,0,0,0.06)",
                    "shadowBlur": 6,
                },
            }
        )

    return {
        "backgroundColor": "transparent",
        "animationDuration": 600,
        "animationEasing": "cubicOut",
        "grid": {
            "left": 48,
            "right": 24,
            "top": 40,
            "bottom": 32,
            "containLabel": False,
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "shadow", "shadowStyle": {"opacity": 0.08}},
            "formatter": JsCode(
                """
                function(params) {
                    var p = params && params[0];
                    if (!p || !p.data) return '';
                    var d = p.data;
                    var val = Math.abs(Number(p.value)).toFixed(1);
                    return (d.levierFull || '') + '<br/>'
                        + (d.categorie || '') + '<br/>'
                        + (d.noteLevel || '') + '<br/>'
                        + '<b>' + val + ' ktCO₂e</b>';
                }
                """
            ),
        },
        "xAxis": {
            "type": "category",
            "data": [""] * len(ordered),
            "axisLine": {"show": False},
            "axisTick": {"show": False},
            "axisLabel": {"show": False},
        },
        "yAxis": {
            "type": "value",
            "name": "ktCO₂e",
            "nameTextStyle": {"color": "#888", "fontSize": 11},
            "axisLine": {"show": False},
            "axisTick": {"show": False},
            "axisLabel": {"color": "#888", "fontSize": 11},
            "splitLine": {"lineStyle": {"color": "#ebebeb", "type": "dashed"}},
        },
        "series": [
            {
                "type": "bar",
                "data": series_data,
                "barMaxWidth": 36,
                "emphasis": {
                    "itemStyle": {
                        "shadowColor": "rgba(0,0,0,0.12)",
                        "shadowBlur": 10,
                    }
                },
                "label": {"show": False},
            }
        ],
    }

TREEMAP_CLICK_EVENTS = {
    "click": """
    function(params) {
        var d = params.data;
        if (!d || !d.levierName) return null;
        return {
            levier: d.levierName,
            categorie: d.categorieName,
            categorieId: d.categorieId,
        };
    }
    """,
}


def extract_chart_event(component_value) -> dict | None:
    """Extrait l'événement JS depuis la valeur retournée par st_echarts v0.6+."""
    if component_value is None:
        return None
    if hasattr(component_value, "chart_event"):
        event = component_value.chart_event
        return event if isinstance(event, dict) else None
    if isinstance(component_value, dict):
        if "chart_event" in component_value:
            event = component_value["chart_event"]
            return event if isinstance(event, dict) else None
        if component_value.get("levier"):
            return component_value
    return None


def prepare_treemap_display_data(
    treemap_children: list[dict], *, show_labels: bool
) -> list[dict]:
    """Prépare les données affichées : libellés vides si masqués."""
    if show_labels:
        return treemap_children

    return [
        {
            **levier_node,
            "children": [{**leaf, "name": ""} for leaf in levier_node["children"]],
        }
        for levier_node in treemap_children
    ]


def build_echarts_options(treemap_children: list[dict], *, show_labels: bool = True) -> dict:
    """Construit l'option ECharts pour la treemap à deux niveaux."""
    display_data = prepare_treemap_display_data(
        treemap_children, show_labels=show_labels
    )
    return {
        "backgroundColor": "transparent",
        "tooltip": {
            "formatter": JsCode(
                """
                function(params) {
                    var d = params.data;
                    if (!d || !d.levierName) return '';
                    var taille = Number(d.value).toFixed(1);
                    return d.levierName + '<br/>'
                        + d.categorieName + '<br/>'
                        + 'Note : ' + d.noteLevel + '<br/>'
                        + 'Taille : ' + taille + ' ktCO2';
                }
                """
            ),
        },
        "series": [
            {
                "type": "treemap",
                "roam": False,
                "nodeClick": False,
                "left": 0,
                "top": 0,
                "right": 0,
                "bottom": 0,
                "breadcrumb": {"show": False},
                "levels": [
                    {
                        "itemStyle": {
                            "borderColor": "#444",
                            "borderWidth": 1,
                            "gapWidth": 1,
                        },
                        "upperLabel": {"show": False},
                        "label": {"show": False},
                    },
                    {
                        "itemStyle": {
                            "borderColor": "#fff",
                            "borderWidth": 1,
                            "gapWidth": 1,
                        },
                        "label": {
                            "show": True,
                            "fontSize": 10,
                            "lineHeight": 14,
                            "color": "#333",
                            "overflow": "break",
                            "width": 80,
                        },
                        "upperLabel": {"show": False},
                    },
                ],
                "data": display_data,
            }
        ],
    }


def render_note_color_legend() -> None:
    """Légende des couleurs par état de mobilisation (treemap, Impact Chart)."""
    items = "".join(
        f'<span style="display:inline-flex;align-items:center;margin-right:1.5rem;">'
        f'<span style="display:inline-block;width:14px;height:14px;border-radius:3px;'
        f"background:{NOTE_COLORS[note]};border:1px solid rgba(0,0,0,0.12);"
        f'margin-right:0.45rem;flex-shrink:0;"></span>'
        f'<span style="font-size:0.875rem;color:#333;">{NOTE_LABELS[note]}</span>'
        f"</span>"
        for note in range(4)
    )
    st.markdown(
        f'<div style="display:flex;flex-wrap:wrap;align-items:center;'
        f'margin-bottom:0.75rem;">{items}</div>',
        unsafe_allow_html=True,
    )


# ==========================
# Interface
# ==========================

st.title("🧭 Diagnostic")

st.markdown(
    "Après le **périmètre d'action**, cette étape permet de **visualiser l'état "
    "de mobilisation** des leviers de votre collectivité. Toutes les actions "
    "retenues ont été **classées par cible** (levier × type d'action). "
    "La vue d'ensemble met en évidence les **priorités d'action** : une grande "
    "case indique un **fort enjeu peu mobilisé**."
)

df_collectivites = load_collectivites_priorisees()

if df_collectivites.empty:
    st.warning("Aucune collectivité avec des données de priorisation disponible.")
    st.stop()

nom_par_id = df_collectivites.set_index("collectivite_id")["nom"].to_dict()
collectivite_ids = df_collectivites["collectivite_id"].tolist()
df_fiches_action = load_fiches_action(tuple(collectivite_ids))

selected_id = st.selectbox(
    "Collectivité",
    options=collectivite_ids,
    format_func=lambda cid: nom_par_id[cid],
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

tabs = st.tabs(["Impact Map", "Impact Chart", "Détail mobilisation"])

with tabs[0]:

    show_labels = st.toggle("Libellés", value=False)

    for levier in excluded_leviers:
        st.warning(
            f"Le levier **{levier}** est présent dans la priorisation "
            f"mais sans réduction CO₂ — il est exclu de la treemap."
        )

    if not treemap_children:
        st.info("Aucune case à afficher pour cette collectivité.")
    else:
        if st.session_state.get("treemap_collectivite_id") != selected_id:
            st.session_state.pop("treemap_selection", None)
        st.session_state["treemap_collectivite_id"] = selected_id

        treemap_selection = st.session_state.get("treemap_selection")
        if treemap_selection and treemap_selection.get("levier") not in selected_leviers:
            st.session_state.pop("treemap_selection", None)

        detail_slot = st.empty()

        # TODO: zoom par levier

        render_note_color_legend()
        options = build_echarts_options(treemap_children, show_labels=show_labels)
        click = st_echarts(
            options=options,
            events=TREEMAP_CLICK_EVENTS,
            height=f"{TREEMAP_HEIGHT}px",
            key=f"treemap_{selected_id}_{threshold_pct}_labels_{int(show_labels)}",
        )

        click_event = extract_chart_event(click)
        if click_event and click_event.get("levier"):
            st.session_state["treemap_selection"] = click_event

        selection = st.session_state.get("treemap_selection")
        with detail_slot.container():
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


with tabs[2]:
    note_options = [NOTE_LABELS[i] for i in range(4)]
    selected_note_label = st.segmented_control(
        "État de mobilisation",
        options=note_options,
        default=note_options[0],
        key=f"mobilisation_note_{selected_id}",
    )
    selected_note = next(
        note for note, label in NOTE_LABELS.items() if label == selected_note_label
    )
    note_badge_color = NOTE_BADGE_COLORS.get(selected_note, "orange")

    st.caption(
        f"Leviers **{selected_note_label.lower()}**, "
        "classés par potentiel de réduction décroissant."
    )

    bar_options = build_mobilisation_bar_options(
        priorisation_cases, selected_note
    )
    if bar_options is None:
        st.info(
            f"Aucun levier × catégorie en état « {selected_note_label} » "
            "pour cette collectivité."
        )
    else:
        n_bars = len([c for c in priorisation_cases if c["note"] == selected_note])
        chart_height = max(
            MOBILISATION_BAR_MIN_HEIGHT,
            n_bars * MOBILISATION_BAR_ROW_PX + 80,
        )
        st.markdown(
            f"### :{note_badge_color}-badge[{selected_note_label}]"
        )
        st_echarts(
            options=bar_options,
            height=f"{chart_height}px",
            key=f"mobilisation_bar_{selected_id}_{selected_note}_{threshold_pct}",
        )

with tabs[1]:
    vue_options = build_vue_ensemble_bar_options(priorisation_cases)
    if vue_options is None:
        st.info("Aucune case à afficher pour ce seuil.")
    else:
        render_note_color_legend()
        st_echarts(
            options=vue_options,
            height=f"{VUE_ENSEMBLE_CHART_HEIGHT}px",
            key=f"vue_ensemble_{selected_id}_{threshold_pct}",
        )
