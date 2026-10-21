"""Converte ferramentas do nosso domínio (FerramentaPort) em tools do LangChain.

O LangChain lê a assinatura de `executar` (nomes e tipos dos parâmetros)
para montar o esquema JSON que o modelo preenche no function calling.
"""

from __future__ import annotations

from langchain_core.tools import BaseTool, StructuredTool

from assistente_ia.ports.ferramentas import FerramentaPort


def para_langchain(ferramenta: FerramentaPort) -> BaseTool:
    """Uma FerramentaPort -> um StructuredTool."""
    return StructuredTool.from_function(
        func=ferramenta.executar,
        name=ferramenta.nome,
        description=ferramenta.descricao,
    )


def para_langchain_lista(ferramentas: list[FerramentaPort]) -> list[BaseTool]:
    """Várias de uma vez."""
    return [para_langchain(f) for f in ferramentas]
