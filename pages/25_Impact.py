import streamlit as st

# Configuration de la page en premier
st.set_page_config(
    page_title="Mesure d'impact",
    page_icon="🎯",
    layout="wide"
)

import pandas as pd
from streamlit_elements import elements, nivo, mui
from utils.db import read_table

# ==========================
# Configuration des couleurs
# ==========================

# Couleurs principales du dashboard
COLOR_GREEN_PRIMARY = "#81c995"    # Vert principal (barres, jauge, KPI)
COLOR_GREEN_LIGHT = "#e0e0e0"      # Vert clair (gradient, seconde barre)
COLOR_GREEN_MEDIUM = "#81c995"     # Vert moyen (gradient jauge)
COLOR_YELLOW_LIGHT = "#edf4e3"     # Jaune clair (KPI objectif)
COLOR_RED_OBJECTIVE = "#eb3349"    # Rouge (marqueur objectif)

# ==========================
# Chargement des données
# ==========================

@st.cache_resource(ttl="3d")
def load_data():
    df_blois_impact = read_table('ccph_impact')
    return df_blois_impact

df_blois_impact = load_data()

# ==========================
# Configuration
# ==========================

# Objectif SNBC (en kT CO2) - Modifiable via sidebar
objectif_snbc = df_blois_impact.reduction_leveir.sum()

# ==========================
# Titre et header
# ==========================

st.title("🎯 Modélisation d'impact GES des plans d'actions")
st.markdown(
    "Modélisation des réductions d’émissions de GES de la **Communauté de Communes du Pays Houdanais**."
)
st.markdown('---')

# ==========================
# Calculs des métriques
# ==========================

# Réduction modéliséee totale (basée sur l'implication réelle)
# Note : les valeurs sont NÉGATIVES (ex: -48 kT = réduction de 48 kT)
reduction_totale = df_blois_impact['reduction_theorique'].sum()

# Pourcentage d'atteinte de l'objectif (ratio des valeurs absolues)
# Ex: |-48| / |-209| = 23% de l'objectif atteint
pct_atteinte = (abs(reduction_totale) / abs(objectif_snbc) * 100) if objectif_snbc != 0 else 0

# Écart à l'objectif SNBC (négatif si en dessous de l'objectif)
# Ex: 23% - 100% = -77% (on est à 77% en dessous de l'objectif)
ecart_objectif = pct_atteinte - 100

# Objectif atteint ? (avec des valeurs négatives, plus négatif = meilleur)
objectif_atteint = reduction_totale <= objectif_snbc

# Nombre de leviers
nb_leviers_total = len(df_blois_impact[df_blois_impact.reduction_leveir<0])
# Leviers actifs = ceux avec une réduction négative (donc qui réduisent vraiment)
nb_leviers_actifs = len(df_blois_impact[df_blois_impact['reduction_theorique'] < 0])
nb_leviers_zero = len(df_blois_impact[df_blois_impact['reduction_theorique'] == 0])

# ==========================
# SECTION 1 : KPI GLOBAUX
# ==========================

st.badge('Bilan de la modélisation', icon=':material/trending_up:', color='orange')

ecart_kt = abs(objectif_snbc) - abs(reduction_totale)
st.markdown(f"D'après la modélisation, l'objectif SNBC territorialisé ne sera pas atteint au regard des Plans & Actions suivis actuellement sur Territoires en Transitions.")


# KPIs en colonnes avec Nivo/MUI
with elements("kpi_cards"):
    with mui.Box(sx={
        "display": "grid",
        "gridTemplateColumns": "repeat(2, 1fr)",
        "gap": 2,
        "mb": 3
    }):
        # KPI 1 : Réduction modéliséee totale (valeur absolue pour lisibilité)
        with mui.Card(sx={
            "p": 3,
            "background": COLOR_GREEN_PRIMARY,
            "borderRadius": 3,
            "color": "white",
            "textAlign": "center"
        }):
            mui.Typography("Réduction modéliséee", variant="subtitle2", sx={"opacity": 0.9})
            mui.Typography(f"{abs(reduction_totale):.0f}", variant="h3", sx={"fontWeight": "bold", "my": 1})
            mui.Typography("kt CO₂eq", variant="subtitle1")
        
        # KPI 3 : Pourcentage de l'objectif accompli
        with mui.Card(sx={
            "p": 3,
            "background": COLOR_YELLOW_LIGHT,
            "borderRadius": 3,
            "color": "#333",
            "textAlign": "center"
        }):
            mui.Typography("Atteinte des objectifs SNBC en 2030", variant="subtitle2", sx={"opacity": 0.7})
            mui.Typography(f"{pct_atteinte:.0f}%", variant="h3", sx={"fontWeight": "bold", "my": 1})

