import streamlit as st
import pandas as pd
from firebase.firebase_utils import get_data
from datetime import datetime
import plotly.express as px

def load_trip_data_from_firebase():
    # Obter dados do Firebase
    data = get_data('gastos')

    # Limpar os dados e remover o hash
    cleaned_data = []
    for item in data.values():
        item_cleaned = {k: v for k, v in item.items() if k != '.key'}
        cleaned_data.append(item_cleaned)

    # Converter os dados para um DataFrame do Pandas
    trip_data = pd.DataFrame(cleaned_data)

    # Renomear a coluna 'timestamp' para 'data e hora', se existir
    if 'timestamp' in trip_data.columns:
        trip_data = trip_data.rename(columns={'timestamp': 'data e hora'})

    # Garantir que a coluna 'data e hora' seja convertida para datetime
    if 'data e hora' in trip_data.columns:
        trip_data['data e hora'] = pd.to_datetime(trip_data['data e hora'], errors='coerce')
        # Formatar a data e hora para exibição amigável
        trip_data['data e hora'] = trip_data['data e hora'].dt.strftime('%d/%m/%Y %H:%M:%S')

    # Garantir que a coluna 'valor' seja numérica
    if 'valor' in trip_data.columns:
        trip_data['valor'] = pd.to_numeric(trip_data['valor'], errors='coerce')
        # Adicionar uma linha para a soma dos valores
        total_row = {
            'categoria': 'Total',
            'data': '',
            'descricao': '',
            'data e hora': '',
            'valor': trip_data['valor'].sum()
        }
        trip_data = pd.concat([trip_data, pd.DataFrame([total_row])], ignore_index=True)
        # Criar uma coluna formatada para exibição
        trip_data['valor_formatado'] = trip_data['valor'].apply(lambda x: f'R$ {x:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'))
    else:
        st.write("A coluna 'valor' não foi encontrada nos dados.")

    return trip_data

def highlight_total_row(row):
    """Estilizar a linha 'Total' com uma cor de fundo diferente."""
    if row['categoria'] == 'Total':
        return ['background-color: #ffefc1'] * len(row)
    return [''] * len(row)

# Carregar os dados
trip_data = load_trip_data_from_firebase()

# Exibir o título
st.title("Gastos da Viagem: ")

# Exibir a tabela de gastos de forma dinâmica e estilizada
if not trip_data.empty:
    # Exibir tabela com estilização
    styled_table = trip_data.drop(columns='valor').style.apply(highlight_total_row, axis=1)
    st.write(styled_table, unsafe_allow_html=True)

    # Criar gráfico de gastos ao longo do tempo (exclui a linha "Total")
    trip_data_grafico = trip_data[trip_data['categoria'] != 'Total']
    if 'data e hora' in trip_data_grafico.columns and 'valor' in trip_data_grafico.columns:
        fig = px.line(
            trip_data_grafico,
            x='data e hora',
            y='valor',
            color='categoria',
            title='Gastos ao Longo do Tempo',
            labels={'data e hora': 'Data e Hora', 'valor': 'Valor em R$'}
        )
        st.plotly_chart(fig)  # Exibe o gráfico interativo
else:
    st.write("Nenhum dado disponível.")
