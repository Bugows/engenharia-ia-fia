"""Objetos de domínio usados em todo o projeto.

São dataclasses simples e imutáveis (frozen): fáceis de ler, testar e comparar.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

Papel = Literal["system", "user", "assistant"]


@dataclass(frozen=True)
class Mensagem:
    """Uma mensagem de conversa. papel: system (regras), user (cliente), assistant (IA)."""

    papel: Papel
    conteudo: str


@dataclass(frozen=True)
class RespostaLLM:
    """Resposta de um modelo de linguagem, com a contabilidade de tokens."""

    texto: str
    modelo: str
    tokens_entrada: int = 0
    tokens_saida: int = 0
    tokens_raciocinio: int = 0
    tokens_cache: int = 0


@dataclass(frozen=True)
class Documento:
    """Um pedaço de texto de uma fonte (arquivo, página, base de conhecimento)."""

    id: str
    texto: str
    fonte: str
    metadados: dict = field(default_factory=dict)


@dataclass(frozen=True)
class Trecho:
    """Documento recuperado numa busca, com a pontuação de similaridade (0 a 1)."""

    documento: Documento
    pontuacao: float


def sistema(texto: str) -> Mensagem:
    """Atalho para criar uma mensagem de sistema."""
    return Mensagem("system", texto)


def usuario(texto: str) -> Mensagem:
    """Atalho para criar uma mensagem do usuário."""
    return Mensagem("user", texto)


def assistente(texto: str) -> Mensagem:
    """Atalho para criar uma mensagem do assistente."""
    return Mensagem("assistant", texto)
