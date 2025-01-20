import streamlit as st
import json

# Carregar dados
@st.cache_data
def load_stops_data():
    with open("data/stops_data.json", "r") as file:
        return json.load(file)

stops_data = load_stops_data()

st.title("Paradas Planejadas 🗺️")
st.markdown("Confira as paradas previstas durante a viagem:")
for stop in stops_data:
    st.markdown(f"""
    - **Local:** {stop['local']}
    - **Tipo:** {stop['tipo']}
    - **Descrição:** {stop['descricao']}
    - **Horário estimado:** {stop['horario']}
    """)
