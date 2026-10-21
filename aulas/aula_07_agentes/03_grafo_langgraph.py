"""Aula 7 — Exemplo 3: um fluxo de atendimento com LangGraph (com aprovação humana).

Como rodar:
    uv run python aulas/aula_07_agentes/03_grafo_langgraph.py           # pergunta no terminal
    uv run python aulas/aula_07_agentes/03_grafo_langgraph.py --auto    # aprova sozinho

Workflow x Agente:
- No AGENTE (exemplo 2), o modelo decide os passos.
- No WORKFLOW com LangGraph, VOCÊ desenha os passos; o modelo atua dentro de cada um.
  É mais previsível, mais barato e mais fácil de auditar. Comece por aqui!
"""

import sys

from langgraph.types import Command

from assistente_ia.application.grafo_atendimento import criar_grafo_atendimento
from assistente_ia.config import descrever_ambiente
from assistente_ia.container import criar_llm, criar_servico_rag, modo_fake

print(descrever_ambiente(), "\n")
llm = criar_llm()
grafo = criar_grafo_atendimento(llm, criar_servico_rag("padaria", llm=llm), usar_llm_para_classificar=not modo_fake())

print("Desenho do grafo (cole em https://mermaid.live):")
print(grafo.get_graph().draw_mermaid())

mensagens = [
    "Vocês aceitam pix?",
    "O café veio frio e o atendente foi grosso!",
    "Quero encomendar 50 coxinhas para sábado",
]
for i, texto in enumerate(mensagens, start=1):
    config = {"configurable": {"thread_id": f"cliente-{i}"}}
    print(f"\nCliente: {texto}")
    resultado = grafo.invoke({"pergunta": texto}, config)
    print(f"  categoria: {resultado.get('categoria')}")

    if "__interrupt__" in resultado:  # o grafo PAUSOU esperando um humano
        pedido = resultado["__interrupt__"][0].value
        print(f"  PAUSA para aprovação: {pedido}")
        decisao = "aprovar" if "--auto" in sys.argv else input("  Dona Cida, digite aprovar ou recusar: ")
        resultado = grafo.invoke(Command(resume=decisao), config)  # retoma do ponto exato

    print(f"  resposta: {resultado['resposta']}")
