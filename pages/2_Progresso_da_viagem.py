import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from firebase_admin import db
from datetime import datetime

# Função para inicializar conexão com o Firebase
def initialize_firebase():
    import firebase_admin
    from firebase_admin import credentials
    if not firebase_admin._apps:
        cred = credentials.Certificate(st.secrets["firebase"]["credentials"])
        firebase_admin.initialize_app(cred, {
            "databaseURL": "https://bikepacking-tracker-3fa9f-default-rtdb.firebaseio.com"
        })

# Função para obter dados do Firebase
def get_data(path):
    try:
        ref = db.reference(path)
        data = ref.get()
        return data
    except Exception as e:
        st.error(f"Erro ao recuperar dados do Firebase: {e}")
        return None

# Função para processar os dados em um DataFrame
def process_trip_data(data):
    if not data:
        return pd.DataFrame()

    records = []
    total_distancia = 0
    total_altimetria = 0
    total_minutes = 0

    for key, values in data.items():
        if isinstance(values, dict):
            timestamp = values.get("timestamp", "Sem Data")
            tempo = values.get("tempo", "0:00")
            distancia = values.get("distancia", 0)
            altimetria = values.get("altimetria", 0)

            try:
                # Converte o timestamp para uma data legível
                date = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")
            except ValueError:
                date = "Sem Data"

            # Converte o tempo para minutos
            try:
                h, m = map(int, tempo.split(":"))
                minutes = h * 60 + m
            except ValueError:
                minutes = 0

            # Atualiza totais
            total_distancia += distancia
            total_altimetria += altimetria
            total_minutes += minutes

            # Converte minutos acumulados para o formato HH:MM
            total_hours = total_minutes // 60
            total_remaining_minutes = total_minutes % 60
            formatted_time = f"{total_hours:02}:{total_remaining_minutes:02}"

            # Adiciona registro
            records.append({
                "Hora": formatted_time,
                "Distância (km)": total_distancia,
                "Altimetria (m)": total_altimetria,
                "Data": date
            })

    return pd.DataFrame(records)

# Função para exibir gráficos
def plot_trip_progress(df):
    if df.empty:
        st.warning("Nenhum dado disponível para exibir os gráficos.")
        return

    # Gráfico de progresso por hora
    st.markdown("### Progresso por Hora")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Hora"],
        y=df["Altimetria (m)"],
        fill='tozeroy',
        name='Altimetria (m)',
        line=dict(color='orange', width=2),
        mode='lines+markers',
        marker=dict(size=8)
    ))
    fig.add_trace(go.Scatter(
        x=df["Hora"],
        y=df["Distância (km)"],
        name='Distância (km)',
        line=dict(color='blue', width=3),
        mode='lines+markers',
        marker=dict(size=8)
    ))
    fig.update_layout(
        title="Progresso por Hora 🚴",
        xaxis_title="Hora (HH:MM)",
        yaxis_title="Valores",
        legend_title="Métricas",
        hovermode="x unified",
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Gráfico de comparação de distância e altimetria
    st.markdown("### Comparação de Altimetria e Distância")
    fig_bar = go.Figure(data=[
        go.Bar(name='Distância (km)', x=df["Hora"], y=df["Distância (km)"], marker_color='blue'),
        go.Bar(name='Altimetria (m)', x=df["Hora"], y=df["Altimetria (m)"], marker_color='orange')
    ])
    fig_bar.update_layout(
        barmode='group',
        title="Comparação de Altimetria e Distância",
        xaxis_title="Hora (HH:MM)",
        yaxis_title="Valores",
        template="plotly_white"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# Inicialização do Firebase e recuperação de dados
st.title("Progresso da Viagem 🚴")

initialize_firebase()
trip_data = get_data("progresso_viagem")

# Processar e exibir os dados
if trip_data:
    trip_df = process_trip_data(trip_data)

    # Exibir resumo
    st.markdown("## Resumo da Viagem")
    if not trip_df.empty:
        total_distancia = trip_df["Distância (km)"].iloc[-1]
        total_altimetria = trip_df["Altimetria (m)"].iloc[-1]
        total_horas = len(trip_df)
        st.metric("Distância Total (km)", f"{total_distancia:.2f}")
        st.metric("Altimetria Total (m)", f"{total_altimetria}")
        st.metric("Total de Horas", total_horas)

        # Exibir gráficos
        plot_trip_progress(trip_df)
    else:
        st.warning("Os dados recuperados não possuem informações processáveis.")
else:
    st.warning("Nenhum dado encontrado no Firebase. Verifique sua conexão.")
