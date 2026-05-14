import streamlit as st
import pandas as pd
from streamlit_elements import elements, nivo, mui

from utils.db import read_table
from utils.data import tet_plan_url
from utils.plots import new_note_spider_graph


st.set_page_config(layout="wide")
st.title("🛰️ Dashboard Collectivités")


# === CHARGEMENT DES DONNÉES ===
@st.cache_resource(ttl="1d")
def load_data():
    df_airtable_sync = read_table('airtable_sync')
    df_activite_semaine = read_table('activite_semaine')
    df_note_plan = read_table('note_plan_historique')
    df_note_fiche = read_table(
        'note_fiche_historique',
        where_sql="mois=(select max(mois) from note_fiche_historique)",
    )
    df_pap_date_passage = read_table('pap_date_passage')
    df_collectivite = read_table('collectivite')
    df_fiche_action_plan = read_table('fiche_action_plan')
    return (
        df_airtable_sync,
        df_activite_semaine,
        df_note_plan,
        df_note_fiche,
        df_pap_date_passage,
        df_collectivite,
        df_fiche_action_plan,
    )


(
    df_airtable_sync,
    df_activite_semaine,
    df_note_plan,
    df_note_fiche,
    df_pap_date_passage,
    df_collectivite,
    df_fiche_action_plan,
) = load_data()


# === THÈMES NIVO ===
theme_nivo = {
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


# === SÉLECTION COLLECTIVITÉ ===
collectivites_pap = (
    df_pap_date_passage[['collectivite_id']]
    .drop_duplicates()
    .merge(
        df_collectivite[['collectivite_id', 'nom']],
        on='collectivite_id',
        how='left',
    )
)
collectivites_pap['nom'] = collectivites_pap['nom'].fillna(
    collectivites_pap['collectivite_id'].astype(str)
)
collectivites_pap = collectivites_pap.sort_values('nom')

nom_par_id = dict(zip(collectivites_pap['collectivite_id'], collectivites_pap['nom']))
options_ct = collectivites_pap['collectivite_id'].tolist()

cid_selected = st.selectbox(
    "Collectivité",
    options=options_ct,
    format_func=lambda cid: nom_par_id.get(cid, str(cid)),
    index=None,
    placeholder="Tapez le nom d'une collectivité...",
)

if cid_selected is None:
    st.info("Sélectionnez une collectivité pour afficher son dashboard.")
    st.stop()

st.markdown(f"### {nom_par_id[cid_selected]}")

tab_plan, tab_activite = st.tabs(["📋 Plan", "👥 Activité"])


# ============================================================================
# ONGLET PLAN
# ============================================================================
with tab_plan:
    df_plans_ct = df_pap_date_passage[
        df_pap_date_passage['collectivite_id'] == cid_selected
    ].copy()

    plans_ct = df_plans_ct['plan'].dropna().unique().tolist()

    if not plans_ct:
        st.warning("Aucun plan PAP trouvé pour cette collectivité.")
    else:
        nom_plan_par_id = (
            df_plans_ct.dropna(subset=['plan'])
            .drop_duplicates(subset=['plan'])
            .set_index('plan')['nom_plan_ct']
            .to_dict()
        )

        df_fiches_plans = df_fiche_action_plan[
            df_fiche_action_plan['plan'].isin(plans_ct)
        ]

        df_join = df_fiches_plans.merge(
            df_note_fiche,
            on='fiche_id',
            how='inner',
            suffixes=('', '_note'),
        )

        df_join['axe_pilote'] = df_join['score_pilote'].fillna(0) + df_join['score_pilote_user'].fillna(0)
        df_join['axe_dates'] = df_join['score_date_debut'].fillna(0) + df_join['score_date_fin'].fillna(0)
        df_join['axe_activite'] = (
            df_join['score_modif_6_mois'].fillna(0) + df_join['score_modif_12_mois'].fillna(0)
        )

        axes_cols = [
            'score_titre',
            'score_description',
            'score_statut',
            'score_indicateur',
            'score_objectif',
            'score_budget',
            'score_suivi',
            'axe_pilote',
            'axe_dates',
            'axe_activite',
        ]

        if df_join.empty:
            st.warning("Aucune fiche notée pour les plans de cette collectivité ce mois-ci.")
        else:
            df_plan_scores = (
                df_join.groupby('plan')[axes_cols + ['note_fa']]
                .mean()
                .reset_index()
                .sort_values('note_fa', ascending=False)
                .reset_index(drop=True)
            )

            # --- LINE CHART : ÉVOLUTION DES TOP 10 PLANS ---
            top_plans = df_plan_scores.head(10)['plan'].tolist()

            df_evol_top = (
                df_note_plan[df_note_plan['plan'].isin(top_plans)]
                .copy()
                .sort_values('mois')
            )

            st.badge(
                f"Évolution des {len(top_plans)} meilleurs plans",
                icon=":material/trending_up:",
                color="green",
            )

            if df_evol_top.empty:
                st.info("Pas d'historique de note pour ces plans.")
            else:
                line_data = []
                for plan_id in top_plans:
                    plan_nom = nom_plan_par_id.get(plan_id, str(int(plan_id)))
                    df_p = df_evol_top[df_evol_top['plan'] == plan_id]
                    serie = [
                        {"x": str(row['mois']), "y": round(float(row['note_plan']), 1)}
                        for _, row in df_p.iterrows()
                        if pd.notna(row['note_plan'])
                    ]
                    if serie:
                        line_data.append({"id": plan_nom, "data": serie})

                with elements("line_top_plans"):
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
                            theme=theme_nivo,
                        )

            # --- GALERIE DE RADARS ---
            st.markdown("---")
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
                    plan_id = row['plan']
                    rank = row_idx + 1
                    plan_nom = nom_plan_par_id.get(plan_id, str(int(plan_id)))
                    note_fa = row['note_fa']

                    with col:
                        badge_color = "green" if rank == 1 else "orange" if rank <= 3 else "gray"
                        plan_link = tet_plan_url(cid_selected, plan_id)
                        st.markdown(
                            f"#### :{badge_color}-badge[{rank}] [{plan_nom}]({plan_link})"
                        )
                        st.metric("Note du plan", f"{round(float(note_fa), 1)} / 10")

                        radar_data = new_note_spider_graph(row)

                        with elements(f"radar_plan_{int(plan_id)}_{rank}"):
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
                                    theme=theme_nivo,
                                )

                        st.markdown("---")


