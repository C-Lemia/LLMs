import streamlit as st
from query import consultar_modelo  #------------ Importa a função principal que busca e responde

#------------ Configurações iniciais da página do app
st.set_page_config(page_title="Buscador Inteligente", page_icon="🔍")
st.title("Explorador de Conhecimento Web")

#------------ Campo de entrada onde o usuário digita a pergunta
pergunta_usuario = st.text_input("Pergunte algo :")

#------------ Se o usuário digitar algo, processa a pergunta
if pergunta_usuario:
    with st.spinner("Buscando na web e consultando IA..."):
        try:
            resposta = consultar_modelo(pergunta_usuario)
            st.markdown(f"**Resposta:**\n\n{resposta}")  #------------ Exibe a resposta da IA
        except Exception as erro:
            st.error(f"Ocorreu um erro: {erro}")

