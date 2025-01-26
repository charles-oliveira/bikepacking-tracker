import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from firebase.firebase_utils import initialize_firebase, set_data, get_data, authenticate_user
import json
import geocoder

# Função para carregar credenciais do Firebase
def load_firebase_credentials():
    try:
        cred_string = st.secrets["firebase"]["credentials"]
        cred_dict = json.loads(cred_string)
        st.success("Credenciais carregadas com sucesso!")
        return cred_dict
    except Exception as e:
        st.error(f"Erro ao carregar credenciais: {e}")
        return None

# Função para inicializar o Firebase
def initialize_firebase_connection(cred_dict):
    try:
        DATABASE_URL = "https://bikepacking-tracker-3fa9f-default-rtdb.firebaseio.com"
        initialize_firebase(cred_dict, DATABASE_URL)
        st.success("Firebase inicializado com sucesso!")
    except Exception as e:
        st.error(f"Erro ao inicializar o Firebase: {e}")

# Função para exibir a tela de login
def display_login():
    st.title("Login para acesso")
    email = st.text_input("Email", placeholder="Digite seu email")
    password = st.text_input("Senha", placeholder="Digite sua senha", type="password")

    if st.button("Entrar"):
        try:
            user = authenticate_user(email, password)
            if user:
                st.session_state.authenticated = True
                st.success(f"Bem-vindo(a), {user['email']}!")
            else:
                st.error("Credenciais inválidas. Tente novamente.")
        except Exception as e:
            st.error(f"Erro ao autenticar: {e}")

# Função para exibir a página de progresso da viagem
def show_trip_progress():
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

# Função para exibir o mapa do percurso
def show_route_map():
    st.header("Mapa do Percurso 📍")

    try:
        data = get_data("locations")
        if data:
            locations = []
            for loc in data.values():
                cidade = loc.get("cidade", "Desconhecida")
                latitude = loc.get("latitude")
                longitude = loc.get("longitude")
                if latitude and longitude:
                    locations.append({"cidade": cidade, "latitude": latitude, "longitude": longitude})

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

            st.subheader("Linha do Tempo 🔍")
            for loc in locations:
                st.write(f"- {loc['cidade']} ({loc['latitude']}, {loc['longitude']})")

    except Exception as e:
        st.error(f"Erro ao recuperar os dados: {e}")

    # Captura e envio da localização (latitude, longitude e cidade)
    capture_and_send_location()

    # Captura de localização atual por IP
    capture_location_by_ip()

    # Pesquisa de coordenadas pelo nome da cidade
    capture_location_by_city()

# Função para capturar e enviar uma nova localização
def capture_and_send_location():
    with st.form("form_nova_localizacao"):
        latitude = st.number_input("Latitude", format="%.6f", value=0.0)
        longitude = st.number_input("Longitude", format="%.6f", value=0.0)
        cidade = st.text_input("Cidade", value="")

        submit_location = st.form_submit_button("Enviar Localização")
        if submit_location:
            if not latitude or not longitude or not cidade:
                st.error("Por favor, preencha todos os campos.")
            else:
                new_location = {
                    "latitude": latitude,
                    "longitude": longitude,
                    "cidade": cidade,
                }
                try:
                    set_data("locations", new_location)
                    st.success("Nova localização enviada para o Firebase!")
                except Exception as e:
                    st.error(f"Erro ao enviar os dados: {e}")

# Função para capturar localização atual por IP
def capture_location_by_ip():
    if st.button("Capturar Localização Atual (por IP)"):
        g = geocoder.ip('me')
        if g.latlng:
            latitude, longitude = g.latlng
            st.session_state["latitude"] = latitude
            st.session_state["longitude"] = longitude
            st.success(f"Localização capturada: ({latitude}, {longitude})")
        else:
            st.error("Não foi possível capturar a localização atual.")

# Função para capturar coordenadas de uma cidade
def capture_location_by_city():
    cidade = st.text_input("Digite sua cidade para obter coordenadas:")
    if cidade:
        g_city = geocoder.osm(cidade)
        if g_city.latlng:
            latitude, longitude = g_city.latlng
            st.session_state["latitude"] = latitude
            st.session_state["longitude"] = longitude
            st.success(f"Localização capturada pela cidade: ({latitude}, {longitude})")
        else:
            st.error("Não foi possível capturar a localização dessa cidade.")

# Carregar credenciais e inicializar Firebase
cred_dict = load_firebase_credentials()
if cred_dict:
    initialize_firebase_connection(cred_dict)

    # Tela de login ou conteúdo após login
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        display_login()
    else:
        st.title("Bikepacking Tracker 📍")
        page = st.sidebar.radio("Selecione a página", ["Progresso da Viagem", "Mapa do Percurso"])

        # Página de Progresso da Viagem
        if page == "Progresso da Viagem":
            show_trip_progress()

        # Página de Mapa do Percurso
        elif page == "Mapa do Percurso":
            show_route_map()
