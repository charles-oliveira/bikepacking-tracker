import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager

def initialize_cookies_manager():
    """
    Inicializa o gerenciador de cookies para a aplicação Streamlit.

    Retorna:
        EncryptedCookieManager: Instância inicializada do gerenciador de cookies.
    """
    # Inicializa o gerenciador de cookies com um prefixo e senha
    cookies = EncryptedCookieManager(prefix="bikepacking_tracker", password="password")

    # Garante que os cookies estejam prontos para uso
    if not cookies.ready():
        st.stop()  # Pausa a execução até que os cookies estejam prontos

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
        # Define o estado de autenticação
        cookies["authenticated"] = "true" if authenticated else "false"
        # Define o email do usuário, se fornecido
        if user_email:
            cookies["user_email"] = user_email
        # Salva as alterações nos cookies
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
        # Remove os cookies relacionados à autenticação
        cookies["authenticated"] = "false"  # Marca como não autenticado
        cookies["user_email"] = ""  # Remove o email armazenado
        # Salva as alterações nos cookies
        cookies.save()
    except Exception as e:
        st.error(f"Erro ao limpar cookies: {e}")
