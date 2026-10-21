"""Aula 1 — Exemplo 1: a primeira conversa com um LLM usando LangChain.

Como rodar:
    uv run python aulas/aula_01_fundamentos/01_ola_llm.py

O que observar:
- `invoke` envia a pergunta e devolve uma AIMessage.
- `usage_metadata` mostra quantos tokens foram usados (e isso vira custo!).
"""

from assistente_ia.config import descrever_ambiente
from assistente_ia.container import criar_chat_model

print(descrever_ambiente(), "\n")

# Com chave: ChatOpenAI(model="gpt-5.4-mini"). Sem chave: modelo simulado.
# Equivalente "puro" em LangChain:
#   from langchain.chat_models import init_chat_model
#   modelo = init_chat_model("openai:gpt-5.4-mini", reasoning_effort="none", max_tokens=200)
modelo = criar_chat_model(max_tokens=200)

resposta = modelo.invoke("Em uma frase, o que é um pão de queijo?")

print("Resposta:", resposta.content)
print("Tokens usados:", resposta.usage_metadata)
