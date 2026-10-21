"""Porta do banco vetorial (onde guardamos e buscamos os pedaços de texto)."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from assistente_ia.domain.modelos import Documento, Trecho


@runtime_checkable
class VectorStorePort(Protocol):
    def adicionar(self, documentos: list[Documento]) -> None:
        """Indexa documentos."""
        ...

    def buscar(self, consulta: str, k: int = 3) -> list[Trecho]:
        """Devolve os k trechos mais parecidos com a consulta."""
        ...
