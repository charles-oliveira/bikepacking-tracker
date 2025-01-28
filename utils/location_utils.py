import streamlit as st
import folium
from streamlit_folium import folium_static
from firebase.firebase_utils import set_data, get_data
import pandas as pd

@st.cache_data
def get_route_data():
    """
    Obtém os dados de localização armazenados no banco de dados Firebase.

    Retorna:
        list: Uma lista de dicionários contendo informações sobre as localizações
              (cidade, latitude e longitude). Retorna uma lista vazia se nenhum dado for encontrado.
    """
    try:
        data = get_data("locations")
        if data:
            return [{"cidade": loc.get("cidade", "Desconhecida"), 
                     "latitude": loc.get("latitude"), 
                     "longitude": loc.get("longitude")} 
                    for loc in data.values() if loc.get("latitude") and loc.get("longitude")]
        return []
    except Exception as e:
        st.error(f"Erro ao obter os dados de localização: {e}")
        return []

def display_map_page():
    """
    Exibe a página de mapa com as localizações armazenadas.

    - Renderiza um mapa interativo com marcadores baseados nas coordenadas armazenadas.
    - Adiciona uma mensagem informativa se não houver localizações disponíveis.
    - Lida com possíveis erros e os exibe ao usuário.
    """
    st.header("Mapa do Percurso")
    try:
        locations = get_route_data()
        if locations:
            map_data = pd.DataFrame(locations)
            
            m = folium.Map(location=[map_data["latitude"].mean(), 
                                     map_data["longitude"].mean()], 
                           zoom_start=10)
            
            for _, row in map_data.iterrows():
                folium.Marker(
                    location=[row["latitude"], row["longitude"]],
                    popup=f"{row['cidade']} ({row['latitude']:.4f}, {row['longitude']:.4f})",
                    icon=folium.Icon(color="green", icon="bicycle", prefix="fa")
                ).add_to(m)
            
            folium_static(m)
        else:
            st.info("Nenhuma localização encontrada.")
    except Exception as e:
        st.error(f"Erro ao carregar o mapa: {e}")
