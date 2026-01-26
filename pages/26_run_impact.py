import streamlit as st
import pandas as pd
from utils.db import read_table

# Configuration de la page en premier
st.set_page_config(
    page_title="Calcul impact",
    page_icon="🥸",
    layout="wide"
)


