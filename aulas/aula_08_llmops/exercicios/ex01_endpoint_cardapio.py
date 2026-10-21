"""Aula 8 — Exercício 1: publique o cardápio numa API.

Crie dois endpoints FastAPI usando as regras do domínio (domain/padaria.py):
  GET /cardapio            -> lista [{"produto": ..., "preco": ...}] em ordem alfabética
  GET /cardapio/{produto}  -> {"produto": ..., "preco": ...} ou erro 404

Rodar e verificar (custo zero):
    uv run python aulas/aula_08_llmops/exercicios/ex01_endpoint_cardapio.py
"""

from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from assistente_ia.domain import padaria
from assistente_ia.exercicios import verificar

app = FastAPI(title="Cardápio Peter Pão")


@app.get("/cardapio")
def listar_cardapio() -> list[dict]:
    # TODO 1: monte a lista a partir de padaria.CARDAPIO, ordenada pelo nome do produto
    raise NotImplementedError("sorted(padaria.CARDAPIO.items()) -> [{'produto': ..., 'preco': ...}]")


@app.get("/cardapio/{produto}")
def consultar_produto(produto: str) -> dict:
    # TODO 2: use padaria.nome_oficial e padaria.preco_de; se não existir,
    #         levante HTTPException(status_code=404, detail="Produto não encontrado")
    raise NotImplementedError("Use padaria.preco_de(produto) e HTTPException(404)")


def checar():
    cliente = TestClient(app, raise_server_exceptions=False)
    resposta = cliente.get("/cardapio")
    if resposta.status_code == 500:
        raise NotImplementedError("Complete o TODO 1 (GET /cardapio).")
    itens = resposta.json()
    assert len(itens) == len(padaria.CARDAPIO), "Liste todos os produtos."
    assert [i["produto"] for i in itens] == sorted(padaria.CARDAPIO), "Ordene por nome."

    resposta = cliente.get("/cardapio/PAO DE QUEIJO")
    if resposta.status_code == 500:
        raise NotImplementedError("Complete o TODO 2 (GET /cardapio/{produto}).")
    assert resposta.json() == {"produto": "pão de queijo", "preco": 4.5}, f"Recebido: {resposta.json()}"
    assert cliente.get("/cardapio/pizza").status_code == 404, "Produto inexistente deve dar 404."


if __name__ == "__main__":
    if verificar("Aula 8 — Exercício 1", checar):
        print("Suba de verdade com: uv run uvicorn --app-dir aulas/aula_08_llmops/exercicios ex01_endpoint_cardapio:app --reload")
    _ = HTTPException
