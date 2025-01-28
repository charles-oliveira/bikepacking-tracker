import streamlit as st
import firebase_admin
from firebase_admin import credentials
from utils.cookies_manager import initialize_cookies_manager, set_auth_cookies, clear_auth_cookies
from firebase import authenticate_user
from utils.expenses_utils import display_expenses_page
from utils.location_utils import display_map_page
from utils.trip_progress import show_trip_progress
import json

credentials_path = "firebase/service_account.json"

database_url = "https://bikepacking-tracker-3fa9f-default-rtdb.firebaseio.com/"  

def initialize_firebase(cred_dict, database_url):
    """
    Inicializa o Firebase com as credenciais fornecidas.

    Parâmetros:
        cred_dict (dict): Dicionário contendo as credenciais do Firebase.
        database_url (str): URL do banco de dados do Firebase.

    Levanta:
        RuntimeError: Caso ocorra algum problema ao inicializar o Firebase.
    """
    try:
        cred = credentials.Certificate(cred_dict)
        if not firebase_admin._apps:  
            firebase_admin.initialize_app(cred, {"databaseURL": database_url})
    except Exception as e:
        raise RuntimeError(f"Erro ao inicializar o Firebase: {e}")

try:
    with open(credentials_path, "r") as f:
        cred_dict = json.load(f)  
    initialize_firebase(cred_dict, database_url)
except FileNotFoundError:
    st.error(f"Arquivo de credenciais não encontrado: {credentials_path}")
except Exception as e:
    st.error(f"Erro ao carregar credenciais: {e}")

cookies = initialize_cookies_manager()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = cookies.get("authenticated") == "true"

def display_login():
    """
    Exibe o formulário de login na interface Streamlit.
    Solicita email e senha do usuário e autentica ao clicar no botão 'Entrar'.
    """
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

def logout():
    """
    Realiza o logout do usuário.
    Define o estado de autenticação como falso e limpa os cookies relacionados.
    """
    st.session_state.authenticated = False
    clear_auth_cookies(cookies)
    st.session_state.logout_message = "Você foi desconectado com sucesso."

def main():
    """
    Gerencia o fluxo principal da aplicação.
    Exibe o menu e as páginas caso o usuário esteja autenticado, ou o formulário de login.
    """
    if st.session_state.authenticated:
        st.sidebar.title("Menu")
        menu_options = ["Progresso da Viagem", "Despesas", "Localização"]
        page = st.sidebar.selectbox("Escolha a página", menu_options)  

        if page == "Progresso da Viagem":
            show_trip_progress()  
        elif page == "Despesas":
            display_expenses_page()  
        elif page == "Localização":
            display_map_page() 

        if st.sidebar.button("Logout"):
            logout()
    else:
        if "logout_message" in st.session_state:
            st.success(st.session_state.logout_message)
            del st.session_state.logout_message 
        display_login()

if __name__ == "__main__":
    main()
