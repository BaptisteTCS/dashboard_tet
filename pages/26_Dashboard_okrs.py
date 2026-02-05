import streamlit as st
from datetime import datetime
# Configuration de la page en premier
st.set_page_config(
    page_title="Dashboard OKRs",
    page_icon="🌠",
    layout="wide"
)

import pandas as pd
import plotly.graph_objects as go
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
    df_pap_13 = read_table('pap_statut_5_fiches_modifiees_13_semaines')
    df_pap_52 = read_table('pap_statut_5_fiches_modifiees_52_semaines')
    df_pap_date_passage = read_table('pap_date_passage')
    df_note_plan = read_table('note_plan_historique')
    df_fa_sharing = read_table('fa_sharing')
    df_activation_user = read_table('activation_user')
    df_activation_collectivite = read_table('activation_collectivite')
    df_activite_semaine = read_table('activite_semaine')
    df_nb_labellisation = read_table('evolution_labellisation')
    df_note_fiche= read_table('note_fiche_historique', where_sql="note_fa>=5")
    df_user_actif_12_mois=read_table('user_actif_12_mois')
    return df_nb_fap_13, df_nb_fap_52, df_nb_fap_pilote_13, df_nb_fap_pilote_52, df_pap_13, df_pap_52, df_pap_date_passage, df_note_plan, df_fa_sharing, df_activation_user, df_activation_collectivite, df_activite_semaine, df_nb_labellisation, df_note_fiche, df_user_actif_12_mois


df_nb_fap_13, df_nb_fap_52, df_nb_fap_pilote_13, df_nb_fap_pilote_52, df_pap_13, df_pap_52, df_pap_date_passage, df_note_plan, df_fa_sharing, df_activation_user, df_activation_collectivite, df_activite_semaine, df_nb_labellisation, df_note_fiche, df_user_actif_12_mois = load_data()

# ==========================
# Configuration Plotly
# ==========================

# Palette de couleurs Pastel2 (équivalent Nivo)
PASTEL2_COLORS = [
    '#B3E2CD', '#FDCDAC', '#CBD5E8', '#F4CAE4', 
    '#E6F5C9', '#FFF2AE', '#F1E2CC', '#CCCCCC'
]

# Palette Category10
CATEGORY10_COLORS = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
    '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
    '#bcbd22', '#17becf'
]

