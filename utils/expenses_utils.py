from datetime import datetime
import streamlit as st
from firebase.firebase_utils import set_data

def display_expenses_page():
    """
    Exibe o formulário para registrar os gastos, incluindo descrição e valor.
    Envia os dados para o Firebase após o envio do formulário.
    """
    st.header("Registrar Gastos")

    # Formulário para adicionar um novo gasto
    with st.form("form_gastos"):
        descricao = st.text_input("Descrição do Gasto")
        categoria = st.selectbox("Categoria", ["Alimentação", "Hospedagem", "Transporte", "Outros"])
        valor = st.number_input("Valor (R$)", min_value=0.0, step=0.1, format="%.2f")
        data = st.date_input("Data do Gasto", value=datetime.today())  # Seleção manual da data
        submit_button = st.form_submit_button("Adicionar Gasto")

        if submit_button:
            if not descricao or valor <= 0:
                st.error("Por favor, preencha a descrição e o valor do gasto.")
            else:
                gasto_data = {
                    "descricao": descricao,
                    "categoria": categoria,
                    "valor": valor,
                    "data": data.strftime("%Y-%m-%d")  # Formata a data escolhida
                }
                try:
                    set_data("gastos", gasto_data)  # Envia os dados para o Firebase
                    st.success("Gasto registrado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao registrar o gasto: {e}")
