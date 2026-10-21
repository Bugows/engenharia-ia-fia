"""Aula 4 — Exercício 2: crie sua própria métrica.

Regra do negócio: toda resposta do RAG deve citar a fonte entre colchetes, ex.: [faq.md].
Implemente a métrica e calcule a taxa de citação de um conjunto de respostas.

Rodar e verificar (custo zero):
    uv run python aulas/aula_04_avaliacao/exercicios/ex02_metrica_cita_fonte.py
"""

import re

from assistente_ia.exercicios import verificar

FONTES_VALIDAS = {"cardapio.md", "faq.md", "politicas.md", "historia.md"}


def fontes_citadas(resposta: str) -> set[str]:
    """Conjunto de nomes entre colchetes, ex.: 'veja [faq.md]' -> {'faq.md'}."""
    # TODO: use re.findall(r"\[([^\]]+)\]", resposta) e transforme em set
    raise NotImplementedError("set(re.findall(...))")


def cita_fonte_valida(resposta: str) -> bool:
    """True se cita pelo menos UMA fonte que existe de verdade (evita fonte inventada)."""
    # TODO: interseção entre fontes_citadas(resposta) e FONTES_VALIDAS
    raise NotImplementedError("bool(fontes_citadas(resposta) & FONTES_VALIDAS)")


def taxa_de_citacao(respostas: list[str]) -> float:
    """Proporção (0 a 1) de respostas que citam fonte válida."""
    # TODO
    raise NotImplementedError("sum(...) / len(respostas)")


def checar():
    assert fontes_citadas("Abrimos às 6h [faq.md].") == {"faq.md"}
    assert cita_fonte_valida("R$ 4,50 [cardapio.md]")
    assert not cita_fonte_valida("R$ 4,50 [site-da-padaria.com]"), "Fonte inventada não vale!"
    assert not cita_fonte_valida("R$ 4,50")
    respostas = ["a [faq.md]", "b", "c [cardapio.md] [faq.md]", "d [inventado.md]"]
    assert taxa_de_citacao(respostas) == 0.5


if __name__ == "__main__":
    verificar("Aula 4 — Exercício 2", checar)
    _ = re  # o módulo re é usado na sua solução