# Configuration du layout Plotly
def get_plotly_layout():
    return {
        'font': {'family': 'Source Sans Pro, sans-serif', 'size': 13, 'color': '#31333F'},
        'hovermode': 'x unified',
        'plot_bgcolor': 'white',
        'paper_bgcolor': 'white',
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
        st.metric(f"{label_prefix}Dec 2023", f"{val_2024:,}".replace(",", " "))
    with col2:
        st.metric(f"{label_prefix}Dec 2024", f"{val_2025:,}".replace(",", " "), delta=val_2025 - val_2024 if val_2024 > 0 else None)
    with col3:
        st.metric(f"{label_prefix}Dec 2025", f"{val_2026:,}".replace(",", " "), delta=val_2026 - val_2025 if val_2025 > 0 else None)
    with col4:
        st.metric(f"{label_prefix}{derniere_date_label}", f"{derniere_valeur:,}".replace(",", " "), delta=derniere_valeur - val_2026 if val_2026 > 0 else None)


def afficher_graphique_plotly(
    df,
    x_column,
    y_column,
    element_id=None,  # Non utilisé avec Plotly mais gardé pour compatibilité
    graph_type="area_stacked",
    group_column=None,
    group_values=None,
    legend_x="Mois",
    legend_y="Valeur",
    height=450,
    margin_right=110,
    color_scheme="pastel2",
    trend_group_value=None,  # Valeur du groupe pour lequel afficher la tendance (ex: "actif", "Autonome", etc.)
    trend_calculation="linear",  # "linear" (défaut) ou "budget_3m_pct"
    target_value=None  # Valeur cible à afficher comme ligne horizontale
):
    """
    Affiche un graphique Plotly avec différentes configurations et projection de tendance optionnelle.
    
    Paramètres:
    - df: DataFrame contenant les données
    - x_column: nom de la colonne pour l'axe X
    - y_column: nom de la colonne pour l'axe Y
    - element_id: identifiant unique (non utilisé avec Plotly)
    - graph_type: type de graphique ("area_stacked", "area_simple", "line")
    - group_column: nom de la colonne pour grouper les séries (optionnel)
    - group_values: liste des valeurs à afficher dans l'ordre (optionnel)
    - legend_x: légende de l'axe X
    - legend_y: légende de l'axe Y
    - height: hauteur du graphique
    - margin_right: marge à droite pour la légende
    - color_scheme: schéma de couleurs ("pastel2" ou "category10")
    - trend_group_value: valeur du groupe pour afficher la tendance jusqu'à 2026-12 (optionnel)
    - target_value: valeur cible à afficher comme ligne horizontale rouge/orangée (optionnel)
    """
    if df.empty:
        st.info("Aucune donnée disponible pour le graphique d'évolution.")
        return
    
    # Sélectionner la palette de couleurs
    colors = PASTEL2_COLORS if color_scheme == "pastel2" else CATEGORY10_COLORS
    
    # Créer la figure
    fig = go.Figure()
    
    if group_column is None:
        # Une seule série
        if graph_type in ["area_stacked", "area_simple"]:
            fig.add_trace(go.Scatter(
                x=df[x_column],
                y=df[y_column],
                mode='lines',
                fill='tozeroy',
                name=y_column,
                line=dict(color=colors[0], width=2),
                fillcolor=f'rgba({int(colors[0][1:3], 16)}, {int(colors[0][3:5], 16)}, {int(colors[0][5:7], 16)}, 0.7)'
            ))
        else:  # line
            fig.add_trace(go.Scatter(
                x=df[x_column],
                y=df[y_column],
                mode='lines+markers',
                name=y_column,
                line=dict(color=colors[0], width=2),
                marker=dict(size=6)
            ))
    else:
        # Plusieurs séries
        if group_values is None:
            group_values = df[group_column].unique().tolist()
        
        for idx, value in enumerate(group_values):
            df_filtered = df[df[group_column] == value].copy()
            if not df_filtered.empty:
                color = colors[idx % len(colors)]
                
                if graph_type == "area_stacked":
                    fig.add_trace(go.Scatter(
                        x=df_filtered[x_column],
                        y=df_filtered[y_column],
                        mode='lines',
                        name=str(value).capitalize(),
                        line=dict(color=color, width=2),
                        stackgroup='one',
                        fillcolor=f'rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.7)'
                    ))
                elif graph_type == "area_simple":
                    fig.add_trace(go.Scatter(
                        x=df_filtered[x_column],
                        y=df_filtered[y_column],
                        mode='lines',
                        name=str(value).capitalize(),
                        fill='tozeroy',
                        line=dict(color=color, width=2),
                        fillcolor=f'rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.7)'
                    ))
                else:  # line
                    fig.add_trace(go.Scatter(
                        x=df_filtered[x_column],
                        y=df_filtered[y_column],
                        mode='lines+markers',
                        name=str(value),
                        line=dict(color=color, width=2),
                        marker=dict(size=6)
                    ))
    
    # Ajouter la projection de tendance si demandée
    if trend_group_value is not None:
        # Déterminer quelle série utiliser pour la tendance
        if group_column is None:
            df_trend = df.copy()
            trend_color = colors[0]
        else:
            df_trend = df[df[group_column] == trend_group_value].copy()
            # Trouver l'index de la couleur correspondante
            if group_values and trend_group_value in group_values:
                idx = group_values.index(trend_group_value)
                trend_color = colors[idx % len(colors)]
            else:
                trend_color = colors[0]
        
        if not df_trend.empty and len(df_trend) >= 4:
            # Trier par date
            df_trend = df_trend.sort_values(x_column)
            
            # Prendre les 4 derniers points
            last_4_points = df_trend.tail(4)
            
            # Calculer la pente / facteur (sur les 3 derniers mois)
            valeur_m1 = float(last_4_points.iloc[-1][y_column])  # Dernier point
            valeur_m4 = float(last_4_points.iloc[0][y_column])   # 4ème point avant la fin

            pente = None
            facteur_mensuel = None
            if trend_calculation == "budget_3m_pct":
                # Variation multiplicative sur 3 mois, appliquée en continu (composition mensuelle)
                if valeur_m4 > 0:
                    facteur_3m = valeur_m1 / valeur_m4
                    # Si facteur_3m == 0 => décroissance vers 0 (ok). Si négatif => incohérent, on force le fallback.
                    if facteur_3m >= 0:
                        facteur_mensuel = facteur_3m ** (1 / 3)
                # Fallback si données non compatibles (0 au dénominateur, valeurs incohérentes, etc.)
                if facteur_mensuel is None:
                    pente = (valeur_m1 - valeur_m4) / 3
                    trend_calculation_effective = "linear"
                else:
                    trend_calculation_effective = "budget_3m_pct"
            else:
                pente = (valeur_m1 - valeur_m4) / 3
                trend_calculation_effective = "linear"
            
            # Point de départ : dernier point de données
            dernier_x = df_trend.iloc[-1][x_column]
            dernier_y = float(df_trend.iloc[-1][y_column])
            
            # Générer les dates futures jusqu'à 2026-12
            dates_projection = []
            valeurs_projection = []
            
            # Format des dates (YYYY-MM)
            try:
                # Parser la dernière date
                if isinstance(dernier_x, str) and '-' in dernier_x:
                    annee, mois = dernier_x.split('-')
                    date_actuelle = pd.Period(f"{annee}-{mois}", freq='M')
                    
                    # Générer les mois jusqu'à 2026-12
                    date_fin = pd.Period('2026-12', freq='M')
                    
                    # Ajouter le point de départ (dernier point réel)
                    dates_projection.append(dernier_x)
                    valeurs_projection.append(dernier_y)
                    
                    # Projeter mois par mois
                    date_courante = date_actuelle + 1
                    mois_projection = 1
                    while date_courante <= date_fin:
                        dates_projection.append(date_courante.strftime('%Y-%m'))
                        if trend_calculation_effective == "budget_3m_pct":
                            valeur_projetee = dernier_y * (facteur_mensuel ** mois_projection)
                            valeurs_projection.append(round(max(0, valeur_projetee), 2))
                        else:
                            valeurs_projection.append(round(max(0, dernier_y + pente * mois_projection), 0))  # Éviter les valeurs négatives
                        date_courante += 1
                        mois_projection += 1
                    
                    # Ajouter la trace de tendance en pointillés
                    if len(dates_projection) > 1:
                        fig.add_trace(go.Scatter(
                            x=dates_projection,
                            y=valeurs_projection,
                            mode='lines',
                            name="Tendance",
                            line=dict(color=trend_color, width=2, dash='dot'),
                            showlegend=True
                        ))
            except Exception as e:
                # En cas d'erreur, ne pas afficher la tendance
                st.warning(f"Impossible de calculer la tendance : {str(e)}")
    
    # Ajouter la ligne de cible si demandée (projection vers 2027-01)
    if target_value is not None:
        # Déterminer quelle série utiliser pour obtenir le point de départ
        if group_column is None:
            df_target = df.copy()
        else:
            # Utiliser la même série que la tendance si disponible, sinon toutes les données
            if trend_group_value is not None:
                df_target = df[df[group_column] == trend_group_value].copy()
            else:
                df_target = df.copy()
        
        if not df_target.empty:
            # Trier par date
            df_target = df_target.sort_values(x_column)
            
            # Point de départ : dernier point de données
            dernier_x = df_target.iloc[-1][x_column]
            dernier_y = df_target.iloc[-1][y_column]
            
            # Générer la projection linéaire jusqu'à 2027-01
            dates_cible = []
            valeurs_cible = []
            
            # Format des dates (YYYY-MM)
            try:
                # Parser la dernière date
                if isinstance(dernier_x, str) and '-' in dernier_x:
                    annee, mois = dernier_x.split('-')
                    date_actuelle = pd.Period(f"{annee}-{mois}", freq='M')
                    
                    # Date cible : 2027-01
                    date_fin = pd.Period('2027-01', freq='M')
                    
                    # Calculer le nombre de mois entre maintenant et la cible
                    nb_mois = (date_fin - date_actuelle).n
                    
                    if nb_mois > 0:
                        # Calculer la pente pour atteindre la cible
                        pente = (target_value - dernier_y) / nb_mois
                        
                        # Ajouter le point de départ (dernier point réel)
                        dates_cible.append(dernier_x)
                        valeurs_cible.append(dernier_y)
                        
                        # Projeter mois par mois jusqu'à 2027-01
                        date_courante = date_actuelle + 1
                        mois_projection = 1
                        while date_courante <= date_fin:
                            dates_cible.append(date_courante.strftime('%Y-%m'))
                            valeur_projetee = dernier_y + pente * mois_projection
                            valeurs_cible.append(round(valeur_projetee, 0))
                            date_courante += 1
                            mois_projection += 1
                        
                        # Ajouter la trace de cible en pointillés
                        if len(dates_cible) > 1:
                            fig.add_trace(go.Scatter(
                                x=dates_cible,
                                y=valeurs_cible,
                                mode='lines',
                                name='Cible',
                                line=dict(color='#FFD888', width=2, dash='dot'),  # Orange/rouge
                                showlegend=True
                            ))
                    else:
                        # Si on est déjà en 2027 ou après, afficher une ligne horizontale
                        all_x_values = df[x_column].unique().tolist()
                        fig.add_trace(go.Scatter(
                            x=all_x_values,
                            y=[target_value] * len(all_x_values),
                            mode='lines',
                            name='Cible',
                            line=dict(color='#FF6B35', width=2, dash='dot'),
                            showlegend=True
                        ))
            except Exception as e:
                # En cas d'erreur, afficher une ligne horizontale classique
                st.warning(f"Impossible de calculer la projection de cible : {str(e)}")
                all_x_values = df[x_column].unique().tolist()
                fig.add_trace(go.Scatter(
                    x=all_x_values,
                    y=[target_value] * len(all_x_values),
                    mode='lines',
                    name='Cible',
                    line=dict(color='#FF6B35', width=2, dash='dot'),
                    showlegend=True
                ))
    
    # Configuration du layout
    fig.update_layout(
        **get_plotly_layout(),
        height=height,
        xaxis=dict(
            title=legend_x,
            tickangle=-45,
            showgrid=True,
            gridcolor='rgba(128, 128, 128, 0.2)',
            showline=True,
            linecolor='rgba(128, 128, 128, 0.3)'
        ),
        yaxis=dict(
            title=legend_y,
            showgrid=True,
            gridcolor='rgba(128, 128, 128, 0.2)',
            showline=True,
            linecolor='rgba(128, 128, 128, 0.3)',
            rangemode='tozero'
        ),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.01,
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor='rgba(0, 0, 0, 0.1)',
            borderwidth=1
        ),
        margin=dict(l=60, r=margin_right, t=20, b=60)
    )
    
    # Afficher le graphique
    st.plotly_chart(fig, use_container_width=True)


