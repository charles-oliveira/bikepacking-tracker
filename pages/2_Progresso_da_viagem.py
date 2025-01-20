import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar dados
@st.cache_data
def load_trip_data():
    return pd.read_csv("data/trip_data.csv")

trip_data = load_trip_data()

# Gráficos
st.title("Progresso da Viagem 🔄")
st.markdown("### Quilometragem e Altimetria")
fig_km_alt = px.line(
    trip_data,
    x="Dia",
    y=["Distância (km)", "Altimetria (m)"],
    labels={"value": "Valores", "variable": "Métrica"},
    title="Progresso Diário"
)
st.plotly_chart(fig_km_alt, use_container_width=True)
