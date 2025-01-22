import streamlit as st
from firebase.firebase_utils import initialize_firebase, set_data, get_data, authenticate_user
import json

# Carregar credenciais do Firebase
try:
    cred_string = st.secrets["firebase"]["credentials"]
    cred_dict = json.loads(cred_string)
    if isinstance(cred_dict, dict):
        st.success("Credenciais carregadas com sucesso!")
    else:
        st.error("Credenciais no formato incorreto.")
except Exception as e:
    st.error(f"Erro ao carregar credenciais: {e}")
    cred_dict = None

# Verificar se as credenciais foram carregadas corretamente
if not isinstance(cred_dict, dict):
    st.error("As credenciais do Firebase não foram encontradas ou estão mal formatadas. Verifique a configuração.")
else:
    # URL do banco de dados Firebase
    DATABASE_URL = "https://bikepacking-tracker-3fa9f-default-rtdb.firebaseio.com"

    # Inicializar Firebase
    try:
        initialize_firebase(cred_dict, DATABASE_URL)
        st.success("Firebase inicializado com sucesso!")
    except Exception as e:
        st.error(f"Erro ao inicializar o Firebase: {e}")

    # Tela de login
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.title("Login para acesso")
        email = st.text_input("Email", placeholder="Digite seu email")
        password = st.text_input("Senha", placeholder="Digite sua senha", type="password")

        if st.button("Entrar"):
            try:
                user = authenticate_user(email, password)
                if user:
                    st.session_state.authenticated = True
                    st.success(f"Bem-vindo(a), {user['email']}!")
                else:
                    st.error("Credenciais inválidas. Tente novamente.")
            except Exception as e:
                st.error(f"Erro ao autenticar: {e}")
    else:
        # Interface de usuário após autenticação
        st.title("Bikepacking Tracker")

        # Formulário para enviar dados
        with st.form("form_percurso"):
            distancia = st.number_input("Distância (km)", min_value=0.0, step=0.1, format="%.2f")
            altimetria = st.number_input("Altimetria (m)", min_value=0, step=1)
            tempo = st.text_input("Tempo estimado (hh:mm)")

            if st.form_submit_button("Enviar"):
                if not tempo:
                    st.error("Por favor, preencha o campo de tempo.")
                else:
                    data = {
                        "distancia": distancia,
                        "altimetria": altimetria,
                        "tempo": tempo,
                    }
                    try:
                        set_data("percurso/custom", data)
                        st.success("Dados enviados para o Firebase!")
                    except Exception as e:
                        st.error(f"Erro ao enviar os dados: {e}")

        # Recuperar e exibir dados do Firebase
        try:
            data = get_data("percurso/custom")
            if data:
                st.subheader("Dados no Firebase:")
                st.write(data)
            else:
                st.info("Nenhum dado encontrado no Firebase.")
        except Exception as e:
            st.error(f"Erro ao recuperar os dados: {e}")

        # Botão para sair
        if st.button("Sair"):
            st.session_state.authenticated = False
            st.success("Você saiu com sucesso.")
