"""Configuração dos testes: TUDO roda em modo fake, exceto os marcados com @pytest.mark.openai."""

import pytest

from assistente_ia.config import obter_config


@pytest.fixture(autouse=True)
def forcar_fake(request, monkeypatch):
    if request.node.get_closest_marker("openai") is None:
        monkeypatch.setenv("MODO", "fake")
    obter_config.cache_clear()
    yield
    obter_config.cache_clear()
