"""Aula 3 — Exemplo 4: temperatura e criatividade.

Como rodar (usa a API: centavos):
    uv run python aulas/aula_03_modelos/04_temperatura.py

Regra do GPT-5.x: temperature só vale com reasoning_effort="none".
Com outro esforço, o LangChain REMOVE a temperatura em silêncio — e o nosso
container avisa com um erro, para você não ser enganado.
"""

from assistente_ia.config import descrever_ambiente
from assistente_ia.container import criar_chat_model, modo_fake

print(descrever_ambiente(), "\n")
if modo_fake():
    print("Este exemplo precisa do modelo real. Configure a chave e rode de novo.")
    raise SystemExit(0)

pedido = "Invente um nome criativo para um pão doce nordestino recheado com goiabada. Só o nome."

for temperatura in [0.0, 0.7, 1.4]:
    modelo = criar_chat_model(reasoning_effort="none", temperature=temperatura, max_tokens=30)
    nomes = [str(modelo.invoke(pedido).content).strip() for _ in range(3)]
    print(f"temperature={temperatura}: {nomes}")

print("\nObserve: com 0.0 os nomes se repetem; com 1.4 variam (e às vezes viajam).")

try:
    criar_chat_model(reasoning_effort="low", temperature=0.2)
except ValueError as erro:
    print(f"\nTentativa inválida bloqueada: {erro}")
