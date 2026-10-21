"""Aula 2 — Exercício 2: o custo total de 12 meses (TCO).

TCO = custo de montar (setup) + 12 x (tokens + infraestrutura + manutenção humana)

Rodar e verificar:
    uv run python aulas/aula_02_planejamento/exercicios/ex02_tco_12_meses.py
"""

from assistente_ia.domain.custos import custo_usd, formatar_brl
from assistente_ia.exercicios import verificar


def custo_tokens_mensal_brl(conversas: int, entrada: int, saida: int, cotacao: float) -> float:
    """Custo mensal dos tokens em reais, usando o gpt-5.4-mini."""
    # TODO: use custo_usd("gpt-5.4-mini", entrada, saida), multiplique pelas conversas e pela cotação
    raise NotImplementedError("custo_usd(...) * conversas * cotacao")


def tco_12_meses(
    custo_setup: float,
    custo_tokens_mensal: float,
    custo_infra_mensal: float,
    horas_manutencao_mes: float,
    valor_hora: float,
) -> float:
    """Custo total do primeiro ano, em reais."""
    # TODO: setup + 12 * (tokens + infra + horas * valor_hora)
    raise NotImplementedError("Some o setup com 12 vezes o custo mensal completo.")


def checar_tokens():
    valor = custo_tokens_mensal_brl(conversas=1000, entrada=2000, saida=500, cotacao=5.0)
    esperado = custo_usd("gpt-5.4-mini", 2000, 500) * 1000 * 5.0
    assert abs(valor - esperado) < 0.01, f"Esperava R$ {esperado:.2f}, recebi R$ {valor:.2f}"


def checar_tco():
    valor = tco_12_meses(2000, 50, 100, 4, 120)
    assert valor == 2000 + 12 * (50 + 100 + 4 * 120), f"TCO incorreto: {valor}"


if __name__ == "__main__":
    if verificar("Aula 2 — Exercício 2", checar_tokens, checar_tco):
        mensal = custo_tokens_mensal_brl(3000, 2500, 300, 5.5)
        print(f"Padaria: tokens {formatar_brl(mensal)}/mês | TCO 12 meses: {formatar_brl(tco_12_meses(3000, mensal, 150, 4, 120))}")
