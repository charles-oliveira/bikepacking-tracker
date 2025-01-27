from datetime import datetime
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from firebase.firebase_utils import initialize_firebase, set_data, get_data, authenticate_user
import json
import geocoder
from streamlit_cookies_manager import EncryptedCookieManager

# Inicializando o gerenciador de cookies
cookies = EncryptedCookieManager(prefix="bikepacking_tracker", password="password")
if not cookies.ready():
    st.stop()

def load_firebase_credentials():
    """
    Carrega as credenciais do Firebase a partir dos segredos do Streamlit.

    Retorna:
        dict: Um dicionário contendo as credenciais do Firebase.
    """
    try:
        cred_string = st.secrets["firebase"]["credentials"]
        cred_dict = json.loads(cred_string)
        st.success("Credenciais carregadas com sucesso!")
        return cred_dict
    except Exception as e:
        st.error(f"Erro ao carregar credenciais: {e}")
        return None

def initialize_firebase_connection(cred_dict):
    """
    Inicializa a conexão com o Firebase usando as credenciais fornecidas.

    Parâmetros:
        cred_dict (dict): Dicionário contendo as credenciais do Firebase.

    Levanta:
        RuntimeError: Se houver um erro ao inicializar o Firebase.
    """
    try:
        DATABASE_URL = "https://bikepacking-tracker-3fa9f-default-rtdb.firebaseio.com"
        initialize_firebase(cred_dict, DATABASE_URL)
        st.success("Firebase inicializado com sucesso!")
    except Exception as e:
        st.error(f"Erro ao inicializar o Firebase: {e}")

def display_login():
    """
    Exibe a tela de login para autenticação do usuário.
    Permite que o usuário insira o email e a senha para acessar a aplicação.
    """
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
                st.error("Credenciais inválidas. Tente novamente.")
        except Exception as e:
            st.error(f"Erro ao autenticar: {e}")

def logout():
    """
    Realiza o logout do usuário, removendo a autenticação e limpando os cookies.
    """
    st.session_state.authenticated = False
    cookies.delete("authenticated")
    cookies.delete("user_email")
    st.success("Você saiu com sucesso!")

def show_trip_progress():
    """
    Exibe o formulário para registrar o progresso da viagem, incluindo distância, altimetria e tempo estimado.
    Envia os dados para o Firebase após o envio do formulário.
    """
    st.header("Progresso da Viagem")
    with st.form("form_progresso"):
        distancia = st.number_input("Distância (km)", min_value=0.0, step=0.1, format="%.2f")
        altimetria = st.number_input("Altimetria (m)", min_value=0, step=1)
        tempo = st.text_input("Tempo estimado (hh:mm)")

        submit_button = st.form_submit_button("Enviar")
        if submit_button:
            if not tempo:
                st.error("Por favor, preencha o campo de tempo.")
            else:
                data = {
                    "distancia": distancia,
                    "altimetria": altimetria,
                    "tempo": tempo,
                }
                try:
                    set_data("progresso_viagem", data)
                    st.success("Dados enviados para o Firebase!")
                except Exception as e:
                    st.error(f"Erro ao enviar os dados: {e}")

@st.cache_data
def get_route_data():
    """
    Obtém os dados das localizações do Firebase, armazenando-os em cache para evitar chamadas repetidas.

    Retorna:
        list: Uma lista de dicionários contendo as informações de localização.
    """
    data = get_data("locations")
    if data:
        locations = []
        for loc in data.values():
            cidade = loc.get("cidade", "Desconhecida")
            latitude = loc.get("latitude")
            longitude = loc.get("longitude")
            if latitude and longitude:
                locations.append({"cidade": cidade, "latitude": latitude, "longitude": longitude})
        return locations
    return []

