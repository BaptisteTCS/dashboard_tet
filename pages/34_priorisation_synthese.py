import streamlit as st

st.set_page_config(
    page_title="Priorisation — synthèse",
    page_icon="📋",
    layout="wide",
)

import pandas as pd
from sqlalchemy import text
from streamlit_echarts import JsCode, st_echarts

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

COLOR_green_3 = {
    0: "#E2E5E9",
    1: "#f5ebe0",
    2: "#5DCF69",
    3: "#389D49",
}

NOTE_COLORS = COLOR_green_3

# Orange foncé : cible peu mobilisée (note 0/1) avec ≥1 action retenue
COLOR_ACTION_RETENUE = "#D84315"

NOTES_ENJEU_BAS = {0, 1}

VUE_ENSEMBLE_THRESHOLDS = [50, 60, 70, 80, 90, 100]

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

TREEMAP_HEIGHT = 800
VUE_ENSEMBLE_CHART_HEIGHT = 750


def levier_label_court(levier: str) -> str:
    return LEVIER_LABELS.get(levier, levier)


def origine_depuis_fiche(
    collectivite_id_fiche: int,
    nom_par_id: dict[int, str],
) -> str:
    return nom_par_id.get(collectivite_id_fiche, f"Collectivité #{collectivite_id_fiche}")


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


def build_category_weights(df_poids: pd.DataFrame) -> dict[str, dict[int, float]]:
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


def cibles_avec_actions(df_actions: pd.DataFrame) -> set[tuple[str, int]]:
    return {
        (row["levier"], int(row["categorie"]))
        for _, row in df_actions.iterrows()
    }


def actions_by_cible(
    df_actions: pd.DataFrame,
) -> dict[tuple[str, int], list[int]]:
    result: dict[tuple[str, int], list[int]] = {}
    for _, row in df_actions.iterrows():
        key = (row["levier"], int(row["categorie"]))
        result.setdefault(key, []).append(int(row["fiche_action_id"]))
    return result


def select_leviers_pareto(
    leviers: list[str],
    reductions: dict[str, float],
    threshold_pct: int,
) -> set[str]:
    """Plus petit ensemble de leviers couvrant au moins threshold_pct % de la réduction totale."""
    contributions = [
        (levier, abs(float(reductions[levier])))
        for levier in leviers
        if levier in reductions
    ]
    if not contributions:
        return set()

    total = sum(value for _, value in contributions)
    if total == 0:
        return set()

    contributions.sort(key=lambda item: item[1], reverse=True)
    target = total * threshold_pct / 100
    selected: list[str] = []
    cumul = 0.0
    for levier, value in contributions:
        selected.append(levier)
        cumul += value
        if cumul >= target:
            break
    return set(selected)


# ==========================
# (b) Logique de coloration orange + treemap
# ==========================


def case_color(
    levier: str,
    cat: int,
    note: int,
    cibles_actions: set[tuple[str, int]],
) -> str:
    """
    Palette mobilisation par défaut ; orange foncé si la cible (note 0/1)
    comporte au moins une action retenue dans priorisation_action.
    L'orange ne remplace que du gris (notes 0/1), jamais le vert (notes 2/3).
    """
    if note in NOTES_ENJEU_BAS and (levier, cat) in cibles_actions:
        return COLOR_ACTION_RETENUE
    return NOTE_COLORS.get(note, NOTE_COLORS[0])


