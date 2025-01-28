import firebase_admin
from firebase_admin import credentials, db, auth
from datetime import datetime

def initialize_firebase(cred_dict, database_url):
    """
    Inicializa a conexão com o Firebase utilizando as credenciais fornecidas e a URL do banco de dados.

    Parâmetros:
        cred_dict (dict): Dicionário contendo as credenciais do Firebase.
        database_url (str): URL do banco de dados Firebase.

    Levanta:
        RuntimeError: Se houver um erro ao inicializar a conexão com o Firebase.
    """
    try:
        cred = credentials.Certificate(cred_dict)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred, {"databaseURL": database_url})
    except Exception as e:
        raise RuntimeError(f"Erro ao inicializar o Firebase: {e}")


def authenticate_user(email: str, password: str):
    """
    Autentica um usuário no Firebase com base no email fornecido.

    Parâmetros:
        email (str): O email do usuário.
        password (str): A senha do usuário (não utilizada diretamente aqui, mas incluída por questão de consistência).

    Retorna:
        dict: Um dicionário contendo o 'uid' e 'email' do usuário autenticado, ou None se o usuário não for encontrado.
    
    Levanta:
        RuntimeError: Se houver um erro durante o processo de autenticação.
    """
    try:
        user = auth.get_user_by_email(email)
        return {"uid": user.uid, "email": user.email}
    except auth.UserNotFoundError:
        return None
    except Exception as e:
        raise RuntimeError(f"Erro ao autenticar usuário: {e}")

def set_data(reference_path: str, data: dict):
    """
    Envia dados para o Firebase, incluindo um timestamp automático.

    Parâmetros:
        reference_path (str): O caminho de referência no banco de dados Firebase onde os dados serão armazenados.
        data (dict): Os dados a serem enviados para o Firebase.
    
    Levanta:
        RuntimeError: Se houver um erro ao enviar os dados para o Firebase.
    """
    try:
        ref = db.reference(reference_path)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_with_timestamp = {**data, "timestamp": timestamp}
        ref.push(data_with_timestamp)
    except Exception as e:
        raise RuntimeError(f"Erro ao enviar dados: {e}")

def get_data(reference_path: str):
    """
    Obtém dados do Firebase a partir de um caminho de referência específico.

    Parâmetros:
        reference_path (str): O caminho de referência no banco de dados Firebase de onde os dados serão obtidos.
    
    Retorna:
        dict: O dicionário contendo os dados obtidos do Firebase.
    
    Levanta:
        RuntimeError: Se houver um erro ao recuperar os dados.
    """
    try:
        ref = db.reference(reference_path)
        return ref.get()
    except Exception as e:
        raise RuntimeError(f"Erro ao obter dados: {e}")
