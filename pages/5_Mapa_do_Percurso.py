import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from firebase.firebase_utils import get_data

# Configuração da página
st.title("Mapa do Percurso 📍")

# Função para carregar dados do Firebase
def fetch_map_data():
    try:
        # Corrigido o caminho para "locations"
        data = get_data("locations")
        if data:
            locations = []
            for entry in data.values():
                locations.append({
                    "cidade": entry.get("cidade", "Desconhecida"),
                    "latitude": float(entry.get("latitude", 0)),
                    "longitude": float(entry.get("longitude", 0)),
                    "hora": entry.get("timestamp", "Sem horário"),
                })
            
            if not locations:
                st.warning("Nenhuma localização válida encontrada no Firebase.")
            return pd.DataFrame(locations) if locations else pd.DataFrame(
                columns=["cidade", "latitude", "longitude", "hora"]
            )
        else:
            st.warning("Nenhum dado encontrado no caminho 'locations'.")
            return pd.DataFrame(columns=["cidade", "latitude", "longitude", "hora"])
    except Exception as e:
        st.error(f"Erro ao buscar dados do Firebase: {e}")
        return pd.DataFrame(columns=["cidade", "latitude", "longitude", "hora"])

# Carregar dados
map_data = fetch_map_data()

# Exibir mapa com rastro se houver dados
if not map_data.empty:
    try:
        # Criar o mapa base
        m = folium.Map(location=[map_data["latitude"].mean(), map_data["longitude"].mean()], zoom_start=10)

        # Adicionar marcadores de bicicleta
        locations = []  # Lista para armazenar as coordenadas dos pontos
        for index, row in map_data.iterrows():
            folium.Marker(
                location=[row["latitude"], row["longitude"]],
                popup=f"{row['cidade']}<br>{row['hora']}<br>({row['latitude']:.4f}, {row['longitude']:.4f})",
                icon=folium.Icon(color="green", icon="bicycle", prefix="fa"),  # Ícone de bicicleta (FontAwesome)
            ).add_to(m)
            # Adicionar coordenada à lista para desenhar a linha
            locations.append([row["latitude"], row["longitude"]])

        # Adicionar linha conectando os pontos
        if len(locations) > 1:
            folium.PolyLine(locations, color="green", weight=2.5, opacity=1).add_to(m)

        # Exibir o mapa
        folium_static(m)

        # Exibir a linha do tempo
        st.subheader("Linha do Tempo 📜")
        
        # Exibir os dados das cidades
        for index, row in map_data.iterrows():
            st.markdown(f"### {row['cidade']}")
            st.markdown(f"**Hora:** {row['hora']}")
            st.markdown(f"**Coordenadas:** ({row['latitude']:.4f}, {row['longitude']:.4f})")
            st.markdown("---")  # Linha de separação para as outras cidades

    except Exception as e:
        st.error(f"Erro ao renderizar o mapa: {e}")
else:
    st.info("Nenhuma localização registrada ainda.")
