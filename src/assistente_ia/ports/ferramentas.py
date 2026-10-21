"""Porta de ferramentas (tools) que um agente pode usar.

Uma ferramenta tem nome, descrição (o modelo lê isso para decidir quando usar)
e um método `executar` com parâmetros TIPADOS — os tipos viram o "esquema"
que o modelo precisa preencher no function calling.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class FerramentaPort(Protocol):
    nome: str
    descricao: str

    def executar(self, *args: Any, **kwargs: Any) -> str:
        """Executa a ação e devolve um texto para o modelo ler."""
        ...
