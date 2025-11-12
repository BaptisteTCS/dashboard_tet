import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_elements import elements, nivo, mui

from utils.data import load_df_pap_notes
from utils.plots import prepare_radar_data_nivo


# Configuration de la page
st.set_page_config(layout="wide")

df_notes = load_df_pap_notes()

if df_notes.empty:
    st.info("Aucune donnée de notes. Alimentez `load_df_pap_notes()`.")
    st.stop()

# Conserver les deux dernières semaines disponibles
semaines = sorted(df_notes['semaine'].dropna().unique(), reverse=True)[:2]
df_2 = df_notes[df_notes['semaine'].isin(semaines)].copy()

# Titre avec la date de la dernière semaine
if len(semaines) > 0:
    derniere_semaine = pd.to_datetime(semaines[0])
    semaine_str = derniere_semaine.strftime("%d/%m/%Y")
    st.title(f"🏆 Top 10 des Champions de la semaine du {semaine_str}")
else:
    st.title("🏆 Top 10 des Champions")

st.markdown("### Les collectivités qui ont le plus progressé cette semaine")
st.markdown("---")

if len(semaines) < 2:
    st.warning("⚠️ Pas assez d'historique pour comparer les semaines N et N-1.")
    st.stop()

# Calcul des différences de scores
df_pivot = df_2.pivot(index=['collectivite_id', 'plan_id'], columns='semaine', values='score')

if df_pivot.shape[1] >= 2:
    df_pivot['difference_score'] = df_pivot.iloc[:, 1] - df_pivot.iloc[:, 0]
    df_diff = df_pivot[['difference_score']].reset_index()
    top_rows = df_diff.sort_values(by='difference_score', ascending=False).head(10)
    
    if top_rows.empty or top_rows['difference_score'].max() <= 0:
        st.info("ℹ️ Aucune progression significative détectée cette semaine.")
        st.stop()
    
    
    # Badges de classement
    badges = {1: "🥇", 2: "🥈", 3: "🥉", 4: "4️⃣", 5: "5️⃣", 6: "6️⃣", 7: "7️⃣", 8: "8️⃣", 9: "9️⃣", 10: "10"}
    
    # Affichage en galerie (2 colonnes)
    rank = 1
    for idx in range(0, len(top_rows), 2):
        cols = st.columns(2)
        
        for col_idx, col in enumerate(cols):
            row_idx = idx + col_idx
            if row_idx < len(top_rows):
                top_row = top_rows.iloc[row_idx]
                plan_id = top_row['plan_id']
                diff = top_row['difference_score']
                
                df_plan = df_2[df_2['plan_id'] == plan_id].sort_values(by='semaine', ascending=False)
                if len(df_plan) < 2:
                    continue
                    
                row = df_plan.iloc[0]
                row_precedente = df_plan.iloc[1]
                
                with col:
                    
                    # Header avec badge et infos (tronqué pour éviter le décalage)
                    collectivite_nom = row['nom_ct']
                    plan_nom = row['nom']
                    
                    # Tronquer si trop long pour éviter les décalages
                    titre_complet = f"{collectivite_nom} - {plan_nom}"
                    if len(titre_complet) > 50:
                        titre_affiche = titre_complet[:47] + "..."
                    else:
                        titre_affiche = titre_complet
                    
                    st.markdown(f"### {badges.get(rank, '🏅')} {titre_affiche}")
                    
                    # Metrics
                    col_metric1, col_metric2, col_metric3 = st.columns(3)
                    with col_metric1:
                        st.metric(
                            "Score actuel",
                            f"{round(row['score'], 2)}",
                            delta=f"+{round(diff, 2)}"
                        )
                    with col_metric2:
                        st.metric(
                            "Score précédent",
                            f"{round(row_precedente['score'], 2)}"
                        )
                    with col_metric3:
                        progression_pct = (diff / row_precedente['score'] * 100) if row_precedente['score'] > 0 else 0
                        st.metric(
                            "Progression",
                            f"+{round(progression_pct, 1)}%"
                        )
                    
                    # Infos collectivité
                    with st.expander("ℹ️ Détails de la collectivité", expanded=False):
                        st.write(f"**Collectivité :** {row['nom_ct']}")
                        st.write(f"**Plan :** {row['nom']}")
                        st.write(f"**Type :** {row.get('type_collectivite', 'N/A')}")
                        st.write(f"**Région :** {row.get('region_name', 'N/A')}")
                        st.write(f"**Population :** {int(row.get('population_totale', 0)):,} habitants".replace(',', ' '))
                    
                    # Graphe radar avec comparaison Nivo
                    radar_data = prepare_radar_data_nivo(row, row_precedente)
                    
                    with elements(f"radar_champion_{plan_id}_{rank}"):
                        with mui.Box(sx={"height": 500}):
                            nivo.Radar(
                                data=radar_data,
                                keys=["Actuelle", "Précédente"],
                                indexBy="taste",
                                maxValue=5,
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
                                colors=["#ffc121", "#999999"],
                                fillOpacity=0.5,
                                blendMode="multiply",
                                animate=True,
                                motionConfig="wobbly",
                                isInteractive=True,
                                theme={
                                    "text": {
                                        "fontFamily": "Source Sans Pro, sans-serif",
                                        "fontSize": 13,
                                        "fill": "#808495"
                                    },
                                    "labels": {
                                        "text": {
                                            "fontFamily": "Source Sans Pro, sans-serif",
                                            "fontSize": 16,
                                            "fill": "#808495"
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
                                            "fill": "#808495"
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
                                },
                                legends=[
                                    {
                                        "anchor": "top-left",
                                        "direction": "column",
                                        "translateX": -50,
                                        "translateY": -40,
                                        "itemWidth": 80,
                                        "itemHeight": 20,
                                        "itemTextColor": "#808495",
                                        "symbolSize": 12,
                                        "symbolShape": "circle",
                                    }
                                ]
                            )
                    
                    st.markdown("---")
                    
                rank += 1
    
    # Statistiques globales en bas
    st.markdown("---")
    st.markdown("### 📊 Statistiques globales")
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    
    with col_stat1:
        st.metric("Meilleure progression", f"+{round(top_rows['difference_score'].max(), 2)}")
    with col_stat2:
        st.metric("Progression moyenne (Top 10)", f"+{round(top_rows['difference_score'].mean(), 2)}")
    with col_stat3:
        nb_total_progressions = len(df_diff[df_diff['difference_score'] > 0])
        st.metric("Collectivités en progression", nb_total_progressions)
    with col_stat4:
        st.metric("Semaines comparées", f"{len(semaines)}")
    
else:
    st.info("ℹ️ Données insuffisantes pour calculer la différence de score.")


