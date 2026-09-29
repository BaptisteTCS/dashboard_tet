import streamlit as st

st.set_page_config(
    page_title="Matrice d'impact des leviers",
    page_icon="🎯",
    layout="wide",
)

from streamlit_echarts import st_echarts

from utils.collectivite_selection import (
    default_collectivite_index,
    set_selected_collectivite,
)
from utils.priorisation_data import (
    build_priorisation_context,
    load_collectivites_priorisees,
)
from utils.priorisation_matrice_leviers import (
    CHART_HEIGHT,
    X_SEUIL_DEFAULT,
    build_matrice_echarts_options,
    build_matrice_leviers,
    filter_matrice_by_potentiel_min,
)

st.title("🎯 Matrice d'impact des leviers")
st.markdown(
    "Chaque point est un **levier** : sa **mobilisation** en abscisse "
    "(moyenne pondérée des notes 0–3 des volets, hors compétence exclue) "
    "et son **potentiel de réduction CO₂** en ordonnée. "
    "En haut à gauche, les **angles morts** : fort impact, peu mobilisés."
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

collectivite_id = st.selectbox(
    "Collectivité",
    options=collectivite_ids,
    index=default_collectivite_index(collectivite_ids),
    format_func=lambda cid: nom_par_id[cid],
    key="matrice_impact_collectivite",
)
set_selected_collectivite(collectivite_id)

ctx = build_priorisation_context(collectivite_id, nom_par_id, collectivite_ids)

df_matrice, excluded = build_matrice_leviers(
    ctx.leviers_notes,
    ctx.notes,
    ctx.weights,
    ctx.reductions,
    ctx.exclusions,
)

if df_matrice.empty:
    st.info("Aucun levier avec une note et un potentiel de réduction pour cette collectivité.")
    if excluded:
        st.caption("Exclus : " + " · ".join(excluded))
    st.stop()

col_toggle, col_slider = st.columns([1, 2])
with col_toggle:
    show_all_labels = st.toggle("Afficher tous les libellés", value=False)
with col_slider:
    potentiel_min = st.slider(
        "Potentiel minimum (ktCO₂e)",
        min_value=0,
        max_value=30,
        value=0,
        step=1,
        help="Masque les leviers dont le potentiel de réduction CO₂ est inférieur à ce seuil.",
        key="matrice_impact_potentiel_min",
    )

df_matrice = filter_matrice_by_potentiel_min(df_matrice, float(potentiel_min))
if df_matrice.empty:
    st.info(
        f"Aucun levier avec un potentiel ≥ {potentiel_min} ktCO₂e pour cette collectivité."
    )
    st.stop()

y_seuil = float(df_matrice["y_seuil"].iloc[0])
n_angles_morts = int((df_matrice["quadrant"] == "angles_morts").sum())

c1, c2, c3, c4 = st.columns(4)
c1.metric("Leviers affichés", len(df_matrice))
c2.metric("Angles morts", n_angles_morts)
c3.metric("Seuil mobilisation", f"{X_SEUIL_DEFAULT:.0f} %")
c4.metric("Seuil potentiel (médiane)", f"{y_seuil:.1f} ktCO₂e")

options = build_matrice_echarts_options(
    df_matrice,
    x_seuil=X_SEUIL_DEFAULT,
    show_all_labels=show_all_labels,
)
st_echarts(
    options=options,
    height=f"{CHART_HEIGHT}px",
    key=f"matrice_impact_{collectivite_id}_{int(show_all_labels)}_{potentiel_min}",
)

if potentiel_min > 0:
    st.caption(
        f"Seuil potentiel minimum : **{potentiel_min} ktCO₂e** — "
        f"les leviers en dessous sont masqués du graphe."
    )

if excluded:
    st.caption(f"{len(excluded)} levier(s) exclu(s) : " + " · ".join(excluded))

st.markdown("##### Détail par levier")
df_table = df_matrice[
    ["levier", "mobilisation_pct", "potentiel_ktco2e", "quadrant_label"]
].copy()
df_table["mobilisation_pct"] = df_table["mobilisation_pct"].round(1)
df_table["potentiel_ktco2e"] = df_table["potentiel_ktco2e"].round(1)
st.dataframe(
    df_table.rename(
        columns={
            "levier": "Levier",
            "mobilisation_pct": "Mobilisation (%)",
            "potentiel_ktco2e": "Potentiel (ktCO₂e)",
            "quadrant_label": "Quadrant",
        }
    ),
    use_container_width=True,
    hide_index=True,
)
