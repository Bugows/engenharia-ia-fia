"""Aula 4 — Exemplo 1: avaliar o RAG da padaria contra o golden dataset.

Como rodar:
    uv run python aulas/aula_04_avaliacao/01_rodar_golden.py
    MODO=fake uv run python aulas/aula_04_avaliacao/01_rodar_golden.py

Golden dataset = perguntas com resposta conhecida (dados/golden/padaria_golden.jsonl).
É o "gabarito da prova" do seu sistema. Sem ele, qualquer mudança é chute.
"""

from rich.console import Console
from rich.markup import escape
from rich.table import Table

from assistente_ia.application.avaliacao import avaliar, carregar_golden, relatorio_markdown
from assistente_ia.config import PASTA_DADOS, PASTA_SAIDAS, descrever_ambiente
from assistente_ia.container import criar_observabilidade, criar_servico_rag

console = Console()
console.print(descrever_ambiente(), "\n")

casos = carregar_golden(PASTA_DADOS / "golden" / "padaria_golden.jsonl")
observabilidade = criar_observabilidade(silencioso=True)
rag = criar_servico_rag("padaria", observabilidade=observabilidade)

relatorio = avaliar("RAG padrão (k=3)", lambda pergunta: rag.perguntar(pergunta).resposta, casos)

tabela = Table(title=f"Golden dataset — acerto {relatorio.taxa_acerto:.0%}")
for coluna in ("id", "pergunta", "ok?", "resposta"):
    tabela.add_column(coluna)
for r in relatorio.resultados:
    tabela.add_row(r.caso.id, escape(r.caso.pergunta), "sim" if r.acertou else "NÃO", escape(r.resposta[:90]))
console.print(tabela)
console.print(f"Latência média: {relatorio.latencia_media:.2f}s | Custo: US$ {observabilidade.custo_total_usd():.5f}")

PASTA_SAIDAS.mkdir(exist_ok=True)
(PASTA_SAIDAS / "relatorio_golden.md").write_text(relatorio_markdown([relatorio]), encoding="utf-8")
console.print("Relatório salvo em saidas/relatorio_golden.md")
