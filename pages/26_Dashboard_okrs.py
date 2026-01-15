import streamlit as st

# Configuration de la page en premier
st.set_page_config(
    page_title="Dashboard OKRs",
    page_icon="🌠",
    layout="wide"
)

import pandas as pd
from streamlit_elements import elements, nivo, mui
from utils.db import read_table

# ==========================
# Chargement des données
# ==========================

@st.cache_resource(ttl="2d")
def load_data():
    df_nb_fap_13 = read_table('nb_fap_13')
    df_nb_fap_52 = read_table('nb_fap_52')
    df_nb_fap_pilote_13 = read_table('nb_fap_pilote_13')
    df_nb_fap_pilote_52 = read_table('nb_fap_pilote_52')
    df_pap_13 = read_table('okr_plan_actif_13')
    df_pap_52 = read_table('okr_plan_actif_52')
    df_pap_date_passage = read_table('pap_date_passage')
    df_pap_note = read_table('pap_note')
    df_fa_sharing = read_table('fa_sharing')
    df_activation_user = read_table('activation_user')
    df_activation_collectivite = read_table('activation_collectivite')
    df_activite_semaine = read_table('activite_semaine')
    return df_nb_fap_13, df_nb_fap_52, df_nb_fap_pilote_13, df_nb_fap_pilote_52, df_pap_13, df_pap_52, df_pap_date_passage, df_pap_note, df_fa_sharing, df_activation_user, df_activation_collectivite, df_activite_semaine


df_nb_fap_13, df_nb_fap_52, df_nb_fap_pilote_13, df_nb_fap_pilote_52, df_pap_13, df_pap_52, df_pap_date_passage, df_pap_note, df_fa_sharing, df_activation_user, df_activation_collectivite, df_activite_semaine = load_data()

# ==========================
# Thème graphique
# ==========================

theme_actif = {
    "text": {
        "fontFamily": "Source Sans Pro, sans-serif",
        "fontSize": 13,
        "fill": "#31333F"
    },
    "labels": {
        "text": {
            "fontFamily": "Source Sans Pro, sans-serif",
            "fontSize": 13,
            "fill": "#000000"
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
            "border": "1px solid rgba(0, 0, 0, 0.1)"
        }
    }
}

# ==========================
# Fonctions utilitaires
# ==========================

def afficher_metriques_temporelles(df, value_column, label_prefix="", date_column='mois_label'):
    """
    Affiche 4 métriques : Décembre 2023, 2024, 2025 et la valeur la plus récente.
    
    Paramètres:
    - df: DataFrame contenant les données
    - value_column: nom de la colonne contenant les valeurs à afficher
    - label_prefix: préfixe pour les labels des métriques (ex: "Actifs - ")
    - date_column: nom de la colonne contenant les dates (défaut: 'mois_label')
    """
    # Extraction des valeurs pour décembre de chaque année
    jan_2024 = df[df[date_column] == '2023-12'][value_column].values
    jan_2025 = df[df[date_column] == '2024-12'][value_column].values
    jan_2026 = df[df[date_column] == '2025-12'][value_column].values
    
    val_2024 = int(jan_2024[0]) if len(jan_2024) > 0 else 0
    val_2025 = int(jan_2025[0]) if len(jan_2025) > 0 else 0
    val_2026 = int(jan_2026[0]) if len(jan_2026) > 0 else 0
    
    # Trouver la valeur la plus récente
    if not df.empty and date_column in df.columns:
        df_sorted = df.sort_values(date_column, ascending=False)
        derniere_date = df_sorted.iloc[0][date_column]
        derniere_valeur = int(df_sorted.iloc[0][value_column])
        
        # Formater la date pour l'affichage (YYYY-MM -> Mois YYYY)
        mois_labels = {
            '01': 'Janvier', '02': 'Février', '03': 'Mars', '04': 'Avril',
            '05': 'Mai', '06': 'Juin', '07': 'Juillet', '08': 'Août',
            '09': 'Septembre', '10': 'Octobre', '11': 'Novembre', '12': 'Décembre'
        }
        if '-' in str(derniere_date):
            annee, mois = derniere_date.split('-')
            derniere_date_label = f"{mois_labels.get(mois, mois)} {annee}"
        else:
            derniere_date_label = str(derniere_date)
    else:
        derniere_valeur = 0
        derniere_date_label = "N/A"
    
    # Affichage des 4 colonnes
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(f"{label_prefix}Décembre 2023", val_2024)
    with col2:
        st.metric(f"{label_prefix}Décembre 2024", val_2025, delta=val_2025 - val_2024 if val_2024 > 0 else None)
    with col3:
        st.metric(f"{label_prefix}Décembre 2025", val_2026, delta=val_2026 - val_2025 if val_2025 > 0 else None)
    with col4:
        st.metric(f"{label_prefix}{derniere_date_label}", derniere_valeur, delta=derniere_valeur - val_2026 if val_2026 > 0 else None)


