import streamlit as st
import folium
from streamlit_folium import folium_static
from firebase.firebase_utils import set_data, get_data
import pandas as pd
import geocoder
from streamlit.components.v1 import html

def get_route_data():
    """
    Obtém os dados de localização armazenados no banco de dados Firebase.
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

def add_location_to_db(location):
    """
    Adiciona uma nova localização no banco de dados Firebase.
    """
    try:
        set_data("locations", location)
        st.success(f"Localização {location['cidade']} adicionada com sucesso!")
        st.experimental_rerun() 
    except Exception as e:
        st.error(f"Erro ao adicionar localização: {e}")

def display_map_page():
    """
    Exibe a página de mapa com as localizações armazenadas.
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

    st.subheader("Adicionar Nova Localização")
    location_option = st.radio(
        "Escolha como você deseja capturar a localização:",
        ("Manual", "GPS")
    )

    if location_option == "Manual":
        cidade = st.text_input("Cidade")
        latitude = st.number_input("Latitude", format="%.6f")
        longitude = st.number_input("Longitude", format="%.6f")
        
        if st.button("Adicionar Localização Manual"):
            if cidade and latitude and longitude:
                new_location = {
                    "cidade": cidade,
                    "latitude": latitude,
                    "longitude": longitude
                }
                add_location_to_db(new_location)
            else:
                st.warning("Por favor, preencha todos os campos.")

    elif location_option == "GPS":
        gps_location = get_gps_location()

        if gps_location:
            st.write(f"Localização atual via GPS: {gps_location['cidade']} ({gps_location['latitude']:.6f}, {gps_location['longitude']:.6f})")
            add_location_to_db(gps_location)

def get_gps_location():
    """
    Captura a localização via GPS usando JavaScript.
    """
    location = None
    gps_code = """
    <script>
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                var latitude = position.coords.latitude;
                var longitude = position.coords.longitude;
                var city = 'Desconhecida';  // Pode usar uma API para obter a cidade com base nas coordenadas
                var location = {latitude: latitude, longitude: longitude, cidade: city};
                window.parent.postMessage(location, '*');
            });
        } else {
            alert("Geolocalização não suportada.");
        }
    </script>
    """
    html(gps_code, height=0)

    return location
