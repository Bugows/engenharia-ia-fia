"""Aula 4 — Exemplo 3: comparar configurações com dados, não com opinião.

Como rodar:
    uv run python aulas/aula_04_avaliacao/03_comparar_configs.py

Comparamos 3 variações do RAG no mesmo golden dataset:
  A) k=1 trecho   B) k=3 trechos   C) k=3 + prompt "seco" (sem regras de segurança)
"""

from assistente_ia.application.avaliacao import avaliar, carregar_golden, relatorio_markdown
from assistente_ia.application.rag import ServicoRAG
from assistente_ia.config import PASTA_DADOS, PASTA_SAIDAS, descrever_ambiente
from assistente_ia.container import carregar_base, criar_llm, criar_observabilidade

print(descrever_ambiente(), "\n")
casos = carregar_golden(PASTA_DADOS / "golden" / "padaria_golden.jsonl")
llm = criar_llm()
base = carregar_base("padaria")  # indexa uma vez e reaproveita

PROMPT_SECO = "Responda a pergunta usando os documentos."

configuracoes = {
    "A) k=1": ServicoRAG(llm, base, k=1),
    "B) k=3": ServicoRAG(llm, base, k=3),
    "C) k=3 prompt seco": ServicoRAG(llm, base, k=3, prompt_sistema=PROMPT_SECO),
}

relatorios = []
for nome, servico in configuracoes.items():
    observabilidade = criar_observabilidade(silencioso=True)
    servico.observabilidade = observabilidade
    relatorio = avaliar(nome, lambda p, s=servico: s.perguntar(p).resposta, casos)
    relatorios.append(relatorio)
    print(f"{nome:<22} acerto {relatorio.taxa_acerto:>4.0%} | latência {relatorio.latencia_media:.2f}s "
          f"| custo US$ {observabilidade.custo_total_usd():.5f}")

PASTA_SAIDAS.mkdir(exist_ok=True)
(PASTA_SAIDAS / "relatorio_aula4.md").write_text(relatorio_markdown(relatorios), encoding="utf-8")
print("\nRelatório comparativo em saidas/relatorio_aula4.md")
print("Pergunta: qual configuração você colocaria em produção? Justifique com os números.")
