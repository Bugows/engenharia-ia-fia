import pytest

from assistente_ia.config import ChaveAusenteError, Configuracoes


def test_sem_chave_vira_fake():
    assert Configuracoes(openai_api_key=None, modo="auto").usar_fake


def test_chave_com_formato_invalido_vira_fake():
    assert Configuracoes(openai_api_key="minha-chave", modo="auto").usar_fake


def test_modo_openai_sem_chave_da_erro_amigavel():
    with pytest.raises(ChaveAusenteError, match="OPENAI_API_KEY"):
        _ = Configuracoes(openai_api_key=None, modo="openai").usar_fake


def test_chave_nunca_aparece_no_repr():
    cfg = Configuracoes(openai_api_key="sk-segredo-123")
    assert "segredo" not in repr(cfg)
    assert "segredo" not in str(cfg)
