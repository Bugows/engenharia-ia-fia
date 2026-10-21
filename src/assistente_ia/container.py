"""Container de dependências: o "quadro de tomadas" do projeto.

É o ÚNICO lugar que decide qual adaptador ligar em cada porta.
Sem chave (ou MODO=fake) -> adaptadores simulados. Com chave -> OpenAI.
O resto do código nunca precisa saber qual foi escolhido.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage

from assistente_ia.config import obter_config
from assistente_ia.ports.embeddings import EmbeddingsPort
from assistente_ia.ports.llm import LLMPort


def modo_fake() -> bool:
    return obter_config().usar_fake


def criar_llm() -> LLMPort:
    """LLMPort: OpenAILLM (com chave) ou FakeLLM (sem chave)."""
    cfg = obter_config()
    if cfg.usar_fake:
        from assistente_ia.adapters.llm.fake_llm import FakeLLM

        return FakeLLM()
    from assistente_ia.adapters.llm.openai_llm import OpenAILLM  # import tardio

    return OpenAILLM(cfg)


def criar_chat_model(roteiro_fake: Iterable[AIMessage] | None = None, **ajustes: Any) -> BaseChatModel:
    """Modelo de chat do LangChain (para agentes e grafos).

    - Com chave: ChatOpenAI (aceita ajustes como reasoning_effort, max_tokens, temperature).
    - Sem chave: FakeChatModel seguindo o `roteiro_fake` (lista de AIMessage).
    """
    cfg = obter_config()
    if cfg.usar_fake:
        from assistente_ia.adapters.llm.fake_llm import FakeChatModel

        extras = {"rate_limiter": ajustes["rate_limiter"]} if "rate_limiter" in ajustes else {}
        return FakeChatModel(roteiro=list(roteiro_fake or []), **extras)
    from assistente_ia.adapters.llm.langchain_modelos import criar_chat_openai

    return criar_chat_openai(cfg, **ajustes)


def criar_embeddings() -> EmbeddingsPort:
    """EmbeddingsPort. O objeto LangChain equivalente fica em `.langchain`."""
    cfg = obter_config()
    if cfg.usar_fake:
        from assistente_ia.adapters.embeddings.fake_embeddings import FakeEmbeddings

        return FakeEmbeddings()
    from assistente_ia.adapters.embeddings.openai_embeddings import OpenAIEmbeddingsAdapter

    return OpenAIEmbeddingsAdapter(cfg)


def criar_vector_store(embeddings: EmbeddingsPort | None = None):
    from assistente_ia.adapters.vector_store.memoria import VectorStoreMemoria

    return VectorStoreMemoria(embeddings or criar_embeddings())


def carregar_base(pasta: str = "padaria", embeddings: EmbeddingsPort | None = None):
    """Lê os documentos de dados/<pasta>, divide em pedaços e indexa."""
    from assistente_ia.adapters.documentos.arquivos_locais import RepositorioArquivosLocais

    vector_store = criar_vector_store(embeddings)
    vector_store.adicionar(RepositorioArquivosLocais().carregar(pasta))
    return vector_store


def criar_observabilidade(silencioso: bool = False):
    from assistente_ia.adapters.observabilidade.console import ObservabilidadeConsole

    return ObservabilidadeConsole(limite_usd=obter_config().limite_custo_sessao_usd, silencioso=silencioso)


def criar_servico_rag(pasta: str = "padaria", llm: LLMPort | None = None, observabilidade=None):
    from assistente_ia.application.rag import ServicoRAG

    return ServicoRAG(llm or criar_llm(), carregar_base(pasta), observabilidade)


def criar_agente_garcom(
    roteiro_fake: Iterable[AIMessage] | None = None,
    aprovar: Iterable[str] = ("registrar_encomenda",),
):
    from assistente_ia.application.agente import AgenteLangChain
    from assistente_ia.application.ferramentas import ferramentas_padaria

    modelo = criar_chat_model(roteiro_fake, reasoning_effort="low", max_tokens=600)
    return AgenteLangChain(modelo, ferramentas_padaria(), aprovar=aprovar)
