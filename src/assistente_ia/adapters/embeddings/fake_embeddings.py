"""Embeddings SIMULADOS: "saco de palavras" com hash. Grátis e determinístico.

Como funciona:
1. remove acentos e palavras muito comuns ("de", "que", "o"...);
2. corta cada palavra nas 5 primeiras letras (radical caseiro: "aceitamos" -> "aceit");
3. cada radical cai numa posição do vetor (via hash) e soma 1.

Limitação proposital (ótima para a Aula 3): ele só reconhece palavras PARECIDAS NA ESCRITA.
"aipim" e "mandioca" ficam distantes aqui, mas próximos no embedding real.
"""

from __future__ import annotations

import hashlib
import math
import re
import unicodedata

from langchain_core.embeddings import Embeddings

PALAVRAS_COMUNS = {
    "a", "o", "as", "os", "de", "da", "do", "das", "dos", "e", "em", "no", "na", "nos", "nas",
    "um", "uma", "que", "qual", "quais", "com", "para", "por", "se", "ao", "voces", "voce",
    "eu", "me", "meu", "minha", "tem", "ter", "sao", "ou", "mais", "como", "quanto",
}


def _palavras(texto: str) -> list[str]:
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    palavras = re.findall(r"[a-z0-9]+", sem_acento.lower())
    return [p[:5] for p in palavras if p not in PALAVRAS_COMUNS]


class FakeEmbeddings(Embeddings):
    """Implementa a EmbeddingsPort e também a interface Embeddings do LangChain."""

    def __init__(self, dimensoes: int = 512) -> None:
        self.dimensoes = dimensoes

    def _vetor(self, texto: str) -> list[float]:
        vetor = [0.0] * self.dimensoes
        for palavra in _palavras(texto):
            indice = int(hashlib.md5(palavra.encode()).hexdigest(), 16) % self.dimensoes
            vetor[indice] += 1.0
        norma = math.sqrt(sum(x * x for x in vetor)) or 1.0
        return [x / norma for x in vetor]

    # EmbeddingsPort
    def vetorizar_textos(self, textos: list[str]) -> list[list[float]]:
        return [self._vetor(t) for t in textos]

    def vetorizar_consulta(self, texto: str) -> list[float]:
        return self._vetor(texto)

    # Interface LangChain (permite usar com InMemoryVectorStore na Aula 5)
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self.vetorizar_textos(texts)

    def embed_query(self, text: str) -> list[float]:
        return self.vetorizar_consulta(text)

    @property
    def langchain(self) -> FakeEmbeddings:
        """Mesmo objeto: já é compatível com o LangChain."""
        return self
