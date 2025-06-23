import streamlit as st
from query import load_and_query  # Importa a função load_and_query definida no arquivo query.py


st.set_page_config(page_title="Buscador Inteligente", page_icon="🔍")  # Configurações da página do Streamlit (título da aba e ícone)

st.title("🔍 Explorador de Conhecimento Web")

question = st.text_input("Pergunte algo :") # Campo de entrada de texto onde o usuário digita a pergunta

if question:
    with st.spinner("Buscando na web..."):
        try:
            response = load_and_query(question)
            st.markdown(f"**Resposta:**\n\n{response}") # Exibe a resposta formatada em negrito
        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")