# Jauge de progression visuelle

with elements("gauge_progress"):
    with mui.Box(sx={"height": 60, "px": 2}):
        # Barre de progression personnalisée
        with mui.Box(sx={
            "position": "relative",
            "height": 40,
            "backgroundColor": "#e0e0e0",
            "borderRadius": 2,
            "overflow": "hidden",
            "mt": 2
        }):
            # Barre de progression remplie (utilise pct_atteinte calculé plus haut)
            with mui.Box(sx={
                "position": "absolute",
                "left": 0,
                "top": 0,
                "height": "100%",
                "width": f"{min(pct_atteinte, 100):.0f}%",
                "background": f"linear-gradient(90deg, {COLOR_GREEN_PRIMARY} 0%, {COLOR_GREEN_MEDIUM} 100%)" if pct_atteinte >= 100 else f"linear-gradient(135deg, {COLOR_GREEN_MEDIUM} 0%, {COLOR_GREEN_PRIMARY} 100%)",
                "transition": "width 0.5s ease-in-out"
            }):
                pass
        
        # Légende (valeurs absolues pour lisibilité)
        with mui.Box(sx={"display": "flex", "justifyContent": "space-between", "mt": 1}):
            mui.Typography(
                f"Modélisation : {abs(reduction_totale):.0f} / {abs(objectif_snbc):.0f} ktCO₂eq",
                variant="body2",
                sx={"color": "#31333F"}  # couleur par défaut du texte markdown streamlit
            )


st.markdown("---")

# ==========================
# SECTION 2 : Treemap des secteurs
# ==========================*

st.badge("Synthèse par secteur réglementaire", icon=':material/factory:', color='orange')

# Préparation des données pour les treemaps
df_secteurs_agg = df_blois_impact.groupby('Secteur').agg({
    'reduction_leveir': 'sum',
    'reduction_theorique': 'sum'
}).reset_index()

# Trier les secteurs par potentiel de réduction pour attribuer les couleurs
df_secteurs_sorted = df_secteurs_agg.sort_values('reduction_leveir', ascending=True).copy()

# Palette de couleurs ordonnée (du plus important au moins important)
# Top 3 avec des couleurs vives, les autres avec des couleurs plus douces
color_palette = [
  # Vert pastel vibrant biodiversité natur # Bleu pastel vibrant eau ressources
    "#FFD966",  # Jaune pastel vibrant énergie solaire  # Violet pastel vibrant innovation numérique
    "#FFB36B",
    "#6EC6FF",  # Orange pastel vibrant mobilités
    "#90A4AE",  # Bleu gris pastel structurant industrie bâtiment
    "#FF8A80", 
    "#6EDC8C",
    "#C792EA" # Rouge rose pastel vibrant climat adaptation
]








# Créer un mapping secteur -> couleur basé sur le classement
secteur_colors = {}
for idx, row in df_secteurs_sorted.iterrows():
    rank = list(df_secteurs_sorted.index).index(idx)
    secteur_colors[row['Secteur']] = color_palette[min(rank, len(color_palette) - 1)]

# TreeMap 1 : Potentiel de réduction par secteur (reduction_leveir)
st.markdown("**Potentiel de réduction par secteur** d'après les objectifs SNBC 2030.")

