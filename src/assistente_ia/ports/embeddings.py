"""Porta de embeddings (transformar texto em vetor de números)."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class EmbeddingsPort(Protocol):
    def vetorizar_textos(self, textos: list[str]) -> list[list[float]]:
        """Um vetor para cada texto (usado na indexação)."""
        ...

    def vetorizar_consulta(self, texto: str) -> list[float]:
        """Um vetor para a pergunta do usuário (usado na busca)."""
        ...
