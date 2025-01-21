import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

# Inicializar Firebase (uma única vez)
def initialize_firebase(cred_path: str, database_url: str):
    if not firebase_admin._apps:  # Evitar inicialização múltipla
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred, {"databaseURL": database_url})
    print("Firebase inicializado com sucesso!")

# Enviar dados para o Firebase (adicionando com 'push' e timestamp)
def set_data(reference_path: str, data: dict):
    ref = db.reference(reference_path)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Adiciona um timestamp
    data_with_timestamp = {**data, "timestamp": timestamp}  # Adiciona o timestamp aos dados
    ref.push(data_with_timestamp)  # Usando 'push' para adicionar sem sobrescrever
    print(f"Dados enviados para {reference_path}")

# Atualizar dados no Firebase (esta função pode ser mantida, se necessário)
def update_data(reference_path: str, data: dict):
    ref = db.reference(reference_path)
    ref.update(data)
    print(f"Dados atualizados em {reference_path}")

# Obter dados do Firebase
def get_data(reference_path: str):
    ref = db.reference(reference_path)
    data = ref.get()
    print(f"Dados recuperados de {reference_path}")
    return data