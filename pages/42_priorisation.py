import streamlit as st

st.set_page_config(
    page_title="Priorisation",
    page_icon="🥇",
    layout="wide",
)

from utils.collectivite_selection import (
    default_collectivite_index,
    set_selected_collectivite,
)
from utils.priorisation_data import (
    build_priorisation_context,
    load_collectivites_priorisees,
    load_nb_actions,
    load_plans,
)
from utils.priorisation_tab_actions import render as render_onglet_actions
from utils.priorisation_tab_faisabilite import render as render_onglet_faisabilite
from utils.priorisation_tab_synthese import render as render_onglet_synthese

st.title("🥇 Priorisation")

df_collectivites = load_collectivites_priorisees()
if df_collectivites.empty:
    st.warning(
        "Aucune collectivité avec des données de priorisation disponible.",
        icon=":material/domain_disabled:",
    )
    st.stop()

nom_par_id = df_collectivites.set_index("collectivite_id")["nom"].to_dict()
collectivite_ids = df_collectivites["collectivite_id"].tolist()

collectivite_id = st.selectbox(
    "Collectivité",
    options=collectivite_ids,
    index=default_collectivite_index(collectivite_ids),
    format_func=lambda cid: nom_par_id[cid],
    key="priorisation_select_collectivite",
)

set_selected_collectivite(collectivite_id)

plans = load_plans(collectivite_id)
if plans:
    nb_actions = load_nb_actions(collectivite_id)
    libelle_actions = "l'action" if nb_actions == 1 else f"les {nb_actions} actions"
    libelle_plans = "votre plan" if len(plans) == 1 else "vos plans"
    st.success(
            f"Nous avons analysé {libelle_actions} de {libelle_plans} : "
            f"**{', '.join(plans)}**. "
            "Chaque action a été rattachée à un levier de la transition écologique, "
            "mis en regard de son potentiel de réduction des émissions de CO2.\n\n"
            "Les onglets ci-dessous vous permettent d'identifier vos **leviers prioritaires**, "
            "de consulter des **actions de référence**, puis de visualiser sur un "
            "**tableau de bord** où agit votre plan d'action."
        )

ctx = build_priorisation_context(collectivite_id, nom_par_id, collectivite_ids)

tab_synthese, tab_fais, tab_actions = st.tabs(
    ["Tableau de bord", "Priorisation des leviers", "Actions de référence"]
)

with tab_synthese:
    render_onglet_synthese(ctx)
with tab_fais:
    render_onglet_faisabilite(ctx)
with tab_actions:
    render_onglet_actions(ctx)
