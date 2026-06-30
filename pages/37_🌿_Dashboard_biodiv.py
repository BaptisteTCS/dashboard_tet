import streamlit as st

st.set_page_config(
    page_title="Dashboard Biodiv",
    page_icon="🌿",
    layout="wide",
)

import pandas as pd
from sqlalchemy import text
from streamlit_elements import elements, mui, nivo

from utils.db import get_engine_prod, read_table
from utils.retro_charts import THEME_NIVO

# Mots-clés inclusifs pour détecter une action biodiversité (titre ou description)
BIODIV_KEYWORDS = [
    "trame verte",
    "trame bleue",
    "trame bleu",
    "trame noire",
    "haie",
    "pollution sonore",
    "biodiversité",
    "biodiversite",
    "biodiv",
    "artificialisation",
    "phytosanitaire",
    "pesticide",
    "engrais",
    "espèce exotique",
    "espece exotique",
    "exotique envahissant",
    "captage d'eau",
    "zone de captage",
    "renaturation",
    "restauration de milieu",
    "milieux naturels",
    "aire protégée",
    "aires protégées",
    "natura 2000",
]

PLAN_BIODIV_TYPE = 13
CHART_START = pd.Timestamp("2023-01-01")


def _build_keyword_conditions(column: str) -> str:
    return " OR ".join(
        f"lower(coalesce({column}, '')) LIKE '%' || :kw_{i} || '%'"
        for i in range(len(BIODIV_KEYWORDS))
    )


def _keyword_params() -> dict[str, str]:
    return {f"kw_{i}": kw for i, kw in enumerate(BIODIV_KEYWORDS)}


@st.cache_data(ttl="3d", show_spinner="Chargement des collectivités…")
def load_collectivite_noms() -> pd.DataFrame:
    df = read_table("collectivite", columns=["collectivite_id", "nom"])
    return df.dropna(subset=["collectivite_id"]).drop_duplicates("collectivite_id")


@st.cache_data(ttl="3d", show_spinner="Chargement des plans biodiversité…")
def load_plan_biodiv_statut() -> pd.DataFrame:
    df_pap_52 = read_table("pap_statut_5_fiches_modifiees_52_semaines")
    df_pap_passage = read_table("pap_date_passage", columns=["plan", "type"])

    plans_biodiv = df_pap_passage.loc[
        df_pap_passage["type"] == PLAN_BIODIV_TYPE, "plan"
    ].dropna().unique()

    df = df_pap_52[df_pap_52["plan"].isin(plans_biodiv)].copy()
    df["mois"] = pd.to_datetime(df["mois"], errors="coerce")

    noms = load_collectivite_noms()
    df = df.merge(noms, on="collectivite_id", how="left")
    df = df.rename(columns={"nom": "collectivite"})
    return df.sort_values("mois")


@st.cache_data(ttl="3d", show_spinner="Chargement des statuts actions biodiversité…")
def load_actions_biodiv_statut(fiche_ids: tuple[int, ...]) -> pd.DataFrame:
    if not fiche_ids:
        return pd.DataFrame(columns=["fiche_id", "statut", "mois"])

    df = read_table("statut_fiche_13_semaines")
    df = df[df["fiche_id"].isin(fiche_ids)].copy()
    df["mois"] = pd.to_datetime(df["mois"], errors="coerce")
    return df.sort_values("mois")


@st.cache_data(ttl="3d", show_spinner="Chargement des actions biodiversité…")
def load_actions_biodiv() -> pd.DataFrame:
    titre_cond = _build_keyword_conditions("fa.titre")
    desc_cond = _build_keyword_conditions("fa.description")
    params = _keyword_params()

    sql = f"""
        SELECT DISTINCT
            fa.id,
            fa.created_at,
            fa.collectivite_id,
            fa.titre,
            fa.description,
            fa.statut::text AS statut,
            c.nom AS collectivite
        FROM fiche_action fa
        JOIN collectivite c ON c.id = fa.collectivite_id
        WHERE fa.parent_id IS NULL
          AND (fa.deleted IS NULL OR fa.deleted = FALSE)
          AND c.type != 'test'
          AND (
            EXISTS (
              SELECT 1
              FROM fiche_action_axe faa
              JOIN axe a ON a.id = faa.axe_id
              LEFT JOIN axe plan_root ON plan_root.id = a.plan
              WHERE faa.fiche_id = fa.id
                AND (a.type = {PLAN_BIODIV_TYPE} OR plan_root.type = {PLAN_BIODIV_TYPE})
            )
            OR ({titre_cond})
            OR ({desc_cond})
            OR EXISTS (
              SELECT 1
              FROM fiche_action_action faa2
              WHERE faa2.fiche_id = fa.id
                AND faa2.action_id ILIKE '3.3.4%%'
            )
          )
        ORDER BY fa.created_at
    """

    engine = get_engine_prod()
    with engine.connect() as conn:
        return pd.read_sql_query(text(sql), conn, params=params)