# Créer les children triés par reduction_leveir (pour que les couleurs soient dans l'ordre)
children_potentiel = []
colors_ordered_potentiel = []
for _, row in df_secteurs_sorted.iterrows():
    if row['reduction_leveir'] != 0:
        children_potentiel.append({
            "name": row['Secteur'],
            "value": abs(float(row['reduction_leveir'])),
            "loc": abs(float(row['reduction_leveir']))
        })
        colors_ordered_potentiel.append(secteur_colors[row['Secteur']])

treemap_data_potentiel = {
    "name": "Secteurs",
    "children": children_potentiel
}

with elements("treemap_secteurs_potentiel"):
    with mui.Box(sx={"height": 500}):
        nivo.TreeMap(
            data=treemap_data_potentiel,
            identity="name",
            value="value",
            valueFormat=".0f",
            label="id",
            margin={"top": 10, "right": 10, "bottom": 10, "left": 10},
            labelSkipSize=12,
            labelTextColor={"from": "color", "modifiers": [["darker", 1.8]]},
            parentLabelPosition="left",
            parentLabelTextColor={"from": "color", "modifiers": [["darker", 2]]},
            borderColor={"from": "color", "modifiers": [["darker", 0.3]]},
            colors=colors_ordered_potentiel,  # Couleurs dans l'ordre du classement
            enableParentLabel=True,
            animate=True,
            motionConfig="gentle",
            theme={
                "text": {
                    "fontFamily": "Source Sans Pro, sans-serif",
                    "fontSize": 13,
                    "fill": "#31333F"
                },
                "labels": {
                    "text": {
                        "fontFamily": "Source Sans Pro, sans-serif",
                        "fontSize": 13,
                        "fill": "#ffffff"
                    }
                },
                "tooltip": {
                    "container": {
                        "background": "rgba(30, 30, 30, 0.95)",
                        "color": "#ffffff",
                        "fontSize": "13px",
                        "fontFamily": "Source Sans Pro, sans-serif",
                        "borderRadius": "4px",
                        "boxShadow": "0 2px 8px rgba(0,0,0,0.3)",
                        "padding": "8px 12px",
                        "border": "1px solid rgba(255, 255, 255, 0.1)"
                    }
                }
            }
        )


# TreeMap 2 : Réduction modélisée par secteur (reduction_theorique)
st.markdown("**Réduction modélisée par secteur** d'après les Plans & Actions de la collectivité sur Territoires en Transitions.")

# Créer les children dans le même ordre pour garder les mêmes couleurs
children_theorique = []
colors_ordered_theorique = []
for _, row in df_secteurs_sorted.iterrows():
    # Trouver la valeur correspondante dans df_secteurs_agg
    secteur_data = df_secteurs_agg[df_secteurs_agg['Secteur'] == row['Secteur']]
    if not secteur_data.empty and secteur_data.iloc[0]['reduction_theorique'] != 0:
        children_theorique.append({
            "name": row['Secteur'],
            "value": abs(float(secteur_data.iloc[0]['reduction_theorique'])),
            "loc": abs(float(secteur_data.iloc[0]['reduction_theorique']))
        })
        colors_ordered_theorique.append(secteur_colors[row['Secteur']])

treemap_data_theorique = {
    "name": "Secteurs",
    "children": children_theorique
}

with elements("treemap_secteurs_theorique"):
    with mui.Box(sx={"height": 500}):
        nivo.TreeMap(
            data=treemap_data_theorique,
            identity="name",
            value="value",
            valueFormat=".0f",
            label="id",
            margin={"top": 10, "right": 10, "bottom": 10, "left": 10},
            labelSkipSize=12,
            labelTextColor={"from": "color", "modifiers": [["darker", 1.8]]},
            parentLabelPosition="left",
            parentLabelTextColor={"from": "color", "modifiers": [["darker", 2]]},
            borderColor={"from": "color", "modifiers": [["darker", 0.3]]},
            colors=colors_ordered_theorique,  # Mêmes couleurs dans le même ordre
            enableParentLabel=True,
            animate=True,
            motionConfig="gentle",
            theme={
                "text": {
                    "fontFamily": "Source Sans Pro, sans-serif",
                    "fontSize": 13,
                    "fill": "#31333F"
                },
                "labels": {
                    "text": {
                        "fontFamily": "Source Sans Pro, sans-serif",
                        "fontSize": 13,
                        "fill": "#ffffff"
                    }
                },
                "tooltip": {
                    "container": {
                        "background": "rgba(30, 30, 30, 0.95)",
                        "color": "#ffffff",
                        "fontSize": "13px",
                        "fontFamily": "Source Sans Pro, sans-serif",
                        "borderRadius": "4px",
                        "boxShadow": "0 2px 8px rgba(0,0,0,0.3)",
                        "padding": "8px 12px",
                        "border": "1px solid rgba(255, 255, 255, 0.1)"
                    }
                }
            }
        )

