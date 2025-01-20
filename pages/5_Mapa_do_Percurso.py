import streamlit as st
import pandas as pd

# Dados fictícios de localização
@st.cache_data
def load_map_data():
    return pd.DataFrame({
        "lat": [-23.5489, -23.5505, -23.5523],
        "lon": [-46.6388, -46.6354, -46.6305]
    })

map_data = load_map_data()

st.title("Mapa do Percurso 📍")
st.map(map_data)
