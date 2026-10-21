"""Caso de uso: atendimento com LangGraph (Aula 7).

    START -> classificar --(duvida)----> responder_duvida -----> END
                         --(encomenda)-> registrar_encomenda --> END   (pausa para aprovação humana)
                         --(reclamacao)> tratar_reclamacao ----> END
"""

from __future__ import annotations

import unicodedata
from typing import Literal, TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt
from pydantic import BaseModel

from assistente_ia.application.rag import ServicoRAG
from assistente_ia.domain.modelos import Mensagem
from assistente_ia.ports.llm import LLMPort

Categoria = Literal["duvida", "encomenda", "reclamacao"]


class EstadoAtendimento(TypedDict, total=False):
    pergunta: str
    categoria: Categoria
    resposta: str
    fontes: list[str]


class Classificacao(BaseModel):
    categoria: Categoria


def _normalizar(texto: str) -> str:
    return unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()


def classificar_por_palavras(texto: str) -> Categoria:
    """Classificador por regras: rápido, grátis e previsível."""
    t = _normalizar(texto)
    if any(p in t for p in ("encomend", "reservar", "quero pedir", "para retirar")):
        return "encomenda"
    if any(p in t for p in ("reclam", "pessim", "horrivel", "frio", "atrasou", "veio errado", "ruim")):
        return "reclamacao"
    return "duvida"


def criar_grafo_atendimento(
    llm: LLMPort,
    rag: ServicoRAG,
    usar_llm_para_classificar: bool = False,
    checkpointer=None,
):
    """Monta e compila o grafo. O checkpointer é OBRIGATÓRIO para pausar (interrupt)."""

    def classificar(estado: EstadoAtendimento) -> EstadoAtendimento:
        if usar_llm_para_classificar:
            resultado = llm.responder_estruturado(
                [
                    Mensagem("system", "Classifique a mensagem do cliente de uma padaria em: duvida, encomenda ou reclamacao."),
                    Mensagem("user", estado["pergunta"]),
                ],
                Classificacao,
            )
            return {"categoria": resultado.categoria}
        return {"categoria": classificar_por_palavras(estado["pergunta"])}

    def responder_duvida(estado: EstadoAtendimento) -> EstadoAtendimento:
        resposta = rag.perguntar(estado["pergunta"])
        return {"resposta": resposta.resposta, "fontes": resposta.fontes}

    def registrar_encomenda(estado: EstadoAtendimento) -> EstadoAtendimento:
        # ATENÇÃO: ao retomar, o nó roda DE NOVO desde o início.
        # Por isso, nada de efeitos colaterais (gravar, cobrar) ANTES do interrupt.
        decisao = interrupt({"acao": "registrar encomenda", "pedido": estado["pergunta"]})
        if str(decisao).strip().lower() in {"aprovar", "sim", "s", "ok"}:
            return {"resposta": "Encomenda aprovada pela Dona Cida e registrada! Retirada com 24h de antecedência."}
        return {"resposta": "A encomenda não foi aprovada. Um atendente vai entrar em contato."}

    def tratar_reclamacao(estado: EstadoAtendimento) -> EstadoAtendimento:
        resposta = llm.responder(
            [
                Mensagem("system", "Você é da Padaria Peter Pão. Peça desculpas com empatia em 2 frases e diga que a gerente Dona Cida vai retornar em até 1 hora."),
                Mensagem("user", estado["pergunta"]),
            ]
        )
        return {"resposta": resposta.texto}

    grafo = StateGraph(EstadoAtendimento)
    grafo.add_node("classificar", classificar)
    grafo.add_node("responder_duvida", responder_duvida)
    grafo.add_node("registrar_encomenda", registrar_encomenda)
    grafo.add_node("tratar_reclamacao", tratar_reclamacao)

    grafo.add_edge(START, "classificar")
    grafo.add_conditional_edges(
        "classificar",
        lambda estado: estado["categoria"],
        {
            "duvida": "responder_duvida",
            "encomenda": "registrar_encomenda",
            "reclamacao": "tratar_reclamacao",
        },
    )
    for no in ("responder_duvida", "registrar_encomenda", "tratar_reclamacao"):
        grafo.add_edge(no, END)

    return grafo.compile(checkpointer=checkpointer or InMemorySaver())
