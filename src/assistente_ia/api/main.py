"""API HTTP do assistente (Aula 8 e projeto final).

Rodar:  uv run uvicorn assistente_ia.api.main:app --reload
Docs:   http://localhost:8000/docs
"""

from __future__ import annotations

from functools import lru_cache

from fastapi import FastAPI
from pydantic import BaseModel, Field

from assistente_ia import __version__
from assistente_ia.config import descrever_ambiente
from assistente_ia.container import (
    criar_agente_garcom,
    criar_observabilidade,
    criar_servico_rag,
    modo_fake,
)

app = FastAPI(
    title="Assistente Pão Nosso",
    description="API do curso Engenharia de IA (FIA): RAG, agente e custos.",
    version=__version__,
)


@lru_cache
def observabilidade():
    return criar_observabilidade(silencioso=True)


@lru_cache
def servico_rag():
    return criar_servico_rag("padaria", observabilidade=observabilidade())


@lru_cache
def agente():
    return criar_agente_garcom()


class Pergunta(BaseModel):
    texto: str = Field(min_length=1, max_length=2000, examples=["Que horas a padaria abre no sábado?"])


class MensagemAgente(BaseModel):
    texto: str = Field(min_length=1, max_length=2000)
    sessao: str = Field(default="padrao", max_length=100)


class Decisao(BaseModel):
    sessao: str = "padrao"
    aprovar: bool
    motivo: str = ""


@app.get("/saude")
def saude() -> dict:
    return {"status": "ok", "modo": "fake" if modo_fake() else "openai", "ambiente": descrever_ambiente()}


@app.post("/perguntar")
def perguntar(pergunta: Pergunta) -> dict:
    """RAG sobre os documentos da padaria, com fontes."""
    return servico_rag().perguntar(pergunta.texto).para_dict()


@app.post("/conversar")
def conversar(mensagem: MensagemAgente) -> dict:
    """Agente garçom com ferramentas. Encomendas pedem aprovação humana."""
    resposta = agente().conversar(mensagem.texto, mensagem.sessao)
    return {"resposta": resposta, "aguardando_aprovacao": resposta.startswith("[aguardando aprovação humana]")}


@app.post("/aprovar")
def aprovar(decisao: Decisao) -> dict:
    """Aprova ou rejeita a ação pendente de uma sessão do agente."""
    return {"resposta": agente().decidir(decisao.sessao, decisao.aprovar, decisao.motivo)}


@app.get("/custos")
def custos() -> dict:
    """Uso e custo acumulados pelo RAG desde que a API subiu."""
    return observabilidade().resumo()
