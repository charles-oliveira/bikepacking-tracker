import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from firebase_admin import db
from datetime import datetime, timedelta

# Função para obter dados do Firebase
def get_data(path):
    try:
        ref = db.reference(path)
        data = ref.get()  # Recupera os dados
        # st.write("Dados recuperados do Firebase:", data)  # Para depuração
        return data
    except Exception as e:
        st.error(f"Erro ao recuperar dados do Firebase: {e}")
        return None

# Função para processar os dados em um DataFrame
def prepare_trip_data(data):
    records = []
    total_hours = 0  # Total de horas percorridas
    total_distancia = 0  # Distância total acumulada
    total_altimetria = 0  # Altimetria total acumulada
    hour_counter = []  # Lista para registrar as horas e os respectivos valores
    distance_accumulated = 0  # Distância acumulada
    altimetria_accumulated = 0  # Altimetria acumulada
    
    for key, values in data.items():
        if isinstance(values, dict):  # Verificar se os valores são dicionários
            timestamp = values.get("timestamp")
            if timestamp:
                try:
                    # Converte o timestamp para uma data legível
                    date = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")
                except ValueError:
                    # Se o formato do timestamp for errado, use "Sem Data"
                    date = "Sem Data"
            else:
                # Se o timestamp não estiver presente, use "Sem Data"
                date = "Sem Data"
            
            # Converte o tempo para horas
            tempo = values.get("tempo", "0:00")
            try:
                h, m = map(int, tempo.split(":"))
                hours = h + m / 60
            except ValueError:
                hours = 0  # Caso o tempo não seja no formato esperado
            
            # Adiciona as horas ao total
            total_hours += hours
            total_distancia += values.get("distancia", 0)
            total_altimetria += values.get("altimetria", 0)
            
            # Atualiza a lista de horas acumuladas e os valores de distância e altimetria
            for hour in range(int(hours)):
                hour_counter.append({
                    "Hora": f"{int(total_hours)}h",
                    "Distância (km)": total_distancia,
                    "Altimetria (m)": total_altimetria
                })

    return pd.DataFrame(hour_counter)

# Título da página
st.title("Relatório de Viagem 🚴")

# Recuperar os dados do Firebase
percurso_data = get_data("percurso/custom")  # Caminho correto agora
if percurso_data:
    # Processar os dados
    trip_data = prepare_trip_data(percurso_data)

    # Exibir dados brutos e formatados
    if not trip_data.empty:
        # Painel Resumo
        st.markdown("## Resumo da Viagem")
        total_distancia = trip_data["Distância (km)"].sum()
        total_altimetria = trip_data["Altimetria (m)"].sum()
        total_horas = len(trip_data)
        st.metric("Distância Total (km)", f"{total_distancia:.2f}")
        st.metric("Altimetria Total (m)", f"{total_altimetria}")
        st.metric("Total de Horas", total_horas)

        # Gráfico de área - Progresso por hora
        st.markdown("### Progresso por Hora")
        fig = go.Figure()

        # Adicionar área de Altimetria
        fig.add_trace(go.Scatter(
            x=trip_data["Hora"],
            y=trip_data["Altimetria (m)"],
            fill='tozeroy',
            name='Altimetria (m)',
            line=dict(color='orange', width=2),
            mode='lines+markers',
            marker=dict(size=8)
        ))

        # Adicionar linha de Distância
        fig.add_trace(go.Scatter(
            x=trip_data["Hora"],
            y=trip_data["Distância (km)"],
            name='Distância (km)',
            line=dict(color='blue', width=3),
            mode='lines+markers',
            marker=dict(size=8)
        ))

        fig.update_layout(
            title="Progresso por Hora 🚴",
            xaxis_title="Hora",
            yaxis_title="Valores",
            legend_title="Métricas",
            hovermode="x unified",
            template="plotly_white"
        )

        # Renderizar o gráfico
        st.plotly_chart(fig, use_container_width=True)

        # Gráfico de barras - Comparação de Altimetria e Distância
        st.markdown("### Comparação de Altimetria e Distância")
        fig_bar = go.Figure(data=[
            go.Bar(name='Distância (km)', x=trip_data["Hora"], y=trip_data["Distância (km)"], marker_color='blue'),
            go.Bar(name='Altimetria (m)', x=trip_data["Hora"], y=trip_data["Altimetria (m)"], marker_color='orange')
        ])
        fig_bar.update_layout(
            barmode='group',
            title="Comparação de Altimetria e Distância",
            xaxis_title="Hora",
            yaxis_title="Valores",
            template="plotly_white"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.warning("Nenhum dado processado para exibir.")
else:
    st.warning("Nenhum dado recuperado do Firebase. Verifique a conexão.")
