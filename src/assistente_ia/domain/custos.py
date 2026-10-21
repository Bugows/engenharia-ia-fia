"""Cálculo de custo de chamadas a modelos.

Preços em dólares por 1 milhão de tokens, verificados em out/2026.
Confira sempre a página oficial antes de cada turma: https://openai.com/api/pricing
"""

from __future__ import annotations

PRECOS_USD_POR_MILHAO: dict[str, dict[str, float]] = {
    "gpt-5.4-mini": {"entrada": 0.75, "cache": 0.075, "saida": 4.50},
    "text-embedding-3-small": {"entrada": 0.02, "cache": 0.02, "saida": 0.0},
    "text-embedding-3-large": {"entrada": 0.13, "cache": 0.13, "saida": 0.0},
}

COTACAO_DOLAR_PADRAO = 5.50  # ajuste para a cotação do dia


def custo_usd(modelo: str, entrada: int, saida: int = 0, em_cache: int = 0) -> float:
    """Custo em dólares de uma chamada.

    - entrada: tokens enviados (prompt + contexto)
    - saida: tokens gerados (ATENÇÃO: tokens de raciocínio contam como saída)
    - em_cache: parte da entrada que veio do cache (10x mais barata no gpt-5.4-mini)

    Modelos desconhecidos (ex.: "fake") custam zero.
    """
    precos = PRECOS_USD_POR_MILHAO.get(modelo)
    if precos is None:
        return 0.0
    if em_cache > entrada:
        raise ValueError("Tokens em cache não podem ser maiores que os tokens de entrada.")
    sem_cache = entrada - em_cache
    total = sem_cache * precos["entrada"] + em_cache * precos["cache"] + saida * precos["saida"]
    return total / 1_000_000


def custo_brl(custo_em_dolar: float, cotacao: float = COTACAO_DOLAR_PADRAO) -> float:
    """Converte dólares para reais."""
    return custo_em_dolar * cotacao


def custo_mensal_usd(
    modelo: str, entrada_por_conversa: int, saida_por_conversa: int, conversas_por_mes: int
) -> float:
    """Projeção simples de custo mensal."""
    return custo_usd(modelo, entrada_por_conversa, saida_por_conversa) * conversas_por_mes


def roi(ganho_mensal: float, custo_mensal: float) -> float:
    """Retorno sobre investimento: (ganho - custo) / custo. 1.0 = 100%."""
    if custo_mensal <= 0:
        raise ValueError("O custo mensal precisa ser maior que zero.")
    return (ganho_mensal - custo_mensal) / custo_mensal


def formatar_brl(valor: float) -> str:
    """1234.5 -> 'R$ 1.234,50' (formato brasileiro)."""
    texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"
