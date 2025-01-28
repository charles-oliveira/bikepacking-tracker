import os
import streamlit as st
from firebase.firebase_utils import authenticate_user
from streamlit_cookies_manager import EncryptedCookieManager
from email_validator import validate_email, EmailNotValidError


COOKIE_PASSWORD = os.getenv("COOKIE_MANAGER_PASSWORD", "default_password")  
cookies = EncryptedCookieManager(prefix="bikepacking_tracker", password=COOKIE_PASSWORD)

if not cookies.ready():
    st.stop()

def display_login():
    """
    Exibe o formulário de login na interface Streamlit.
    Solicita email e senha, e autentica o usuário ao clicar no botão "Entrar".

    Fluxo:
    - Se o usuário for autenticado com sucesso:
        - O estado de autenticação é armazenado na sessão (`st.session_state.authenticated`).
        - As informações de autenticação são salvas nos cookies.
        - Uma mensagem de boas-vindas é exibida.
    - Caso contrário:
        - Uma mensagem de erro é exibida.
    """
    st.title("Login para acesso")

    email = st.text_input("Email", placeholder="Digite seu email")
    password = st.text_input("Senha", placeholder="Digite sua senha", type="password")

    if st.button("Entrar"):
        if not email or not password:
            st.error("Por favor, preencha todos os campos.")
            return

        try:
            validate_email(email)  
        except EmailNotValidError as e:
            st.error(f"Email inválido: {e}")
            return

        with st.spinner("Autenticando..."):  
            try:
                user = authenticate_user(email, password)
                if user:
                    st.session_state.authenticated = True
                    cookies["authenticated"] = "true"
                    cookies["user_email"] = user["email"]  
                    cookies.save()  
                    st.success(f"Bem-vindo(a), {user['email']}!")
                else:
                    st.error("Credenciais inválidas.")
            except ConnectionError:
                st.error("Erro de conexão. Verifique sua internet e tente novamente.")
            except Exception as e:
                st.error(f"Erro ao autenticar: {e}")

def logout():
    """
    Realiza o logout do usuário.

    Fluxo:
    - O estado de autenticação é redefinido para falso.
    - Os cookies relacionados à autenticação são excluídos.
    - Uma mensagem de sucesso é exibida.
    """
    st.session_state.authenticated = False
    cookies.delete("authenticated") 
    cookies.delete("user_email")  
    st.success("Você saiu com sucesso!")