def preparer_donnees_graphique(df, x_column, y_column, group_column=None, group_values=None):
    """
    Prépare les données pour le graphique Nivo.
    
    Paramètres:
    - df: DataFrame contenant les données
    - x_column: nom de la colonne pour l'axe X
    - y_column: nom de la colonne pour l'axe Y
    - group_column: nom de la colonne pour grouper les séries (optionnel)
    - group_values: liste des valeurs à afficher dans l'ordre (optionnel, utilise toutes les valeurs si None)
    
    Retourne:
    - Liste de séries formatées pour Nivo
    """
    if group_column is None:
        # Une seule série
        return [{
            "id": y_column,
            "data": [
                {"x": row[x_column], "y": int(row[y_column])}
                for _, row in df.iterrows()
            ]
        }]
    else:
        # Plusieurs séries
        if group_values is None:
            group_values = df[group_column].unique().tolist()
        
        line_data = []
        for value in group_values:
            df_filtered = df[df[group_column] == value].copy()
            if not df_filtered.empty:
                line_data.append({
                    "id": str(value).capitalize(),
                    "data": [
                        {"x": row[x_column], "y": int(row[y_column])}
                        for _, row in df_filtered.iterrows()
                    ]
                })
        return line_data


def afficher_graphique_nivo(
    df,
    x_column,
    y_column,
    element_id,
    graph_type="area_stacked",
    group_column=None,
    group_values=None,
    legend_x="Mois",
    legend_y="Valeur",
    height=450,
    margin_right=110,
    color_scheme="pastel2"
):
    """
    Affiche un graphique Nivo Line avec différentes configurations.
    
    Paramètres:
    - df: DataFrame contenant les données
    - x_column: nom de la colonne pour l'axe X
    - y_column: nom de la colonne pour l'axe Y
    - element_id: identifiant unique pour le composant elements
    - graph_type: type de graphique ("area_stacked", "area_simple", "line")
    - group_column: nom de la colonne pour grouper les séries (optionnel)
    - group_values: liste des valeurs à afficher dans l'ordre (optionnel)
    - legend_x: légende de l'axe X
    - legend_y: légende de l'axe Y
    - height: hauteur du graphique
    - margin_right: marge à droite pour la légende
    - color_scheme: schéma de couleurs Nivo
    """
    if df.empty:
        st.info("Aucune donnée disponible pour le graphique d'évolution.")
        return
    
    # Préparer les données
    line_data = preparer_donnees_graphique(df, x_column, y_column, group_column, group_values)
    
    if not line_data:
        st.info("Aucune donnée disponible pour le graphique d'évolution.")
        return
    
    # Configuration selon le type de graphique
    if graph_type == "area_stacked":
        enable_area = True
        enable_points = False
        y_scale_stacked = True
        area_opacity = 0.7
    elif graph_type == "area_simple":
        enable_area = True
        enable_points = False
        y_scale_stacked = False
        area_opacity = 0.7
    else:  # line
        enable_area = False
        enable_points = True
        y_scale_stacked = False
        area_opacity = 0
    
    # Affichage du graphique
    with elements(element_id):
        with mui.Box(sx={"height": height}):
            config = {
                "data": line_data,
                "margin": {"top": 20, "right": margin_right, "bottom": 60, "left": 60},
                "xScale": {"type": "point"},
                "yScale": {"type": "linear", "min": 0, "max": "auto", "stacked": y_scale_stacked, "reverse": False},
                "curve": "monotoneX",
                "axisTop": None,
                "axisRight": None,
                "axisBottom": {
                    "tickSize": 5,
                    "tickPadding": 5,
                    "tickRotation": -45,
                    "legend": legend_x,
                    "legendOffset": 50,
                    "legendPosition": "middle"
                },
                "axisLeft": {
                    "tickSize": 5,
                    "tickPadding": 5,
                    "tickRotation": 0,
                    "legend": legend_y,
                    "legendOffset": -50,
                    "legendPosition": "middle"
                },
                "enableArea": enable_area,
                "areaOpacity": area_opacity,
                "enablePoints": enable_points,
                "useMesh": True,
                "enableSlices": "x",
                "legends": [
                    {
                        "anchor": "bottom-right",
                        "direction": "column",
                        "justify": False,
                        "translateX": 100,
                        "translateY": 0,
                        "itemsSpacing": 2,
                        "itemWidth": 80,
                        "itemHeight": 20,
                        "itemDirection": "left-to-right",
                        "itemOpacity": 0.85,
                        "symbolSize": 12,
                        "symbolShape": "circle",
                    }
                ],
                "colors": {"scheme": color_scheme},
                "theme": theme_actif,
            }
            
            # Ajouter les paramètres spécifiques pour line chart
            if graph_type == "line":
                config["pointSize"] = 6
                config["pointBorderWidth"] = 2
                config["pointBorderColor"] = {"from": "serieColor"}
            
            nivo.Line(**config)


# ==========================
# Interface
# ==========================

st.title("🌠 Dashboard OKRs")
tabs = st.tabs(["1 - Activation", "2 - Rétention", "3 - Qualité", "5 - Légitimité"])

# ==========================
# TAB 1 : ACTIVATION
# ==========================

