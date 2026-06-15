import streamlit as st
import pandas as pd
from streamlit_elements import elements, nivo, mui

from utils.data import (
    load_df_pap,
    load_df_collectivite,
    load_df_note_plan_semaine,
)
from utils.db import read_table
from utils.plan_note_dashboard import (
    build_plan_scores_df,
    render_notation_definition_expander,
    render_plan_radar_gallery,
    top_plans_weekly_progression,
)

# Mise en cache des données avec TTL de 1 jour

@st.cache_data(ttl="1d")
def get_df_pap():
    """Charge les données PAP."""
    return load_df_pap()

@st.cache_data(ttl="1d")
def get_df_collectivite():
    """Charge les données des collectivités."""
    return load_df_collectivite()

@st.cache_data(ttl="1d")
def get_champions_data():
    """Données champions : note_plan_semaine + radars fiches."""
    df_note_semaine = load_df_note_plan_semaine()
    df_note_fiche = read_table(
        "note_fiche_historique",
        where_sql="mois=(select max(mois) from note_fiche_historique)",
    )
    df_fiche_action_plan = read_table("fiche_action_plan")
    df_pap_passage = read_table("pap_date_passage")
    return df_note_semaine, df_note_fiche, df_fiche_action_plan, df_pap_passage

st.set_page_config(layout="wide")

# === TOGGLE THEME SOMBRE ===
col_title, col_toggle = st.columns([8, 1])

with col_title:
    st.title("⚡ Weekly")
    st.markdown("Les info clés de la semaine.")
with col_toggle:
    st.space("medium")
    dark_mode = st.toggle("🌙", value=False)

