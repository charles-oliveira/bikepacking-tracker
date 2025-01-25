import streamlit as st
import pandas as pd
from firebase.firebase_utils import get_data

# Configuração da página
st.title("Mapa do Percurso 📍")

# Função para carregar dados do Firebase
@st.cache_data
def fetch_map_data():
    try:
        data = get_data("percurso/locations")
        if data:
            # Convertendo os dados em um DataFrame para facilitar a manipulação
            locations = []
            for key, entry in data.items():
                locations.append({
                    "cidade": entry.get("cidade"),
                    "latitude": entry.get("latitude"),
                    "longitude": entry.get("longitude"),
                    "hora": entry.get("timestamp")
                })
            return pd.DataFrame(locations)
        else:
            return pd.DataFrame(columns=["cidade", "latitude", "longitude", "hora"])
    except Exception as e:
        st.error(f"Erro ao buscar dados do Firebase: {e}")
        return pd.DataFrame(columns=["cidade", "latitude", "longitude", "hora"])

# Carregar dados
map_data = fetch_map_data()

# Exibir mapa se houver dados
if not map_data.empty:
    st.map(map_data[["latitude", "longitude"]])

    # Exibir linha do tempo
    st.subheader("Linha do Tempo 📜")
    for index, row in map_data.iterrows():
        st.write(
            f"- **{row['hora']}**: {row['cidade']} "
            f"({row['latitude']}, {row['longitude']})"
        )
else:
    st.info("Nenhuma localização registrada ainda.")
