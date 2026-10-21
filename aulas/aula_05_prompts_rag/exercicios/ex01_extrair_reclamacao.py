"""Aula 5 — Exercício 1: extrair uma reclamação em formato estruturado.

A Dona Cida quer um painel de reclamações. Cada mensagem livre do cliente deve virar
um objeto com: produto, gravidade (baixa/media/alta), resumo e se pede reembolso.

Rodar e verificar (modo fake ou real):
    uv run python aulas/aula_05_prompts_rag/exercicios/ex01_extrair_reclamacao.py
"""

from typing import Literal

from pydantic import BaseModel, Field

from assistente_ia.adapters.llm.fake_llm import FakeLLM
from assistente_ia.domain.modelos import sistema, usuario
from assistente_ia.exercicios import verificar
from assistente_ia.ports import LLMPort


class Reclamacao(BaseModel):
    """TODO: crie 4 campos:
    - produto: str (com description)
    - gravidade: Literal["baixa", "media", "alta"]
    - resumo: str com no máximo 120 caracteres (dica: Field(max_length=120))
    - pede_reembolso: bool
    """

    # TODO: declare os campos aqui


def extrair(llm: LLMPort, mensagem: str) -> Reclamacao:
    """Use llm.responder_estruturado com um prompt de sistema claro."""
    # TODO
    raise NotImplementedError("return llm.responder_estruturado([sistema(...), usuario(mensagem)], Reclamacao)")


def checar_esquema():
    campos = Reclamacao.model_fields
    if not campos:
        raise NotImplementedError("Declare os campos da classe Reclamacao.")
    for nome in ("produto", "gravidade", "resumo", "pede_reembolso"):
        assert nome in campos, f"Falta o campo '{nome}'."
    assert campos["pede_reembolso"].annotation is bool, "pede_reembolso deve ser bool."


def checar_extracao():
    resultado = extrair(FakeLLM(), "A coxinha veio fria e crua por dentro, quero meu dinheiro de volta!")
    assert isinstance(resultado, Reclamacao)
    assert resultado.gravidade in ("baixa", "media", "alta")


if __name__ == "__main__":
    if verificar("Aula 5 — Exercício 1", checar_esquema, checar_extracao):
        from assistente_ia.container import criar_llm

        print(extrair(criar_llm(), "O café com leite veio frio, mas o atendente foi gentil.").model_dump())
    _ = (Literal, Field, sistema, usuario)  # usados na sua solução