with tabs[0]:

    st.markdown("## Objectif 1 : ACTIVATION")
    st.markdown("Permettre à chaque collectivité territoriale française de piloter ses plans & actions.")

    # ======================
    st.markdown("### A-1 (⭐ NS1 - externe)  : Nombre de collectivités avec ≥1 Plan d'Action Pilotable (PAP) dont actifs ≤1 an (12 mois | 52 semaines)")

    # Préparation des données
    df_evolution_statut = df_pap_52.copy()
    df_evolution_statut['semaine'] = pd.to_datetime(df_evolution_statut['semaine'])
    df_evolution_statut['mois'] = df_evolution_statut['semaine'].dt.to_period('M').dt.to_timestamp()
    df_evolution_statut = df_evolution_statut.sort_values('statut').drop_duplicates(subset=['collectivite_id', 'mois'], keep='first')
    df_evolution_statut = df_evolution_statut[df_evolution_statut['mois'] >= '2023-01-01']
    df_evolution_statut = df_evolution_statut.groupby(['mois', 'statut'])['collectivite_id'].nunique().reset_index(name='nb_collectivites')
    df_evolution_statut = df_evolution_statut.sort_values('mois')
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].dt.strftime('%Y-%m')

    # Métriques
    df_actif = df_evolution_statut[df_evolution_statut['statut'] == 'actif']
    afficher_metriques_temporelles(df_actif, 'nb_collectivites', label_prefix="Actifs - ")

    # Graphique
    afficher_graphique_nivo(
        df_evolution_statut,
        x_column='mois_label',
        y_column='nb_collectivites',
        element_id="line_evolution_statuts_pap_52",
        graph_type="area_stacked",
        group_column='statut',
        group_values=["actif", "inactif"],
        legend_y="Nombre de collectivités"
    )


    # ======================
    st.markdown("### A-2 (🌟 NS1 - interne)  : Nombre de collectivités avec ≥1 Plan d'Action Pilotable (PAP) actif ≤3 mois")

    # Préparation des données
    df_evolution_statut = df_pap_13.copy()
    df_evolution_statut['semaine'] = pd.to_datetime(df_evolution_statut['semaine'])
    df_evolution_statut['mois'] = df_evolution_statut['semaine'].dt.to_period('M').dt.to_timestamp()
    df_evolution_statut = df_evolution_statut.sort_values('statut').drop_duplicates(subset=['collectivite_id', 'mois'], keep='first')
    df_evolution_statut = df_evolution_statut[df_evolution_statut['mois'] >= '2023-01-01']
    df_evolution_statut = df_evolution_statut.groupby(['mois', 'statut'])['collectivite_id'].nunique().reset_index(name='nb_collectivites')
    df_evolution_statut = df_evolution_statut.sort_values('mois')
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].dt.strftime('%Y-%m')

    # Métriques
    df_actif = df_evolution_statut[df_evolution_statut['statut'] == 'actif']
    afficher_metriques_temporelles(df_actif, 'nb_collectivites', label_prefix="Actifs - ")

    # Graphique
    afficher_graphique_nivo(
        df_evolution_statut,
        x_column='mois_label',
        y_column='nb_collectivites',
        element_id="line_evolution_statuts_pap_13",
        graph_type="area_stacked",
        group_column='statut',
        group_values=["actif", "inactif"],
        legend_y="Nombre de collectivités"
    )


    # ======================
    st.markdown("### A-3 (💫 - Activité) Nombre d'Actions pilotables actives ≤3 mois")

    # Préparation des données
    df_evolution_statut = df_nb_fap_13.copy()
    df_evolution_statut['mois'] = pd.to_datetime(df_evolution_statut['mois'])
    df_evolution_statut = df_evolution_statut[df_evolution_statut['mois'] >= '2023-12-01']
    df_evolution_statut = df_evolution_statut.sort_values('mois')
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].dt.strftime('%Y-%m')

    # Métriques
    df_actif = df_evolution_statut[df_evolution_statut['statut'] == 'actif']
    afficher_metriques_temporelles(df_actif, 'fiche_id', label_prefix="Actifs - ")

    # Graphique
    afficher_graphique_nivo(
        df_evolution_statut,
        x_column='mois_label',
        y_column='fiche_id',
        element_id="line_evolution_statuts_fap_13",
        graph_type="area_stacked",
        group_column='statut',
        group_values=["actif", "inactif"],
        legend_y="Nombre d'actions pilotables actives"
    )


    # ======================
    st.markdown("### A-3 (bis) (💫 - Activité) Nombre d'Actions pilotables actives ≤12 mois")

    # Préparation des données
    df_evolution_statut = df_nb_fap_52.copy()
    df_evolution_statut['mois'] = pd.to_datetime(df_evolution_statut['mois'])
    df_evolution_statut = df_evolution_statut[df_evolution_statut['mois'] >= '2023-12-01']
    df_evolution_statut = df_evolution_statut.sort_values('mois')
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].dt.strftime('%Y-%m')

    # Métriques
    df_actif = df_evolution_statut[df_evolution_statut['statut'] == 'actif']
    afficher_metriques_temporelles(df_actif, 'fiche_id', label_prefix="Actifs - ")

    # Graphique
    afficher_graphique_nivo(
        df_evolution_statut,
        x_column='mois_label',
        y_column='fiche_id',
        element_id="line_evolution_statuts_fap_52",
        graph_type="area_stacked",
        group_column='statut',
        group_values=["actif", "inactif"],
        legend_y="Nombre d'actions pilotables actives"
    )


    # ======================
    st.markdown("### A-4 (🎇 - Exploration) : Nombre de PAP initialisés de façon autonome")

    # Préparation des données
    df_evolution_statut = df_pap_date_passage.copy()
    df_evolution_statut['passage_pap'] = pd.to_datetime(df_evolution_statut['passage_pap'])
    df_evolution_statut['mois'] = df_evolution_statut['passage_pap'].dt.to_period('M').dt.to_timestamp()
    df_evolution_statut = df_evolution_statut[df_evolution_statut['mois'] >= '2023-01-01']
    df_evolution_statut = df_evolution_statut.sort_values('mois')
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].dt.strftime('%Y-%m')

    # Métriques (Autonomes uniquement)
    df_autonomes = df_evolution_statut[df_evolution_statut['import'] == 'Autonome'].groupby(['mois'])['plan'].nunique().reset_index(name='nb_plans_autonomes')
    df_autonomes = df_autonomes.sort_values('mois')
    df_autonomes['nb_plans_autonomes_cumul'] = df_autonomes['nb_plans_autonomes'].cumsum()
    df_autonomes['mois_label'] = df_autonomes['mois'].dt.strftime('%Y-%m')
    afficher_metriques_temporelles(df_autonomes, 'nb_plans_autonomes_cumul', label_prefix="PAP Autonomes - ")

    # Préparer les données pour le graphique cumulé
    df_graph = df_evolution_statut.groupby(['mois', 'mois_label', 'import'])['plan'].nunique().reset_index(name='nb_plans')
    df_graph = df_graph.sort_values('mois')
    tous_les_mois = df_graph.sort_values('mois')['mois_label'].unique().tolist()
    
    # Calculer le cumulé par type d'import
    df_graph_cumul = []
    for import_type in ["Autonome", "Importé"]:
        df_type = df_graph[df_graph['import'] == import_type].copy()
        valeurs_par_mois = dict(zip(df_type['mois_label'], df_type['nb_plans']))
        cumul = 0
        for mois in tous_les_mois:
            valeur_mois = valeurs_par_mois.get(mois, 0)
            cumul += valeur_mois
            df_graph_cumul.append({
                'mois_label': mois,
                'import': import_type,
                'nb_plans_cumul': cumul
            })
    df_graph_cumul = pd.DataFrame(df_graph_cumul)

    # Graphique
    afficher_graphique_nivo(
        df_graph_cumul,
        x_column='mois_label',
        y_column='nb_plans_cumul',
        element_id="line_evolution_autonome",
        graph_type="area_stacked",
        group_column='import',
        group_values=["Autonome", "Importé"],
        legend_y="Nombre de PAP (cumulé)"
    )