# ==========================
# Interface
# ==========================

st.title("🌠 Dashboard OKRs")
tabs = st.tabs(["Menu", "1 - Activation", "2 - Rétention", "3 - Qualité", "4 - Impact", "5 - Légitimité", "6 - Budget"])

# ==========================
# TAB 0 : MENU - Liste des graphiques
# ==========================

with tabs[0]:
    st.markdown("## Menu")
    
    # Structure des graphiques par catégorie
    graphiques = {
        "1 - ACTIVATION": [
            ("A-1", "Nombre de collectivités avec au moins un PAP actif 12 mois", "🌟 NS1 - externe"),
            ("A-2", "Nombre de collectivités avec au moins un PAP actif 3 mois", "🌟 NS1 - interne"),
            ("A-3", "Nombre d'Actions pilotables actives ≤3 mois", "💫 Activité"),
            ("A-3 bis", "Nombre d'Actions pilotables actives ≤12 mois", "💫 Activité"),
            ("A-4", "Nombre de PAP initialisés de façon autonome", "🎇 Exploration"),
        ],
        "2 - RÉTENTION": [
            ("R-1", "Nombre de CT avec au moins 2 PAP avec contribution active 12 mois", "🌟 NS2 - externe"),
            ("R-2", "Nombre de CT avec au moins 2 PAP avec contribution active 3 mois", "🌟 NS2 - interne"),
            ("R-3", "Nombre d'Actions pilotables actives avec pilote de l'action actif ≤ 12 mois", "💫 Activité"),
            ("R-3 bis", "Nombre d'Actions pilotables actives avec pilote de l'action actif ≤ 3 mois", "💫 Activité"),
            ("R-4", "Nombre d'actions partagées/liées entre collectivités", "🎇 Exploration"),
        ],
        "3 - QUALITÉ": [
            ("Q-1", "Nombre de PAP ayant une note supérieure à 5/10", "🌟 NS3 - externe"),
            ("Q-2", "Nombre de PAP ayant une note supérieure à 8/10", "🌟 NS3 - interne"),
            ("Q-3", "Nombre d'actions ayant une note de 10/10", "💫 Complétude"),
        ],
        "4 - IMPACT": [
            ("—", "Section en construction", ""),
        ],
        "5 - LÉGITIMITÉ": [
            ("L-1", "Nombre d'utilisateurs activés", "🌟 NS5 - externe"),
            ("L-1 bis", "Nombre de collectivités activées", "🌟 NS5 - externe"),
            ("L-2", "Nombre de collectivités actives", "🌟 NS5 - interne"),
            ("L-2 bis", "Nombre d'utilisateurs actifs", "🌟 NS5 - interne"),
            ("L-3", "Nombre de labellisations réalisées sur la plateforme", "💫 Activité"),
        ],
        "6 - BUDGET": [
            ("B-1", "Coût annuel par action pilotable actives 12 mois (€/action)", "🌟 NS6 - externe"),
            ("B-2", "Coût annuel par collectivité ayant un PAP actif 3 mois (€/collectivité)", "🌟 NS6 - interne"),
            ("B-3", "Coût annuel par utilisateur actif ≤ 12 mois (€/utilisateur)", "💫 Activité"),
        ],
    }
    
    # Affichage sous forme de colonnes (alternance gauche-droite)
    categories = list(graphiques.keys())
    
    # Créer des paires de catégories (1-2, 3-4, 5-6)
    for i in range(0, len(categories), 2):
        col1, col2 = st.columns(2)
        
        # Catégorie de gauche
        with col1:
            categorie = categories[i]
            st.markdown(f"### {categorie}")
            for code, nom, badge in graphiques[categorie]:
                if badge:
                    st.markdown(f"**{code}** | {nom}  \n<small style='color: gray;'>{badge}</small>", unsafe_allow_html=True)
                else:
                    st.markdown(f"**{code}** | {nom}")
            st.markdown("")
        
        # Catégorie de droite (si elle existe)
        with col2:
            if i + 1 < len(categories):
                categorie = categories[i + 1]
                st.markdown(f"### {categorie}")
                for code, nom, badge in graphiques[categorie]:
                    if badge:
                        st.markdown(f"**{code}** | {nom}  \n<small style='color: gray;'>{badge}</small>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"**{code}** | {nom}")
                st.markdown("")

# ==========================
# TAB 1 : ACTIVATION
# ==========================

with tabs[1]:

    st.markdown("## Objectif 1 : ACTIVATION")
    st.markdown("Permettre à chaque collectivité territoriale française de piloter ses plans & actions.")
    st.markdown("---")

    # ======================
    st.badge('NS1 - externe', icon="🌟", color="orange")
    st.markdown("### A-1 | Nombre de collectivités avec au moins un PAP actif 12 mois")
    st.markdown("""
    Un PAP actif 12 mois est défini comme un PAP avec 5 actions pilotables chacunes ayant reçu au moins une modification dans les 12 derniers mois.
    Une action pilotable est définie comme une action ayant : 
    - titre
    - description
    - statut
    - personne pilote ou service/direction pilote
    """)

    # Préparation des données
    df_evolution_statut = df_pap_52.copy()
    df_evolution_statut['mois'] = df_evolution_statut['mois'].dt.to_period('M').dt.to_timestamp()
    df_evolution_statut = df_evolution_statut.sort_values('statut').drop_duplicates(subset=['collectivite_id', 'mois'], keep='first')
    df_evolution_statut = df_evolution_statut[df_evolution_statut['mois'] >= '2023-01-01']
    df_evolution_statut = df_evolution_statut.groupby(['mois', 'statut'])['collectivite_id'].nunique().reset_index(name='nb_collectivites')
    df_evolution_statut = df_evolution_statut.sort_values('mois')
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].dt.strftime('%Y-%m')

    # Métriques
    df_actif = df_evolution_statut[df_evolution_statut['statut'] == 'actif']
    afficher_metriques_temporelles(df_actif, 'nb_collectivites', label_prefix="Actifs - ")

    # Graphique
    afficher_graphique_plotly(
        df_evolution_statut,
        x_column='mois_label',
        y_column='nb_collectivites',
        element_id="line_evolution_statuts_pap_52",
        graph_type="area_stacked",
        group_column='statut',
        group_values=["actif", "inactif"],
        legend_y="Nombre de collectivités",
        trend_group_value="actif",
        target_value=600  # Cible à ajuster
    )


    # ======================
    st.markdown("---")
    st.badge('NS1 - interne', icon="🌟", color="orange")
    st.markdown("### A-2 | Nombre de collectivités avec au moins un PAP actif 3 mois")
    st.markdown("""
    Un PAP actif 3 mois est défini comme un PAP avec 5 actions pilotables chacunes ayant reçu au moins une modification dans les 3 derniers mois.
    Une action pilotable est définie comme une action ayant : 
    - titre
    - description
    - statut
    - personne pilote ou service/direction pilote
    """)

    # Préparation des données
    df_evolution_statut = df_pap_13.copy()
    df_evolution_statut['mois'] = df_evolution_statut['mois'].dt.to_period('M').dt.to_timestamp()
    df_evolution_statut = df_evolution_statut.sort_values('statut').drop_duplicates(subset=['collectivite_id', 'mois'], keep='first')
    df_evolution_statut = df_evolution_statut[df_evolution_statut['mois'] >= '2023-01-01']
    df_evolution_statut = df_evolution_statut.groupby(['mois', 'statut'])['collectivite_id'].nunique().reset_index(name='nb_collectivites')
    df_evolution_statut = df_evolution_statut.sort_values('mois')
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].dt.strftime('%Y-%m')

    # Métriques
    df_actif = df_evolution_statut[df_evolution_statut['statut'] == 'actif']
    afficher_metriques_temporelles(df_actif, 'nb_collectivites', label_prefix="Actifs - ")

    # Graphique
    afficher_graphique_plotly(
        df_evolution_statut,
        x_column='mois_label',
        y_column='nb_collectivites',
        element_id="line_evolution_statuts_pap_13",
        graph_type="area_stacked",
        group_column='statut',
        group_values=["actif", "inactif"],
        legend_y="Nombre de collectivités",
        trend_group_value="actif",
        target_value=350  # Cible à ajuster
    )


    # ======================
    st.markdown("---")
    st.badge('Activité', icon="💫", color="blue")
    st.markdown("### A-3 | Nombre d'Actions pilotables actives ≤3 mois")
    st.markdown("""
    Une action pilotable active 3 mois est définie comme une action ayant : 
    - titre
    - description
    - statut
    - personne pilote ou service/direction pilote
    - reçue au moins une modification dans les 3 derniers mois
    """)

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
    afficher_graphique_plotly(
        df_evolution_statut,
        x_column='mois_label',
        y_column='fiche_id',
        element_id="line_evolution_statuts_fap_13",
        graph_type="area_stacked",
        group_column='statut',
        group_values=["actif", "inactif"],
        legend_y="Nombre d'actions pilotables actives",
        trend_group_value="actif",
        target_value=10000  # Cible à ajuster
    )


    # ======================
    st.markdown("---")
    st.badge('Activité', icon="💫", color="blue")
    st.markdown("### A-3 | Nombre d'Actions pilotables actives ≤12 mois")
    st.markdown("""
    Une action pilotable active 3 mois est définie comme une action ayant : 
    - titre
    - description
    - statut
    - personne pilote ou service/direction pilote
    - reçue au moins une modification dans les 12 derniers mois
    """)

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
    afficher_graphique_plotly(
        df_evolution_statut,
        x_column='mois_label',
        y_column='fiche_id',
        element_id="line_evolution_statuts_fap_52",
        graph_type="area_stacked",
        group_column='statut',
        group_values=["actif", "inactif"],
        legend_y="Nombre d'actions pilotables actives",
        trend_group_value="actif",
        target_value=None  # Cible à ajuster
    )


    # ======================
    st.markdown("---")
    st.badge('Exploration', icon="🎇", color="green")
    st.markdown("### A-4 | Nombre de PAP initialisés de façon autonome")
    st.markdown("""
    Un PAP initialisé de façon autonome est défini comme un PAP qui n'a pas été importé par les bizdevs.
    """)

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
    afficher_graphique_plotly(
        df_graph_cumul,
        x_column='mois_label',
        y_column='nb_plans_cumul',
        element_id="line_evolution_autonome",
        graph_type="area_stacked",
        group_column='import',
        group_values=["Autonome", "Importé"],
        legend_y="Nombre de PAP (cumulé)",
        trend_group_value="Autonome",
        target_value=1000  # Cible à ajuster
    )


