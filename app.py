import streamlit as st
from firebase.firebase_utils import initialize_firebase, set_data, get_data

# Caminho para as credenciais e URL do banco
CRED_PATH = "firebase_credentials.json"
DATABASE_URL = "https://bikepacking-tracker-default-rtdb.firebaseio.com"

# Inicializar Firebase
initialize_firebase(CRED_PATH, DATABASE_URL)

# Interface de usuário
st.title("Bikepacking Tracker")

# Formulário para enviar dados
with st.form("form_percurso"):
    distancia = st.number_input("Distância (km)", min_value=0)
    altimetria = st.number_input("Altimetria (m)", min_value=0)
    tempo = st.text_input("Tempo estimado (hh:mm)")
    if st.form_submit_button("Enviar"):
        data = {
            "distancia": distancia,
            "altimetria": altimetria,
            "tempo": tempo,
        }
        set_data("percurso/custom", data)
        st.success("Dados enviados para o Firebase!")


# Obter dados do Firebase
data = get_data("percurso/custom")
