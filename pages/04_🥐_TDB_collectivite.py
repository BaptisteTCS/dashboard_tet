import streamlit as st
import pandas as pd
from streamlit_elements import elements, nivo, mui

from utils.db import read_table
from utils.plan_note_dashboard import (
    THEME_NIVO,
    build_plan_scores_df,
    render_notation_definition_expander,
    render_plan_radar_gallery,
    render_top_plans_evolution_chart,
)


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
    df_pap_13 = read_table('pap_statut_5_fiches_modifiees_13_semaines')
    df_pap_52 = read_table('pap_statut_5_fiches_modifiees_52_semaines')
    df_collectivite = read_table('collectivite')
    df_fiche_action_plan = read_table('fiche_action_plan')
    return (
        df_airtable_sync,
        df_activite_semaine,
        df_note_plan,
        df_note_fiche,
        df_pap_date_passage,
        df_pap_13,
        df_pap_52,
        df_collectivite,
        df_fiche_action_plan,
    )


(
    df_airtable_sync,
    df_activite_semaine,
    df_note_plan,
    df_note_fiche,
    df_pap_date_passage,
    df_pap_13,
    df_pap_52,
    df_collectivite,
    df_fiche_action_plan,
) = load_data()


theme_nivo = THEME_NIVO


def _noms_plans_pap_actifs(
    df_pap: pd.DataFrame,
    collectivite_id: int,
    nom_plan_par_id: dict,
) -> list[str]:
    """Plans avec statut 'actif' au dernier mois disponible."""
    df_ct = df_pap[df_pap['collectivite_id'] == collectivite_id].copy()
    if df_ct.empty:
        return []

    df_ct['mois'] = pd.to_datetime(df_ct['mois'], errors='coerce')
    dernier_mois = df_ct['mois'].max()
    df_actif = df_ct[
        (df_ct['mois'] == dernier_mois) & (df_ct['statut'] == 'actif')
    ]
    if df_actif.empty:
        return []

    if 'nom_plan' in df_actif.columns:
        noms = df_actif['nom_plan'].dropna().unique().tolist()
    else:
        noms = [
            nom_plan_par_id.get(plan_id, str(int(plan_id)))
            for plan_id in df_actif['plan'].dropna().unique()
        ]
    return sorted(noms)


def _render_liste_plans_pap(titre: str, noms: list[str]) -> None:
    st.markdown(f"**{titre}**")
    if noms:
        for nom in noms:
            st.markdown(f"- {nom}")
    else:
        st.caption("Aucun plan actif")


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

    nom_plan_par_id = (
        df_plans_ct.dropna(subset=['plan'])
        .drop_duplicates(subset=['plan'])
        .set_index('plan')['nom_plan_ct']
        .to_dict()
    )

    st.badge("Statut PAP", icon=":material/check_circle:", color="green")
    col_pap_3m, col_pap_12m = st.columns(2)
    with col_pap_3m:
        _render_liste_plans_pap(
            "PAP actif 3 mois",
            _noms_plans_pap_actifs(df_pap_13, cid_selected, nom_plan_par_id),
        )
    with col_pap_12m:
        _render_liste_plans_pap(
            "PAP actif 12 mois",
            _noms_plans_pap_actifs(df_pap_52, cid_selected, nom_plan_par_id),
        )

    st.markdown("---")
    render_notation_definition_expander()

    if not plans_ct:
        st.warning("Aucun plan PAP trouvé pour cette collectivité.")
    else:
        df_plan_scores = build_plan_scores_df(
            df_fiche_action_plan, df_note_fiche, plans_ct
        )

        if df_plan_scores.empty:
            st.warning("Aucune fiche notée pour les plans de cette collectivité ce mois-ci.")
        else:
            df_plan_scores = (
                df_plan_scores.sort_values('note_fa', ascending=False)
                .reset_index(drop=True)
            )

            top_plans = df_plan_scores.head(10)['plan'].tolist()
            render_top_plans_evolution_chart(
                df_note_plan,
                top_plans,
                nom_plan_par_id,
                element_id="line_top_plans",
                theme=theme_nivo,
            )

            st.markdown("---")
            render_plan_radar_gallery(
                df_plan_scores,
                nom_plan_par_id,
                collectivite_id=cid_selected,
                theme=theme_nivo,
            )


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
