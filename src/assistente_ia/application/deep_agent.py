"""Caso de uso: Deep Agent (biblioteca `deepagents`) — Aula 7.

Um deep agent é um agente com "equipamento extra":
- planejamento com lista de tarefas (write_todos — precisa do TodoListMiddleware desde a v0.7);
- sistema de arquivos VIRTUAL (ls, read_file, write_file, edit_file...) guardado no estado;
- subagentes especializados chamados pela ferramenta `task`.
"""

from __future__ import annotations

from typing import Any

from deepagents import create_deep_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, TodoListMiddleware
from langchain_core.language_models.chat_models import BaseChatModel

from assistente_ia.adapters.ferramentas.langchain_tools import para_langchain_lista
from assistente_ia.ports.ferramentas import FerramentaPort

PROMPT_ANALISTA = """Você é o analista de negócios da Padaria Peter Pão.
Para tarefas com várias etapas:
1. Planeje com write_todos.
2. Delegue pesquisas de preço ao subagente 'pesquisador-de-cardapio' usando a ferramenta task.
3. Salve o resultado final em /relatorio.md com write_file.
4. Termine com um resumo de no máximo 5 linhas."""

SUBAGENTE_PESQUISADOR = {
    "name": "pesquisador-de-cardapio",
    "description": "Pesquisa preços e calcula totais de produtos do cardápio. Responde em até 5 linhas.",
    "system_prompt": "Use as ferramentas da padaria para responder com números exatos, em até 5 linhas.",
}


def criar_deep_agent_padaria(
    modelo: BaseChatModel,
    ferramentas: list[FerramentaPort],
    max_chamadas_modelo: int = 15,
    checkpointer=None,
):
    """Monta o deep agent analista com um subagente pesquisador."""
    tools = para_langchain_lista(ferramentas)
    subagente = {**SUBAGENTE_PESQUISADOR, "tools": tools, "model": modelo}
    return create_deep_agent(
        model=modelo,
        tools=tools,
        system_prompt=PROMPT_ANALISTA,
        middleware=[TodoListMiddleware(), ModelCallLimitMiddleware(run_limit=max_chamadas_modelo, exit_behavior="end")],
        subagents=[subagente],
        checkpointer=checkpointer,
    )


def conteudo_do_arquivo(arquivo: Any) -> str:
    """O conteúdo dos arquivos virtuais pode vir como texto ou como dicionário com linhas."""
    if isinstance(arquivo, str):
        return arquivo
    if isinstance(arquivo, dict):
        conteudo = arquivo.get("content", "")
        return "\n".join(conteudo) if isinstance(conteudo, list) else str(conteudo)
    return str(arquivo)


def arquivos_gerados(resultado: dict) -> dict[str, str]:
    """{caminho: conteúdo} de todos os arquivos virtuais criados pelo agente."""
    return {caminho: conteudo_do_arquivo(a) for caminho, a in (resultado.get("files") or {}).items()}
