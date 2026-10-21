"""Porta de agente: qualquer coisa que conversa e usa ferramentas por conta própria."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class AgentePort(Protocol):
    def conversar(self, mensagem: str, sessao: str = "padrao") -> str:
        """Envia uma mensagem na sessão indicada e devolve a resposta final."""
        ...