st.markdown("---")

# ==========================
# SECTION 2 : TOP LEVIERS CONTRIBUTEURS
# ==========================

st.badge("Modélisation par levier", icon=':material/bar_chart:', color='green')

# Sélecteur de secteur global
secteurs = sorted(df_blois_impact['Secteur'].dropna().unique())
selected_secteur = st.selectbox(
    "Filtrer par secteur",
    options=["Tous"] + list(secteurs),
    index=0
)

# Filtrer les données selon le secteur sélectionné
if selected_secteur == "Tous":
    df_filtered = df_blois_impact.copy()
else:
    df_filtered = df_blois_impact[df_blois_impact['Secteur'] == selected_secteur].copy()

# KPIs du secteur/global
reduction_secteur = df_filtered['reduction_theorique'].sum()
potentiel_secteur = df_filtered['reduction_leveir'].sum()
nb_leviers_secteur = len(df_filtered[df_filtered.reduction_leveir<0])
nb_actifs_secteur = len(df_filtered[df_filtered['reduction_theorique'] < 0])

col1, col2, col3, col4 = st.columns(4)
col1.metric("Projection", f"{abs(reduction_secteur):.0f} kt")
col2.metric("Potentiel", f"{abs(potentiel_secteur):.0f} kt")
col3.metric("Leviers actifs", f"{nb_actifs_secteur}/{nb_leviers_secteur}")
col4.metric("Part de l'objectif", f"{(abs(reduction_secteur)/abs(potentiel_secteur)*100):.0f}%")


st.markdown('Trier par :')

# Segmented control pour choisir le tri
vue_tri = st.segmented_control(
    "Mode de tri",
    options=["Réduction modélisée par levier", "Potentiel de réduction par levier", "Effort estimé par levier"],
    default="Réduction modélisée par levier",
    label_visibility="collapsed"
)

# Calculer le taux d'exploitation (ratio theorique/potentiel en %)
df_filtered['taux_exploitation'] = (df_filtered['reduction_theorique'] / df_filtered['reduction_leveir'].replace(0, float('nan'))) * 100

# Trier selon le mode sélectionné (décroissant)
if vue_tri == "Réduction modélisée par levier":
    # Par Réduction modéliséee (nsmallest car valeurs négatives = plus grande réduction)
    df_top = df_filtered.nsmallest(20, 'reduction_theorique')
elif vue_tri == "Potentiel de réduction par levier":
    # Par potentiel du levier (reduction_leveir)
    df_top = df_filtered.nsmallest(20, 'reduction_leveir')
else:  # Exploitation
    # Par taux d'exploitation (plus grand taux en premier)
    df_top = df_filtered.nlargest(20, 'taux_exploitation')

