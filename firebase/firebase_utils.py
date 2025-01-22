import firebase_admin
from firebase_admin import credentials, db, auth
from datetime import datetime

def initialize_firebase(cred_dict, database_url):
    try:
        # Criar credenciais a partir do dicionário
        cred = credentials.Certificate(cred_dict)

        # Inicializar o app Firebase
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred, {
                "databaseURL": database_url
            })
        print("Firebase inicializado com sucesso!")
    except Exception as e:
        print(f"Erro ao inicializar o Firebase: {e}")
        raise

# Função para autenticar o usuário usando o Firebase Authentication
def authenticate_user(email: str, password: str):
    try:
        user = auth.get_user_by_email(email)
        # Note que autenticação de senha normalmente acontece no front-end. 
        # Aqui, apenas verificamos se o usuário existe. Para uma autenticação mais robusta:
        # - Integre com Firebase Client SDK no frontend para autenticar com senha.
        # - Valide o token no back-end (opcional).
        print(f"Usuário {user.email} autenticado com sucesso!")
        return {"uid": user.uid, "email": user.email}
    except auth.UserNotFoundError:
        print(f"Usuário não encontrado para o email: {email}")
        return None
    except Exception as e:
        print(f"Erro ao autenticar usuário: {e}")
        return None

# Função para enviar dados para o Firebase (adicionando com 'push' e timestamp)
def set_data(reference_path: str, data: dict):
    ref = db.reference(reference_path)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Adiciona um timestamp
    data_with_timestamp = {**data, "timestamp": timestamp}  # Adiciona o timestamp aos dados
    ref.push(data_with_timestamp)  # Usando 'push' para adicionar sem sobrescrever
    print(f"Dados enviados para {reference_path}")

# Função para atualizar dados no Firebase
def update_data(reference_path: str, data: dict):
    ref = db.reference(reference_path)
    ref.update(data)
    print(f"Dados atualizados em {reference_path}")

# Função para obter dados do Firebase
def get_data(reference_path: str):
    ref = db.reference(reference_path)
    data = ref.get()
    print(f"Dados recuperados de {reference_path}")
    return data
