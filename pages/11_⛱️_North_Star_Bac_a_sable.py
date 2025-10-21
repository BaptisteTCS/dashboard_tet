import streamlit as st
import pandas as pd
import numpy as np

from utils.data import (
    load_df_pap,
    load_df_contribution_semaine,
    load_df_activite_semaine,
    load_df_pap_statut_semaine,
    load_df_fa_pilotable,
    load_df_fa_contribution_semaine,
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

def compute_statut_pap_par_proportion(
    df_contribution_semaine,      # cols: fiche_id, semaine
    nb_fiches_par_plan,           # cols: plan, nb_fiches
    df_fa_pilotable,              # cols: fiche_id, plan
    df_passage_pap,               # cols: plan, passage_pap (datetime-like)
    P=0.5,                        # fraction attendue, ex 0.5 pour 50%
    window_weeks=13,
    inclusive_current_week=True   # True: inclut la semaine courante dans la fenêtre. False: fenêtre strictement précédente
):
    # 1. Normalisation des dates et des clés
    act = df_contribution_semaine.copy()
    act["semaine"] = pd.to_datetime(act["semaine"]).dt.to_period("W").dt.start_time

    plan_map = df_fa_pilotable.copy()  # fiche_id -> plan
    pap = df_passage_pap.copy()
    pap["passage_pap"] = pd.to_datetime(pap["passage_pap"])
    pap["pap_week"] = pap["passage_pap"].dt.to_period("W").dt.start_time

    # 2. Horizon temporel
    if len(act) == 0:
        # pas d’activité, on retourne des plans inactifs à la semaine du pap uniquement
        base = pap[["plan", "pap_week"]].rename(columns={"pap_week": "semaine"}).copy()
        base["part_fiches_actives"] = 0.0
        base["statut"] = np.where(0 >= P, "actif", "inactif")
        return base[["plan", "semaine", "part_fiches_actives", "statut"]]

    last_week = act["semaine"].max()

    # 3. Actes filtrés pour ignorer ce qui est antérieur au passage au pap du plan
    #    On rattache chaque contribution à son plan puis on coupe avant pap_week
    act = act.merge(plan_map, on="fiche_id", how="left")
    act = act.merge(pap[["plan", "pap_week"]], on="plan", how="left")
    act = act[act["semaine"] >= act["pap_week"]]
    act = act[["fiche_id", "plan", "semaine"]].drop_duplicates()
    act["had_contribution"] = 1

    # 4. Grille hebdomadaire continue par fiche depuis le pap de son plan jusqu’à la dernière semaine
    #    On prend les fiches rattachées à un plan qui a un pap_week connu
    fiches_ok = plan_map.merge(pap[["plan", "pap_week"]], on="plan", how="inner")
    fiches_ok = fiches_ok.dropna(subset=["pap_week"]).copy()
    fiches_ok["n_weeks"] = ((last_week - fiches_ok["pap_week"]) // pd.Timedelta(weeks=1)) + 1
    fiches_ok = fiches_ok[fiches_ok["n_weeks"] > 0]

    fiches_ok["offsets"] = fiches_ok["n_weeks"].apply(lambda n: range(int(n)))
    grid_fiche = fiches_ok.explode("offsets", ignore_index=True)
    grid_fiche["semaine"] = grid_fiche["pap_week"] + pd.to_timedelta(grid_fiche["offsets"] * 7, unit="D")
    grid_fiche = grid_fiche[["fiche_id", "plan", "semaine"]]

    # 5. Marquer les semaines avec contribution puis calculer un flag actif par fiche via fenêtre glissante
    res_fiche = grid_fiche.merge(act[["fiche_id", "semaine", "had_contribution"]],
                                 on=["fiche_id", "semaine"], how="left")
    res_fiche["had_contribution"] = res_fiche["had_contribution"].fillna(0).astype(int)
    res_fiche = res_fiche.sort_values(["fiche_id", "semaine"]).copy()

    # Option d’exclusion de la semaine courante
    if inclusive_current_week:
        serie = res_fiche.groupby("fiche_id")["had_contribution"] \
                         .transform(lambda s: s.rolling(window=window_weeks, min_periods=1).sum())
    else:
        serie = res_fiche.groupby("fiche_id")["had_contribution"] \
                         .transform(lambda s: s.shift(1).rolling(window=window_weeks, min_periods=1).sum())

    res_fiche["fiche_active"] = (serie > 0).astype(int)

    # 6. Agrégation par plan et semaine
    agg_plan = res_fiche.groupby(["plan", "semaine"], as_index=False)["fiche_active"].sum() \
                        .rename(columns={"fiche_active": "nb_fiches_actives"})

    # 7. Denominateur et pourcentage de fiches actives
    denom = nb_fiches_par_plan.rename(columns={"plan": "plan", "nb_fiches": "nb_fiches_total"}).copy()
    agg_plan = agg_plan.merge(denom, on="plan", how="left")

    # Protection contre division par zéro
    agg_plan["nb_fiches_total"] = agg_plan["nb_fiches_total"].replace(0, np.nan)

    agg_plan["part_fiches_actives"] = agg_plan["nb_fiches_actives"] / agg_plan["nb_fiches_total"]
    agg_plan["part_fiches_actives"] = agg_plan["part_fiches_actives"].fillna(0.0)

    # 8. Statut du plan selon P
    agg_plan["statut"] = np.where(agg_plan["part_fiches_actives"] >= P, "actif", "inactif")

    # 9. Format final
    # garder la semaine en datetime de début de semaine, ou en string si tu préfères
    # agg_plan["semaine"] = agg_plan["semaine"].dt.strftime("%Y-%m-%d")

    return agg_plan[["plan", "semaine", "part_fiches_actives", "statut"]]

# === CHARGEMENT DES DONNÉES ===
@st.cache_data(show_spinner=False)
def load_data():
    df_pap = load_df_pap()
    df_activite_semaine = load_df_activite_semaine()
    df_contribution_semaine = load_df_contribution_semaine()
    ct_passage_pap = df_pap.sort_values(by=['passage_pap']).drop_duplicates(subset='collectivite_id', keep='first').copy()
    df_pap_statut_semaine = load_df_pap_statut_semaine()
    df_fa_pilotable = load_df_fa_pilotable()
    df_fa_contribution_semaine = load_df_fa_contribution_semaine()
    
    # Calcul des données supplémentaires pour la proportion
    nb_fiches_par_plan = df_fa_pilotable.groupby('plan')['fiche_id'].count().reset_index()
    nb_fiches_par_plan.columns = ['plan', 'nb_fiches']
    
    df_passage_pap = df_pap.sort_values(by=['passage_pap']).drop_duplicates(subset='collectivite_id', keep='first')[['plan', 'passage_pap']].copy()
    
    return df_pap, df_activite_semaine, df_contribution_semaine, ct_passage_pap, df_pap_statut_semaine, df_fa_pilotable, df_fa_contribution_semaine, nb_fiches_par_plan, df_passage_pap

df_pap, df_activite_semaine, df_contribution_semaine, ct_passage_pap, df_pap_statut_semaine, df_fa_pilotable, df_fa_contribution_semaine, nb_fiches_par_plan, df_passage_pap = load_data()

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

# Paramètres supplémentaires pour le mode Contribution
mode_calcul = "Simple"
proportion_value = 0.5

if type_donnees == "📝 Contribution":
    col_param3, col_param4 = st.columns(2)
    
    with col_param3:
        st.markdown("**Mode de calcul**")
        mode_calcul = st.segmented_control(
            "Mode de calcul",
            options=["Simple", "Proportion"],
            default="Simple",
            label_visibility="collapsed"
        )
    
    with col_param4:
        if mode_calcul == "Proportion":
            st.markdown("**Seuil de proportion (%)**")
            proportion_slider = st.slider(
                "proportion",
                min_value=10,
                max_value=100,
                value=50,
                step=5,
                label_visibility="collapsed",
                help="Pourcentage minimum de fiches actives pour qu'un plan soit considéré comme actif"
            )
            proportion_value = proportion_slider / 100.0
        else:
            st.markdown("**Seuil de proportion (%)**")
            st.markdown("_Non applicable en mode Simple_")

map_type_donnees = {"📝 Contribution": "contribution", "🍿 Visite": "visite"}

if type_donnees == "📝 Contribution" and mode_calcul == "Proportion":
    st.info(
        f"💡 Un plan d'action est considéré comme actif si au moins **{int(proportion_value*100)}%** de ses fiches "
        f"ont eu au moins une **contribution** dans les **{window} dernières semaines**."
    )
else:
    st.info(
        f"💡 Une collectivité est considérée comme active si elle a eu au moins "
        f"une **{map_type_donnees[type_donnees]}** dans les **{window} dernières semaines**."
    )

# === CALCUL DES RÉSULTATS ===
with st.spinner("🔄 Calcul en cours..."):
    # Sélection du DataFrame approprié et calcul du statut
    if type_donnees == "📝 Contribution" and mode_calcul == "Proportion":
        # Mode Proportion: calcul basé sur les plans d'actions
        titre_graph = f"North Star - Contribution par proportion (fenêtre de {window} semaines, seuil {int(proportion_value*100)}%)"
        
        # Utilisation de la fonction de calcul par proportion
        plan_statut_semaine = compute_statut_pap_par_proportion(
            df_fa_contribution_semaine[["fiche_id", "semaine"]],
            nb_fiches_par_plan,
            df_fa_pilotable[["fiche_id", "plan"]],
            df_passage_pap,
            P=proportion_value,
            window_weeks=window
        )
        
        # Conversion en format collectivité pour l'affichage
        # On associe chaque plan à sa collectivité
        plan_to_collectivite = df_pap[['plan', 'collectivite_id']].drop_duplicates()
        ct_pap_statut_semaine = plan_statut_semaine.merge(
            plan_to_collectivite,
            on='plan',
            how='left'
        )[['collectivite_id', 'semaine', 'statut']].dropna()
        
        # Conversion de la colonne semaine en datetime si nécessaire
        if not pd.api.types.is_datetime64_any_dtype(ct_pap_statut_semaine['semaine']):
            ct_pap_statut_semaine['semaine'] = pd.to_datetime(ct_pap_statut_semaine['semaine'])
        
    else:
        # Mode Simple (Visite ou Contribution simple)
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