from fastapi.testclient import TestClient

from assistente_ia.api import main


def _cliente():
    for funcao in (main.observabilidade, main.servico_rag, main.agente):
        funcao.cache_clear()
    return TestClient(main.app)


def test_saude():
    resposta = _cliente().get("/saude")
    assert resposta.status_code == 200
    assert resposta.json()["modo"] == "fake"


def test_perguntar_devolve_fontes():
    resposta = _cliente().post("/perguntar", json={"texto": "Aceitam pix?"})
    assert resposta.status_code == 200
    assert "faq.md" in resposta.json()["fontes"]


def test_custos():
    cliente = _cliente()
    cliente.post("/perguntar", json={"texto": "Aceitam pix?"})
    assert cliente.get("/custos").json()["chamadas"] == 1


def test_texto_vazio_e_rejeitado():
    assert _cliente().post("/perguntar", json={"texto": ""}).status_code == 422
