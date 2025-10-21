import streamlit as st
import pandas as pd

from utils.data import (
    load_df_pap,
    load_df_contribution_semaine,
    load_df_activite_semaine,
    load_df_pap_statut_semaine,
)

from utils.analytics import (
    compute_totals_by_period,
    date_to_month,
    display_totals_table,
)
from utils.plots import plot_area_with_totals


st.set_page_config(page_title="North Star Bac à sable", page_icon="⛱️", layout="wide")

# === EN-TÊTE ===
st.markdown(
    """
    <div style="padding: 5px 5px; margin-bottom: 5px;">
      <h2 style="margin: 0; font-size: 40px;">⛱️ North Star - Bac à Sable</h2>
      <p style="margin-top: 8px; color: gray; font-size: 16px;">
        Expérimentez avec différents paramètres pour analyser l'impact sur la North Star
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)


def compute_statut_pap(df_pap, df_activite_ou_contribution, window):
    # 1. Normalisation des dates
    df_4 = df_pap.copy()
    df_4["passage_pap"] = pd.to_datetime(df_4["passage_pap"])
    df_4["pap_week"] = df_4["passage_pap"].dt.to_period("W").dt.start_time

    df_act = df_activite_ou_contribution.copy()
    df_act["semaine"] = pd.to_datetime(df_act["semaine"])
    df_act["semaine"] = df_act["semaine"].dt.to_period("W").dt.start_time

    # 2. Horizon temporel pris comme la dernière semaine disponible dans l'activité
    last_week = df_act["semaine"].max()

    # 3. Filtrer l'activité pour ignorer tout ce qui est antérieur au passage pap
    df_act = df_act.merge(df_4[["collectivite_id", "pap_week"]], on="collectivite_id", how="left")
    df_act = df_act[df_act["semaine"] >= df_act["pap_week"]][["collectivite_id", "semaine"]].drop_duplicates()
    df_act["had_connexion"] = 1

    # 4. Construire la grille hebdomadaire par collectivité à partir de pap_week jusqu'à last_week
    #    Si last_week est avant pap_week pour une collectivité, on l'ignore
    df_4 = df_4[df_4["pap_week"].notna()].copy()
    df_4["n_weeks"] = ((last_week - df_4["pap_week"]) // pd.Timedelta(weeks=1)) + 1
    df_4 = df_4[df_4["n_weeks"] > 0]

    df_4["offsets"] = df_4["n_weeks"].apply(lambda n: range(int(n)))
    grid = df_4.explode("offsets", ignore_index=True)
    grid["semaine"] = grid["pap_week"] + pd.to_timedelta(grid["offsets"] * 7, unit="D")
    grid = grid[["collectivite_id", "semaine"]]

    # 5. Marquer les semaines avec connexion puis calculer le statut par fenêtre glissante de 13 semaines
    result = grid.merge(df_act, on=["collectivite_id", "semaine"], how="left")
    result["had_connexion"] = result["had_connexion"].fillna(0).astype(int)
    result = result.sort_values(["collectivite_id", "semaine"])

    rolling_sum = (
        result
        .groupby("collectivite_id", group_keys=False)["had_connexion"]
        .rolling(window=window, min_periods=1)
        .sum()
        .reset_index(level=0, drop=True)
    )
    result["statut"] = rolling_sum.gt(0).map({True: "actif", False: "inactif"})

    # 6. Format final
    result["semaine"] = result["semaine"].dt.strftime("%Y-%m-%d")
    result = result[["collectivite_id", "semaine", "statut"]]

    return result


# === CHARGEMENT DES DONNÉES ===
@st.cache_data(show_spinner=False)
def load_data():
    df_pap = load_df_pap()
    df_activite_semaine = load_df_activite_semaine()
    df_contribution_semaine = load_df_contribution_semaine()
    ct_passage_pap = df_pap.sort_values(by=['passage_pap']).drop_duplicates(subset='collectivite_id', keep='first').copy()
    df_pap_statut_semaine = load_df_pap_statut_semaine()
    return df_pap, df_activite_semaine, df_contribution_semaine, ct_passage_pap, df_pap_statut_semaine

df_pap, df_activite_semaine, df_contribution_semaine, ct_passage_pap, df_pap_statut_semaine = load_data()

df = df_pap_statut_semaine \
    .sort_values(by=['semaine', 'collectivite_id'],ascending=[False, True]) \
    .drop_duplicates(subset=['collectivite_id'], keep='first')

nb_pap_actifs_actuels = df[df.statut=='actif'].shape[0]

# === INTERFACE DE CONFIGURATION ===
st.markdown("---")

# Paramètres interactifs en haut
col_param1, col_param2 = st.columns(2)

with col_param1:
    st.markdown("**Type d'activité sur les plans d'actions**")
    type_donnees = st.segmented_control(
        "Type de données",
        options=["🍿 Visite", "📝 Contribution"],
        default="🍿 Visite",
        label_visibility="collapsed"
    )

with col_param2:
    st.markdown("**Fenêtre glissante (en semaines)**")
    window = st.slider(
        "window",
        min_value=1,
        max_value=52,
        value=13,
        step=1,
        label_visibility="collapsed",
        help="Nombre de semaines pour la fenêtre glissante d'analyse"
    )

map_type_donnees = {"📝 Contribution": "contribution", "🍿 Visite": "visite"}

st.info(
    f"💡 Une collectivité est considérée comme active si elle a eu au moins "
    f"une **{map_type_donnees[type_donnees]}** dans les **{window} dernières semaines**."
)

# === CALCUL DES RÉSULTATS ===
with st.spinner("🔄 Calcul en cours..."):
    # Sélection du DataFrame approprié
    if type_donnees == "📝 Contribution":
        df_selected = df_contribution_semaine[["semaine", "collectivite_id"]]
        titre_graph = f"North Star - Contribution (fenêtre de {window} semaines)"
    else:
        df_selected = df_activite_semaine[["semaine", "collectivite_id"]]
        titre_graph = f"North Star - Visite (fenêtre de {window} semaines)"
    
    # Calcul du statut
    ct_pap_statut_semaine = compute_statut_pap(
        ct_passage_pap[["collectivite_id", "passage_pap"]], 
        df_selected, 
        window
    )
    
    # Conversion de la colonne semaine en datetime pour le graphique
    ct_pap_statut_semaine['semaine'] = pd.to_datetime(ct_pap_statut_semaine['semaine'])

# === AFFICHAGE DES RÉSULTATS ===
col_left, col_right = st.columns([1, 3])

with col_left:
    # Métriques récapitulatives
    with st.container(border=True):
        st.subheader("💡 Impact sur les PAP", divider="green")
        
        # Statistiques actuelles
        derniere_semaine = ct_pap_statut_semaine['semaine'].max()
        donnees_derniere_semaine = ct_pap_statut_semaine[
            ct_pap_statut_semaine['semaine'] == derniere_semaine
        ]
        
        nb_actifs = len(donnees_derniere_semaine[donnees_derniere_semaine['statut'] == 'actif'])
        nb_inactifs = len(donnees_derniere_semaine[donnees_derniere_semaine['statut'] == 'inactif'])

        total = nb_actifs + nb_inactifs

        delta = (nb_actifs-nb_pap_actifs_actuels)/nb_pap_actifs_actuels * 100 if total > 0 else 0
        
        st.markdown(f"**Dernière semaine ({derniere_semaine.strftime('%d/%m/%Y')}) :**")
        
        st.metric("✅ Actifs", nb_actifs, delta=f"{delta:.1f}% (par rapport au PAP 3 mois)")
        st.metric("❌ Inactifs", nb_inactifs)

with col_right:
    # Affichage du graphique
    with st.container(border=True):
        st.subheader("✨ Résultats", divider="blue")
        
        fig = plot_area_with_totals(
            df=ct_pap_statut_semaine,
            date_col="semaine",
            group_col="statut",
            time_granularity='W',
            cumulatif=False,
            min_date=ct_pap_statut_semaine['semaine'].min().strftime('%Y-%m-%d'),
            values_graph=False,
            objectif=500,
            title=titre_graph,
            legend_title="Statut"
        )
        
        st.plotly_chart(fig, use_container_width=True)