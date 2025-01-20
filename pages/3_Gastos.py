import streamlit as st
import pandas as pd

# Carregar dados
@st.cache_data
def load_trip_data():
    return pd.read_csv("data/trip_data.csv")

trip_data = load_trip_data()

st.title("Gastos 💰")
st.table(trip_data[["Dia", "Gastos (R$)"]])
