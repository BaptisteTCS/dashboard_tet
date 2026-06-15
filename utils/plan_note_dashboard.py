"""Composants partagés pour l'affichage des notes de plans (/10)."""

import streamlit as st
import pandas as pd
from streamlit_elements import elements, nivo, mui

from utils.data import tet_plan_url
from utils.plots import new_note_spider_graph

THEME_NIVO = {
    "text": {
        "fontFamily": "Source Sans Pro, sans-serif",
        "fontSize": 13,
        "fill": "#31333F",
    },
    "labels": {
        "text": {
            "fontFamily": "Source Sans Pro, sans-serif",
            "fontSize": 16,
            "fill": "#31333F",
        }
    },
    "grid": {
        "line": {
            "stroke": "#e0e0e0",
            "strokeWidth": 1,
            "strokeOpacity": 0.8,
        }
    },
    "legends": {
        "text": {
            "fontFamily": "Source Sans Pro, sans-serif",
            "fontSize": 12,
            "fill": "#31333F",
        }
    },
    "tooltip": {
        "container": {
            "background": "rgba(255, 255, 255, 0.95)",
            "color": "#31333F",
            "fontSize": "13px",
            "fontFamily": "Source Sans Pro, sans-serif",
            "borderRadius": "4px",
            "boxShadow": "0 2px 8px rgba(0,0,0,0.15)",
            "padding": "8px 12px",
            "border": "1px solid rgba(0, 0, 0, 0.1)",
        }
    },
}

AXES_COLS = [
    "score_titre",
    "score_description",
    "score_statut",
    "score_indicateur",
    "score_objectif",
    "score_budget",
    "score_suivi",
    "axe_pilote",
    "axe_dates",
    "axe_activite",
]


def render_notation_definition_expander() -> None:
    with st.expander("Définition de la notation"):
        st.markdown("### Définition de la note d'une action")
        st.markdown(
            """
        - **Titre** + 1pt
        - **Description** + 1pt
        - **Statut** + 1pt
        - **Personne pilote** + 0.5pt
        - **Au moins une des personnes pilotes est rattachée à un compte utilisateur** +0.5pt
        - **Date de début** + 0.5pt
        - **Date de fin (ou action continue est coché)** + 0.5pt
        - **Indicateur lié** + 1pt
        - **Objectif** + 1pt *(au moins un objectif chiffré dans TOUS les indicateurs liés pour une année supérieur ou égalé à l'année actuelle)*
        - **Budget** + 1pt *(budget investissement ou fonctionnement ou financeurs ou champs financements ou moyens humains)*
        - **Note de suivi de moins d'un an** + 1pt
        - **Date de dernière MAJ de l'action <12 mois** + 0.5pt (si statut non terminé/Abandonné) *(la modification d'une relation n'est pas comptabilisée comme lier des indicateurs, mesures, budget, etc.)*
        - **Date de dernière MAJ de l'action <6 mois** + 0.5pt (si statut non terminé/Abandonné) *(idem)*
        """
        )
        st.markdown("### Définition de la note d'un plan")
        st.markdown(
            "La note d'un plan se calcule en prenant la moyenne des notes de toutes ses fiches actions."
        )


