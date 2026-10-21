"""Adaptador REAL de embeddings: OpenAI text-embedding-3-small via LangChain."""

from __future__ import annotations

from langchain_openai import OpenAIEmbeddings

from assistente_ia.config import Configuracoes


class OpenAIEmbeddingsAdapter:
    """Implementa a EmbeddingsPort. Também expõe o objeto LangChain em `.langchain`."""

    def __init__(self, cfg: Configuracoes) -> None:
        parametros = {"model": cfg.modelo_embeddings, "api_key": cfg.exigir_chave()}
        if cfg.openai_base_url:
            parametros["base_url"] = cfg.openai_base_url
        self.langchain = OpenAIEmbeddings(**parametros)

    def vetorizar_textos(self, textos: list[str]) -> list[list[float]]:
        return self.langchain.embed_documents(textos)

    def vetorizar_consulta(self, texto: str) -> list[float]:
        return self.langchain.embed_query(texto)
