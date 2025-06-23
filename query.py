import os
import requests    # Para fazer requisições HTTP à API do Together.ai
from dotenv import load_dotenv   # Para carregar variáveis de ambiente de um arquivo .env
from duckduckgo_search import DDGS  # Biblioteca para realizar buscas via DuckDuckGo

load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY") # Lê a chave da API da Together.ai do .env

#web usando DuckDuckGo
def web_search(question, max_results=5):
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(question, region="wt-wt", safesearch="off", max_results=max_results):
            results.append(f"{r['title']}: {r['body']}\nLink: {r['href']}\n")
    return "\n".join(results)

#busca e envia a pergunta para o modelo
def load_and_query(question):
    search_results = web_search(question)

    prompt = f"""
Responda **em português** com base nas informações abaixo. Seja direto e cite fontes se possível.

🔎 Resultados da busca:
{search_results}

❓ Pergunta: {question}
"""

    response = requests.post(
        "https://api.together.xyz/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
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
            "temperature": 0.7,   # Grau de criatividade da resposta
            "max_tokens": 512  # Limite de tamanho da resposta
        }
    )

    if response.status_code != 200:
        raise Exception(f"Erro {response.status_code}: {response.text}")

    return response.json()["choices"][0]["message"]["content"]      # Retorna o conteúdo da resposta do modelo