if not df_top.empty:
    # Format pour Nivo Bar (horizontal) - valeurs absolues pour lisibilité
    bar_data_top = [
        {
            "levier": row['Leviers SGPE'][:50] + "..." if len(row['Leviers SGPE']) > 50 else row['Leviers SGPE'],
            "levier_full": row['Leviers SGPE'],
            "Réduction modéliséee": abs(float(row['reduction_theorique'])),
            "Réduction potentielle": abs(float(row['reduction_leveir'])) - abs(float(row['reduction_theorique'])),
            "secteur": row['Secteur'],
            "implication": row['implication'],
            "justification": row['justification'] if pd.notna(row['justification']) else "Aucune action sur ce levier",
            "taux_exploitation": f"{row['taux_exploitation']:.1f}%" if pd.notna(row['taux_exploitation']) else "N/A"
        }
        for _, row in df_top.iterrows()
    ]
    # Inverser pour avoir le plus grand en haut
    bar_data_top = bar_data_top[::-1]

    # Hauteur dynamique : 40px par barre + marges
    chart_height = max(300, len(bar_data_top) * 40 + 70)
    
    with elements("bar_top_leviers"):
        with mui.Box(sx={"height": chart_height}):
            nivo.Bar(
                data=bar_data_top,
                keys=["Réduction modéliséee", "Réduction potentielle"],
                indexBy="levier",
                layout="horizontal",
                margin={"top": 20, "right": 200, "bottom": 50, "left": 280},
                padding=0.3,
                valueScale={"type": "linear"},
                indexScale={"type": "band", "round": True},
                colors=[COLOR_GREEN_PRIMARY, COLOR_GREEN_LIGHT],
                borderColor={"from": "color", "modifiers": [["darker", 1.6]]},
                axisTop=None,
                axisRight=None,
                axisBottom={
                    "tickSize": 5,
                    "tickPadding": 5,
                    "tickRotation": 0,
                    "legend": "kt CO₂eq",
                    "legendPosition": "middle",
                    "legendOffset": 40
                },
                axisLeft={
                    "tickSize": 5,
                    "tickPadding": 5,
                    "tickRotation": 0
                },
                labelSkipWidth=12,
                labelSkipHeight=12,
                labelTextColor={"from": "color", "modifiers": [["darker", 3]]},
                legends=[
                    {
                        "dataFrom": "keys",
                        "anchor": "bottom-right",
                        "direction": "column",
                        "justify": False,
                        "translateX": 120,
                        "translateY": 0,
                        "itemsSpacing": 2,
                        "itemWidth": 100,
                        "itemHeight": 20,
                        "itemDirection": "left-to-right",
                        "itemOpacity": 0.85,
                        "symbolSize": 20
                    }
                ],
                animate=True,
                motionConfig="gentle",
                theme={
                    "text": {
                        "fontFamily": "Source Sans Pro, sans-serif",
                        "fontSize": 11,
                        "fill": "#31333F"
                    },
                    "tooltip": {
                        "container": {
                            "background": "rgba(30, 30, 30, 0.95)",
                            "color": "#ffffff",
                            "fontSize": "13px",
                            "fontFamily": "Source Sans Pro, sans-serif",
                            "borderRadius": "4px",
                            "boxShadow": "0 2px 8px rgba(0,0,0,0.3)",
                            "padding": "8px 12px"
                        }
                    }
                }
            )


    st.markdown("---")
    st.badge("Détail par levier", icon=':material/list:', color='green')
    
    # CSS pour les cartes style warning Streamlit
    st.markdown("""
    <style>
    .levier-warning {
        border-radius: 4px;
        padding: 1rem;
        margin-bottom: 8px;
        border-left: 4px solid;
        transition: all 0.2s ease;
    }
    .levier-warning:hover {
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
        transform: translateX(2px);
    }
    .levier-warning-orange {
        background: #fffaf0;
        border-left-color: #ff8c00;
    }
    .levier-warning-yellow {
        background: #fffff0;
        border-left-color: #d69e2e;
    }
    .levier-warning-green {
        background: #f0fff4;
        border-left-color: #81c995;
    }
    .levier-warning-greener {
        background: #d4f4dd;
        border-left-color: #38a169;
    }
    .levier-title {
        font-size: 14px;
        font-weight: 600;
        color: #1a1a2e;
        margin: 0 0 6px 0;
        line-height: 1.4;
    }
    .levier-subtitle {
        font-size: 13px;
        color: #666;
        margin: 0 0 8px 0;
    }
    .levier-justification {
        font-size: 13px;
        color: #555;
        line-height: 1.5;
        margin: 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Fonction pour déterminer le style selon l'implication
    def get_implication_style(implication):
        """Retourne la classe CSS et l'emoji selon le niveau d'implication (0-100)"""
        try:
            impl = float(implication)
        except (ValueError, TypeError):
            return "levier-warning-yellow", "⚠️"
        
        if impl < 25:
            return "levier-warning-orange", "❕"
        elif impl < 50:
            return "levier-warning-yellow", "❕"
        elif impl < 75:
            return "levier-warning-green", "💪"
        else:
            return "levier-warning-greener", "💪💪"
    
    # Filtrer les cartes selon le secteur sélectionné
    cartes_filtrees = bar_data_top[::-1]
    
    # Afficher toutes les cartes filtrées
    for idx, item in enumerate(cartes_filtrees):
        # Récupérer les IDs correspondants
        levier_row = df_blois_impact[df_blois_impact['Leviers SGPE'] == item['levier_full']]
        has_ids = not levier_row.empty and 'ids' in levier_row.columns and levier_row.iloc[0]['ids']
        
        # Style selon l'implication
        css_class, emoji = get_implication_style(item['implication'])
        
        col_card, col_btn = st.columns([5, 1])
        
        with col_card:
            st.markdown(f"""
            <div class="levier-warning {css_class}">
                <p class="levier-title">{emoji} {item['levier_full']}</p>
                <p class="levier-subtitle">Effort estimé : {int(item['implication'])}% <br /> Secteur : {item['secteur']}</p>
                <p class="levier-justification">{item['justification']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_btn:
            col_btn.space('stretch')
            btn_label = "Voir les actions de références" if item['justification'] == "Aucune action sur ce levier" else "Aller aux actions"
            if st.button(btn_label, key=f"btn_top_{idx}", use_container_width=True, type='primary'):
                st.info("🔧 **Fonction à venir**")
                if has_ids:
                    st.caption(f"IDs : {levier_row.iloc[0]['ids']}")

else:
    st.warning("⚠️ Aucun levier avec une Réduction modéliséee positive")

st.markdown("---")

# ==========================
# SECTION 4 : LEVIERS À ZÉRO
# ==========================

st.badge("Leviers non exploités", icon=':material/warning:', color='orange')

df_zero = df_filtered[(df_filtered['reduction_theorique'] == 0) & (df_filtered['reduction_leveir'] < 0)].copy()

if not df_zero.empty:
    st.warning(f"⚠️ **{len(df_zero)} leviers** n'ont pas été exploités. Cela correspond à un manque totale de : {abs(df_zero['reduction_leveir'].sum()):.0f} kt CO₂eq")
    
    # Trier par abs(reduction_leveir) décroissant (nsmallest car valeurs négatives)
    df_zero_sorted = df_zero.sort_values('reduction_leveir', ascending=True)
    
    # Bar chart des leviers à zéro
    bar_data_zero = [
        {"levier": row['Leviers SGPE'], "Reduction potentielle": abs(float(row['reduction_leveir']))}
        for _, row in df_zero_sorted.iterrows()
    ]
    # Inverser pour avoir le plus grand en haut du graphique horizontal
    bar_data_zero = bar_data_zero[::-1]
    
    with elements("bar_zero_secteurs"):
        with mui.Box(sx={"height": 350}):
            nivo.Bar(
                data=bar_data_zero,
                keys=["Reduction potentielle"],
                indexBy="levier",
                layout="horizontal",
                margin={"top": 20, "right": 150, "bottom": 50, "left": 250},
                padding=0.3,
                colors=["#ef5350"],
                axisBottom={
                    "legend": "Reduction potentielle (kt CO₂eq)",
                    "legendPosition": "middle",
                    "legendOffset": 40
                },
                labelTextColor="#ffffff",
                animate=True,
                theme={
                    "text": {
                        "fontFamily": "Source Sans Pro, sans-serif",
                        "fontSize": 11,
                        "fill": "#31333F"
                    },
                    "tooltip": {
                        "container": {
                            "background": "rgba(30, 30, 30, 0.95)",
                            "color": "#ffffff",
                            "fontSize": "13px",
                            "fontFamily": "Source Sans Pro, sans-serif",
                            "borderRadius": "4px",
                            "boxShadow": "0 2px 8px rgba(0,0,0,0.3)",
                            "padding": "8px 12px"
                        }
                    }
                }
            )

else:
    st.success("✅ Tous les leviers ont une Réduction modéliséee positive !")