def add_location():
    """
    Exibe um formulário para adicionar uma nova localização e envia para o Firebase.
    """
    st.header("Adicionar Localização")

    with st.form("form_adicionar_localizacao"):
        cidade = st.text_input("Cidade")
        latitude = st.number_input("Latitude", min_value=-90.0, max_value=90.0, format="%.6f")
        longitude = st.number_input("Longitude", min_value=-180.0, max_value=180.0, format="%.6f")
        submit_button = st.form_submit_button("Adicionar Localização")

        if submit_button:
            if cidade and latitude and longitude:
                location_data = {
                    "cidade": cidade,
                    "latitude": latitude,
                    "longitude": longitude
                }
                try:
                    set_data(f"locations/{cidade}", location_data)  # Salvando no Firebase com a chave baseada na cidade
                    st.success(f"Localização {cidade} adicionada com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao adicionar a localização: {e}")
            else:
                st.error("Por favor, preencha todos os campos.")

def show_route_map():
    """
    Exibe o mapa do percurso, utilizando os dados de localização obtidos do Firebase.
    Utiliza a biblioteca Folium para gerar o mapa e visualizá-lo na aplicação.
    """
    st.header("Mapa do Percurso")

    try:
        locations = get_route_data()

        if locations:
            map_data = pd.DataFrame(locations)

            if not map_data.empty:
                m = folium.Map(location=[map_data["latitude"].mean(), map_data["longitude"].mean()], zoom_start=10)
                locations_coords = []
                for _, row in map_data.iterrows():
                    folium.Marker(
                        location=[row["latitude"], row["longitude"]],
                        popup=f"{row['cidade']}<br>({row['latitude']:.4f}, {row['longitude']:.4f})",
                        icon=folium.Icon(color="green", icon="bicycle", prefix="fa"),
                    ).add_to(m)
                    locations_coords.append([row["latitude"], row["longitude"]])

                if len(locations_coords) > 1:
                    folium.PolyLine(locations_coords, color="green", weight=2.5, opacity=1).add_to(m)

                folium_static(m)
            else:
                st.info("Nenhuma localização válida encontrada para exibir no mapa.")

            st.subheader("Linha do Tempo")
            for loc in locations:
                st.write(f"- {loc['cidade']} ({loc['latitude']}, {loc['longitude']})")

    except Exception as e:
        st.error(f"Erro ao recuperar os dados: {e}")


def show_expenses():
    """
    Exibe o formulário para registrar os gastos, incluindo descrição e valor.
    Envia os dados para o Firebase após o envio do formulário.
    """
    st.header("Registrar Gastos")

    # Formulário para adicionar um novo gasto
    with st.form("form_gastos"):
        descricao = st.text_input("Descrição do Gasto")
        categoria = st.selectbox("Categoria", ["Alimentação", "Hospedagem", "Transporte", "Outros"])
        valor = st.number_input("Valor (R$)", min_value=0.0, step=0.1, format="%.2f")
        data = st.date_input("Data do Gasto", value=datetime.today())  # Seleção manual da data
        submit_button = st.form_submit_button("Adicionar Gasto")

        if submit_button:
            if not descricao or valor <= 0:
                st.error("Por favor, preencha a descrição e o valor do gasto.")
            else:
                gasto_data = {
                    "descricao": descricao,
                    "categoria": categoria,
                    "valor": valor,
                    "data": data.strftime("%Y-%m-%d")  # Formata a data escolhida
                }
                try:
                    set_data("gastos", gasto_data)  # Envia os dados para o Firebase
                    st.success("Gasto registrado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao registrar o gasto: {e}")

# Função principal
def main():
    """
    Função principal que gerencia a navegação do aplicativo Streamlit.
    """
    if "authenticated" not in st.session_state:
        # Se não houver estado de autenticação, verifica se o cookie está presente
        if cookies.get("authenticated") == "true":
            st.session_state.authenticated = True
            st.session_state.user_email = cookies.get("user_email")
    else:
        # Se já estiver autenticado, não precisa fazer mais nada
        pass

    if st.session_state.authenticated:
        st.sidebar.title(f"Bem-vindo, {st.session_state.user_email}")
        menu = st.sidebar.selectbox("Menu", ["Progresso da Viagem", "Adicionar Localização e Mapa", "Registrar Gastos"])
        st.sidebar.button("Logout", on_click=logout)

        if menu == "Progresso da Viagem":
            show_trip_progress()
        elif menu == "Adicionar Localização e Mapa":
            add_location()
            show_route_map()
        elif menu == "Registrar Gastos":
            show_expenses()

    else:
        display_login()


if __name__ == "__main__":
    main()
