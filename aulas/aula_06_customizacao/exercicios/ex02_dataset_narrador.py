"""Aula 6 — Exercício 2: crie o dataset do "Narrador Empolgado".

A rádio comunitária do bairro quer um assistente que narre os resultados da
Copa da Várzea como um narrador de futebol empolgado ("É GOOOOL!").
Escreva pelo menos 6 exemplos de alta qualidade.

Rodar e verificar (custo zero):
    uv run python aulas/aula_06_customizacao/exercicios/ex02_dataset_narrador.py
"""

import json

from assistente_ia.config import PASTA_SAIDAS
from assistente_ia.domain.dataset import validar_linhas
from assistente_ia.exercicios import verificar

SISTEMA = "Você é o Galvão da Várzea, narrador empolgado da rádio comunitária. Seja animado, mas nunca invente placar."

# Cada exemplo: (mensagem do usuário, resposta ideal do narrador)
PARES: list[tuple[str, str]] = [
    ("Resultado: Unidos da Vila 2 x 1 Leões do Morro", "É DA VILA! Dois a um no Campo do Seu Zé, e a torcida não para de cantar! Os Leões do Morro brigaram até o fim, mas hoje deu Unidos da Vila!"),
    # TODO: escreva mais 5 pares (no mínimo). Varie: empate, goleada, virada, jogo suspenso, artilheiro.
]


def montar_dataset() -> list[dict]:
    """Transforme PARES em exemplos no formato {"messages": [system, user, assistant]}."""
    # TODO
    raise NotImplementedError("Para cada (usuario, resposta) em PARES, monte o dicionário com 3 mensagens.")


def checar():
    dataset = montar_dataset()
    assert len(dataset) >= 6, f"Escreva pelo menos 6 exemplos (você tem {len(dataset)})."
    relatorio = validar_linhas([json.dumps(e, ensure_ascii=False) for e in dataset])
    assert relatorio.ok, " | ".join(relatorio.erros)
    respostas = [e["messages"][-1]["content"] for e in dataset]
    assert len(set(respostas)) == len(respostas), "As respostas devem ser diferentes entre si."


if __name__ == "__main__":
    if verificar("Aula 6 — Exercício 2", checar):
        PASTA_SAIDAS.mkdir(exist_ok=True)
        destino = PASTA_SAIDAS / "narrador.jsonl"
        destino.write_text("\n".join(json.dumps(e, ensure_ascii=False) for e in montar_dataset()) + "\n", encoding="utf-8")
        print(f"Dataset salvo em {destino}")