# ==========================
# TAB 2 : RÉTENTION
# ==========================

with tabs[1]:

    st.markdown('## Objectif 2 : RÉTENTION')
    st.markdown('Faciliter la transversalité entre Plans & Actions & Contributeurs')

    # ======================
    st.markdown('### R-1 (⭐ NS2 - externe) : Nombre de CT avec ≥ 2 PAP avec contribution active 12 mois')

    # Préparation des données
    df_evolution_statut = df_pap_52.copy()
    df_evolution_statut['semaine'] = pd.to_datetime(df_evolution_statut['semaine'])
    df_evolution_statut['mois'] = df_evolution_statut['semaine'].dt.to_period('M').dt.to_timestamp()
    count_pap = df_evolution_statut.groupby(['mois', 'statut', 'collectivite_id'])['plan_id'].nunique().reset_index(name='nb_paps')
    count_pap = count_pap[(count_pap['nb_paps'] >= 2) & (count_pap['statut'] == 'actif')]
    df_evolution_statut = df_evolution_statut[df_evolution_statut['mois'] >= '2023-01-01']
    df_evolution_statut = df_evolution_statut.merge(count_pap, on=['mois', 'statut', 'collectivite_id'], how='inner')
    df_evolution_statut = df_evolution_statut.groupby(['mois', 'statut'])['collectivite_id'].nunique().reset_index(name='nb_collectivites')
    df_evolution_statut = df_evolution_statut.sort_values('mois')
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].dt.strftime('%Y-%m')

    # Métriques
    df_actif = df_evolution_statut[df_evolution_statut['statut'] == 'actif']
    afficher_metriques_temporelles(df_actif, 'nb_collectivites', label_prefix="")

    # Graphique
    afficher_graphique_nivo(
        df_evolution_statut,
        x_column='mois_label',
        y_column='nb_collectivites',
        element_id="line_evolution_statuts_pap_52_fois_2",
        graph_type="area_stacked",
        group_column='statut',
        group_values=["actif", "inactif"],
        legend_y="Nombre de collectivités"
    )


    # ======================
    st.markdown("---")
    st.markdown('### R-2 (🌟 NS2 - interne) : Nombre de CT avec ≥ 2 PAP avec contribution active 3 mois (dont avec/sans ≥2 pilotes de plans différents)')

    # Préparation des données
    df_evolution_statut = df_pap_13.copy()
    df_evolution_statut['semaine'] = pd.to_datetime(df_evolution_statut['semaine'])
    df_evolution_statut['mois'] = df_evolution_statut['semaine'].dt.to_period('M').dt.to_timestamp()
    count_pap = df_evolution_statut.groupby(['mois', 'statut', 'collectivite_id'])['plan_id'].nunique().reset_index(name='nb_paps')
    count_pap = count_pap[(count_pap['nb_paps'] >= 2) & (count_pap['statut'] == 'actif')]
    df_evolution_statut = df_evolution_statut[df_evolution_statut['mois'] >= '2023-01-01']
    df_evolution_statut = df_evolution_statut.merge(count_pap, on=['mois', 'statut', 'collectivite_id'], how='inner')
    df_evolution_statut['multi_pilotes'] = df_evolution_statut['nb_pilotes'].apply(lambda x: '>= 2 pilotes' if x>1 else '1 pilote ou moins')
    df_evolution_statut = df_evolution_statut.groupby(['mois', 'statut', 'multi_pilotes'])['collectivite_id'].nunique().reset_index(name='nb_collectivites')
    df_evolution_statut = df_evolution_statut.sort_values('mois')
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].dt.strftime('%Y-%m')

    # Métriques
    df_actif = df_evolution_statut[df_evolution_statut['statut'] == 'actif']
    afficher_metriques_temporelles(df_actif, 'nb_collectivites', label_prefix="")

    # Préparer les données complètes (boucher les trous)
    tous_les_mois = df_evolution_statut.sort_values('mois')['mois_label'].unique().tolist()
    df_graph_complet = []
    for statut_val in [">= 2 pilotes", "1 pilote ou moins"]:
        df_statut = df_evolution_statut[df_evolution_statut['multi_pilotes'] == statut_val].copy()
        valeurs_par_mois = dict(zip(df_statut['mois_label'], df_statut['nb_collectivites']))
        for mois in tous_les_mois:
            df_graph_complet.append({
                'mois_label': mois,
                'multi_pilotes': statut_val,
                'nb_collectivites': valeurs_par_mois.get(mois, 0)
            })
    df_graph_complet = pd.DataFrame(df_graph_complet)

    # Graphique
    afficher_graphique_nivo(
        df_graph_complet,
        x_column='mois_label',
        y_column='nb_collectivites',
        element_id="line_evolution_statuts_pap_13_fois_2",
        graph_type="area_stacked",
        group_column='multi_pilotes',
        group_values=[">= 2 pilotes", "1 pilote ou moins"],
        legend_y="Nombre de collectivités",
        margin_right=160
    )


    # ======================
    st.markdown("---")
    st.markdown('### R-3 (💫 - Activité) : Nombre d\'Actions pilotables actives avec pilote de l\'action actif ≤ 3 mois')

    # Préparation des données
    df_evolution_statut = df_nb_fap_pilote_13.copy()
    df_evolution_statut['mois'] = pd.to_datetime(df_evolution_statut['mois'])
    df_evolution_statut = df_evolution_statut[df_evolution_statut['mois'] >= '2023-12-01']
    df_evolution_statut = df_evolution_statut.sort_values('mois')
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].dt.strftime('%Y-%m')

    # Métriques
    df_actif = df_evolution_statut[df_evolution_statut['statut'] == 'actif']
    afficher_metriques_temporelles(df_actif, 'fiche_id', label_prefix="Actifs - ")

    # Graphique
    afficher_graphique_nivo(
        df_evolution_statut,
        x_column='mois_label',
        y_column='fiche_id',
        element_id="line_evolution_statuts_fap_pilote_13",
        graph_type="area_stacked",
        group_column='statut',
        group_values=["actif", "inactif"],
        legend_y="Nombre d'actions pilotables actives"
    )


    # ======================
    st.markdown("### R-3 (bis) (💫 - Activité) : Nombre d'Actions pilotables actives avec pilote de l'action actif ≤ 12 mois")

    # Préparation des données
    df_evolution_statut = df_nb_fap_pilote_52.copy()
    df_evolution_statut['mois'] = pd.to_datetime(df_evolution_statut['mois'])
    df_evolution_statut = df_evolution_statut[df_evolution_statut['mois'] >= '2023-12-01']
    df_evolution_statut = df_evolution_statut.sort_values('mois')
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].dt.strftime('%Y-%m')

    # Métriques
    df_actif = df_evolution_statut[df_evolution_statut['statut'] == 'actif']
    afficher_metriques_temporelles(df_actif, 'fiche_id', label_prefix="Actifs - ")

    # Graphique
    afficher_graphique_nivo(
        df_evolution_statut,
        x_column='mois_label',
        y_column='fiche_id',
        element_id="line_evolution_statuts_fap_pilote_52",
        graph_type="area_stacked",
        group_column='statut',
        group_values=["actif", "inactif"],
        legend_y="Nombre d'actions pilotables actives"
    )


    # ======================
    st.markdown("---")
    st.markdown("### R-4 (🎇 - Exploration) : Nombre d'actions partagées/liées entre collectivités")

    # Préparation des données
    df_evolution_statut = df_fa_sharing.copy()
    df_evolution_statut = df_evolution_statut.sort_values('mois')
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].dt.strftime('%Y-%m')

    # Graphique (area simple)
    afficher_graphique_nivo(
        df_evolution_statut,
        x_column='mois_label',
        y_column='nb_fa_shared',
        element_id="line_evolution_statuts_fa_sharing",
        graph_type="area_simple",
        legend_y="Nombre de FA partagées"
    )