def _aggregate_plan_evolution(df: pd.DataFrame) -> pd.DataFrame:
    total = df.groupby("mois").size().reset_index(name="nb")
    total["serie"] = "Total"

    by_statut = (
        df.groupby(["mois", "statut"])
        .size()
        .reset_index(name="nb")
    )
    by_statut["serie"] = by_statut["statut"].str.capitalize()

    return pd.concat(
        [total, by_statut.drop(columns=["statut"])],
        ignore_index=True,
    ).sort_values("mois")


def _aggregate_actions_statut(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["mois", "statut"])
        .size()
        .reset_index(name="nb")
        .sort_values("mois")
    )


def _aggregate_actions_monthly(df: pd.DataFrame) -> pd.DataFrame:
    work = df.copy()
    work["created_at"] = pd.to_datetime(work["created_at"], errors="coerce")
    if getattr(work["created_at"].dt, "tz", None) is not None:
        work["created_at"] = work["created_at"].dt.tz_localize(None)
    work["mois"] = work["created_at"].dt.to_period("M").dt.to_timestamp()

    monthly = (
        work.groupby("mois")
        .size()
        .reset_index(name="nb_crees")
        .sort_values("mois")
    )
    return monthly


def _filter_from_2023(df: pd.DataFrame, mois_col: str = "mois") -> pd.DataFrame:
    work = df.copy()
    work[mois_col] = pd.to_datetime(work[mois_col], errors="coerce")
    return (
        work[work[mois_col] >= CHART_START]
        .sort_values(mois_col)
        .reset_index(drop=True)
    )


def _mois_labels(df: pd.DataFrame, col: str = "mois") -> pd.Series:
    return pd.to_datetime(df[col]).dt.strftime("%Y-%m")


def _chart_tick_values(df: pd.DataFrame, mois_col: str = "mois") -> list[str]:
    work = _filter_from_2023(df, mois_col)
    work["mois_label"] = _mois_labels(work, mois_col)
    return work["mois_label"].drop_duplicates().tolist()


def _to_nivo_lines(
    df: pd.DataFrame,
    *,
    x_col: str,
    y_col: str,
    series_col: str,
    series_order: list[str] | None = None,
    sort_col: str = "mois",
) -> list[dict]:
    # Axe X commun, trié chronologiquement et partagé par toutes les séries.
    # Cela évite que des mois présents dans une seule série soient ajoutés
    # en fin d'axe (dates dans le désordre) et que les courbes se chevauchent.
    full_axis = (
        df[[sort_col, x_col]]
        .drop_duplicates()
        .sort_values(sort_col)
    )
    x_values = full_axis[x_col].tolist()

    requested = series_order or sorted(df[series_col].unique())
    series_names = [s for s in requested if s in set(df[series_col].unique())]

    line_data = []
    for name in series_names:
        subset = df[df[series_col] == name]
        y_by_x = dict(zip(subset[x_col], subset[y_col]))
        line_data.append({
            "id": name,
            "data": [
                {"x": x, "y": int(y_by_x.get(x, 0))}
                for x in x_values
            ],
        })
    return line_data


