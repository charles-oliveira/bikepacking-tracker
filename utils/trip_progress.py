import streamlit as st
from datetime import datetime
from firebase_admin import db

# Função para enviar os dados para o Firebase
def set_data(path, data):
    try:
        ref = db.reference(path)
        ref.push(data)
    except Exception as e:
        st.error(f"Erro ao enviar os dados: {e}")

def show_trip_progress():
    """
    Exibe o formulário para registrar o progresso da viagem, incluindo distância, altimetria e tempo estimado.
    Envia os dados para o Firebase após o envio do formulário.
    """
    st.header("Progresso da Viagem")
    with st.form("form_progresso"):
        distancia = st.number_input("Distância (km)", min_value=0.0, step=0.1, format="%.2f")
        altimetria = st.number_input("Altimetria (m)", min_value=0, step=1)
        tempo = st.text_input("Tempo estimado (hh:mm)")

        submit_button = st.form_submit_button("Enviar")
        if submit_button:
            if not tempo:
                st.error("Por favor, preencha o campo de tempo.")
            else:
                data = {
                    "distancia": distancia,
                    "altimetria": altimetria,
                    "tempo": tempo,
                }
                try:
                    set_data("progresso_viagem", data)
                    st.success("Dados enviados para o Firebase!")
                except Exception as e:
                    st.error(f"Erro ao enviar os dados: {e}")
