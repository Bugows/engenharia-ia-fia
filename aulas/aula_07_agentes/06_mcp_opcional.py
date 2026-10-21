"""Aula 7 — Exemplo 6 (opcional): agente usando ferramentas via MCP.

Como rodar:
    uv run python aulas/aula_07_agentes/06_mcp_opcional.py

Usa a biblioteca langchain-mcp-adapters (já instalada com o projeto).
O agente não conhece o código do estoque: ele descobre as ferramentas conversando
com o servidor MCP (servidor_mcp_estoque.py), que roda como um processo separado.
"""

import asyncio
import sys
from pathlib import Path

from langchain.agents import create_agent
from langchain_core.messages import AIMessage
from langchain_mcp_adapters.client import MultiServerMCPClient

from assistente_ia.config import descrever_ambiente
from assistente_ia.container import criar_chat_model

SERVIDOR = Path(__file__).parent / "servidor_mcp_estoque.py"


async def main() -> None:
    print(descrever_ambiente(), "\n")
    cliente = MultiServerMCPClient(
        {"estoque": {"command": sys.executable, "args": [str(SERVIDOR)], "transport": "stdio"}}
    )
    ferramentas = await cliente.get_tools()
    print("Ferramentas descobertas via MCP:", [f.name for f in ferramentas])

    roteiro = [  # usado só no modo fake
        AIMessage(content="", tool_calls=[{"name": "produtos_em_falta", "args": {}, "id": "m1"}]),
        AIMessage(content="", tool_calls=[{"name": "consultar_estoque", "args": {"produto": "coxinha"}, "id": "m2"}]),
        AIMessage(content="O sonho está em falta hoje, mas temos 35 coxinhas disponíveis."),
    ]
    agente = create_agent(
        criar_chat_model(roteiro, reasoning_effort="low", max_tokens=400),
        tools=ferramentas,
        system_prompt="Você controla o estoque da Padaria Peter Pão. Use as ferramentas.",
    )
    resultado = await agente.ainvoke(
        {"messages": [{"role": "user", "content": "O que está em falta hoje? E quantas coxinhas temos?"}]}
    )
    print("Resposta:", resultado["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