def _render_nivo_line(
    line_data: list[dict],
    *,
    chart_key: str,
    y_legend: str,
    stacked: bool = False,
    colors: list[str] | dict | None = None,
    enable_area: bool = True,
    x_tick_values: list[str] | None = None,
) -> None:
    if not line_data:
        st.info("Aucune donnée disponible pour ce graphique.")
        return

    color_prop = colors or {"scheme": "pastel2"}
    axis_bottom = {
        "tickSize": 5,
        "tickPadding": 5,
        "tickRotation": -45,
        "legend": "Mois",
        "legendOffset": 50,
        "legendPosition": "middle",
    }
    if x_tick_values:
        axis_bottom["tickValues"] = x_tick_values

    with elements(chart_key):
        with mui.Box(sx={"height": 480}):
            nivo.Line(
                data=line_data,
                margin={"top": 20, "right": 130, "bottom": 60, "left": 70},
                xScale={"type": "point"},
                yScale={
                    "type": "linear",
                    "min": 0,
                    "max": "auto",
                    "stacked": stacked,
                    "reverse": False,
                },
                curve="monotoneX",
                axisTop=None,
                axisRight=None,
                axisBottom=axis_bottom,
                axisLeft={
                    "tickSize": 5,
                    "tickPadding": 5,
                    "tickRotation": 0,
                    "legend": y_legend,
                    "legendOffset": -55,
                    "legendPosition": "middle",
                },
                enableArea=enable_area,
                areaOpacity=0.35 if not stacked else 0.7,
                enablePoints=False,
                useMesh=True,
                enableSlices="x",
                colors=color_prop,
                legends=[
                    {
                        "anchor": "bottom-right",
                        "direction": "column",
                        "justify": False,
                        "translateX": 120,
                        "translateY": 0,
                        "itemsSpacing": 2,
                        "itemWidth": 90,
                        "itemHeight": 20,
                        "itemDirection": "left-to-right",
                        "itemOpacity": 0.85,
                        "symbolSize": 12,
                        "symbolShape": "circle",
                    }
                ],
                theme=THEME_NIVO,
            )


# ==========================
# Interface
# ==========================

st.title("🌿 Dashboard Biodiv")

with st.expander("Critères de détection des actions biodiversité"):
    st.markdown("""
    Une action est comptée si **au moins une** des conditions suivantes est vraie :
    - elle est rattachée à un plan biodiversité (`axe.type = 13`, y compris via un sous-axe) ;
    - son **titre** ou sa **description** contient l'un des mots-clés ci-dessous ;
    - elle est liée au référentiel CAE via `fiche_action_action` avec `action_id` commençant par `3.3.4`.
    """)
    st.markdown("**Mots-clés recherchés :** " + ", ".join(f"*{kw}*" for kw in BIODIV_KEYWORDS))

# Toutes les données sont chargées une seule fois (mises en cache), pour
# l'ensemble des collectivités. La sélection ne fait ensuite qu'un filtrage
# en mémoire : aucune requête DB n'est relancée au changement de sélection.
df_plans_all = load_plan_biodiv_statut()
df_actions_all = load_actions_biodiv()

# Statuts chargés pour TOUTES les actions biodiv, une seule fois, puis associés
# à leur collectivité afin de pouvoir filtrer en mémoire.
all_fiche_ids = tuple(df_actions_all["id"].dropna().astype(int).unique())
df_statut_all = load_actions_biodiv_statut(all_fiche_ids).copy()
fiche_to_ct = df_actions_all.set_index("id")["collectivite"]
df_statut_all["collectivite"] = df_statut_all["fiche_id"].map(fiche_to_ct)

# Champ de recherche : filtre toutes les sections par nom de collectivité.
collectivites_dispo = sorted(
    set(df_plans_all["collectivite"].dropna()) | set(df_actions_all["collectivite"].dropna())
)
selection_ct = st.multiselect(
    "🔎 Rechercher une ou plusieurs collectivités",
    options=collectivites_dispo,
    placeholder="Toutes les collectivités",
    help="Laisser vide pour afficher l'ensemble des collectivités.",
)
if selection_ct:
    df_plans = df_plans_all[df_plans_all["collectivite"].isin(selection_ct)]
    df_actions = df_actions_all[df_actions_all["collectivite"].isin(selection_ct)]
    df_statut = df_statut_all[df_statut_all["collectivite"].isin(selection_ct)]
