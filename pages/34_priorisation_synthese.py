import streamlit as st

st.set_page_config(
    page_title="Priorisation — synthèse",
    page_icon="🏆",
    layout="wide",
)

import pandas as pd
from sqlalchemy import text

from components.priorisation_echarts_export import priorisation_echarts_export
from utils.db import get_engine, get_engine_prod
from utils.priorisation_impact_charts import (
    CATEGORIES,
    NOTES_ENJEU_BAS,
    TREEMAP_HEIGHT,
    VUE_ENSEMBLE_CHART_HEIGHT_SYNTHESE,
    build_bar_export_options,
    build_priorisation_cases,
    build_treemap_data,
    build_treemap_export_options,
    render_impact_chart,
    render_impact_map,
)
from utils.priorisation_faisabilite import build_top_leviers_faisabilite_pdf
from utils.priorisation_pdf import (
    build_compte_rendu_pdf,
    build_cibles_par_levier,
    sanitize_filename,
)
from utils.priorisation_navigation import render_etape_4_retour
from utils.priorisation_pareto import (
    enjeu_cible,
    list_cibles_enjeu,
    render_seuil_impact_cibles_expander,
)

QUANTIGES_URL = (
    "https://librairie.ademe.fr/changement-climatique/"
    "4827-methode-quantiges-9791029718236.html"
)


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
def load_collectivites_avec_actions() -> pd.DataFrame:
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql_query(
            text("""
                SELECT DISTINCT c.collectivite_id, c.nom
                FROM collectivite c
                INNER JOIN priorisation_action pa ON pa.collectivite_id = c.collectivite_id
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


def potentiel_priorise_kt(
    df_actions: pd.DataFrame,
    reductions: dict[str, float],
    weights: dict[str, dict[int, float]],
) -> float:
    """Somme des enjeux des couples (levier, catégorie) présents dans priorisation_action."""
    if df_actions.empty:
        return 0.0
    pairs = df_actions[["levier", "categorie"]].drop_duplicates()
    return sum(
        enjeu_cible(row["levier"], int(row["categorie"]), reductions, weights)
        for _, row in pairs.iterrows()
    )


def potentiel_total_plan_kt(
    leviers: list[str],
    reductions: dict[str, float],
    weights: dict[str, dict[int, float]],
    exclusions: set[tuple[str, int]],
) -> float:
    """T1 : potentiel cumulé de toutes les cibles du plan (avant priorisation des actions)."""
    return sum(
        value
        for _, value in list_cibles_enjeu(leviers, reductions, weights, exclusions)
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

st.markdown("""
Cette synthèse présente les actions sélectionnées et identifies dans quelle leviers elle se trouve. Il s’agit d’un support pour la discussion avec les élus. Pour rappel, la taille des cases traduit l'enjeu relatif, sans valeur chiffrée affichée.
"""
)

df_collectivites = load_collectivites_avec_actions()
if df_collectivites.empty:
    st.warning(
        "Aucune collectivité avec des actions enregistrées. "
        "Complétez d'abord l'étape « Choix des actions »."
    )
    st.stop()

nom_par_id_select = df_collectivites.set_index("collectivite_id")["nom"].to_dict()
collectivite_ids = df_collectivites["collectivite_id"].tolist()
nom_par_id = (
    load_collectivites_priorisees()
    .set_index("collectivite_id")["nom"]
    .to_dict()
)

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
    format_func=lambda cid: nom_par_id_select[cid],
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

n_cibles_priorisees = (
    len(df_actions[["levier", "categorie"]].drop_duplicates())
    if not df_actions.empty
    else 0
)
n_actions_retenues = (
    int(df_actions["fiche_action_id"].nunique()) if not df_actions.empty else 0
)
potentiel_kt = potentiel_priorise_kt(df_actions, reductions, weights)
t1_avant_priorisation = potentiel_total_plan_kt(
    leviers, reductions, weights, exclusions
)
x_potentiel_mobilise = potentiel_kt
t2_apres_priorisation = t1_avant_priorisation + x_potentiel_mobilise
pct_potentiel_supplementaire = (
    (x_potentiel_mobilise / t1_avant_priorisation * 100)
    if t1_avant_priorisation > 0
    else 0.0
)

col_cibles, col_actions = st.columns(2)
with col_cibles:
    st.metric("Nombre de cibles priorisées", n_cibles_priorisees)
with col_actions:
    st.metric("Nombre d'actions sauvergardées", n_actions_retenues)

_potentiel_sk = f"synthese_potentiel_etape_{collectivite_id}"
etape_potentiel = st.session_state.get(_potentiel_sk, 0)

if etape_potentiel == 0:
    if st.button(
        "Afficher le potentiel CO₂ mobilisé",
        key=f"synthese_btn_potentiel_intro_{collectivite_id}",
    ):
        st.session_state[_potentiel_sk] = 1
        st.rerun()
elif etape_potentiel == 1:
    lib_actions = (
        "action sauvegardée" if n_actions_retenues == 1 else "actions sauvegardées"
    )
    lib_cibles = (
        "cible priorisée" if n_cibles_priorisees == 1 else "cibles priorisées"
    )
    st.info(
        f"Les **{n_actions_retenues}** {lib_actions} agissent sur "
        f"**{n_cibles_priorisees}** {lib_cibles}. Pour chacune de ces cibles, "
        f"l'outil fournit une estimation du potentiel de réduction de GES "
        f"(ktCO₂e).\n\n"
        f"En les agrégeant, on obtient un **ordre de grandeur** du potentiel "
        f"de réduction sur lequel portent vos actions. Ce chiffre n'est pas une "
        f"vérité absolue : c'est une approximation **plutôt fidèle**, utile pour "
        f"donner une représentation concrète de l'impact attendu et nourrir la "
        f"discussion avec les élus."
    )
    if st.button(
        "J'ai compris. Voir l'ordre de grandeur estimé",
        key=f"synthese_btn_potentiel_confirm_{collectivite_id}",
    ):
        st.session_state[_potentiel_sk] = 2
        st.rerun()
else:
    st.metric(
        "Estimation du potentiel global priorisé (ktCO₂)",
        f"{int(potentiel_kt)}",
    )
    if t1_avant_priorisation > 0:
        st.markdown(
            f"**{int(x_potentiel_mobilise)}** ktCO₂e de réduction représentent "
            f"**{int(pct_potentiel_supplementaire)} %** de réduction potentielle "
            f"supplémentaire par rapport à votre plan original. "
            f"*({int(t2_apres_priorisation)} ktCO₂e après priorisation vs "
            f"{int(t1_avant_priorisation)} ktCO₂e avant)*"
        )
    else:
        st.caption(
            "Potentiel du plan original indisponible (aucune cible avec enjeu calculable)."
        )
    st.link_button(
        "Aller plus loin dans le calcul de réduction des émissions de GES "
        "avec l'outil QuantiGES",
        QUANTIGES_URL,
        key=f"synthese_btn_quantiges_{collectivite_id}",
        type="primary",
    )

threshold_pct, selected_cibles = render_seuil_impact_cibles_expander(
    leviers,
    reductions,
    weights,
    exclusions,
    key_prefix=f"synthese_vue_ensemble_{collectivite_id}",
)

treemap_children, excluded_leviers = build_treemap_data(
    leviers,
    reductions,
    notes,
    weights,
    exclusions,
    cibles_actions=cibles_actions,
    selected_cibles=selected_cibles,
)
diag_treemap_children, _ = build_treemap_data(
    leviers,
    reductions,
    notes,
    weights,
    exclusions,
    selected_cibles=selected_cibles,
)
priorisation_cases = build_priorisation_cases(
    leviers,
    reductions,
    notes,
    weights,
    exclusions,
    cibles_actions=cibles_actions,
    selected_cibles=selected_cibles,
)
diag_priorisation_cases = build_priorisation_cases(
    leviers,
    reductions,
    notes,
    weights,
    exclusions,
    selected_cibles=selected_cibles,
)
df_faisabilite = load_faisabilite(collectivite_id)
faisabilites = {
    (row["levier"], int(row["categorie"])): int(row["faisabilite"])
    for _, row in df_faisabilite.iterrows()
}

tabs = st.tabs(["Impact Map", "Impact Chart"])

with tabs[0]:
    render_impact_map(
        treemap_children,
        excluded_leviers,
        chart_key_prefix=f"synthese_treemap_{collectivite_id}",
        threshold_pct=threshold_pct,
        labels_toggle_key="synthese_show_labels",
        show_actions_retenues=True,
    )

with tabs[1]:
    render_impact_chart(
        priorisation_cases,
        chart_key=f"synthese_vue_ensemble_{collectivite_id}_{threshold_pct}",
        show_actions_retenues=True,
        height=VUE_ENSEMBLE_CHART_HEIGHT_SYNTHESE,
    )

_export_pdf_key = f"synthese_export_pdf_{collectivite_id}"
_pdf_pending_key = f"synthese_pdf_pending_{collectivite_id}"
_pdf_attempt_key = f"synthese_pdf_attempt_{collectivite_id}"
st.markdown(
    f"""
    <style>
    div.st-key-{_export_pdf_key} button {{
        background-color: #D84315 !important;
        border-color: #D84315 !important;
        color: #ffffff !important;
    }}
    div.st-key-{_export_pdf_key} button:hover {{
        background-color: #b71c1c !important;
        border-color: #b71c1c !important;
        color: #ffffff !important;
    }}
    div.st-key-{_export_pdf_key} button:focus {{
        background-color: #c62828 !important;
        border-color: #c62828 !important;
        box-shadow: 0 0 0 0.2rem rgba(198, 40, 40, 0.35) !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)
if st.button(
    "Exporte le compte rendu PDF",
    type="primary",
    key=_export_pdf_key,
):
    st.session_state[_pdf_pending_key] = True
    st.session_state[_pdf_attempt_key] = (
        st.session_state.get(_pdf_attempt_key, 0) + 1
    )
    st.rerun()

if st.session_state.get(_pdf_pending_key):
    has_chart_data = bool(diag_priorisation_cases or priorisation_cases)
    if not has_chart_data:
        st.warning("Aucune case à exporter pour cette collectivité.")
        del st.session_state[_pdf_pending_key]
    else:
        pdf_show_labels = True
        export_charts: list[dict] = []

        diag_bar = build_bar_export_options(diag_priorisation_cases)
        if diag_bar:
            export_charts.append(
                {"type": "bar", "option": diag_bar, "height": TREEMAP_HEIGHT}
            )
        diag_treemap = build_treemap_export_options(
            diag_treemap_children, show_labels=pdf_show_labels
        )
        if diag_treemap_children:
            export_charts.append(
                {
                    "type": "treemap",
                    "option": diag_treemap,
                    "height": TREEMAP_HEIGHT,
                }
            )

        synth_treemap = build_treemap_export_options(
            treemap_children, show_labels=pdf_show_labels
        )
        if treemap_children:
            export_charts.append(
                {
                    "type": "treemap",
                    "option": synth_treemap,
                    "height": TREEMAP_HEIGHT,
                }
            )
        synth_bar = build_bar_export_options(priorisation_cases)
        if synth_bar:
            export_charts.append(
                {
                    "type": "bar",
                    "option": synth_bar,
                    "height": VUE_ENSEMBLE_CHART_HEIGHT_SYNTHESE,
                }
            )

        with st.spinner("Génération du PDF en cours…"):
            capture_result = priorisation_echarts_export(
                charts=export_charts,
                key=(
                    f"synthese_echarts_export_{collectivite_id}_"
                    f"{threshold_pct}_{st.session_state.get(_pdf_attempt_key, 0)}"
                ),
            )

        pngs = (capture_result or {}).get("pngs") or []
        png_iter = iter(pngs)
        diagnostic_bar_png = next(png_iter, None) if diag_bar else None
        diagnostic_treemap_png = (
            next(png_iter, None) if diag_treemap_children else None
        )
        synthese_treemap_png = next(png_iter, None) if treemap_children else None
        synthese_bar_png = next(png_iter, None) if synth_bar else None

        expected_count = sum(
            bool(x)
            for x in (
                diag_bar,
                diag_treemap_children,
                treemap_children,
                synth_bar,
            )
        )
        charts_ok = len(pngs) == expected_count and expected_count > 0

        if charts_ok:
            collectivite_nom = nom_par_id[collectivite_id]
            top_leviers_pdf = build_top_leviers_faisabilite_pdf(
                leviers,
                reductions,
                notes,
                exclusions,
                weights,
                faisabilites,
            )
            pdf_bytes = build_compte_rendu_pdf(
                collectivite_nom,
                diagnostic_bar_png=diagnostic_bar_png,
                diagnostic_treemap_png=diagnostic_treemap_png,
                top_leviers_faisabilite=top_leviers_pdf,
                n_cibles_priorisees=n_cibles_priorisees,
                n_actions_retenues=n_actions_retenues,
                cibles_par_levier=build_cibles_par_levier(df_actions),
                synthese_treemap_png=synthese_treemap_png,
                synthese_bar_png=synthese_bar_png,
                threshold_pct=threshold_pct,
            )
            filename = f"synthese_{sanitize_filename(collectivite_nom)}.pdf"
            del st.session_state[_pdf_pending_key]
            st.success("PDF généré.")
            st.download_button(
                "Télécharger le PDF",
                data=pdf_bytes,
                file_name=filename,
                mime="application/pdf",
                type="primary",
                key=(
                    f"synthese_pdf_download_{collectivite_id}_"
                    f"{st.session_state.get(_pdf_attempt_key, 0)}"
                ),
            )
        elif capture_result is None:
            st.info("Capture des graphiques en cours…")
        else:
            st.error("Échec de la capture des graphiques pour le PDF.")
            del st.session_state[_pdf_pending_key]

st.markdown("---")
st.subheader("Actions sauvegardées par cible")

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

st.markdown("---")
render_etape_4_retour(collectivite_id, key=f"nav_synth_retour_{collectivite_id}")
