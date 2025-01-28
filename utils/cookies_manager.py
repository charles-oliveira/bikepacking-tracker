import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager

def initialize_cookies_manager():
    """
    Inicializa o gerenciador de cookies para a aplicação Streamlit.

    Retorna:
        EncryptedCookieManager: Instância inicializada do gerenciador de cookies.
    """
    cookies = EncryptedCookieManager(prefix="bikepacking_tracker", password="password")

    if not cookies.ready():
        st.stop()  

    return cookies

def set_auth_cookies(cookies, authenticated, user_email=None):
    """
    Define os cookies de autenticação.

    Parâmetros:
        cookies (EncryptedCookieManager): Instância do gerenciador de cookies.
        authenticated (bool): Estado de autenticação do usuário.
        user_email (str, opcional): Email do usuário autenticado.
    """
    try:
        cookies["authenticated"] = "true" if authenticated else "false"
        if user_email:
            cookies["user_email"] = user_email
        cookies.save()
    except Exception as e:
        st.error(f"Erro ao definir cookies: {e}")

def clear_auth_cookies(cookies):
    """
    Redefine os cookies relacionados à autenticação.

    Parâmetros:
        cookies (EncryptedCookieManager): Instância do gerenciador de cookies.
    """
    try:
        cookies["authenticated"] = "false"  
        cookies["user_email"] = ""  
        cookies.save()
    except Exception as e:
        st.error(f"Erro ao limpar cookies: {e}")
