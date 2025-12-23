import geopandas as gpd
import streamlit as st
import plotly.express as px

from utils.db import (
    read_table
)

@st.cache_resource(ttl="2d")
def load_data():
    df_ct_niveau = read_table('ct_niveau')
    return df_ct_niveau

@st.cache_resource(ttl=None)
def load_epci():
    return gpd.read_parquet("data/epci_simplifie.parquet")

gdf_epci = load_epci()
df_ct_niveau = load_data() 

st.set_page_config(layout="wide")
st.title("🗺️ Carte de France")


st.badge("Carte de France", icon=':material/map:', color='orange')

gdf_epci_selected = gdf_epci.merge(df_ct_niveau, on='siren')

# Reprojection Lambert-93 (EPSG:2154) → WGS84 (EPSG:4326) pour Plotly/Mapbox
if gdf_epci_selected.crs is None:
    gdf_epci_selected = gdf_epci_selected.set_crs(epsg=2154)
gdf_epci_selected = gdf_epci_selected.to_crs(epsg=4326)

# Couleurs par niveau (-1 à 3) - clés en string pour Plotly
color_map = {
    "Inactives": "#f4a5a5",
    "Activées": "#ffcc99",
    "PAP": "#a1d99b",
    "PAP actif": "#74c476",
    "PAP actif >2.5": "#31a354"
}

# Convertir niveau en string pour le mapping des couleurs
gdf_epci_selected['niveau_str'] = gdf_epci_selected['niveau'].astype(str)

# Convertir en GeoJSON pour Plotly
geojson = gdf_epci_selected.geometry.__geo_interface__

# Créer la carte choropleth
fig = px.choropleth_mapbox(
    gdf_epci_selected,
    geojson=geojson,
    locations=gdf_epci_selected.index,
    color="niveau_str",
    color_discrete_map=color_map,
    custom_data=["nom", "score"] if "nom" in gdf_epci_selected.columns else ["score"],
    mapbox_style="carto-positron",
    zoom=5,
    center={"lat": 46.2276, "lon": 2.2137},
    opacity=0.7,
    category_orders={"niveau_str": ["Inactives", "Activées", "PAP", "PAP actif", "PAP actif >2.5"]}
)

# Personnaliser le hover pour n'afficher que le nom et le score
if "nom" in gdf_epci_selected.columns:
    fig.update_traces(hovertemplate="<b>%{customdata[0]}</b><br>Score: %{customdata[1]}<extra></extra>")
else:
    fig.update_traces(hovertemplate="Score: <b>%{customdata[0]}</b><extra></extra>")

fig.update_layout(
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    legend_title_text="Niveau",
    height=700
)

st.plotly_chart(fig, use_container_width=True)

