"""Aula 8 — Exemplo 4: observabilidade de custo e orçamento por sessão.

Como rodar:
    uv run python aulas/aula_08_llmops/04_custos.py

Toda chamada passa pela ObservabilidadePort, que soma tokens e custo
e INTERROMPE a sessão quando o orçamento estoura. Melhor um erro claro
do que uma fatura surpresa.
"""

from assistente_ia.adapters.observabilidade.console import LimiteDeCustoAtingido, ObservabilidadeConsole
from assistente_ia.application.chat import ServicoChat
from assistente_ia.config import descrever_ambiente
from assistente_ia.container import criar_llm
from assistente_ia.domain.custos import custo_brl, formatar_brl
from assistente_ia.domain.modelos import RespostaLLM

print(descrever_ambiente(), "\n")

observabilidade = ObservabilidadeConsole(limite_usd=0.05)
chat = ServicoChat(criar_llm(), observabilidade=observabilidade)

for pergunta in ["Bom dia! Tem pão de queijo?", "E que horas abre no domingo?", "Aceitam pix?"]:
    print(f"\nCliente: {pergunta}")
    print(f"Atendente: {chat.perguntar(pergunta)}")

resumo = observabilidade.resumo()
print(f"\nResumo da sessão: {resumo} (~{formatar_brl(custo_brl(resumo['custo_usd']))})")

print("\nSimulando um prompt gigante esquecido num loop...")
try:
    for _ in range(10):
        observabilidade.registrar_uso(RespostaLLM("...", "gpt-5.4-mini", tokens_entrada=40_000, tokens_saida=2_000), "loop")
except LimiteDeCustoAtingido as erro:
    print(f"\nPROTEÇÃO ACIONADA: {erro}")
