"""Aula 3 — Exercício 2: similaridade de cosseno feita à mão.

cos(a, b) = (a · b) / (|a| x |b|)
  a · b = soma de a[i] * b[i]
  |a|   = raiz quadrada da soma de a[i]²

Rodar e verificar (custo zero):
    uv run python aulas/aula_03_modelos/exercicios/ex02_cosseno_na_mao.py
"""

import math

from assistente_ia.exercicios import verificar


def produto_escalar(a: list[float], b: list[float]) -> float:
    # TODO
    raise NotImplementedError("sum(x * y for x, y in zip(a, b))")


def norma(a: list[float]) -> float:
    # TODO
    raise NotImplementedError("math.sqrt(sum(x * x for x in a))")


def cosseno(a: list[float], b: list[float]) -> float:
    # TODO: use as duas funções acima (cuidado com divisão por zero: devolva 0.0)
    raise NotImplementedError("produto_escalar / (norma(a) * norma(b))")


def mais_parecido(consulta: list[float], candidatos: dict[str, list[float]]) -> str:
    """Nome do candidato com MAIOR cosseno em relação à consulta."""
    # TODO
    raise NotImplementedError("max(candidatos, key=lambda nome: cosseno(consulta, candidatos[nome]))")


# Vetores de brinquedo com 3 dimensões: [doce, salgado, bebida]
CARDAPIO_VETORIAL = {
    "sonho": [0.9, 0.1, 0.0],
    "coxinha": [0.0, 1.0, 0.0],
    "café": [0.1, 0.0, 0.9],
    "pão de queijo": [0.1, 0.9, 0.0],
}


def checar_basico():
    assert produto_escalar([1, 2], [3, 4]) == 11
    assert math.isclose(norma([3, 4]), 5)
    assert math.isclose(cosseno([1, 0], [1, 0]), 1.0)
    assert math.isclose(cosseno([1, 0], [0, 1]), 0.0)
    assert cosseno([0, 0], [1, 1]) == 0.0, "Vetor zerado deve dar cosseno 0.0"


def checar_busca():
    assert mais_parecido([1.0, 0.0, 0.1], CARDAPIO_VETORIAL) == "sonho"
    assert mais_parecido([0.0, 0.2, 1.0], CARDAPIO_VETORIAL) == "café"


if __name__ == "__main__":
    verificar("Aula 3 — Exercício 2", checar_basico, checar_busca)
