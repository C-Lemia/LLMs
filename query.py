import os
import requests                #------------ Usado para fazer requisição HTTP à API do Together.ai
from dotenv import load_dotenv #------------ Carrega variáveis de ambiente do arquivo .env
from duckduckgo_search import DDGS  #------------ Biblioteca para buscas via DuckDuckGo

#------------ Carrega a chave da API da Together.ai
load_dotenv()
CHAVE_API_TOGETHER = os.getenv("TOGETHER_API_KEY")

#------------ Faz uma busca na web usando DuckDuckGo
def buscar_na_web(pergunta, max_resultados=5):
    resultados = []
    with DDGS() as buscador:
        for resultado in buscador.text(pergunta, region="wt-wt", safesearch="off", max_results=max_resultados):
            resultados.append(f"{resultado['title']}: {resultado['body']}\nLink: {resultado['href']}\n")
    return "\n".join(resultados)

#------------ Realiza a busca e envia a pergunta para o modelo de IA
def consultar_modelo(pergunta):
    resultados_busca = buscar_na_web(pergunta)

    prompt = f"""
Responda **em português** com base nas informações abaixo. Seja direto e cite fontes se possível.

🔎 Resultados da busca:
{resultados_busca}

❓ Pergunta: {pergunta}
"""

    resposta = requests.post(
        "https://api.together.xyz/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {CHAVE_API_TOGETHER}",
            "Content-Type": "application/json"
        },
        json={
            "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",  #------------ Modelo utilizado
            "messages": [
                {
                    "role": "system",
                    "content": "Você é um assistente inteligente que responde sempre em português. Seja direto e cite fontes se possível."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,     #------------ Grau de criatividade da resposta
            "max_tokens": 512       #------------ Tamanho máximo da resposta gerada
        }
    )

    if resposta.status_code != 200:
        raise Exception(f"Erro {resposta.status_code}: {resposta.text}")

    #------------ Extrai apenas o conteúdo útil da resposta
    return resposta.json()["choices"][0]["message"]["content"]
