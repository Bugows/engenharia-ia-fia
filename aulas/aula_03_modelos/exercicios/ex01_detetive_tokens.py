"""Aula 3 — Exercício 1: detetive de tokens.

Escreva funções que mostram onde o português "custa caro".

Rodar e verificar (custo zero):
    uv run python aulas/aula_03_modelos/exercicios/ex01_detetive_tokens.py
"""

from assistente_ia.adapters.tokenizador import contar_tokens
from assistente_ia.exercicios import verificar


def tokens_por_palavra(frase: str) -> float:
    """Razão entre número de tokens e número de palavras (separadas por espaço)."""
    # TODO: conte os tokens com contar_tokens e divida pelo número de palavras
    raise NotImplementedError("contar_tokens(frase) / len(frase.split())")


def frase_mais_cara(frases: list[str]) -> str:
    """Devolve a frase com a MAIOR razão tokens/palavra."""
    # TODO: use max(...) com key=tokens_por_palavra
    raise NotImplementedError("max(frases, key=tokens_por_palavra)")


SUSPEITAS = [
    "o pão está quente",
    "anticonstitucionalissimamente inconstitucional",
    "the bread is hot",
]


def checar_razao():
    razao = tokens_por_palavra("pão de queijo")
    assert razao > 0, "A razão precisa ser positiva."
    assert abs(razao - contar_tokens("pão de queijo") / 3) < 1e-9, "Divida pelo número de palavras (3)."


def checar_mais_cara():
    resposta = frase_mais_cara(SUSPEITAS)
    assert resposta == max(SUSPEITAS, key=tokens_por_palavra), f"Frase errada: {resposta!r}"


if __name__ == "__main__":
    if verificar("Aula 3 — Exercício 1", checar_razao, checar_mais_cara):
        for frase in SUSPEITAS:
            print(f"{tokens_por_palavra(frase):.2f} tokens/palavra -> {frase}")
