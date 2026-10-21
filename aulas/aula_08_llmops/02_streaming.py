"""Aula 8 — Exemplo 2: streaming (a resposta aparece enquanto é gerada).

Como rodar:
    uv run python aulas/aula_08_llmops/02_streaming.py

O tempo total não muda, mas o tempo até a PRIMEIRA palavra (TTFT) cai muito.
Para o usuário, isso é a diferença entre "travou" e "está respondendo".
"""

import time

from assistente_ia.config import descrever_ambiente
from assistente_ia.container import criar_llm
from assistente_ia.domain.modelos import sistema, usuario

print(descrever_ambiente(), "\n")
llm = criar_llm()
mensagens = [
    sistema("Você é a Vovó Lurdes, da Padaria Peter Pão. Conte histórias curtas e carinhosas."),
    usuario("Conte, em 5 frases, como surgiu o bolo de rolo da padaria."),
]

inicio = time.perf_counter()
primeira = None
for pedaco in llm.transmitir(mensagens):
    if primeira is None:
        primeira = time.perf_counter() - inicio
    print(pedaco, end="", flush=True)
    time.sleep(0.02 if "fake" in type(llm).__name__.lower() else 0)  # efeito visual no modo fake
total = time.perf_counter() - inicio
print(f"\n\nTempo até a primeira palavra: {primeira or 0:.2f}s | tempo total: {total:.2f}s")