# ============================================================================
# ONGLET ACTIVITÉ
# ============================================================================
with tab_activite:
    df_act_ct = df_activite_semaine[
        df_activite_semaine['collectivite_id'] == cid_selected
    ].copy()

    if df_act_ct.empty:
        st.info("Aucune activité enregistrée pour cette collectivité.")
    else:
        df_act_ct['semaine_dt'] = pd.to_datetime(df_act_ct['semaine'], errors='coerce')
        df_act_ct = df_act_ct.dropna(subset=['semaine_dt'])

        st.markdown("Activité des agents uniquement.")

        col_chart, col_lb = st.columns([2, 1])


        # --- LINE CHART : NB USERS CONNECTÉS PAR SEMAINE (12 derniers mois) ---
        with col_chart:
            st.badge(
                "Utilisateurs connectés par semaine",
                icon=":material/group:",
                color="blue",
            )

            cutoff_1y = pd.Timestamp.now().normalize() - pd.DateOffset(years=1)
            df_chart = df_act_ct[df_act_ct['semaine_dt'] >= cutoff_1y]

            if df_chart.empty:
                st.info("Aucune activité sur les 12 derniers mois.")
            else:
                nb_users_by_week = df_chart.groupby('semaine_dt')['email'].nunique()
                start = max(cutoff_1y, nb_users_by_week.index.min())
                end = nb_users_by_week.index.max()

                # Grille hebdomadaire alignée sur le jour de semaine présent dans les données
                all_weeks = pd.date_range(start=start, end=end, freq='7D')
                grid = (
                    nb_users_by_week.reindex(all_weeks, fill_value=0)
                    .reset_index()
                )
                grid.columns = ['semaine_dt', 'nb_users']

                line_data_act = [
                    {
                        "id": "Utilisateurs",
                        "data": [
                            {
                                "x": row['semaine_dt'].strftime('%d/%m/%Y'),
                                "y": int(row['nb_users']),
                            }
                            for _, row in grid.iterrows()
                        ],
                    }
                ]

                # Ticks tous les 4 semaines pour aérer l'axe X
                tick_values = [
                    row['semaine_dt'].strftime('%d/%m/%Y')
                    for i, (_, row) in enumerate(grid.iterrows())
                    if i % 4 == 0
                ]

                with elements("line_users_per_semaine"):
                    with mui.Box(sx={"height": 500}):
                        nivo.Line(
                            data=line_data_act,
                            margin={"top": 30, "right": 40, "bottom": 80, "left": 60},
                            xScale={"type": "point"},
                            yScale={
                                "type": "linear",
                                "min": 0,
                                "max": "auto",
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
                                "tickValues": tick_values,
                                "legend": "Semaine",
                                "legendOffset": 65,
                                "legendPosition": "middle",
                            },
                            axisLeft={
                                "tickSize": 5,
                                "tickPadding": 5,
                                "tickRotation": 0,
                                "legend": "Nb utilisateurs",
                                "legendOffset": -45,
                                "legendPosition": "middle",
                            },
                            enablePoints=False,
                            enableArea=True,
                            areaOpacity=0.15,
                            useMesh=True,
                            enableSlices="x",
                            colors=["#1f77b4"],
                            theme=theme_nivo,
                        )

        # --- LEADERBOARD : NB SEMAINES DE CONNEXION SUR LES 6 DERNIERS MOIS ---
        with col_lb:
            st.badge(
                "Classement (6 derniers mois)",
                icon=":material/leaderboard:",
                color="violet",
            )

            cutoff_6m = pd.Timestamp.now().normalize() - pd.DateOffset(months=6)
            df_6m = df_act_ct[df_act_ct['semaine_dt'] >= cutoff_6m]

            if df_6m.empty:
                st.info("Aucune activité sur les 6 derniers mois.")
            else:
                df_leaderboard = (
                    df_6m.groupby('email')['semaine_dt']
                    .nunique()
                    .reset_index(name='Semaines')
                    .sort_values('Semaines', ascending=False)
                    .reset_index(drop=True)
                )
                df_leaderboard.index += 1
                df_leaderboard.index.name = 'Rang'
                df_leaderboard = df_leaderboard.rename(columns={'email': 'Utilisateur'})

                st.dataframe(
                    df_leaderboard,
                    use_container_width=True,
                    height=500,
                    column_config={
                        'Semaines': st.column_config.ProgressColumn(
                            'Semaines',
                            format='%d',
                            min_value=0,
                            max_value=int(df_leaderboard['Semaines'].max()),
                        ),
                    },
                )
