import streamlit as st
from firebase.firebase_utils import authenticate_user
from streamlit_cookies_manager import EncryptedCookieManager

cookies = EncryptedCookieManager(prefix="bikepacking_tracker", password="password")
if not cookies.ready():
    st.stop()

def display_login():
    st.title("Login para acesso")
    email = st.text_input("Email", placeholder="Digite seu email")
    password = st.text_input("Senha", placeholder="Digite sua senha", type="password")
    if st.button("Entrar"):
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
        except Exception as e:
            st.error(f"Erro ao autenticar: {e}")

def logout():
    st.session_state.authenticated = False
    cookies.delete("authenticated")
    cookies.delete("user_email")
    st.success("Você saiu com sucesso!")
