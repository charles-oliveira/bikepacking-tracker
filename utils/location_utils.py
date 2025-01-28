import streamlit as st
import folium
from streamlit_folium import folium_static
from firebase.firebase_utils import set_data, get_data
import pandas as pd

@st.cache_data
def get_route_data():
    data = get_data("locations")
    if data:
        return [{"cidade": loc.get("cidade", "Desconhecida"), 
                 "latitude": loc.get("latitude"), 
                 "longitude": loc.get("longitude")} 
                for loc in data.values() if loc.get("latitude") and loc.get("longitude")]
    return []

def display_map_page():
    st.header("Mapa do Percurso")
    try:
        locations = get_route_data()
        if locations:
            map_data = pd.DataFrame(locations)
            m = folium.Map(location=[map_data["latitude"].mean(), map_data["longitude"].mean()], zoom_start=10)
            for _, row in map_data.iterrows():
                folium.Marker([row["latitude"], row["longitude"]],
                              popup=f"{row['cidade']} ({row['latitude']:.4f}, {row['longitude']:.4f})",
                              icon=folium.Icon(color="green", icon="bicycle", prefix="fa")).add_to(m)
            folium_static(m)
        else:
            st.info("Nenhuma localização encontrada.")
    except Exception as e:
        st.error(f"Erro ao carregar o mapa: {e}")