# ==========================
# TAB 2 : RÉTENTION
# ==========================

with tabs[2]:

    st.markdown('## Objectif 2 : RÉTENTION')
    st.markdown('Faciliter la transversalité entre Plans & Actions & Contributeurs')
    st.markdown("---")

    # ======================
    st.badge('NS2 - externe', icon="🌟", color="orange")
    st.markdown('### R-1 | Nombre de CT avec au moins 2 PAP avec contribution active 12 mois')
    st.markdown("""
    Un PAP actif 12 mois est défini comme un PAP avec 5 actions pilotables chacunes ayant reçu au moins une modification dans les 12 derniers mois.
    Une action pilotable est définie comme une action ayant : 
    - titre
    - description
    - statut
    - personne pilote ou service/direction pilote
    """)

    # Préparation des données
    df_evolution_statut = df_pap_52.copy()
    df_evolution_statut['mois'] = df_evolution_statut['mois'].dt.to_period('M').dt.to_timestamp()
    count_pap = df_evolution_statut.groupby(['mois', 'statut', 'collectivite_id'])['plan'].nunique().reset_index(name='nb_paps')
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
    afficher_graphique_plotly(
        df_evolution_statut,
        x_column='mois_label',
        y_column='nb_collectivites',
        element_id="line_evolution_statuts_pap_52_fois_2",
        graph_type="area_stacked",
        group_column='statut',
        group_values=["actif", "inactif"],
        legend_y="Nombre de collectivités",
        trend_group_value="actif",
        target_value=250  # Cible à ajuster
    )


    # ======================
    st.markdown("---")
    st.badge('NS2 - interne', icon="🌟", color="orange")
    st.markdown('### R-2 | Nombre de CT avec au moins 2 PAP avec contribution active 3 mois (dont avec/sans ≥2 pilotes de plans différents)')
    st.markdown("""
    Un PAP actif 3 mois est défini comme un PAP avec 5 actions pilotables chacunes ayant reçu au moins une modification dans les 3 derniers mois.
    Une action pilotable est définie comme une action ayant : 
    - titre
    - description
    - statut
    - personne pilote ou service/direction pilote

    On fait la distinction entre les CT qui ont au moins 2 pilotes de plans différents sur l'ensemble et les CT qui ont 1 pilote ou moins.
    """)

    # Préparation des données
    df_evolution_statut = df_pap_13.copy()
    df_evolution_statut['mois'] = df_evolution_statut['mois'].dt.to_period('M').dt.to_timestamp()
    count_pap = df_evolution_statut.groupby(['mois', 'statut', 'collectivite_id'])['plan'].nunique().reset_index(name='nb_paps')
    count_pap = count_pap[(count_pap['nb_paps'] >= 2) & (count_pap['statut'] == 'actif')]
    df_evolution_statut = df_evolution_statut[df_evolution_statut['mois'] >= '2023-01-01']
    df_evolution_statut = df_evolution_statut.merge(count_pap, on=['mois', 'statut', 'collectivite_id'], how='inner')
    df_evolution_statut['multi_pilotes'] = df_evolution_statut['nb_pilotes'].apply(lambda x: '>= 2 pilotes' if x>1 else '1 pilote ou moins')
    df_evolution_statut = df_evolution_statut.groupby(['mois', 'statut', 'multi_pilotes'])['collectivite_id'].nunique().reset_index(name='nb_collectivites')
    df_evolution_statut = df_evolution_statut.sort_values('mois')
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].dt.strftime('%Y-%m')

    # Métriques
    df_actif = df_evolution_statut[df_evolution_statut['statut'] == 'actif']
    afficher_metriques_temporelles(df_actif[df_actif['multi_pilotes'] == '>= 2 pilotes'], 'nb_collectivites', label_prefix="")

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
    afficher_graphique_plotly(
        df_graph_complet,
        x_column='mois_label',
        y_column='nb_collectivites',
        element_id="line_evolution_statuts_pap_13_fois_2",
        graph_type="area_stacked",
        group_column='multi_pilotes',
        group_values=[">= 2 pilotes", "1 pilote ou moins"],
        legend_y="Nombre de collectivités",
        margin_right=160,
        trend_group_value=">= 2 pilotes",
        target_value=50  # Cible à ajuster
    )


    # ======================
    st.markdown("---")
    st.badge('Activité', icon="💫", color="blue")   
    st.markdown("### R-3 | Nombre d'Actions pilotables actives avec pilote de l'action actif ≤ 12 mois")
    st.markdown("""
    Une action pilotable active 12 mois est définie comme une action ayant :
    - titre
    - description
    - statut
    - personne pilote ou service/direction pilote
    - reçue au moins une modification dans les 12 derniers mois
    """)

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
    afficher_graphique_plotly(
        df_evolution_statut,
        x_column='mois_label',
        y_column='fiche_id',
        element_id="line_evolution_statuts_fap_pilote_52",
        graph_type="area_stacked",
        group_column='statut',
        group_values=["actif", "inactif"],
        legend_y="Nombre d'actions pilotables actives",
        trend_group_value="actif",
        target_value=10000  # Cible à ajuster
    )

    # ======================
    st.markdown("---")
    st.badge('Activité', icon="💫", color="blue")
    st.markdown('### R-3 (bis) (💫 - Activité) : Nombre d\'Actions pilotables actives avec pilote de l\'action actif ≤ 3 mois')

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
    afficher_graphique_plotly(
        df_evolution_statut,
        x_column='mois_label',
        y_column='fiche_id',
        element_id="line_evolution_statuts_fap_pilote_13",
        graph_type="area_stacked",
        group_column='statut',
        group_values=["actif", "inactif"],
        legend_y="Nombre d'actions pilotables actives",
        trend_group_value="actif",
        target_value=None  # Cible à ajuster
    )

    # ======================
    st.markdown("---")
    st.badge('Exploration', icon="🎇", color="green")
    st.markdown("### R-4 | Nombre d'actions partagées/liées entre collectivités")
    st.markdown("Nombre d'actions uniques partagées entre au moins deux collectivités")

    # Préparation des données
    df_evolution_statut = df_fa_sharing.copy()
    df_evolution_statut = df_evolution_statut.sort_values('mois')
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].dt.strftime('%Y-%m')

    # Graphique (area simple)
    afficher_graphique_plotly(
        df_evolution_statut,
        x_column='mois_label',
        y_column='nb_fa_shared',
        element_id="line_evolution_statuts_fa_sharing",
        graph_type="area_simple",
        legend_y="Nombre de FA partagées",
        trend_group_value="nb_fa_shared",
        target_value=1270
    )


