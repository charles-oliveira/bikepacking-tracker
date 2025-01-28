import streamlit as st
from datetime import datetime
from firebase_admin import db

def set_data(path, data):
    """
    Envia dados para o banco de dados Firebase em um caminho específico.

    Parâmetros:
        path (str): O caminho no banco de dados Firebase onde os dados serão armazenados.
        data (dict): Os dados a serem enviados.

    Tratamento de Erros:
        Exibe uma mensagem de erro no Streamlit caso ocorra uma exceção ao enviar os dados.
    """
    try:
        ref = db.reference(path)
        ref.push(data)
    except Exception as e:
        st.error(f"Erro ao enviar os dados: {e}")

def show_trip_progress():
    """
    Exibe o formulário para registrar o progresso da viagem.

    - Permite ao usuário registrar distância, altimetria e tempo estimado.
    - Valida os dados de entrada para evitar envios incompletos.
    - Envia os dados validados para o Firebase em um caminho definido.

    Interface:
        - Campos para distância (em km), altimetria (em metros) e tempo estimado (em formato hh:mm).
        - Botão de envio que valida os dados antes de enviá-los.

    Feedback ao Usuário:
        - Exibe mensagens de erro em caso de entrada inválida ou falha no envio.
        - Exibe mensagem de sucesso ao enviar os dados com êxito.
    """
    st.header("Progresso da Viagem")
    with st.form("form_progresso"):
        distancia = st.number_input(
            label="Distância (km)",
            min_value=0.0,
            step=0.1,
            format="%.2f",
            help="Insira a distância percorrida em quilômetros."
        )

        altimetria = st.number_input(
            label="Altimetria (m)",
            min_value=0,
            step=1,
            help="Insira a altimetria acumulada em metros."
        )

        tempo = st.text_input(
            label="Tempo estimado (hh:mm)",
            placeholder="Exemplo: 02:30",
            help="Insira o tempo estimado no formato hh:mm."
        )

        submit_button = st.form_submit_button("Enviar")

        if submit_button:
            if not tempo:
                st.error("Por favor, preencha o campo de tempo.")
            else:
                try:
                    datetime.strptime(tempo, "%H:%M")
                    data = {
                        "distancia": distancia,
                        "altimetria": altimetria,
                        "tempo": tempo,
                        "data_envio": datetime.now().isoformat()  
                    }

                    set_data("progresso_viagem", data)
                    st.success("Dados enviados com sucesso para o Firebase!")
                except ValueError:
                    st.error("Por favor, insira o tempo no formato correto (hh:mm).")
