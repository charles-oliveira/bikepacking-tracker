import firebase_admin
from firebase_admin import credentials, db, auth
from datetime import datetime

# Inicializar o Firebase com credenciais e URL do banco de dados
def initialize_firebase(cred_dict, database_url):
    try:
        cred = credentials.Certificate(cred_dict)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred, {"databaseURL": database_url})
    except Exception as e:
        raise RuntimeError(f"Erro ao inicializar o Firebase: {e}")

# Autenticar o usuário usando o Firebase Authentication
def authenticate_user(email: str, password: str):
    try:
        user = auth.get_user_by_email(email)
        return {"uid": user.uid, "email": user.email}
    except auth.UserNotFoundError:
        return None
    except Exception as e:
        raise RuntimeError(f"Erro ao autenticar usuário: {e}")

# Enviar dados para o Firebase com timestamp automático
def set_data(reference_path: str, data: dict):
    try:
        ref = db.reference(reference_path)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_with_timestamp = {**data, "timestamp": timestamp}
        ref.push(data_with_timestamp)
    except Exception as e:
        raise RuntimeError(f"Erro ao enviar dados: {e}")

# Obter dados do Firebase a partir de um caminho de referência
def get_data(reference_path: str):
    try:
        ref = db.reference(reference_path)
        return ref.get()
    except Exception as e:
        raise RuntimeError(f"Erro ao obter dados: {e}")