# Définition des thèmes Nivo
theme_clair = {
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

theme_sombre = {
    "text": {
        "fontFamily": "Source Sans Pro, sans-serif",
        "fontSize": 13,
        "fill": "#FFFFFF"
    },
    "labels": {
        "text": {
            "fontFamily": "Source Sans Pro, sans-serif",
            "fontSize": 13,
            "fill": "#FFFFFF"
        }
    },
    "tooltip": {
        "container": {
            "background": "rgba(30, 30, 30, 0.95)",
            "color": "#FFFFFF",
            "fontSize": "13px",
            "fontFamily": "Source Sans Pro, sans-serif",
            "borderRadius": "4px",
            "boxShadow": "0 2px 8px rgba(0,0,0,0.3)",
            "padding": "8px 12px",
            "border": "1px solid rgba(255, 255, 255, 0.1)"
        }
    }
}

# Sélection du thème actif
theme_actif = theme_sombre if dark_mode else theme_clair

# Définition des thèmes Radar Nivo
theme_radar_clair = {
    "text": {
        "fontFamily": "Source Sans Pro, sans-serif",
        "fontSize": 13,
        "fill": "#31333F"
    },
    "labels": {
        "text": {
            "fontFamily": "Source Sans Pro, sans-serif",
            "fontSize": 16,
            "fill": "#31333F"
        }
    },
    "grid": {
        "line": {
            "stroke": "#e0e0e0",
            "strokeWidth": 1,
            "strokeOpacity": 0.8
        }
    },
    "legends": {
        "text": {
            "fontFamily": "Source Sans Pro, sans-serif",
            "fontSize": 12,
            "fill": "#31333F"
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

theme_radar_sombre = {
    "text": {
        "fontFamily": "Source Sans Pro, sans-serif",
        "fontSize": 13,
        "fill": "#FFFFFF"
    },
    "labels": {
        "text": {
            "fontFamily": "Source Sans Pro, sans-serif",
            "fontSize": 16,
            "fill": "#FFFFFF"
        }
    },
    "grid": {
        "line": {
            "stroke": "#4a4a4a",
            "strokeWidth": 1,
            "strokeOpacity": 0.3
        }
    },
    "legends": {
        "text": {
            "fontFamily": "Source Sans Pro, sans-serif",
            "fontSize": 12,
            "fill": "#FFFFFF"
        }
    },
    "tooltip": {
        "container": {
            "background": "rgba(30, 30, 30, 0.95)",
            "color": "#FFFFFF",
            "fontSize": "13px",
            "fontFamily": "Source Sans Pro, sans-serif",
            "borderRadius": "4px",
            "boxShadow": "0 2px 8px rgba(0,0,0,0.3)",
            "padding": "8px 12px",
            "border": "1px solid rgba(255, 255, 255, 0.1)"
        }
    }
}

# Sélection du thème radar actif
theme_radar_actif = theme_radar_sombre if dark_mode else theme_radar_clair

# === CHARGEMENT DES DONNÉES ===
df_pap = get_df_pap()
df_ct = get_df_collectivite()

if df_pap.empty:
    st.info("Aucune donnée. Branchez vos sources dans `utils/data.py`.")
    st.stop()

# Jointure avec les collectivités
df_pap_enrichi = pd.merge(df_pap, df_ct, on='collectivite_id', how='left')

# Préparation des dates
df_pap_enrichi['passage_pap'] = pd.to_datetime(df_pap_enrichi['passage_pap'], errors='coerce').dt.tz_localize(None)
df_pap_enrichi['semaine_pap'] = df_pap_enrichi['passage_pap'].dt.to_period('W').dt.to_timestamp()

# === IDENTIFICATION DES SEMAINES S-1 ET S-2 ===
semaines_disponibles = sorted(df_pap_enrichi['semaine_pap'].dropna().unique(), reverse=True)

if len(semaines_disponibles) < 2:
    st.warning("⚠️ Pas assez de données pour comparer S-1 et S-2.")
    st.stop()

# S-1 = dernière semaine, S-2 = avant-dernière semaine
s1 = semaines_disponibles[0]
s2 = semaines_disponibles[1]

s1_str = pd.to_datetime(s1).strftime("%d/%m/%Y")
s2_str = pd.to_datetime(s2).strftime("%d/%m/%Y")

st.markdown("---")

# === DONNÉES S-1 ET S-2 ===
df_s1 = df_pap_enrichi[df_pap_enrichi['semaine_pap'] == s1].copy()
df_s2 = df_pap_enrichi[df_pap_enrichi['semaine_pap'] == s2].copy()

# Nouveaux PAP en S-1
nouveaux_pap_s1 = len(df_s1)
nouveaux_pap_s2 = len(df_s2)
diff_pap = nouveaux_pap_s1 - nouveaux_pap_s2

# Nouvelles collectivités PAP en S-1 (qui n'avaient jamais eu de PAP avant)
# Pour S-1 : collectivités ayant un PAP avant S-1
ct_avant_s1 = df_pap_enrichi[df_pap_enrichi['semaine_pap'] < s1]['collectivite_id'].unique()
ct_s1 = df_s1['collectivite_id'].unique()
nouvelles_ct_s1 = len([ct for ct in ct_s1 if ct not in ct_avant_s1])

# Pour S-2 : collectivités ayant un PAP avant S-2
ct_avant_s2 = df_pap_enrichi[df_pap_enrichi['semaine_pap'] < s2]['collectivite_id'].unique()
ct_s2 = df_s2['collectivite_id'].unique()
nouvelles_ct_s2 = len([ct for ct in ct_s2 if ct not in ct_avant_s2])

diff_ct = nouvelles_ct_s1 - nouvelles_ct_s2

# Répartition Import/Autonome
if 'import' in df_s1.columns and 'import' in df_s2.columns:
    nb_importes_s1 = len(df_s1[df_s1['import'] == 'Importé'])
    nb_importes_s2 = len(df_s2[df_s2['import'] == 'Importé'])
    diff_importes = nb_importes_s1 - nb_importes_s2
    
    nb_autonomes_s1 = len(df_s1[df_s1['import'] == 'Autonome'])
    nb_autonomes_s2 = len(df_s2[df_s2['import'] == 'Autonome'])
    diff_autonomes = nb_autonomes_s1 - nb_autonomes_s2
else:
    nb_importes_s1 = 0
    nb_autonomes_s1 = 0
    diff_importes = 0
    diff_autonomes = 0

# === CALCUL DES ÉVOLUTIONS SUR 2 MOIS ===
# Prendre les 8 dernières semaines (environ 2 mois)
nb_semaines_evolution = min(8, len(semaines_disponibles))
semaines_evolution = semaines_disponibles[:nb_semaines_evolution][::-1]  # Ordre chronologique

# Initialisation des listes d'évolution
evolution_pap = []
evolution_ct = []
evolution_importes = []
evolution_autonomes = []

# Calcul pour chaque semaine
for semaine in semaines_evolution:
    df_semaine = df_pap_enrichi[df_pap_enrichi['semaine_pap'] == semaine]
    
    # Nouveaux PAP
    evolution_pap.append(len(df_semaine))
    
    # Nouvelles collectivités (jamais vu avant)
    ct_avant_semaine = df_pap_enrichi[df_pap_enrichi['semaine_pap'] < semaine]['collectivite_id'].unique()
    ct_semaine = df_semaine['collectivite_id'].unique()
    nouvelles_ct_semaine = len([ct for ct in ct_semaine if ct not in ct_avant_semaine])
    evolution_ct.append(nouvelles_ct_semaine)
    
    # PAP Importés et Autonomes
    if 'import' in df_semaine.columns:
        evolution_importes.append(len(df_semaine[df_semaine['import'] == 'Importé']))
        evolution_autonomes.append(len(df_semaine[df_semaine['import'] == 'Autonome']))
    else:
        evolution_importes.append(0)
        evolution_autonomes.append(0)

st.badge("Indicateurs clés", icon=":material/key:", color="green")

# === INDICATEURS CLÉS ===
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Nouveaux PAP",
        nouveaux_pap_s1,
        delta=f"{diff_pap:+d}",
        delta_color="normal",
        border = True,
        chart_type="line",
        chart_data=evolution_pap
    )

with col2:
    st.metric(
        "Nouvelles collectivités PAP",
        nouvelles_ct_s1,
        delta=f"{diff_ct:+d}",
        delta_color="normal",
        border = True,
        chart_type="line",
        chart_data=evolution_ct
    )

with col3:
    if 'import' in df_s1.columns:
        st.metric(
            "PAP Importés",
            nb_importes_s1,
            delta=f"{diff_importes:+d}",
            delta_color="normal",
            border = True,
            chart_type="line",
            chart_data=evolution_importes
        )
    else:
        st.metric("PAP Importés", "N/A")

with col4:
    if 'import' in df_s1.columns:
        st.metric(
            "PAP Autonomes",
            nb_autonomes_s1,
            delta=f"{diff_autonomes:+d}",
            delta_color="normal",
            border = True,
            chart_type="line",
            chart_data=evolution_autonomes
        )
    else:
        st.metric("PAP Autonomes", "N/A")

# === GRAPHIQUES DE RÉPARTITION ===
tab1, tab2, tab3, tab4 = st.tabs(["🆕 Plans", "🎉 Nouvelles collectivités", "💪 Champions", "📢 Fiches actions"])

with tab1:
    if not df_s1.empty and 'nom_plan' in df_s1.columns:
        # Préparer les données pour le Pie Chart Nivo
        pap_par_plan_s1 = df_s1['nom_plan'].value_counts().reset_index()
        pap_par_plan_s1.columns = ['Type de plan', 'Nombre']
        
        # Convertir au format Nivo Pie : [{ "id": "label", "value": number }, ...]
        pie_data = [
            {
                "id": row['Type de plan'],
                "label": row['Type de plan'],
                "value": int(row['Nombre'])
            }
            for _, row in pap_par_plan_s1.iterrows()
        ]
        
        # Afficher le Pie Chart Nivo avec thème par défaut
        with elements("pie_plans"):
            with mui.Box(sx={"height": 450}):
                nivo.Pie(
                    data=pie_data,
                    margin={"top": 40, "right": 80, "bottom": 80, "left": 80},
                    innerRadius=0.5,
                    padAngle=0.7,
                    cornerRadius=3,
                    activeOuterRadiusOffset=8,
                    borderWidth=1,
                    borderColor={"from": "color", "modifiers": [["darker", 0.2]]},
                    arcLinkLabelsSkipAngle=10,
                    arcLinkLabelsTextColor=theme_actif["text"]["fill"],
                    arcLinkLabelsThickness=2,
                    arcLinkLabelsColor={"from": "color"},
                    arcLabelsSkipAngle=10,
                    arcLabelsTextColor={"from": "color", "modifiers": [["darker", 2]]},
                    enableArcLabels=True,
                    enableArcLinkLabels=True,
                    theme=theme_actif
                )
    else:
        st.info("Pas de données pour S-1")

    st.dataframe(df_s1[['nom', 'nom_plan', 'type_collectivite', 'population_totale', 'import']].sort_values(by='population_totale', ascending=False), hide_index=True)
        
with tab2: 
    # Ne garder que les collectivités qui n'avaient jamais eu de PAP avant S-1
    df_s1_nouvelles = df_s1[df_s1['collectivite_id'].isin([ct for ct in ct_s1 if ct not in ct_avant_s1])].copy()

    # Collectivités uniques de S-1 (seulement les nouvelles)
    collectivites_s1 = df_s1_nouvelles.groupby('collectivite_id').agg({
        'nom': 'first',
        'type_collectivite': 'first',
        'population_totale': 'first',
        'import': 'first' if 'import' in df_s1_nouvelles.columns else lambda x: 'N/A',
        # nom_plan peut être numérique ou autre selon le back — tout passer en str pour join
        'nom_plan': lambda x: ', '.join(str(v) for v in pd.unique(x.dropna())),
    }).reset_index()

    collectivites_s1.columns = [
        'ID Collectivité', 'Nom', 'Type', 'Population', 'Statut Import', 'Plans'
    ]

    # Tri par population décroissante
    collectivites_s1 = collectivites_s1.sort_values(by='Population', ascending=False)
    collectivites_s1['Population'] = collectivites_s1['Population'].fillna(0).astype(int)

    # Affichage du tableau
    st.dataframe(
        collectivites_s1[['Nom', 'Plans', 'Statut Import', 'Type', 'Population']],
        hide_index=True
    )

with tab3:
    (
        df_note_semaine,
        df_note_fiche,
        df_fiche_action_plan,
        df_pap_passage,
    ) = get_champions_data()

    render_notation_definition_expander()

    progression = top_plans_weekly_progression(df_note_semaine)

    if progression is None:
        st.warning("⚠️ Pas assez d'historique hebdomadaire pour comparer les progressions.")
    else:
        semaine_actuelle = progression["semaine_actuelle"]
        semaine_precedente = progression["semaine_precedente"]
        st.caption(
            f"Progression entre le {semaine_precedente.strftime('%d/%m/%Y')} "
            f"et le {semaine_actuelle.strftime('%d/%m/%Y')} "
            f"(note /10 depuis `note_plan_semaine`)"
        )

        top_plans = progression["top_plans"]
        if not top_plans:
            st.info("ℹ️ Aucune progression significative détectée cette semaine.")
        else:
            delta_by_plan = progression["delta_by_plan"]
            note_by_plan = progression["note_by_plan"]

            meta_plans = (
                df_pap_passage.dropna(subset=["plan"])
                .drop_duplicates(subset=["plan"])
                .set_index("plan")
            )
            nom_plan_par_id = meta_plans["nom_plan_ct"].to_dict()
            collectivite_id_by_plan = meta_plans["collectivite_id"].to_dict()
            nom_ct_par_plan = (
                df_pap_passage.dropna(subset=["plan"])
                .drop_duplicates(subset=["plan"])
                .set_index("plan")["nom"]
                .to_dict()
            )
            display_name_by_plan = {
                plan_id: (
                    f"{nom_ct_par_plan.get(plan_id, 'Collectivité')} — "
                    f"{nom_plan_par_id.get(plan_id, str(int(plan_id)))}"
                )
                for plan_id in top_plans
            }

            df_plan_scores = build_plan_scores_df(
                df_fiche_action_plan, df_note_fiche, top_plans
            )
            if df_plan_scores.empty:
                st.warning("Aucune fiche notée pour les plans champions cette semaine.")
            else:
                plans_affichables = [
                    p for p in top_plans if p in df_plan_scores["plan"].values
                ]
                df_plan_scores = (
                    df_plan_scores.set_index("plan")
                    .loc[plans_affichables]
                    .reset_index()
                )

                render_plan_radar_gallery(
                    df_plan_scores,
                    nom_plan_par_id,
                    collectivite_id_by_plan=collectivite_id_by_plan,
                    display_name_by_plan=display_name_by_plan,
                    delta_by_plan={p: delta_by_plan[p] for p in plans_affichables},
                    note_by_plan={p: note_by_plan[p] for p in plans_affichables},
                    theme=theme_radar_actif,
                    element_key_prefix="weekly_radar_plan",
                )
    