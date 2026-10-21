"""Caso de uso: agente com ferramentas (Aula 7), usando `create_agent` do LangChain 1.x.

Implementa a AgentePort. Inclui proteções de produção via middleware:
- limite de chamadas ao modelo (evita loop infinito e conta alta);
- mascaramento de dados pessoais (e-mail e CPF) antes de enviar ao modelo;
- aprovação humana para ferramentas sensíveis (ex.: registrar encomenda).
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from langchain.agents import create_agent
from langchain.agents.middleware import (
    HumanInTheLoopMiddleware,
    ModelCallLimitMiddleware,
    PIIMiddleware,
)
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

from assistente_ia.adapters.ferramentas.langchain_tools import para_langchain_lista
from assistente_ia.ports.ferramentas import FerramentaPort

PROMPT_GARCOM = """Você é o garçom virtual da Padaria Pão Nosso.
- Use SEMPRE as ferramentas para preços, totais, divisão de conta, horários e encomendas.
- Nunca invente preços nem produtos.
- Responda em português do Brasil, de forma simpática e curta."""

REGEX_CPF = r"\d{3}\.\d{3}\.\d{3}-\d{2}"


def _texto(conteudo: Any) -> str:
    if isinstance(conteudo, str):
        return conteudo
    if isinstance(conteudo, list):
        return "".join(b.get("text", "") if isinstance(b, dict) else str(b) for b in conteudo)
    return str(conteudo)


class AgenteLangChain:
    def __init__(
        self,
        modelo: BaseChatModel,
        ferramentas: list[FerramentaPort],
        system_prompt: str = PROMPT_GARCOM,
        aprovar: Iterable[str] = (),
        max_chamadas_modelo: int = 8,
        checkpointer=None,
    ) -> None:
        middleware = [
            ModelCallLimitMiddleware(run_limit=max_chamadas_modelo, exit_behavior="end"),
            PIIMiddleware("email", strategy="redact"),
            PIIMiddleware("cpf", detector=REGEX_CPF, strategy="mask"),
        ]
        aprovar = list(aprovar)
        if aprovar:
            middleware.append(HumanInTheLoopMiddleware(interrupt_on={nome: True for nome in aprovar}))

        self.grafo = create_agent(
            modelo,
            tools=para_langchain_lista(ferramentas),
            system_prompt=system_prompt,
            middleware=middleware,
            checkpointer=checkpointer or InMemorySaver(),
        )

    @staticmethod
    def _config(sessao: str) -> dict:
        return {"configurable": {"thread_id": sessao}}

    def _resultado_para_texto(self, resultado: dict) -> str:
        pendentes = resultado.get("__interrupt__")
        if pendentes:
            acoes = pendentes[0].value.get("action_requests", [])
            descricao = ", ".join(f"{a['name']}({a['args']})" for a in acoes)
            return f"[aguardando aprovação humana] {descricao}"
        return _texto(resultado["messages"][-1].content)

    def conversar(self, mensagem: str, sessao: str = "padrao") -> str:
        resultado = self.grafo.invoke({"messages": [{"role": "user", "content": mensagem}]}, self._config(sessao))
        return self._resultado_para_texto(resultado)

    def decidir(self, sessao: str, aprovar: bool, motivo: str = "") -> str:
        """Responde a uma pausa de aprovação humana: aprova ou rejeita a ação pendente."""
        if aprovar:
            decisao = {"type": "approve"}
        else:
            decisao = {"type": "reject", "message": motivo or "Ação recusada pela gerente."}
        resultado = self.grafo.invoke(Command(resume={"decisions": [decisao]}), self._config(sessao))
        return self._resultado_para_texto(resultado)

    def historico(self, sessao: str = "padrao") -> list:
        return self.grafo.get_state(self._config(sessao)).values.get("messages", [])
