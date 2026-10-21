"""Testes que chamam a API REAL. Rodam só com chave: uv run pytest -m openai"""

import pytest

from assistente_ia.config import obter_config
from assistente_ia.domain.modelos import Mensagem

pytestmark = pytest.mark.openai


@pytest.fixture(autouse=True)
def exigir_chave():
    obter_config.cache_clear()
    if not obter_config().tem_chave:
        pytest.skip("Sem OPENAI_API_KEY: teste de integração pulado.")


def test_chat_real_responde_e_conta_tokens():
    from assistente_ia.adapters.llm.openai_llm import OpenAILLM

    resposta = OpenAILLM(obter_config()).responder([Mensagem("user", "Responda apenas: oi")])
    assert resposta.texto.strip()
    assert resposta.tokens_saida > 0


def test_temperature_funciona_com_esforco_none():
    from assistente_ia.adapters.llm.langchain_modelos import criar_chat_openai

    modelo = criar_chat_openai(obter_config(), reasoning_effort="none", temperature=0.2, max_tokens=20)
    assert modelo.invoke("Diga 'ok'").content


def test_embeddings_reais():
    from assistente_ia.adapters.embeddings.openai_embeddings import OpenAIEmbeddingsAdapter

    vetor = OpenAIEmbeddingsAdapter(obter_config()).vetorizar_consulta("pão de queijo")
    assert len(vetor) == 1536