def build_treemap_data(
    leviers: list[str],
    reductions: dict[str, float],
    notes: dict[tuple[str, int], int],
    weights: dict[str, dict[int, float]],
    exclusions: set[tuple[str, int]],
    cibles_actions: set[tuple[str, int]],
) -> tuple[list[dict], list[str]]:
    """Treemap : taille = enjeu relatif, couleur = mobilisation ou action retenue."""
    excluded_leviers: list[str] = []
    children: list[dict] = []

    for levier in sorted(leviers):
        if levier not in reductions:
            excluded_leviers.append(levier)
            continue

        reduction_abs = abs(float(reductions[levier]))
        levier_weights = weights.get(levier, {})
        cat_nodes: list[dict] = []

        for cat in range(1, 7):
            if (levier, cat) in exclusions:
                continue
            poids = levier_weights.get(cat)
            if poids is None or pd.isna(poids) or poids == 0:
                continue

            taille = reduction_abs * float(poids)
            if taille == 0:
                continue

            note = int(notes.get((levier, cat), 0))
            categorie = CATEGORIES[cat]
            has_action = (levier, cat) in cibles_actions and note in NOTES_ENJEU_BAS
            cat_nodes.append(
                {
                    "name": f"{levier_label_court(levier)}\n{categorie}",
                    "value": round(taille, 2),
                    "itemStyle": {
                        "color": case_color(levier, cat, note, cibles_actions)
                    },
                    "levierName": levier,
                    "categorieName": categorie,
                    "categorieId": cat,
                    "noteLevel": NOTE_LABELS.get(note, NOTE_LABELS[0]),
                    "actionRetenue": has_action,
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
    exclusions: set[tuple[str, int]],
    cibles_actions: set[tuple[str, int]],
) -> list[dict]:
    cases: list[dict] = []
    for levier in sorted(leviers):
        if levier not in reductions:
            continue
        reduction_abs = abs(float(reductions[levier]))
        levier_weights = weights.get(levier, {})
        for cat in range(1, 7):
            if (levier, cat) in exclusions:
                continue
            poids = levier_weights.get(cat)
            if poids is None or pd.isna(poids) or poids == 0:
                continue
            enjeu = reduction_abs * float(poids)
            if enjeu == 0:
                continue
            note = int(notes.get((levier, cat), 0))
            cases.append(
                {
                    "levier": levier,
                    "categorie": CATEGORIES[cat],
                    "categorie_id": cat,
                    "note": note,
                    "enjeu": round(enjeu, 2),
                    "color": case_color(levier, cat, note, cibles_actions),
                    "label": f"{levier_label_court(levier)} · {CATEGORIES[cat]}",
                    "action_retenue": (levier, cat) in cibles_actions
                    and note in NOTES_ENJEU_BAS,
                }
            )
    return cases


def case_sort_value(case: dict) -> float:
    """Tri décroissant : vert + orange (positif) à gauche, gris/beige sans action (négatif) à droite."""
    if case["note"] in NOTES_ENJEU_BAS and not case.get("action_retenue"):
        return -case["enjeu"]
    return case["enjeu"]


def case_chart_value(case: dict) -> float:
    """Orange (action retenue) compté positif comme le vert ; seules les notes 0/1 sans action en négatif."""
    if case["note"] in NOTES_ENJEU_BAS and not case.get("action_retenue"):
        return -case["enjeu"]
    return case["enjeu"]


def build_vue_ensemble_bar_options(cases: list[dict]) -> dict | None:
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
                "actionRetenue": c["action_retenue"],
                "itemStyle": {
                    "color": c["color"],
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
                    var lines = (d.levierFull || '') + '<br/>'
                        + (d.categorie || '') + '<br/>'
                        + (d.noteLevel || '') + '<br/>'
                        + '<b>' + val + ' ktCO₂e</b>';
                    if (d.actionRetenue) {
                        lines += '<br/><b>Action(s) retenue(s)</b>';
                    }
                    return lines;
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


def prepare_treemap_display_data(
    treemap_children: list[dict], *, show_labels: bool
) -> list[dict]:
    if show_labels:
        return treemap_children
    return [
        {
            **levier_node,
            "children": [{**leaf, "name": ""} for leaf in levier_node["children"]],
        }
        for levier_node in treemap_children
    ]


def build_echarts_options(
    treemap_children: list[dict], *, show_labels: bool = True
) -> dict:
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
                    var lines = d.levierName + '<br/>'
                        + d.categorieName + '<br/>'
                        + 'Note : ' + d.noteLevel + '<br/>'
                        + 'Taille : ' + taille + ' ktCO2';
                    if (d.actionRetenue) {
                        lines += '<br/><b>Action(s) retenue(s)</b>';
                    }
                    return lines;
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
    """Légende mobilisation (page 30) + actions retenues."""
    items = "".join(
        f'<span style="display:inline-flex;align-items:center;margin-right:1.5rem;">'
        f'<span style="display:inline-block;width:14px;height:14px;border-radius:3px;'
        f"background:{NOTE_COLORS[note]};border:1px solid rgba(0,0,0,0.12);"
        f'margin-right:0.45rem;flex-shrink:0;"></span>'
        f'<span style="font-size:0.875rem;color:#333;">{NOTE_LABELS[note]}</span>'
        f"</span>"
        for note in range(4)
    )
    items += (
        f'<span style="display:inline-flex;align-items:center;margin-right:1.5rem;">'
        f'<span style="display:inline-block;width:14px;height:14px;border-radius:3px;'
        f"background:{COLOR_ACTION_RETENUE};border:1px solid rgba(0,0,0,0.12);"
        f'margin-right:0.45rem;flex-shrink:0;"></span>'
        f'<span style="font-size:0.875rem;color:#333;">Action(s) retenue(s)</span>'
        f"</span>"
    )
    st.markdown(
        f'<div style="display:flex;flex-wrap:wrap;align-items:center;'
        f'margin-bottom:0.75rem;">{items}</div>',
        unsafe_allow_html=True,
    )


def build_detail_par_cible(
    cibles_actions: set[tuple[str, int]],
    actions_map: dict[tuple[str, int], list[int]],
    df_fiches: pd.DataFrame,
    notes: dict[tuple[str, int], int],
    nom_par_id: dict[int, str],
) -> list[dict]:
    """Cibles orange uniquement : note 0/1 avec au moins une action retenue."""
    detail: list[dict] = []
    fiches_by_id = df_fiches.set_index("id")

    for levier, cat in sorted(cibles_actions):
        if notes.get((levier, cat), 0) not in NOTES_ENJEU_BAS:
            continue
        fiche_ids = actions_map.get((levier, cat), [])
        if not fiche_ids:
            continue

        actions = []
        for fid in fiche_ids:
            if fid not in fiches_by_id.index:
                actions.append(
                    {"intitule": f"Fiche #{fid}", "origine": "—"}
                )
                continue
            row = fiches_by_id.loc[fid]
            ct_id = int(row["collectivite_id"])
            actions.append(
                {
                    "intitule": row.get("titre") or f"Fiche #{fid}",
                    "origine": origine_depuis_fiche(ct_id, nom_par_id),
                }
            )

        detail.append(
            {
                "levier": levier,
                "categorie": CATEGORIES[cat],
                "actions": actions,
            }
        )

    return detail


# ==========================
# Interface
# ==========================

st.title("🏆 Synthèse opérationnelle")

st.markdown(
    "Cette synthèse présente les **actions retenues** et **où elles s'inscrivent** "
    "sur la cartographie de mobilisation de votre collectivité. C'est un **support "
    "pour la discussion avec les élus** : la taille des cases traduit l'enjeu relatif, "
    "sans valeur chiffrée affichée."
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
    key="synthese_select_collectivite",
)

st.markdown("---")

df_priorisation = load_priorisation(collectivite_id)
df_reductions = load_reductions(collectivite_id)
df_poids = load_poids_categories()
df_actions = load_actions_choisies(collectivite_id)
fiche_ids = tuple(
    int(fid) for fid in df_actions["fiche_action_id"].unique().tolist()
) if not df_actions.empty else ()
df_fiches = load_fiches_by_ids(fiche_ids)

notes = {
    (row["levier"], int(row["categorie"])): int(row["note"])
    for _, row in df_priorisation.iterrows()
}
reductions = df_reductions.set_index("levier")["reduction"].to_dict()
exclusions = hors_competence_pairs(load_hors_competence(collectivite_id))
weights = build_category_weights(df_poids)
cibles_actions = cibles_avec_actions(df_actions)
actions_map = actions_by_cible(df_actions)

leviers = sorted(reductions.keys())

with st.expander(
    "Réduire le nombre de cibles en selectionnant uniquement les plus importantes"
):
    threshold_pct = st.select_slider(
        "Part de réduction d'émissions de GES couvertes par les leviers.",
        options=VUE_ENSEMBLE_THRESHOLDS,
        value=100,
        key=f"synthese_vue_ensemble_threshold_{collectivite_id}",
        help=(
            "Conserve le minimum de leviers les plus contributeurs "
            "dont la réduction cumulée atteint ce seuil. Ex: 80% = les 80% des leviers "
            "les plus contributeurs couvrent au moins 80% de la réduction d'émissions de GES."
        ),
    )
    selected_leviers = select_leviers_pareto(leviers, reductions, threshold_pct)
    n_leviers_total = len({levier for levier in leviers if levier in reductions})
    st.caption(
        f"**{len(selected_leviers)}** leviers retenus sur {n_leviers_total} "
        f"(seuil Pareto {threshold_pct} %)."
    )

leviers_pareto = [levier for levier in leviers if levier in selected_leviers]

treemap_children, excluded_leviers = build_treemap_data(
    leviers_pareto, reductions, notes, weights, exclusions, cibles_actions
)
priorisation_cases = build_priorisation_cases(
    leviers_pareto, reductions, notes, weights, exclusions, cibles_actions
)

tabs = st.tabs(["Impact Map", "Impact Chart"])

with tabs[0]:
    show_labels = st.toggle("Libellés", value=True, key="synthese_show_labels")

    for levier in excluded_leviers:
        st.warning(
            f"Le levier **{levier}** est présent dans la priorisation "
            f"mais sans réduction CO₂ — il est exclu de la treemap."
        )

    if not treemap_children:
        st.info("Aucune case à afficher pour cette collectivité.")
    else:
        render_note_color_legend()
        options = build_echarts_options(treemap_children, show_labels=show_labels)
        st_echarts(
            options=options,
            height=f"{TREEMAP_HEIGHT}px",
            key=f"synthese_treemap_{collectivite_id}_{threshold_pct}_labels_{int(show_labels)}",
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
            key=f"synthese_vue_ensemble_{collectivite_id}_{threshold_pct}",
        )

st.markdown("---")
st.subheader("Actions retenues par cible")

detail = build_detail_par_cible(
    cibles_actions, actions_map, df_fiches, notes, nom_par_id
)

if not detail:
    st.info(
        "Aucune action retenue sur une cible peu mobilisée. "
        "Complétez l'étape « Choix des actions » pour alimenter cette synthèse."
    )
else:
    for bloc in detail:
        st.markdown(f"**{bloc['levier']}** · {bloc['categorie']}")
        for action in bloc["actions"]:
            st.markdown(f"- {action['intitule']} — *{action['origine']}*")
        st.markdown("")