# ==========================
# TAB 3 : QUALITÉ
# ==========================

with tabs[3]:

    st.markdown('## Objectif 3 : QUALITÉ')
    st.markdown('Augmenter la qualité des Plans & Actions')
    st.markdown("---")
    st.markdown('### Définition de la note d\'une Action')
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
    - **Objectif** + 1pt *(au moins un objectif chiffré dans TOUS les indicateurs liés pour une année supérieur ou égalé à l’année actuelle)*
    - **Budget** + 1pt *(budget investissement ou fonctionnement ou financeurs ou champs financements ou moyens humains)*
    - **Note de suivi de moins d’un an** + 1pt
    - **Date de dernière MAJ de l’action <12 mois** + 0.5pt (si statut non terminé/Abandonné) *(la modification d'une relation n'est pas comptabilisée comme lier des indicateurs, mesures, budget, etc.)*
    - **Date de dernière MAJ de l’action <6 mois** + 0.5pt (si statut non terminé/Abandonné) *(idem)*
    """)

    st.markdown('### Définition de la note d\'un PAP')
    st.markdown('La note d\'un PAP se calcule en prenant la moyenne des notes de toutes ses fiches actions.')

    # ======================
    st.markdown('---')
    st.badge('NS3 - externe', icon="🌟", color="orange")
    st.markdown('### Q-1 | Nombre de PAP ayant une note supérieur à 5/10')
    
    # Préparation des données
    df_evolution_statut = df_note_plan.copy()

    df_evolution_statut['statut'] = df_evolution_statut['note_plan'].apply(lambda x: '>= 5' if x>=5 else '< 5')

    df_evolution_statut['mois'] = pd.to_datetime(df_evolution_statut['mois'])
    df_evolution_statut['mois'] = df_evolution_statut['mois'].dt.to_period('M').dt.to_timestamp()

    df_evolution_statut = df_evolution_statut.groupby(['mois', 'statut'])['plan'].nunique().reset_index(name='nb_plans')
    
    df_evolution_statut = df_evolution_statut[df_evolution_statut['mois'] >= '2023-01-01']
    df_evolution_statut = df_evolution_statut.sort_values('mois')
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].dt.strftime('%Y-%m')

    # Graphique
    afficher_graphique_plotly(
        df_evolution_statut,
        x_column='mois_label',
        y_column='nb_plans',
        element_id="line_evolution_note_plan_50pct",
        graph_type="area_stacked",
        group_column='statut',
        group_values=['>= 5', '< 5'],
        legend_y="Nombre de PAP",
        trend_group_value=">= 5",
        target_value=800  # Cible à ajuster
    )


    # ======================
    st.markdown('---')
    st.badge('NS3 - interne', icon="🌟", color="orange")
    st.markdown('### Q-2 | Nombre de PAP ayant une note supérieur à 8/10')

    # Préparation des données
    df_evolution_statut = df_note_plan.copy()
    df_evolution_statut['statut'] = df_evolution_statut['note_plan'].apply(lambda x: '>= 8' if x>=8 else '< 8')
    df_evolution_statut['mois'] = pd.to_datetime(df_evolution_statut['mois'])
    df_evolution_statut['mois'] = df_evolution_statut['mois'].dt.to_period('M').dt.to_timestamp()

    df_evolution_statut = df_evolution_statut.groupby(['mois', 'statut'])['plan'].nunique().reset_index(name='nb_plans')
    
    df_evolution_statut = df_evolution_statut[df_evolution_statut['mois'] >= '2023-01-01']
    df_evolution_statut = df_evolution_statut.sort_values('mois')
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].dt.strftime('%Y-%m')

    # Graphique
    afficher_graphique_plotly(
        df_evolution_statut,
        x_column='mois_label',
        y_column='nb_plans',
        element_id="line_evolution_note_plan_80pct",
        graph_type="area_stacked",
        group_column='statut',
        group_values=['>= 8', '< 8'],
        legend_y="Nombre de PAP",
        trend_group_value=">= 8",
        target_value=600   # Cible à ajuster
    )

    # ======================
    st.markdown('---')
    st.badge('Complétude', icon="💫", color="blue")
    st.markdown("### Q-3 | Nombre d'actions ayant une note de 10/10")

    df_evolution_statut = df_note_fiche[df_note_fiche.note_fa==10].copy()
    df_evolution_statut['mois'] = pd.to_datetime(df_evolution_statut['mois'])
    df_evolution_statut['mois'] = df_evolution_statut['mois'].dt.to_period('M').dt.to_timestamp()

    df_evolution_statut = df_evolution_statut.groupby(['mois'])['fiche_id'].nunique().reset_index(name='nb_fiches')
    
    df_evolution_statut = df_evolution_statut[df_evolution_statut['mois'] >= '2023-01-01']
    df_evolution_statut = df_evolution_statut.sort_values('mois')
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].dt.strftime('%Y-%m')

    # Graphique
    afficher_graphique_plotly(
        df_evolution_statut,
        x_column='mois_label',
        y_column='nb_fiches',
        element_id="line_evolution_statuts_fiches_10",
        graph_type="line",
        legend_y="Nombre de fiches à 10/10",
        trend_group_value="nb_fiches",
        target_value=500   # Cible à ajuster
    )
    

# ==========================
# TAB 4 : IMPACT
# ==========================

with tabs[4]:
    st.markdown("## Objectif 4 : Impact")


# ==========================
# TAB 5 : LÉGITIMITÉ
# ==========================

with tabs[5]:

    # ======================
    st.markdown('## Objectif 5: Légitimité')
    st.markdown("---")

    st.badge('NS5 - externe', icon="🌟", color="orange")
    st.markdown("### L-1 | Nombre d'utilisateurs activés")
    st.markdown("""
    Nombre d'utilisateurs uniques rattachés à une collectivité :

    - qui n'est jamais défini comme conseiller ou partenaire
    - qui n'est pas un utilisateur interne (nous)
    - dont l'email ne contient pas 'ademe'
    """)

    # Préparation des données
    df_evolution_statut = df_activation_user.copy()
    df_evolution_statut = df_evolution_statut.sort_values('mois')
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].dt.strftime('%Y-%m')

    afficher_metriques_temporelles(df_evolution_statut, 'nb_users', label_prefix="Actifs - ")

    # Graphique (area simple)
    afficher_graphique_plotly(
        df_evolution_statut,
        x_column='mois_label',
        y_column='nb_users',
        element_id="line_evolution_statuts_activation_user",
        graph_type="area_simple",
        legend_y="Nombre d'utilisateurs activés",
        margin_right=180,
        trend_group_value="nb_users",
        target_value=10000
    )


    # ======================
    st.markdown('---')
    st.badge('NS5 - externe', icon="🌟", color="orange")
    st.markdown('### L-1 (bis) | Nombre de collectivités activées')
    st.markdown("""
    Nombre de collectivités avec au moins un utilisateur rattaché :

    - qui n'est jamais défini comme conseiller ou partenaire
    - qui n'est pas un utilisateur interne (nous)
    - dont l'email ne contient pas 'ademe'
    """)

    # Préparation des données
    df_evolution_statut = df_activation_collectivite.copy()
    df_evolution_statut = df_evolution_statut.sort_values('mois')
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].dt.strftime('%Y-%m')

    # Métriques (3 colonnes pour cette section)
    afficher_metriques_temporelles(df_evolution_statut, 'nb_collectivite', label_prefix="Actifs - ")

    # Graphique (area simple)
    afficher_graphique_plotly(
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
    st.badge('NS5 - interne', icon="🌟", color="orange") 
    st.markdown('### L-2 | Nombre de collectivités actives')
    st.markdown("""
    Nombre de collectivités avec au moins un utilsateur actif au cours de la période sélectionnée :
    - qui n'est jamais défini comme conseiller ou partenaire
    - qui n'est pas un utilisateur interne (nous)
    - dont l'email ne contient pas 'ademe'
    """)


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
    afficher_graphique_plotly(
        df_evolution_statut,
        x_column='periode_label',
        y_column='nb_collectivites',
        element_id="line_evolution_collectivites_actives_par_semaine",
        graph_type="line",
        group_column='annee',
        legend_x=legende_x,
        legend_y="Nombre de collectivités actives",
        margin_right=180,
        color_scheme="category10",
        trend_group_value="nb_collectivites",
        target_value=1000
    )


    # ======================
    st.markdown("---")
    st.badge('NS5 - interne', icon="🌟", color="orange") 
    st.markdown('### L-2 | Nombre d\'utilisateurs actifs')
    st.markdown("""
    Nombre d'utilisateurs actifs au cours de la période sélectionnée :
    - qui n'est jamais défini comme conseiller ou partenaire
    - qui n'est pas un utilisateur interne (nous)
    - dont l'email ne contient pas 'ademe'
    """)

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
    afficher_graphique_plotly(
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


    # ======================
    st.markdown("---")
    st.badge('Activité', icon="💫", color="blue")   
    st.markdown('### L-3 | Nombre de labellisations réalisées sur la plateforme')
    st.markdown("""
    Nombre de labellisations réalisées sur la plateforme. Chaque audit qui aboutit au discernement d'une étoile est une labellisation.
    """)

    # Préparation des données
    df_evolution_statut = df_nb_labellisation[df_nb_labellisation.mois>"2021-01-01"].copy()
    df_evolution_statut = df_evolution_statut.sort_values('mois')
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].dt.strftime('%Y-%m')

    afficher_metriques_temporelles(df_evolution_statut, 'nb_labellisation_cumule', label_prefix="Labellisations - ")

    # Graphique (area simple)
    afficher_graphique_plotly(
        df_evolution_statut,
        x_column='mois_label',
        y_column='nb_labellisation_cumule',
        element_id="line_evolution_statuts_nb_labellisation_cumule",
        graph_type="area_simple",
        legend_y="Nombre de labellisations réalisées",
        margin_right=180,
        trend_group_value="nb_labellisation_cumule",
        target_value=None
    )

with tabs[6]: 

    # ======================
    # Objectif 6 : Budget
    # ======================

    st.markdown('## Objectif 6 : Budget')
    st.markdown("---")
    st.markdown("""
        ### Principe de calcul

        Chaque mois, on regarde une certaine **quantitée absolue** : actions pilotables actives, PAP actif, utilisateurs actifs... sur Territoires en Transitions. On divise ensuite le **budget annuel** par ce total pour avoir le cout annuel par quantitée arrété au mois.
        ### Exemple

        - **Budget annuel 2025** : 10 €

        **Juin 2025**  
        - 2 actions pilotables actives
        - Coût par action = 10 € ÷ 2 = **5 €**

        **Juillet 2025**  
        - 4 actions pilotables actives  
        - Coût par action = 10 € ÷ 4 = **2,50 €**

        **Août 2025**  
        - 1 action pilotable active  
        - Coût par action = 10 € ÷ 1 = **10 €**

        ### Comment interpréter cette métrique

        Cette métrique doit être lue comme :  
        > *« À ce mois donné, compte tenu du volume d’actions observé et du budget annuel, voici le coût par action pilotable. »*

        Elle reflète donc une **photo à date**, et non une moyenne sur l’année.
        """)

    # Champs de saisie pour les budgets
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        budget_2023 = st.number_input("Budget 2023", value=1_345_421, step=100_000, format="%d")
    with col2:
        budget_2024 = st.number_input("Budget 2024", value=1_776_764, step=100_000, format="%d")
    with col3:
        budget_2025 = st.number_input("Budget 2025", value=1_948_146, step=100_000, format="%d")
    with col4:
        budget_2026 = st.number_input("Budget 2026", value=1_600_000, step=100_000, format="%d")

    st.markdown("---")
    st.badge('NS6 - externe', icon="🌟", color="orange")

    st.markdown('### B-1 | Coût annuel par action pilotable actives 12 mois (€/action)')
    st.markdown("""
    Une action pilotable 12 mois est définie comme une action ayant : 
    - titre
    - description
    - statut
    - personne pilote ou service/direction pilote
    - reçue au moins une modification dans les 12 derniers mois
    """)
    
    # Préparation des données
    df_evolution_statut = df_nb_fap_52.copy()
    df_evolution_statut['mois'] = pd.to_datetime(df_evolution_statut['mois'])
    df_evolution_statut = df_evolution_statut[df_evolution_statut['mois'] >= '2023-01-01']
    df_evolution_statut = df_evolution_statut.sort_values('mois')
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].dt.strftime('%Y-%m')
    df_evolution_statut['annee'] = df_evolution_statut['mois'].dt.year
    
    # Associer le budget à chaque année
    budget_mapping = {2023: budget_2023, 2024: budget_2024, 2025: budget_2025, 2026: budget_2026}
    df_evolution_statut['budget_annuel'] = df_evolution_statut['annee'].map(budget_mapping)
    
    # Calculer le coût par action pilotable (budget annuel / 12 pour obtenir le budget mensuel, puis diviser par le nombre d'actions actives)
    df_actif = df_evolution_statut[df_evolution_statut['statut'] == 'actif'].copy()
    df_actif['Cout par action pilotable'] = (df_actif['budget_annuel']) / df_actif['fiche_id']
    df_actif['Cout par action pilotable'] = df_actif['Cout par action pilotable'].fillna(0).round(2)
    
    # Métriques
    afficher_metriques_temporelles(df_actif, 'Cout par action pilotable', label_prefix="Coût/Action - ")
    
    # Graphique
    afficher_graphique_plotly(
        df_actif,
        x_column='mois_label',
        y_column='Cout par action pilotable',
        element_id="line_evolution_Cout_par_action_pilotable",
        graph_type="line",
        legend_y="Coût par action pilotable (€)",
        trend_group_value="Cout par action pilotable",
        trend_calculation="budget_3m_pct",
        target_value=None
    )

    # ======================
    st.markdown("---")
    st.badge('NS6 - interne', icon="🌟", color="orange")
    st.markdown('### B-2 | Coût annuel par collectivité ayant un PAP actif 3 mois (€/collectivité)')
    st.markdown("""
    Un PAP actif 3 mois est défini comme un PAP avec 5 actions pilotables actives 3 mois.
    Une action pilotable active 3 mois est définie comme une action ayant : 
    - titre
    - description
    - statut
    - personne pilote ou service/direction pilote
    - reçue au moins une modification dans les 3 derniers mois
    """)
    
    # Préparation des données
    df_evolution_statut = df_pap_13.copy()
    df_evolution_statut['mois'] = df_evolution_statut['mois'].dt.to_period('M').dt.to_timestamp()
    df_evolution_statut = df_evolution_statut.sort_values('statut').drop_duplicates(subset=['collectivite_id', 'mois'], keep='first')
    df_evolution_statut = df_evolution_statut[df_evolution_statut['mois'] >= '2023-01-01']
    df_evolution_statut = df_evolution_statut.groupby(['mois', 'statut'])['collectivite_id'].nunique().reset_index(name='nb_collectivites')
    df_evolution_statut = df_evolution_statut.sort_values('mois')
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].dt.strftime('%Y-%m')
    df_evolution_statut['annee'] = df_evolution_statut['mois'].dt.year

    # Associer le budget à chaque année
    budget_mapping = {2023: budget_2023, 2024: budget_2024, 2025: budget_2025, 2026: budget_2026}
    df_evolution_statut['budget_annuel'] = df_evolution_statut['annee'].map(budget_mapping)
    
    # Calculer le coût par collectivité (budget annuel / 12 pour obtenir le budget mensuel, puis diviser par le nombre de collectivités actives)
    df_actif = df_evolution_statut[df_evolution_statut['statut'] == 'actif'].copy()
    df_actif['cout_par_collectivite'] = (df_actif['budget_annuel']) / df_actif['nb_collectivites']
    df_actif['cout_par_collectivite'] = df_actif['cout_par_collectivite'].fillna(0).round(2)
    
    # Métriques
    afficher_metriques_temporelles(df_actif, 'cout_par_collectivite', label_prefix="Coût/Collectivité - ")
    
    # Graphique
    afficher_graphique_plotly(
        df_actif,
        x_column='mois_label',
        y_column='cout_par_collectivite',
        element_id="line_evolution_cout_par_collectivite",
        graph_type="line",
        legend_y="Coût par collectivité avec PAP actif (€)",
        trend_group_value="cout_par_collectivite",
        trend_calculation="budget_3m_pct",
        target_value=None
    )


    # ======================
    st.markdown("---")
    st.badge('Activité', icon="💫", color="blue")
    st.markdown('### B-3 | Coût annuel par utilisateur actif ≤ 12 mois (€/utilisateur)')
    st.markdown("""
    Un utilisateur actif 12 mois est défini comme un utilisateur :

    - qui n'est jamais défini comme conseiller ou partenaire
    - qui n'est pas un utilisateur interne (nous)
    - dont l'email ne contient pas 'ademe'
    - qui a effectué au moins une connexion dans les 12 derniers mois

    Limites : 
    
    - certains utilisateurs qui ne sont pas des agents passent quand même ces filtres
    - certains utilisateurs utilisent des ad blockers, j'en récupère néanmoins une bonne partie en tenant compte aussi de toutes les modifications sur les FA
    """)
    
    # Préparation des données
    df_evolution_statut = df_user_actif_12_mois.copy()
    df_evolution_statut = df_evolution_statut[df_evolution_statut['mois'] >= '2023-01-01'].copy()
    df_evolution_statut['annee'] = df_evolution_statut['mois'].dt.year
    
    # Grouper par année et mois pour obtenir le nombre d'utilisateurs uniques actifs par mois
    df_evolution_statut = df_evolution_statut.groupby(['annee', 'mois'])['email'].nunique().reset_index(name='nb_users')
    df_evolution_statut = df_evolution_statut.sort_values('mois')
    df_evolution_statut['mois_label'] = df_evolution_statut['mois'].apply(lambda x: x.strftime('%Y-%m'))
    
    # Associer le budget à chaque année
    budget_mapping = {2023: budget_2023, 2024: budget_2024, 2025: budget_2025, 2026: budget_2026}
    df_evolution_statut['budget_annuel'] = df_evolution_statut['annee'].map(budget_mapping)
    
    # Calculer le coût par utilisateur actif (budget annuel / 12 pour obtenir le budget mensuel, puis diviser par le nombre d'utilisateurs actifs)
    df_evolution_statut['cout_par_user'] = (df_evolution_statut['budget_annuel']) / df_evolution_statut['nb_users']
    df_evolution_statut['cout_par_user'] = df_evolution_statut['cout_par_user'].fillna(0).round(2)
    
    # Métriques
    afficher_metriques_temporelles(df_evolution_statut, 'cout_par_user', label_prefix="Coût/User - ")
    
    # Graphique
    afficher_graphique_plotly(
        df_evolution_statut,
        x_column='mois_label',
        y_column='cout_par_user',
        element_id="line_evolution_cout_par_user",
        graph_type="line",
        legend_y="Coût par utilisateur actif (€)",
        trend_group_value="cout_par_user",
        trend_calculation="budget_3m_pct",
        target_value=None
    )
    