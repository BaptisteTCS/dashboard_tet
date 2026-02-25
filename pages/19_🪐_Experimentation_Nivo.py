import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sources et Méthodologies", page_icon="📚", layout="wide")

st.title("📚 Sources de données et méthodologies par région")

# Lire et afficher le contenu du fichier markdown
try:
    with open('data/sources_et_methodologies_par_region.md', 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    st.markdown(markdown_content, unsafe_allow_html=True)
    
except FileNotFoundError:
    st.error("Le fichier sources_et_methodologies_par_region.md est introuvable.")
except Exception as e:
    st.error(f"Erreur lors de la lecture du fichier : {e}")
