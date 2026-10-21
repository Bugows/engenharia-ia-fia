"""Regras de negócio da Padaria Peter Pão (empresa fictícia do curso).

Tudo em Python puro: estas funções são usadas tanto pelo código "normal"
quanto pelas ferramentas dos agentes (Aula 7).
"""

from __future__ import annotations

import unicodedata

CARDAPIO: dict[str, float] = {
    "pão francês": 0.90,
    "pão de queijo": 4.50,
    "coxinha": 7.00,
    "sonho": 6.00,
    "bolo de rolo": 9.00,
    "café": 4.00,
    "café com leite": 5.50,
    "suco de laranja": 8.00,
    "pão na chapa": 6.50,
    "misto quente": 12.00,
}

HORARIO = {
    "segunda a sexta": "6h às 20h",
    "sábado": "6h às 18h",
    "domingo": "7h às 13h",
}

ENCOMENDA_MINIMA_HORAS = 24
LIMITE_ENCOMENDA_SEM_APROVACAO = 30  # unidades


def _chave(produto: str) -> str:
    """Normaliza o nome do produto (minúsculas, sem acento, sem espaços extras)."""
    sem_acento = unicodedata.normalize("NFKD", produto).encode("ascii", "ignore").decode()
    return " ".join(sem_acento.lower().split())


_INDICE = {_chave(nome): nome for nome in CARDAPIO}


def nome_oficial(produto: str) -> str | None:
    """Encontra o nome oficial do produto ('PAO DE QUEIJO' -> 'pão de queijo')."""
    return _INDICE.get(_chave(produto))


def preco_de(produto: str) -> float | None:
    """Preço unitário em reais, ou None se o produto não existe."""
    nome = nome_oficial(produto)
    return CARDAPIO[nome] if nome else None


def total_do_pedido(itens: dict[str, int]) -> float:
    """Soma o pedido. Ex.: {'café': 2, 'sonho': 1} -> 14.0"""
    total = 0.0
    for produto, quantidade in itens.items():
        preco = preco_de(produto)
        if preco is None:
            raise ValueError(f"Produto fora do cardápio: {produto}")
        if quantidade <= 0:
            raise ValueError("A quantidade precisa ser positiva.")
        total += preco * quantidade
    return round(total, 2)


def dividir_conta(total: float, pessoas: int, gorjeta_percentual: float = 0.0) -> float:
    """Quanto cada pessoa paga (com gorjeta opcional)."""
    if pessoas <= 0:
        raise ValueError("Precisa ter pelo menos 1 pessoa.")
    return round(total * (1 + gorjeta_percentual / 100) / pessoas, 2)


def encomenda_precisa_aprovacao(quantidade: int) -> bool:
    """Encomendas grandes precisam de aprovação humana (regra da gerente Dona Cida)."""
    return quantidade > LIMITE_ENCOMENDA_SEM_APROVACAO


def precos_desconhecidos(texto: str) -> list[float]:
    """Guardrail de saída: valores em R$ citados no texto que NÃO existem no cardápio.

    Útil para pegar preço inventado (alucinação). Totais calculados também aparecem aqui,
    então use como ALERTA para revisão, não como bloqueio automático.
    """
    import re

    precos_validos = {round(p, 2) for p in CARDAPIO.values()}
    encontrados = re.findall(r"R\$\s?(\d+(?:\.\d{3})*(?:,\d{2})?)", texto)
    valores = [round(float(v.replace(".", "").replace(",", ".")), 2) for v in encontrados]
    return [v for v in valores if v not in precos_validos]
