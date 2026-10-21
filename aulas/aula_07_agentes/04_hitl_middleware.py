"""Aula 7 — Exemplo 4: aprovação humana no agente via middleware.

Como rodar:
    uv run python aulas/aula_07_agentes/04_hitl_middleware.py           # pergunta no terminal
    uv run python aulas/aula_07_agentes/04_hitl_middleware.py --auto    # aprova sozinho

O HumanInTheLoopMiddleware pausa o agente ANTES de executar ferramentas sensíveis.
Exige um checkpointer (memória de estado) para conseguir retomar depois.
Nosso AgenteLangChain (src/assistente_ia/application/agente.py) já vem com:
  - limite de chamadas ao modelo; - máscara de e-mail e CPF; - aprovação humana.
"""

import sys

from langchain_core.messages import AIMessage

from assistente_ia.config import descrever_ambiente
from assistente_ia.container import criar_agente_garcom

print(descrever_ambiente(), "\n")

roteiro = [  # usado só no modo fake
    AIMessage(content="", tool_calls=[{
        "name": "registrar_encomenda",
        "args": {"produto": "coxinha", "quantidade": 50, "data_retirada": "20/12"},
        "id": "e1",
    }]),
    AIMessage(content="Prontinho! Sua encomenda de 50 coxinhas para 20/12 está registrada."),
]
agente = criar_agente_garcom(roteiro)

pedido = "Quero encomendar 50 coxinhas para retirar dia 20/12. Meu e-mail é joana@exemplo.com"
print(f"Cliente: {pedido}")
resposta = agente.conversar(pedido, sessao="joana")
print(f"Agente:  {resposta}")

if resposta.startswith("[aguardando aprovação humana]"):
    escolha = "s" if "--auto" in sys.argv else input("Dona Cida, aprova? (s/n): ").strip().lower()
    resposta = agente.decidir("joana", aprovar=escolha == "s", motivo="Sem estoque de frango para 50 unidades.")
    print(f"Agente:  {resposta}")

print("\nO que o modelo recebeu (repare no e-mail mascarado):")
print(" ", agente.historico("joana")[0].content)