# ==========================
# TAB 3 : QUALITÉ
# ==========================

with tabs[2]:

    st.markdown('## Objectif 3 : QUALITÉ')
    st.markdown('Augmenter la qualité des Plans & Actions')
    st.markdown('### Définition de la note des PAP')
    st.markdown(
    """
    Une fiche action est jugée sur 5 axes, et 6 si la collectivité est engagée dans le programme TETE : 
    - **Pilotabilité :** la fiche a un titre, une description, un statut et un pilote.
    - **Indicateurs :** la fiche est liée à au moins un indicateur.
    - **Objectifs :** les indicateurs liés ont au moins un objectif associé.
    - **Avancement :** la fiche action a au moins une étape renseignée ou une note de suivi.
    - **Budget :** la fiche action a la colonne "budget previsionnel" renseignée (à vérifier avec les devs la relation avec la table budget)
    - **Référentiel (collectivité TETE uniquement) :** la fiche action est liée à au moins une mesure du référentiel.

    Pour chaque fiche, on attribue 0 ou 1 à l'axe suivant si la condition est respectée. On obtient alors une note sur 5, et 6 pour les collectivités engagées TETE qu'on remene sur 5 (ex: 3/6 -> 2.5/5).

    On calcule ensuite la moyenne des notes de toute les fiches du plan pour déterminer la note du plan.

    La meilleur note parmi toutes les notes des plans d'une collectivité devient **LA** note de la collectivité.
    """)

    # ======================
    st.markdown('---')
    st.markdown('### Q-1 (⭐ NS3 - externe) : Nombre de PAP ayant un Score de complétude ≥ 2,5 (score ≥50%)')
    
    # Préparation des données
    df_evolution_statut = df_pap_note.copy()
    df_evolution_statut['semaine'] = pd.to_datetime(df_evolution_statut['semaine'])
    df_evolution_statut['mois'] = df_evolution_statut['semaine'].dt.to_period('M').dt.to_timestamp()
    df_evolution_statut = df_evolution_statut.sort_values('score', ascending=False).drop_duplicates(subset=['plan_id', 'mois'], keep='first')
    df_evolution_statut = df_evolution_statut[df_evolution_statut['mois'] >= '2023-01-01']
    df_evolution_statut['statut'] = df_evolution_statut['score'].apply(lambda x: "Score >=50%" if x>=2 else "Score <50%")
    df_evolution_statut = df_evolution_statut.groupby(['mois', 'statut'])['plan_id'].nunique().reset_index(name='nb_plans')
    df_evolution_statut = df_evolution_statut.sort_values('mois')
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].dt.strftime('%Y-%m')

    # Métriques
    df_actif = df_evolution_statut[df_evolution_statut['statut'] == 'Score >=50%']
    may_2025 = df_actif[df_actif['mois_label'] == '2025-05']['nb_plans'].values
    dec_2025 = df_actif[df_actif['mois_label'] == '2025-12']['nb_plans'].values
    
    val_may_2025 = int(may_2025[0]) if len(may_2025) > 0 else 0
    val_dec_2025 = int(dec_2025[0]) if len(dec_2025) > 0 else 0
    
    # Trouver la valeur la plus récente
    if not df_actif.empty:
        df_actif_sorted = df_actif.sort_values('mois_label', ascending=False)
        derniere_date = df_actif_sorted.iloc[0]['mois_label']
        derniere_valeur = int(df_actif_sorted.iloc[0]['nb_plans'])
        
        # Formater la date pour l'affichage
        mois_labels = {
            '01': 'Janvier', '02': 'Février', '03': 'Mars', '04': 'Avril',
            '05': 'Mai', '06': 'Juin', '07': 'Juillet', '08': 'Août',
            '09': 'Septembre', '10': 'Octobre', '11': 'Novembre', '12': 'Décembre'
        }
        annee, mois = derniere_date.split('-')
        derniere_date_label = f"{mois_labels.get(mois, mois)} {annee}"
    else:
        derniere_valeur = 0
        derniere_date_label = "N/A"
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Score >=50% - Mai 2025", val_may_2025)
    with col2:
        st.metric("Score >=50% - Décembre 2025", val_dec_2025, delta=val_dec_2025 - val_may_2025 if val_may_2025 > 0 else None)
    with col3:
        st.metric(f"Score >=50% - {derniere_date_label}", derniere_valeur, delta=derniere_valeur - val_dec_2025 if val_dec_2025 > 0 else None)

    # Graphique
    afficher_graphique_nivo(
        df_evolution_statut,
        x_column='mois_label',
        y_column='nb_plans',
        element_id="line_evolution_statuts_pap_note_13",
        graph_type="area_stacked",
        group_column='statut',
        group_values=["Score >=50%", "Score <50%"],
        legend_y="Nombre de PAP"
    )


    # ======================
    st.markdown('---')
    st.markdown('### Q-2 (🌟 NS3 - interne) : Nombre de PAP ayant un Score de complétude ≥3.2 (score ≥80%)')

    # Préparation des données
    df_evolution_statut = df_pap_note.copy()
    df_evolution_statut['semaine'] = pd.to_datetime(df_evolution_statut['semaine'])
    df_evolution_statut['mois'] = df_evolution_statut['semaine'].dt.to_period('M').dt.to_timestamp()
    df_evolution_statut = df_evolution_statut.sort_values('score', ascending=False).drop_duplicates(subset=['plan_id', 'mois'], keep='first')
    df_evolution_statut = df_evolution_statut[df_evolution_statut['mois'] >= '2023-01-01']
    df_evolution_statut['statut'] = df_evolution_statut['score'].apply(lambda x: "Score >=80%" if x>=3.2 else "Score <80%")
    df_evolution_statut = df_evolution_statut.groupby(['mois', 'statut'])['plan_id'].nunique().reset_index(name='nb_plans')
    df_evolution_statut = df_evolution_statut.sort_values('mois')
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].dt.strftime('%Y-%m')

    # Métriques
    df_actif = df_evolution_statut[df_evolution_statut['statut'] == 'Score >=80%']
    may_2025 = df_actif[df_actif['mois_label'] == '2025-05']['nb_plans'].values
    dec_2025 = df_actif[df_actif['mois_label'] == '2025-12']['nb_plans'].values
    
    val_may_2025 = int(may_2025[0]) if len(may_2025) > 0 else 0
    val_dec_2025 = int(dec_2025[0]) if len(dec_2025) > 0 else 0
    
    # Trouver la valeur la plus récente
    if not df_actif.empty:
        df_actif_sorted = df_actif.sort_values('mois_label', ascending=False)
        derniere_date = df_actif_sorted.iloc[0]['mois_label']
        derniere_valeur = int(df_actif_sorted.iloc[0]['nb_plans'])
        
        # Formater la date pour l'affichage
        mois_labels = {
            '01': 'Janvier', '02': 'Février', '03': 'Mars', '04': 'Avril',
            '05': 'Mai', '06': 'Juin', '07': 'Juillet', '08': 'Août',
            '09': 'Septembre', '10': 'Octobre', '11': 'Novembre', '12': 'Décembre'
        }
        annee, mois = derniere_date.split('-')
        derniere_date_label = f"{mois_labels.get(mois, mois)} {annee}"
    else:
        derniere_valeur = 0
        derniere_date_label = "N/A"
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Score >=80% - Mai 2025", val_may_2025)
    with col2:
        st.metric("Score >=80% - Décembre 2025", val_dec_2025, delta=val_dec_2025 - val_may_2025 if val_may_2025 > 0 else None)
    with col3:
        st.metric(f"Score >=80% - {derniere_date_label}", derniere_valeur, delta=derniere_valeur - val_dec_2025 if val_dec_2025 > 0 else None)

    # Graphique
    afficher_graphique_nivo(
        df_evolution_statut,
        x_column='mois_label',
        y_column='nb_plans',
        element_id="line_evolution_statuts_pap_note_13_80pct",
        graph_type="area_stacked",
        group_column='statut',
        group_values=["Score >=80%", "Score <80%"],
        legend_y="Nombre de PAP"
    )