else:
    df_plans = df_plans_all
    df_actions = df_actions_all
    df_statut = df_statut_all

st.markdown("---")
st.subheader("Évolution des plans biodiversité")
st.caption("Critère d'activité à 1 an : un plan biodiversité est actif si au moins 5 actions pilotables ont été modifiées dans les 12 derniers mois.")

if df_plans.empty:
    st.info("Aucun plan biodiversité trouvé dans pap_statut (1 an).")
else:
    dernier_mois = df_plans["mois"].max()
    df_dernier = df_plans[df_plans["mois"] == dernier_mois]
    cols = st.columns(3)
    cols[0].metric("Plans au dernier mois", len(df_dernier))
    cols[1].metric("Actifs", int((df_dernier["statut"] == "actif").sum()))
    cols[2].metric("Inactifs", int((df_dernier["statut"] == "inactif").sum()))

    evolution_plans = _aggregate_plan_evolution(_filter_from_2023(df_plans))
    evolution_plans["mois_label"] = _mois_labels(evolution_plans)
    tick_plans = _chart_tick_values(evolution_plans)

    line_plans = _to_nivo_lines(
        evolution_plans,
        x_col="mois_label",
        y_col="nb",
        series_col="serie",
        series_order=["Total", "Actif", "Inactif"],
    )
    _render_nivo_line(
        line_plans,
        chart_key="biodiv_plans_evolution",
        y_legend="Nombre de plans",
        stacked=False,
        colors=["#2ca02c", "#98df8a", "#ff9896"],
        enable_area=False,
        x_tick_values=tick_plans,
    )

st.markdown("---")
st.subheader("Évolution des actions biodiversité")

if df_actions.empty:
    st.info("Aucune action biodiversité détectée.")
else:
    monthly_actions = _aggregate_actions_monthly(df_actions)
    monthly_actions = _filter_from_2023(monthly_actions)
    monthly_actions["mois_label"] = _mois_labels(monthly_actions)
    tick_actions = _chart_tick_values(monthly_actions)

    cols_fa = st.columns(2)
    cols_fa[0].metric("Actions biodiv identifiées", len(df_actions))
    cols_fa[1].metric(
        "Créées sur le dernier mois",
        int(monthly_actions.iloc[-1]["nb_crees"]) if len(monthly_actions) else 0,
    )

    line_crees = [{
        "id": "Créations mensuelles",
        "data": [
            {"x": row["mois_label"], "y": int(row["nb_crees"])}
            for _, row in monthly_actions.iterrows()
        ],
    }]
    _render_nivo_line(
        line_crees,
        chart_key="biodiv_actions_monthly",
        y_legend="Actions créées",
        stacked=False,
        colors=["#1f77b4"],
        enable_area=True,
        x_tick_values=tick_actions,
    )

    st.caption(
        "Critère d'activité à 13 semaines : une action est active si elle a reçu "
        "au moins une modification dans les 13 dernières semaines."
    )

    if df_statut.empty:
        st.info("Aucun statut disponible pour les actions biodiversité.")
    else:
        statut_actions = _aggregate_actions_statut(_filter_from_2023(df_statut))
        statut_actions["mois_label"] = _mois_labels(statut_actions)
        statut_actions["serie"] = statut_actions["statut"].str.capitalize()
        tick_statut = _chart_tick_values(statut_actions)

        line_statut = _to_nivo_lines(
            statut_actions,
            x_col="mois_label",
            y_col="nb",
            series_col="serie",
            series_order=["Actif", "Inactif"],
        )
        _render_nivo_line(
            line_statut,
            chart_key="biodiv_actions_statut",
            y_legend="Nombre d'actions",
            stacked=False,
            colors=["#2ca02c", "#ff9896"],
            enable_area=False,
            x_tick_values=tick_statut,
        )

st.markdown("---")
st.subheader("Liste des actions biodiversité")

if df_actions.empty:
    st.info("Aucune action biodiversité à afficher.")
else:
    df_liste = (
        df_actions[["collectivite", "titre", "description", "statut"]]
        .sort_values(["collectivite", "titre"], na_position="last")
        .reset_index(drop=True)
    )
    st.dataframe(df_liste, use_container_width=True, hide_index=True)
