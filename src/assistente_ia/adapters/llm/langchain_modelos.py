"""Fábrica de modelos de chat do LangChain (ChatOpenAI) a partir da configuração.

Usada pelo adaptador OpenAILLM e pelos agentes (que precisam de um modelo LangChain).
"""

from __future__ import annotations

from typing import Any

from langchain_openai import ChatOpenAI

from assistente_ia.config import Configuracoes


def criar_chat_openai(cfg: Configuracoes, **ajustes: Any) -> ChatOpenAI:
    """Cria um ChatOpenAI com os padrões econômicos do curso.

    Qualquer parâmetro pode ser sobrescrito, por exemplo:
        criar_chat_openai(cfg, reasoning_effort="low", max_tokens=1500)

    Atenção (GPT-5.x): `temperature` só é aceita com reasoning_effort="none".
    Com outro esforço, o LangChain REMOVE a temperature silenciosamente.
    """
    parametros: dict[str, Any] = {
        "model": cfg.modelo_chat,
        "api_key": cfg.exigir_chave(),
        "reasoning_effort": cfg.esforco_raciocinio,
        "max_tokens": cfg.max_tokens_saida,
        "max_retries": 2,
        "timeout": 60,
    }
    if cfg.openai_base_url:
        parametros["base_url"] = cfg.openai_base_url
    parametros.update(ajustes)

    esforco = parametros.get("reasoning_effort")
    if parametros.get("temperature") is not None and esforco not in (None, "none"):
        raise ValueError(
            "No GPT-5.x, temperature só funciona com reasoning_effort='none'. "
            f"Você pediu reasoning_effort={esforco!r}."
        )
    return ChatOpenAI(**parametros)
