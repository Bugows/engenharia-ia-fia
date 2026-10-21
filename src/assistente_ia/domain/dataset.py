"""Validação de datasets no formato de conversa (JSONL) — Aula 6.

Cada linha do arquivo é um exemplo:
{"messages": [{"role": "system", ...}, {"role": "user", ...}, {"role": "assistant", ...}]}
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field

PAPEIS_VALIDOS = {"system", "user", "assistant"}
PADRAO_CPF = re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b")
PADRAO_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")


@dataclass
class RelatorioDataset:
    """Resultado da validação."""

    total: int = 0
    validos: int = 0
    erros: list[str] = field(default_factory=list)
    avisos: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.erros


def validar_exemplo(exemplo: dict, numero: int = 1) -> list[str]:
    """Lista os problemas de UM exemplo (lista vazia = exemplo válido)."""
    problemas: list[str] = []
    mensagens = exemplo.get("messages")
    if not isinstance(mensagens, list) or not mensagens:
        return [f"linha {numero}: falta a lista 'messages'"]

    papeis = []
    for i, msg in enumerate(mensagens):
        papel = msg.get("role")
        conteudo = msg.get("content")
        if papel not in PAPEIS_VALIDOS:
            problemas.append(f"linha {numero}: papel inválido na mensagem {i}: {papel!r}")
        if not isinstance(conteudo, str) or not conteudo.strip():
            problemas.append(f"linha {numero}: conteúdo vazio na mensagem {i}")
        elif PADRAO_CPF.search(conteudo) or PADRAO_EMAIL.search(conteudo):
            problemas.append(f"linha {numero}: dado pessoal (CPF/e-mail) na mensagem {i}")
        papeis.append(papel)

    if "user" not in papeis:
        problemas.append(f"linha {numero}: precisa de pelo menos uma mensagem 'user'")
    if not papeis or papeis[-1] != "assistant":
        problemas.append(f"linha {numero}: a última mensagem deve ser do 'assistant'")
    return problemas


def validar_linhas(linhas: list[str]) -> RelatorioDataset:
    """Valida um conjunto de linhas JSONL e detecta duplicatas."""
    relatorio = RelatorioDataset()
    vistos: set[str] = set()
    for numero, linha in enumerate(linhas, start=1):
        if not linha.strip():
            continue
        relatorio.total += 1
        try:
            exemplo = json.loads(linha)
        except json.JSONDecodeError as erro:
            relatorio.erros.append(f"linha {numero}: JSON inválido ({erro.msg})")
            continue
        problemas = validar_exemplo(exemplo, numero)
        assinatura = json.dumps(exemplo, sort_keys=True, ensure_ascii=False)
        if assinatura in vistos:
            problemas.append(f"linha {numero}: exemplo duplicado")
        vistos.add(assinatura)
        if problemas:
            relatorio.erros.extend(problemas)
        else:
            relatorio.validos += 1
    if 0 < relatorio.validos < 10:
        relatorio.avisos.append("Menos de 10 exemplos válidos: pouco para customizar um modelo.")
    return relatorio