# ==========================
# TAB 4 : LÉGITIMITÉ
# ==========================

with tabs[3]:

    # ======================
    st.markdown("### L-1 (⭐ NS5 - externe - Acquisition) : Nombre d'utilisateurs activés")

    # Préparation des données
    df_evolution_statut = df_activation_user.copy()
    df_evolution_statut = df_evolution_statut.sort_values('mois')
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].dt.strftime('%Y-%m')

    afficher_metriques_temporelles(df_evolution_statut, 'nb_users', label_prefix="Actifs - ")

    # Graphique (area simple)
    afficher_graphique_nivo(
        df_evolution_statut,
        x_column='mois_label',
        y_column='nb_users',
        element_id="line_evolution_statuts_activation_user",
        graph_type="area_simple",
        legend_y="Nombre d'utilisateurs activés",
        margin_right=180
    )


    # ======================
    st.markdown('### L-1 (bis) (⭐ NS5 - externe - Acquisition) : Nombre de collectivités activées')

    # Préparation des données
    df_evolution_statut = df_activation_collectivite.copy()
    df_evolution_statut = df_evolution_statut.sort_values('mois')
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].dt.strftime('%Y-%m')

    # Métriques (3 colonnes pour cette section)
    afficher_metriques_temporelles(df_evolution_statut, 'nb_collectivite', label_prefix="Actifs - ")

    # Graphique (area simple)
    afficher_graphique_nivo(
        df_evolution_statut,
        x_column='mois_label',
        y_column='nb_collectivite',
        element_id="line_evolution_statuts_activation_collectivite",
        graph_type="area_simple",
        legend_y="Nombre de collectivités activées",
        margin_right=180
    )


    # ======================
    st.markdown("---")
    st.markdown('### L-2 (🌟 NS5 - interne - Stickyness) : Nombre de collectivités actives')

    # Segmented control
    periode_aggregation = st.segmented_control(
        "Période d'agrégation",
        options=["Année", "Mois", "Semaine"],
        default="Mois",
        label_visibility="collapsed"
    )

    # Préparation des données
    df_evolution_statut = df_activite_semaine.copy()
    df_evolution_statut = df_evolution_statut[df_evolution_statut['semaine'] >= '2024-01-01'].copy()
    df_evolution_statut = df_evolution_statut.sort_values('semaine')
    df_evolution_statut['semaine'] = pd.to_datetime(df_evolution_statut['semaine'])
    df_evolution_statut['annee'] = df_evolution_statut['semaine'].dt.year
    
    if periode_aggregation == "Année":
        df_evolution_statut['periode_label'] = df_evolution_statut['semaine'].dt.strftime('%Y')
        df_evolution_statut['periode_sort'] = df_evolution_statut['semaine'].dt.year
        legende_x = "Année"
    elif periode_aggregation == "Mois":
        df_evolution_statut['periode_label'] = df_evolution_statut['semaine'].dt.strftime('%m')
        df_evolution_statut['periode_sort'] = df_evolution_statut['semaine'].dt.month
        legende_x = "Mois"
    else:  # Semaine
        df_evolution_statut['periode_label'] = df_evolution_statut['semaine'].dt.strftime('S%U')
        df_evolution_statut['periode_sort'] = df_evolution_statut['semaine'].dt.isocalendar().week
        legende_x = "Semaine"

    df_evolution_statut = df_evolution_statut.groupby(['annee', 'periode_label', 'periode_sort'])['collectivite_id'].nunique().reset_index(name='nb_collectivites')
    df_evolution_statut = df_evolution_statut.sort_values(['annee', 'periode_sort'])

    # Calculer moyennes mensuelles
    df_moyennes = df_activite_semaine.copy()
    df_moyennes = df_moyennes[df_moyennes['semaine'] >= '2024-01-01'].copy()
    df_moyennes['semaine'] = pd.to_datetime(df_moyennes['semaine'])
    df_moyennes['annee'] = df_moyennes['semaine'].dt.year
    df_moyennes['mois'] = df_moyennes['semaine'].dt.to_period('M')
    df_moyennes = df_moyennes.groupby(['annee', 'mois'])['collectivite_id'].nunique().reset_index(name='nb_collectivites')
    moyennes_annuelles = df_moyennes.groupby('annee')['nb_collectivites'].mean().round(0)
    
    moy_2024 = moyennes_annuelles.get(2024, 0)
    moy_2025 = moyennes_annuelles.get(2025, 0)
    moy_2026 = moyennes_annuelles.get(2026, 0)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Moyenne mensuelle 2024", f"{moy_2024:.0f}")
    with col2:
        delta_2025 = moy_2025 - moy_2024 if moy_2024 > 0 else None
        st.metric("Moyenne mensuelle 2025", f"{moy_2025:.0f}", delta=f"{delta_2025:.0f}" if delta_2025 is not None else None)
    with col3:
        delta_2026 = moy_2026 - moy_2025 if moy_2025 > 0 else None
        st.metric("Moyenne mensuelle 2026", f"{moy_2026:.0f}", delta=f"{delta_2026:.0f}" if delta_2026 is not None else None)

    # Graphique line chart
    afficher_graphique_nivo(
        df_evolution_statut,
        x_column='periode_label',
        y_column='nb_collectivites',
        element_id="line_evolution_collectivites_actives_par_semaine",
        graph_type="line",
        group_column='annee',
        legend_x=legende_x,
        legend_y="Nombre de collectivités actives",
        margin_right=180,
        color_scheme="category10"
    )


    # ======================
    st.markdown('### L-2 (🌟 NS5 - interne - Stickyness) : Nombre de users actifs')

    # Segmented control
    periode_aggregation_2 = st.segmented_control(
        "Période d'agrégation",
        options=["Année", "Mois", "Semaine"],
        default="Mois",
        label_visibility="collapsed",
        key="periode_aggregation_2"
    )

    # Préparation des données
    df_evolution_statut = df_activite_semaine.copy()
    df_evolution_statut = df_evolution_statut[df_evolution_statut['semaine'] >= '2024-01-01'].copy()
    df_evolution_statut = df_evolution_statut.sort_values('semaine')
    df_evolution_statut['semaine'] = pd.to_datetime(df_evolution_statut['semaine'])
    df_evolution_statut['annee'] = df_evolution_statut['semaine'].dt.year
    
    if periode_aggregation_2 == "Année":
        df_evolution_statut['periode_label'] = df_evolution_statut['semaine'].dt.strftime('%Y')
        df_evolution_statut['periode_sort'] = df_evolution_statut['semaine'].dt.year
        legende_x = "Année"
    elif periode_aggregation_2 == "Mois":
        df_evolution_statut['periode_label'] = df_evolution_statut['semaine'].dt.strftime('%m')
        df_evolution_statut['periode_sort'] = df_evolution_statut['semaine'].dt.month
        legende_x = "Mois"
    else:  # Semaine
        df_evolution_statut['periode_label'] = df_evolution_statut['semaine'].dt.strftime('S%U')
        df_evolution_statut['periode_sort'] = df_evolution_statut['semaine'].dt.isocalendar().week
        legende_x = "Semaine"

    df_evolution_statut = df_evolution_statut.groupby(['annee', 'periode_label', 'periode_sort'])['email'].nunique().reset_index(name='nb_users')
    df_evolution_statut = df_evolution_statut.sort_values(['annee', 'periode_sort'])

    # Calculer moyennes mensuelles
    df_moyennes = df_activite_semaine.copy()
    df_moyennes = df_moyennes[df_moyennes['semaine'] >= '2024-01-01'].copy()
    df_moyennes['semaine'] = pd.to_datetime(df_moyennes['semaine'])
    df_moyennes['annee'] = df_moyennes['semaine'].dt.year
    df_moyennes['mois'] = df_moyennes['semaine'].dt.to_period('M')
    df_moyennes = df_moyennes.groupby(['annee', 'mois'])['email'].nunique().reset_index(name='nb_users')
    moyennes_annuelles = df_moyennes.groupby('annee')['nb_users'].mean().round(0)
    
    moy_2024 = moyennes_annuelles.get(2024, 0)
    moy_2025 = moyennes_annuelles.get(2025, 0)
    moy_2026 = moyennes_annuelles.get(2026, 0)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Moyenne mensuelle 2024", f"{moy_2024:.0f}")
    with col2:
        delta_2025 = moy_2025 - moy_2024 if moy_2024 > 0 else None
        st.metric("Moyenne mensuelle 2025", f"{moy_2025:.0f}", delta=f"{delta_2025:.0f}" if delta_2025 is not None else None)
    with col3:
        delta_2026 = moy_2026 - moy_2025 if moy_2025 > 0 else None
        st.metric("Moyenne mensuelle 2026", f"{moy_2026:.0f}", delta=f"{delta_2026:.0f}" if delta_2026 is not None else None)

    # Graphique line chart
    afficher_graphique_nivo(
        df_evolution_statut,
        x_column='periode_label',
        y_column='nb_users',
        element_id="line_evolution_users_actifs_par_semaine",
        graph_type="line",
        group_column='annee',
        legend_x=legende_x,
        legend_y="Nombre de users actifs",
        margin_right=180,
        color_scheme="category10"
    )