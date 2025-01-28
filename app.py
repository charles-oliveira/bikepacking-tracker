import streamlit as st
import firebase_admin
from firebase_admin import credentials
from utils.cookies_manager import initialize_cookies_manager, set_auth_cookies, clear_auth_cookies
from firebase import authenticate_user
from utils.expenses_utils import display_expenses_page
from utils.location_utils import display_map_page
from utils.trip_progress import show_trip_progress
import json

# Caminho para o arquivo de credenciais do Firebase
credentials_path = "firebase/service_account.json"

# URL do banco de dados Firebase (substitua com a URL correta do seu banco de dados)
database_url = "https://bikepacking-tracker-3fa9f-default-rtdb.firebaseio.com/"  # Substitua com a URL correta

# Função para inicializar o Firebase
def initialize_firebase(cred_dict, database_url):
    try:
        cred = credentials.Certificate(cred_dict)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred, {"databaseURL": database_url})
    except Exception as e:
        raise RuntimeError(f"Erro ao inicializar o Firebase: {e}")

# Carregar credenciais
try:
    with open(credentials_path, "r") as f:
        cred_dict = json.load(f)
    # Inicializar Firebase
    initialize_firebase(cred_dict, database_url)
except FileNotFoundError:
    st.error(f"Arquivo de credenciais não encontrado: {credentials_path}")
except Exception as e:
    st.error(f"Erro ao carregar credenciais: {e}")

# Inicializar Cookies Manager
cookies = initialize_cookies_manager()

# Estado inicial da sessão
if "authenticated" not in st.session_state:
    st.session_state.authenticated = cookies.get("authenticated") == "true"

# Função de Login
def display_login():
    st.title("Login")
    email = st.text_input("Email", placeholder="Digite seu email")
    password = st.text_input("Senha", placeholder="Digite sua senha", type="password")

    if st.button("Entrar"):
        try:
            user = authenticate_user(email, password)
            if user:
                st.session_state.authenticated = True
                set_auth_cookies(cookies, authenticated=True, user_email=user["email"])
                st.success(f"Bem-vindo(a), {user['email']}!")
            else:
                st.error("Credenciais inválidas. Tente novamente.")
        except Exception as e:
            st.error(f"Erro ao autenticar: {e}")

# Função de Logout
def logout():
    st.session_state.authenticated = False
    clear_auth_cookies(cookies)
    st.session_state.logout_message = "Você foi desconectado com sucesso."


# Página principal
def main():
    if st.session_state.authenticated:
        # Exibe o menu lateral apenas se o usuário estiver autenticado
        st.sidebar.title("Menu")
        menu_options = ["Progresso da Viagem", "Despesas", "Localização"]
        page = st.sidebar.selectbox("Escolha a página", menu_options)

        if page == "Progresso da Viagem":
            show_trip_progress()  # Exibe a página de progresso da viagem
        elif page == "Despesas":
            display_expenses_page()  # Exibe a página de registro de despesas
        elif page == "Localização":
            display_map_page()  # Exibe a página de registro de localização

        # Botão de logout no final do menu
        if st.sidebar.button("Logout"):
            logout()
    else:
        # Exibe mensagem de logout, se houver
        if "logout_message" in st.session_state:
            st.success(st.session_state.logout_message)
            del st.session_state.logout_message  # Remove a mensagem após exibir
        display_login()  # Exibe o login se o usuário não estiver autenticado

# Executar a aplicação
if __name__ == "__main__":
    main()
