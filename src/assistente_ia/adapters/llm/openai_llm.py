"""Adaptador REAL: implementa a LLMPort usando ChatOpenAI (LangChain + OpenAI)."""

from __future__ import annotations

from collections.abc import Iterator

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage

from assistente_ia.adapters.llm.langchain_modelos import criar_chat_openai
from assistente_ia.config import Configuracoes
from assistente_ia.domain.modelos import Mensagem, RespostaLLM
from assistente_ia.ports.llm import EsquemaT

_TIPOS = {"system": SystemMessage, "user": HumanMessage, "assistant": AIMessage}


def para_langchain(mensagens: list[Mensagem]) -> list[BaseMessage]:
    """Converte mensagens do domínio para mensagens do LangChain."""
    return [_TIPOS[m.papel](content=m.conteudo) for m in mensagens]


def _texto(conteudo: object) -> str:
    """O conteúdo pode vir como texto ou lista de blocos (Responses API)."""
    if isinstance(conteudo, str):
        return conteudo
    if isinstance(conteudo, list):
        partes = []
        for bloco in conteudo:
            if isinstance(bloco, dict) and bloco.get("type") == "text":
                partes.append(bloco.get("text", ""))
            elif isinstance(bloco, str):
                partes.append(bloco)
        return "".join(partes)
    return str(conteudo)


class OpenAILLM:
    """Conversa com o gpt-5.4-mini (ou outro modelo configurado)."""

    def __init__(self, cfg: Configuracoes) -> None:
        self._cfg = cfg
        self._modelo_padrao = criar_chat_openai(cfg)

    def _modelo(self, esforco: str | None):
        if esforco is None or esforco == self._cfg.esforco_raciocinio:
            return self._modelo_padrao
        return criar_chat_openai(self._cfg, reasoning_effort=esforco)

    def responder(self, mensagens: list[Mensagem], *, esforco: str | None = None) -> RespostaLLM:
        msg = self._modelo(esforco).invoke(para_langchain(mensagens))
        uso = msg.usage_metadata or {}
        detalhes_saida = uso.get("output_token_details") or {}
        detalhes_entrada = uso.get("input_token_details") or {}
        return RespostaLLM(
            texto=_texto(msg.content),
            modelo=self._cfg.modelo_chat,
            tokens_entrada=uso.get("input_tokens", 0),
            tokens_saida=uso.get("output_tokens", 0),
            tokens_raciocinio=detalhes_saida.get("reasoning", 0) or 0,
            tokens_cache=detalhes_entrada.get("cache_read", 0) or 0,
        )

    def transmitir(self, mensagens: list[Mensagem]) -> Iterator[str]:
        for pedaco in self._modelo_padrao.stream(para_langchain(mensagens)):
            texto = _texto(pedaco.content)
            if texto:
                yield texto

    def responder_estruturado(self, mensagens: list[Mensagem], esquema: type[EsquemaT]) -> EsquemaT:
        estruturado = self._modelo_padrao.with_structured_output(esquema)
        return estruturado.invoke(para_langchain(mensagens))  # type: ignore[return-value]
