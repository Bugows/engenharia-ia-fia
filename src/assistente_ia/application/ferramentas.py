"""Ferramentas da Padaria Pão Nosso que os agentes podem usar.

Cada classe "encaixa" na FerramentaPort: tem `nome`, `descricao` e `executar(...)`.
As regras de verdade ficam no domínio (domain/padaria.py).
"""

from __future__ import annotations

from datetime import datetime

from assistente_ia.domain import padaria
from assistente_ia.domain.custos import formatar_brl
from assistente_ia.ports.ferramentas import FerramentaPort


class ConsultarPreco:
    nome = "consultar_preco"
    descricao = "Consulta o preço unitário, em reais, de um produto do cardápio da padaria."

    def executar(self, produto: str) -> str:
        preco = padaria.preco_de(produto)
        if preco is None:
            opcoes = ", ".join(padaria.CARDAPIO)
            return f"'{produto}' não está no cardápio. Opções: {opcoes}."
        return f"{padaria.nome_oficial(produto)}: {formatar_brl(preco)}"


class CalcularTotal:
    nome = "calcular_total"
    descricao = (
        "Calcula o valor total de um pedido. Recebe um dicionário com o nome do produto "
        "e a quantidade, por exemplo {'café': 2, 'sonho': 1}."
    )

    def executar(self, itens: dict[str, int]) -> str:
        try:
            total = padaria.total_do_pedido(itens)
        except ValueError as erro:
            return f"Não consegui calcular: {erro}"
        return f"Total do pedido: {formatar_brl(total)}"


class RacharConta:
    nome = "rachar_conta"
    descricao = "Divide um valor total entre várias pessoas, com gorjeta percentual opcional."

    def executar(self, total: float, pessoas: int, gorjeta_percentual: float = 0.0) -> str:
        try:
            parte = padaria.dividir_conta(total, pessoas, gorjeta_percentual)
        except ValueError as erro:
            return f"Não consegui dividir: {erro}"
        return f"Cada pessoa paga {formatar_brl(parte)}"


class VerHorario:
    nome = "ver_horario"
    descricao = "Informa o horário de funcionamento da padaria em cada dia da semana."

    def executar(self) -> str:
        return "; ".join(f"{dia}: {horas}" for dia, horas in padaria.HORARIO.items())


class RegistrarEncomenda:
    nome = "registrar_encomenda"
    descricao = (
        "Registra uma encomenda de um produto do cardápio. Use somente quando o cliente "
        "confirmar produto, quantidade e data de retirada (formato DD/MM)."
    )

    def __init__(self) -> None:
        self.encomendas: list[dict] = []

    def executar(self, produto: str, quantidade: int, data_retirada: str) -> str:
        nome = padaria.nome_oficial(produto)
        if nome is None:
            return f"'{produto}' não está no cardápio."
        if quantidade <= 0:
            return "A quantidade precisa ser positiva."
        registro = {
            "produto": nome,
            "quantidade": quantidade,
            "data_retirada": data_retirada,
            "registrado_em": datetime.now().isoformat(timespec="seconds"),
        }
        self.encomendas.append(registro)
        return f"Encomenda nº {len(self.encomendas)} registrada: {quantidade}x {nome} para {data_retirada}."


def ferramentas_padaria() -> list[FerramentaPort]:
    """Kit padrão de ferramentas do garçom virtual."""
    return [ConsultarPreco(), CalcularTotal(), RacharConta(), VerHorario(), RegistrarEncomenda()]
