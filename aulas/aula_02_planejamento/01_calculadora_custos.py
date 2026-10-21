"""Aula 2 — Exemplo 1: quanto custa o assistente por mês?

Como rodar (não usa a API, custo zero):
    uv run python aulas/aula_02_planejamento/01_calculadora_custos.py

Contamos os tokens do contexto (FAQ + cardápio) com o tiktoken e projetamos o custo.
Atenção: o encoding o200k_base é uma APROXIMAÇÃO; o número oficial vem do `usage_metadata`.
"""

from rich.console import Console
from rich.table import Table

from assistente_ia.adapters.tokenizador import contar_tokens as tokens
from assistente_ia.config import PASTA_DADOS
from assistente_ia.domain.custos import custo_brl, custo_usd, formatar_brl

console = Console()


# 1) Contexto que vai em toda pergunta (no RAG, só os trechos relevantes; aqui, o pior caso)
contexto = (PASTA_DADOS / "padaria" / "faq.md").read_text(encoding="utf-8")
contexto += (PASTA_DADOS / "padaria" / "cardapio.md").read_text(encoding="utf-8")
prompt_sistema = "Você é o atendente virtual da Padaria Peter Pão. Responda com base nos documentos."
pergunta_media = "Oi, boa tarde! Que horas vocês abrem no sábado e aceitam pix?"

entrada = tokens(prompt_sistema) + tokens(contexto) + tokens(pergunta_media)
saida = 120  # resposta curta típica

console.print(f"Tokens de entrada por pergunta: [bold]{entrada}[/] | saída estimada: [bold]{saida}[/]")

# 2) Cenários
tabela = Table(title="Custo mensal estimado — gpt-5.4-mini")
for coluna in ("Cenário", "Conversas/mês", "Raciocínio", "US$/mês", "Reais/mês"):
    tabela.add_column(coluna, justify="right")

cenarios = [
    ("Piloto", 500, 0),
    ("Padaria", 3_000, 0),
    ("Rede com 5 lojas", 15_000, 0),
    ("Padaria + raciocínio 'medium'", 3_000, 400),  # tokens de raciocínio contam como SAÍDA
]
for nome, conversas, raciocinio in cenarios:
    usd = custo_usd("gpt-5.4-mini", entrada, saida + raciocinio) * conversas
    tabela.add_row(nome, f"{conversas:,}", f"+{raciocinio} tok", f"{usd:,.2f}", formatar_brl(custo_brl(usd)))
console.print(tabela)

# 3) O poder do cache: o prompt de sistema + contexto fixo podem vir do cache (10x mais barato)
em_cache = tokens(prompt_sistema) + tokens(contexto)
com_cache = custo_usd("gpt-5.4-mini", entrada, saida, em_cache=em_cache) * 3_000
sem_cache = custo_usd("gpt-5.4-mini", entrada, saida) * 3_000
console.print(f"\nCom cache de prompt: US$ {com_cache:.2f}/mês (sem cache: US$ {sem_cache:.2f}) "
              f"-> economia de {1 - com_cache / sem_cache:.0%}")
console.print("\n[dim]Dica: deixe o prompt de sistema e o contexto fixo SEMPRE no início e iguais.[/]")