def prepare_note_plan_semaine(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise note_plan_semaine (plan, semaine, note_plan)."""
    if df.empty:
        return df
    df = df.copy()
    df["plan"] = pd.to_numeric(df["plan"], errors="coerce")
    df["semaine"] = pd.to_datetime(df["semaine"], errors="coerce").dt.normalize()
    df["note_plan"] = pd.to_numeric(df["note_plan"], errors="coerce")
    return (
        df.dropna(subset=["semaine", "plan", "note_plan"])
        .sort_values("semaine")
        .drop_duplicates(subset=["plan", "semaine"], keep="last")
        .astype({"plan": "int64"})
    )


def top_plans_weekly_progression(
    df_note_semaine: pd.DataFrame,
    n: int = 10,
) -> dict | None:
    """Top plans par delta note_plan entre les 2 dernières semaines."""
    df = prepare_note_plan_semaine(df_note_semaine)
    if df.empty:
        return None

    semaines = sorted(df["semaine"].unique(), reverse=True)
    if len(semaines) < 2:
        return None

    semaine_actuelle, semaine_precedente = semaines[0], semaines[1]
    df_2s = df[df["semaine"].isin([semaine_actuelle, semaine_precedente])]

    df_pivot = df_2s.pivot(index="plan", columns="semaine", values="note_plan")
    if df_pivot.shape[1] < 2:
        return None

    cols_chrono = sorted(df_pivot.columns)
    df_pivot["difference_note"] = df_pivot[cols_chrono[1]] - df_pivot[cols_chrono[0]]
    top_rows = (
        df_pivot[["difference_note"]]
        .reset_index()
        .sort_values("difference_note", ascending=False)
        .head(n)
    )

    if top_rows.empty or top_rows["difference_note"].max() <= 0:
        return {
            "top_plans": [],
            "delta_by_plan": {},
            "note_by_plan": {},
            "semaine_actuelle": semaine_actuelle,
            "semaine_precedente": semaine_precedente,
        }

    top_plans = top_rows["plan"].tolist()
    return {
        "top_plans": top_plans,
        "delta_by_plan": df_pivot.loc[top_plans, "difference_note"].to_dict(),
        "note_by_plan": df_pivot.loc[top_plans, cols_chrono[1]].to_dict(),
        "semaine_actuelle": semaine_actuelle,
        "semaine_precedente": semaine_precedente,
    }


def build_plan_scores_df(
    df_fiche_action_plan: pd.DataFrame,
    df_note_fiche: pd.DataFrame,
    plan_ids: list,
) -> pd.DataFrame:
    """Agrège les scores par plan (moyenne des fiches notées)."""
    if not plan_ids:
        return pd.DataFrame(columns=["plan", *AXES_COLS, "note_fa"])

    df_fiches_plans = df_fiche_action_plan[
        df_fiche_action_plan["plan"].isin(plan_ids)
    ]

    df_join = df_fiches_plans.merge(
        df_note_fiche,
        on="fiche_id",
        how="inner",
        suffixes=("", "_note"),
    )

    if df_join.empty:
        return pd.DataFrame(columns=["plan", *AXES_COLS, "note_fa"])

    df_join["axe_pilote"] = (
        df_join["score_pilote"].fillna(0) + df_join["score_pilote_user"].fillna(0)
    )
    df_join["axe_dates"] = (
        df_join["score_date_debut"].fillna(0) + df_join["score_date_fin"].fillna(0)
    )
    df_join["axe_activite"] = (
        df_join["score_modif_6_mois"].fillna(0)
        + df_join["score_modif_12_mois"].fillna(0)
    )

    return (
        df_join.groupby("plan")[AXES_COLS + ["note_fa"]]
        .mean()
        .reset_index()
    )


def render_top_plans_evolution_chart(
    df_note_plan: pd.DataFrame,
    top_plans: list,
    nom_plan_par_id: dict,
    *,
    element_id: str = "line_top_plans",
    theme: dict | None = None,
) -> None:
    """Courbe d'évolution historique des notes de plans (/10)."""
    theme = theme or THEME_NIVO

    if len(top_plans) >= 10:
        st.badge(
            "Évolution des 10 meilleurs plans",
            icon=":material/trending_up:",
            color="green",
        )
    else:
        st.badge(
            "Évolution des plans",
            icon=":material/trending_up:",
            color="green",
        )

    df_evol_top = (
        df_note_plan[df_note_plan["plan"].isin(top_plans)]
        .copy()
        .sort_values("mois")
    )

    if df_evol_top.empty:
        st.info("Pas d'historique de note pour ces plans.")
        return

    line_data = []
    for plan_id in top_plans:
        plan_nom = nom_plan_par_id.get(plan_id, str(int(plan_id)))
        df_p = df_evol_top[df_evol_top["plan"] == plan_id]
        serie = [
            {"x": str(row["mois"]), "y": round(float(row["note_plan"]), 1)}
            for _, row in df_p.iterrows()
            if pd.notna(row["note_plan"])
        ]
        if serie:
            line_data.append({"id": plan_nom, "data": serie})

    if not line_data:
        st.info("Pas d'historique de note pour ces plans.")
        return

    with elements(element_id):
        with mui.Box(sx={"height": 350}):
            nivo.Line(
                data=line_data,
                margin={"top": 30, "right": 260, "bottom": 70, "left": 60},
                xScale={"type": "point"},
                yScale={
                    "type": "linear",
                    "min": 0,
                    "max": 10,
                    "stacked": False,
                    "reverse": False,
                },
                curve="monotoneX",
                axisTop=None,
                axisRight=None,
                axisBottom={
                    "tickSize": 5,
                    "tickPadding": 5,
                    "tickRotation": -45,
                    "legend": "Mois",
                    "legendOffset": 55,
                    "legendPosition": "middle",
                },
                axisLeft={
                    "tickSize": 5,
                    "tickPadding": 5,
                    "tickRotation": 0,
                    "legend": "Note /10",
                    "legendOffset": -45,
                    "legendPosition": "middle",
                },
                enablePoints=False,
                useMesh=True,
                enableSlices="x",
                colors={"scheme": "category10"},
                legends=[
                    {
                        "anchor": "right",
                        "direction": "column",
                        "justify": False,
                        "translateX": 250,
                        "translateY": 0,
                        "itemsSpacing": 4,
                        "itemDirection": "left-to-right",
                        "itemWidth": 240,
                        "itemHeight": 18,
                        "itemOpacity": 0.85,
                        "symbolSize": 12,
                        "symbolShape": "circle",
                    }
                ],
                theme=theme,
            )


def render_plan_radar_gallery(
    df_plan_scores: pd.DataFrame,
    nom_plan_par_id: dict,
    *,
    collectivite_id: int | None = None,
    collectivite_id_by_plan: dict | None = None,
    display_name_by_plan: dict | None = None,
    delta_by_plan: dict | None = None,
    note_by_plan: dict | None = None,
    theme: dict | None = None,
    element_key_prefix: str = "radar_plan",
    show_plans_badge: bool = True,
) -> None:
    """Galerie de radars par plan avec note /10."""
    theme = theme or THEME_NIVO

    if df_plan_scores.empty:
        st.warning("Aucune fiche notée pour ces plans ce mois-ci.")
        return

    if show_plans_badge:
        nb_plans = len(df_plan_scores)
        st.badge(
            f"{nb_plans} plan{'s' if nb_plans != 1 else ''}",
            icon=":material/radar:",
            color="orange",
        )

    for idx in range(0, len(df_plan_scores), 2):
        cols = st.columns(2)

        for col_idx, col in enumerate(cols):
            row_idx = idx + col_idx
            if row_idx >= len(df_plan_scores):
                continue

            row = df_plan_scores.iloc[row_idx]
            plan_id = row["plan"]
            rank = row_idx + 1
            plan_nom = nom_plan_par_id.get(plan_id, str(int(plan_id)))
            display_name = (
                display_name_by_plan.get(plan_id, plan_nom)
                if display_name_by_plan
                else plan_nom
            )
            note_fa = row["note_fa"]
            note_display = (
                note_by_plan.get(plan_id, note_fa)
                if note_by_plan is not None
                else note_fa
            )
            delta = delta_by_plan.get(plan_id) if delta_by_plan is not None else None

            cid = collectivite_id
            if cid is None and collectivite_id_by_plan is not None:
                cid = collectivite_id_by_plan.get(plan_id)

            plan_link = tet_plan_url(cid, plan_id) if cid is not None else None

            with col:
                badge_color = (
                    "green" if rank == 1 else "orange" if rank <= 3 else "gray"
                )
                if plan_link:
                    st.markdown(
                        f"#### :{badge_color}-badge[{rank}] [{display_name}]({plan_link})"
                    )
                else:
                    st.markdown(f"#### :{badge_color}-badge[{rank}] {display_name}")

                if delta is not None and pd.notna(delta):
                    st.metric(
                        "Note du plan",
                        f"{round(float(note_display), 1)} / 10",
                        delta=f"{float(delta):+.1f}",
                        delta_color="normal",
                    )
                else:
                    st.metric("Note du plan", f"{round(float(note_display), 1)} / 10")

                radar_data = new_note_spider_graph(row)

                with elements(f"{element_key_prefix}_{int(plan_id)}_{rank}"):
                    with mui.Box(sx={"height": 500}):
                        nivo.Radar(
                            data=radar_data,
                            keys=["Note"],
                            indexBy="axe",
                            maxValue=10,
                            margin={"top": 70, "right": 80, "bottom": 40, "left": 80},
                            curve="linearClosed",
                            borderWidth=2,
                            borderColor={"from": "color"},
                            gridLevels=5,
                            gridShape="circular",
                            gridLabelOffset=20,
                            enableDots=True,
                            dotSize=6,
                            dotColor={"theme": "background"},
                            dotBorderWidth=2,
                            dotBorderColor={"from": "color"},
                            enableDotLabel=False,
                            colors=["#ffc121"],
                            fillOpacity=0.5,
                            blendMode="multiply",
                            animate=True,
                            motionConfig="wobbly",
                            isInteractive=True,
                            theme=theme,
                        )

                st.markdown("---")
