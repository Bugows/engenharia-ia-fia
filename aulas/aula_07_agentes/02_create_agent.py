"""Aula 7 — Exemplo 2: o garçom virtual com `create_agent` (LangChain 1.x).

Como rodar:
    uv run python aulas/aula_07_agentes/02_create_agent.py

`create_agent` faz o loop do exemplo 1 por você: pergunta -> tool_calls -> executa -> repete.
"""

from langchain.agents import create_agent
from langchain_core.messages import AIMessage

from assistente_ia.adapters.ferramentas.langchain_tools import para_langchain_lista
from assistente_ia.application.agente import PROMPT_GARCOM
from assistente_ia.application.ferramentas import ferramentas_padaria
from assistente_ia.config import descrever_ambiente
from assistente_ia.container import criar_chat_model

print(descrever_ambiente(), "\n")

roteiro = [  # usado só no modo fake
    AIMessage(content="", tool_calls=[
        {"name": "calcular_total", "args": {"itens": {"café": 2, "pão de queijo": 3, "sonho": 1}}, "id": "c1"},
    ]),
    AIMessage(content="", tool_calls=[{"name": "rachar_conta", "args": {"total": 27.5, "pessoas": 3}, "id": "c2"}]),
    AIMessage(content="O total deu R$ 27,50 e cada um paga R$ 9,17. Bom apetite!"),
]

agente = create_agent(
    model=criar_chat_model(roteiro, reasoning_effort="low", max_tokens=600),
    tools=para_langchain_lista(ferramentas_padaria()),
    system_prompt=PROMPT_GARCOM,
)

resultado = agente.invoke(
    {"messages": [{"role": "user", "content": "Somos 3: pedimos 2 cafés, 3 pães de queijo e 1 sonho. Quanto cada um paga?"}]}
)

print("Passo a passo do agente:")
for mensagem in resultado["messages"]:
    if mensagem.type == "ai" and mensagem.tool_calls:
        for chamada in mensagem.tool_calls:
            print(f"  [modelo pede] {chamada['name']}({chamada['args']})")
    elif mensagem.type == "tool":
        print(f"  [ferramenta]  {mensagem.content}")
print(f"\nResposta final: {resultado['messages'][-1].content}")
