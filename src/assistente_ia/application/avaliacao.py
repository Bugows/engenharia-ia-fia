"""Caso de uso: avaliação com golden dataset e juiz LLM (Aula 4)."""

from __future__ import annotations

import json
import time
import unicodedata
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

from pydantic import BaseModel, Field

from assistente_ia.domain.modelos import Mensagem
from assistente_ia.ports.llm import LLMPort

SINAIS_DE_RECUSA = ("nao posso", "desculpe", "nao tenho essa informacao", "nao consigo ajudar")


def _normalizar(texto: str) -> str:
    return unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()


@dataclass(frozen=True)
class CasoDeTeste:
    id: str
    pergunta: str
    palavras_chave: list[str] = field(default_factory=list)
    deve_recusar: bool = False
    fonte: str | None = None


@dataclass
class ResultadoCaso:
    caso: CasoDeTeste
    resposta: str
    acertou: bool
    segundos: float


@dataclass
class RelatorioAvaliacao:
    nome: str
    resultados: list[ResultadoCaso] = field(default_factory=list)

    @property
    def taxa_acerto(self) -> float:
        return sum(r.acertou for r in self.resultados) / len(self.resultados) if self.resultados else 0.0

    @property
    def latencia_media(self) -> float:
        return sum(r.segundos for r in self.resultados) / len(self.resultados) if self.resultados else 0.0

    def erros(self) -> list[ResultadoCaso]:
        return [r for r in self.resultados if not r.acertou]


def carregar_golden(caminho: str | Path) -> list[CasoDeTeste]:
    """Lê um arquivo JSONL com um caso de teste por linha."""
    casos = []
    for linha in Path(caminho).read_text(encoding="utf-8").splitlines():
        if linha.strip():
            dados = json.loads(linha)
            casos.append(CasoDeTeste(**dados))
    return casos


def contem_palavras_chave(resposta: str, palavras_chave: list[str]) -> bool:
    """True se TODAS as palavras-chave aparecem (ignora acentos e maiúsculas)."""
    normalizada = _normalizar(resposta)
    return all(_normalizar(p) in normalizada for p in palavras_chave)


def recusou(resposta: str) -> bool:
    normalizada = _normalizar(resposta)
    return any(sinal in normalizada for sinal in SINAIS_DE_RECUSA)


def corrigir(caso: CasoDeTeste, resposta: str) -> bool:
    """Regra de correção de um caso."""
    if caso.deve_recusar:
        return recusou(resposta)
    return contem_palavras_chave(resposta, caso.palavras_chave)


def avaliar(nome: str, responder: Callable[[str], str], casos: list[CasoDeTeste]) -> RelatorioAvaliacao:
    """Roda a função `responder` em todos os casos e corrige automaticamente."""
    relatorio = RelatorioAvaliacao(nome)
    for caso in casos:
        inicio = time.perf_counter()
        resposta = responder(caso.pergunta)
        segundos = time.perf_counter() - inicio
        relatorio.resultados.append(ResultadoCaso(caso, resposta, corrigir(caso, resposta), segundos))
    return relatorio


def relatorio_markdown(relatorios: list[RelatorioAvaliacao]) -> str:
    """Tabela comparativa em Markdown."""
    linhas = [
        "# Relatório de avaliação",
        "",
        "| Configuração | Acerto | Latência média (s) | Casos |",
        "|---|---|---|---|",
    ]
    for r in relatorios:
        linhas.append(f"| {r.nome} | {r.taxa_acerto:.0%} | {r.latencia_media:.2f} | {len(r.resultados)} |")
    for r in relatorios:
        if r.erros():
            linhas += ["", f"## Erros em: {r.nome}", ""]
            for e in r.erros():
                linhas.append(f"- **{e.caso.id}** — {e.caso.pergunta} → _{e.resposta[:150]}_")
    return "\n".join(linhas) + "\n"


class NotaJuiz(BaseModel):
    """Saída estruturada do juiz LLM."""

    nota: int = Field(ge=1, le=5, description="1 = péssima, 5 = perfeita")
    justificativa: str = Field(description="Uma frase explicando a nota")


PROMPT_JUIZ = """Você é um avaliador rigoroso de um atendente virtual de padaria.
Compare a RESPOSTA com a REFERÊNCIA e dê uma nota de 1 a 5:
5 = correta e completa; 4 = correta com detalhe faltando; 3 = parcialmente correta;
2 = maior parte errada; 1 = errada, inventada ou perigosa.
Penalize informações que não estão na referência (alucinação)."""


class JuizLLM:
    """LLM-as-a-Judge. Cuidado: juiz e avaliado do mesmo modelo geram viés."""

    def __init__(self, llm: LLMPort) -> None:
        self.llm = llm

    def avaliar(self, pergunta: str, referencia: str, resposta: str) -> NotaJuiz:
        conteudo = f"PERGUNTA: {pergunta}\nREFERÊNCIA: {referencia}\nRESPOSTA: {resposta}"
        return self.llm.responder_estruturado(
            [Mensagem("system", PROMPT_JUIZ), Mensagem("user", conteudo)], NotaJuiz
        )
