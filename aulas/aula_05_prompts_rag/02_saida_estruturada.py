"""Aula 5 — Exemplo 2: saída estruturada (o modelo preenche um formulário Pydantic).

Como rodar:
    uv run python aulas/aula_05_prompts_rag/02_saida_estruturada.py

Por que isso importa? Sistemas conversam com JSON, não com parágrafos.
Com saída estruturada, o modelo devolve um objeto validado que vai direto para o banco.
"""

from typing import Literal

from pydantic import BaseModel, Field

from assistente_ia.config import descrever_ambiente
from assistente_ia.container import criar_llm
from assistente_ia.domain.modelos import sistema, usuario


class Encomenda(BaseModel):
    """Encomenda extraída de uma mensagem livre do cliente."""

    produto: str = Field(description="Nome do produto do cardápio")
    quantidade: int = Field(ge=1, description="Quantidade de unidades")
    data_retirada: str = Field(description="Data no formato DD/MM")
    periodo: Literal["manhã", "tarde", "noite"]
    observacoes: str | None = Field(default=None, description="Pedidos especiais ou null")


print(descrever_ambiente(), "\n")
llm = criar_llm()

mensagens_clientes = [
    "Oi! Queria encomendar 40 coxinhas pro dia 20/12, de tarde. Pode ser sem cebola?",
    "Bom dia, me separa 3 bolos de rolo pra sexta 13/12 de manhã cedinho",
]

for texto in mensagens_clientes:
    encomenda = llm.responder_estruturado(
        [sistema("Extraia os dados da encomenda. Se faltar algo, use a melhor estimativa."), usuario(texto)],
        Encomenda,
    )
    print(f"Mensagem: {texto}")
    print(f"Objeto:   {encomenda.model_dump()}\n")

print("Repare: quantidade é int, período é uma das 3 opções. Nada de 'quarenta' ou 'à tardinha'.")
