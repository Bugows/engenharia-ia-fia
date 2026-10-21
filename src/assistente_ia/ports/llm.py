"""Porta do modelo de linguagem."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Protocol, TypeVar, runtime_checkable

from pydantic import BaseModel

from assistente_ia.domain.modelos import Mensagem, RespostaLLM

EsquemaT = TypeVar("EsquemaT", bound=BaseModel)


@runtime_checkable
class LLMPort(Protocol):
    """Qualquer coisa capaz de conversar."""

    def responder(self, mensagens: list[Mensagem], *, esforco: str | None = None) -> RespostaLLM:
        """Recebe a conversa e devolve a resposta completa."""
        ...

    def transmitir(self, mensagens: list[Mensagem]) -> Iterator[str]:
        """Devolve a resposta aos pedaços (streaming), como digitando."""
        ...

    def responder_estruturado(self, mensagens: list[Mensagem], esquema: type[EsquemaT]) -> EsquemaT:
        """Devolve um objeto Pydantic preenchido (saída estruturada)."""
        ...
