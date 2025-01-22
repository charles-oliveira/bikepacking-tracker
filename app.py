import streamlit as st
from firebase.firebase_utils import initialize_firebase, set_data, get_data

# Obtém as credenciais da variável de ambiente
cred_dict = st.secrets["firebase"]["credentials"]

if cred_dict is None:
    st.error("As credenciais do Firebase não foram encontradas. Verifique a configuração.")
else:
    # URL do banco de dados
    DATABASE_URL = "https://bikepacking-tracker-default-rtdb.firebaseio.com"

    # Inicializar Firebase
    initialize_firebase(cred_dict, DATABASE_URL)

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
