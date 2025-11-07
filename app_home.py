import streamlit as st

st.markdown(
    """
    <div style="padding: 14px 18px; background: linear-gradient(90deg,#3B82F6, #60A5FA); border-radius: 12px; color: white;">
      <h1 style="margin: 0; font-size: 28px;">Dashboard de Territoires en Transitions</h1>
      <p style="margin: 6px 0 0; opacity: 0.95;">Visualisations clés et exploration interactive</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")
st.info("✨ Utilisez le menu à gauche organisé par sections pour naviguer entre les pages")

st.markdown("### 📂 Navigation organisée")
st.markdown("""
Les pages sont maintenant organisées en **7 sections** :

- **📊 Métriques & Suivi** : Indicateurs clés et suivi hebdomadaire
  - North Star & Metrics
  - Weekly
  - Champions

- **🏛️ Tableaux de Bord** : Vues d'ensemble par collectivité et conseillers
  - TDB Collectivité
  - Implication Conseillers
  - Suivi Campagne Régions
  - Suivi Bizdevs

- **🔓 Open Data** : Exploration des données publiques
  - Dashboard Open Data
  - Open Data par Collectivité

- **🤖 Intelligence Artificielle** : Assistants et suggestions
  - AI Stats Assistant
  - Suggestion Indicateurs

- **⚙️ Import & Configuration** : Gestion des données
  - Import Indicateurs
  - Import Groupement Indicateurs

- **🚀 Livraison** : Déploiements pre-prod et prod
  - Livraison Pre-Prod
  - Livraison Prod

- **🧪 Bac à sable** : Environnement de test
  - North Star Bac à sable
""")

