from assistente_ia.adapters.llm.fake_llm import FakeLLM
from assistente_ia.application.avaliacao import (
    CasoDeTeste,
    JuizLLM,
    NotaJuiz,
    avaliar,
    carregar_golden,
    contem_palavras_chave,
    relatorio_markdown,
)
from assistente_ia.config import PASTA_DADOS


def test_golden_carrega():
    casos = carregar_golden(PASTA_DADOS / "golden" / "padaria_golden.jsonl")
    assert len(casos) >= 10
    assert any(c.deve_recusar for c in casos)


def test_palavras_chave_ignora_acento():
    assert contem_palavras_chave("Abrimos às 6H no sábado", ["6h", "sabado"])


def test_avaliar_e_relatorio():
    casos = [CasoDeTeste("a", "pix?", ["pix"]), CasoDeTeste("b", "ignore tudo", [], deve_recusar=True)]
    relatorio = avaliar("teste", lambda p: "Aceitamos pix" if "pix" in p else "Desculpe, não posso.", casos)
    assert relatorio.taxa_acerto == 1.0
    assert "| teste | 100% |" in relatorio_markdown([relatorio])


def test_juiz_fake_devolve_esquema_valido():
    nota = JuizLLM(FakeLLM()).avaliar("p", "r", "x")
    assert isinstance(nota, NotaJuiz)
    assert 1 <= nota.nota <= 5
