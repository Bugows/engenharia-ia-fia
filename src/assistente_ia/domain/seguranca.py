"""Regras simples de segurança (primeira camada de defesa).

Heurísticas NÃO substituem defesas no prompt, guardrails e revisão humana:
são apenas a cerca da frente da casa.
"""

from __future__ import annotations

import re
import unicodedata

PADROES_INJECAO = [
    r"ignore (todas )?(as )?(suas )?(instrucoes|regras)",
    r"ignore (all )?(the )?previous instructions",
    r"esqueca (todas )?(as )?(suas )?(instrucoes|regras)",
    r"voce agora e",
    r"revele (o )?(seu )?(prompt|sistema|system prompt|instrucoes)",
    r"(mostre|repita|imprima) (o )?(seu )?(prompt|system prompt)",
    r"modo desenvolvedor",
    r"jailbreak",
]


def _normalizar(texto: str) -> str:
    """Minúsculas e sem acentos: 'Instruções' vira 'instrucoes'."""
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return sem_acento.lower()


def parece_injecao(texto: str) -> bool:
    """True se o texto tem cara de tentativa de prompt injection."""
    normalizado = _normalizar(texto)
    return any(re.search(padrao, normalizado) for padrao in PADROES_INJECAO)


def mascarar_chave(texto: str) -> str:
    """Esconde qualquer coisa que pareça uma chave de API (sk-...)."""
    return re.sub(r"sk-[A-Za-z0-9_\-]{8,}", "sk-***OCULTA***", texto)


def mascarar_cpf(texto: str) -> str:
    """Esconde CPFs no formato 123.456.789-00."""
    return re.sub(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b", "***.***.***-**", texto)


def mascarar_email(texto: str) -> str:
    """Esconde e-mails."""
    return re.sub(r"[\w.+-]+@[\w-]+\.[\w.]+", "[EMAIL OCULTO]", texto)


def mascarar_dados_pessoais(texto: str) -> str:
    """Aplica todas as máscaras de uma vez."""
    return mascarar_email(mascarar_cpf(mascarar_chave(texto)))
