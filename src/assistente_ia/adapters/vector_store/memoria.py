"""Banco vetorial em memória, em Python puro.

Não é para produção! Serve para o aluno VER como a busca por similaridade funciona.
Em produção, troque por pgvector, Qdrant, Chroma... implementando a mesma porta.
"""

from __future__ import annotations

import math

from assistente_ia.domain.modelos import Documento, Trecho
from assistente_ia.ports.embeddings import EmbeddingsPort


def cosseno(a: list[float], b: list[float]) -> float:
    """Similaridade de cosseno: 1 = mesma direção, 0 = nada a ver."""
    norma_a = math.sqrt(sum(x * x for x in a))
    norma_b = math.sqrt(sum(y * y for y in b))
    if norma_a == 0 or norma_b == 0:
        return 0.0
    return sum(x * y for x, y in zip(a, b, strict=False)) / (norma_a * norma_b)


class VectorStoreMemoria:
    """Implementa a VectorStorePort guardando (documento, vetor) numa lista."""

    def __init__(self, embeddings: EmbeddingsPort) -> None:
        self._embeddings = embeddings
        self._itens: list[tuple[Documento, list[float]]] = []

    def __len__(self) -> int:
        return len(self._itens)

    def adicionar(self, documentos: list[Documento]) -> None:
        if not documentos:
            return
        vetores = self._embeddings.vetorizar_textos([d.texto for d in documentos])
        self._itens.extend(zip(documentos, vetores, strict=True))

    def buscar(self, consulta: str, k: int = 3) -> list[Trecho]:
        if not self._itens:
            return []
        vetor_consulta = self._embeddings.vetorizar_consulta(consulta)
        trechos = [Trecho(doc, cosseno(vetor_consulta, vetor)) for doc, vetor in self._itens]
        trechos.sort(key=lambda t: t.pontuacao, reverse=True)
        return trechos[:k]
