import streamlit as st

# Configuração inicial
st.set_page_config(
    page_title="Bikepacking Tracker",
    page_icon="🚴‍♂️",
    layout="wide"
)

st.title("Bikepacking Tracker 🚵‍♂️")
st.markdown("""
    Bem-vindo ao **Bikepacking Tracker**!  
    Aqui você pode acompanhar todos os detalhes da sua viagem.  
    Use o menu lateral para navegar pelas seções:
    - Introdução.
    - Progresso da Viagem.
    - Gastos.
    - Paradas Planejadas.
    - Mapa do Percurso.
""")
