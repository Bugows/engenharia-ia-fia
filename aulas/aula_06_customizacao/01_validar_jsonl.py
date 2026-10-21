"""Aula 6 — Exemplo 1: validar um dataset de conversa (JSONL) antes de usar.

Como rodar (custo zero):
    uv run python aulas/aula_06_customizacao/01_validar_jsonl.py
    uv run python aulas/aula_06_customizacao/01_validar_jsonl.py caminho/do/seu.jsonl

Regra de ouro da customização: dataset ruim = modelo ruim. Valide SEMPRE.
"""

import sys
from pathlib import Path

from assistente_ia.adapters.tokenizador import contar_tokens
from assistente_ia.config import PASTA_DADOS
from assistente_ia.domain.dataset import validar_linhas

arquivos = [Path(a) for a in sys.argv[1:]] or [
    PASTA_DADOS / "finetune" / "tom_vovo.jsonl",
    PASTA_DADOS / "finetune" / "tom_vovo_com_erros.jsonl",
]

for arquivo in arquivos:
    linhas = arquivo.read_text(encoding="utf-8").splitlines()
    relatorio = validar_linhas(linhas)
    total_tokens = sum(contar_tokens(linha) for linha in linhas)
    print(f"\n=== {arquivo.name} ===")
    print(f"exemplos: {relatorio.total} | válidos: {relatorio.validos} | tokens (aprox.): {total_tokens}")
    for erro in relatorio.erros:
        print(f"  ERRO  {erro}")
    for aviso in relatorio.avisos:
        print(f"  AVISO {aviso}")
    print("  Resultado:", "APROVADO" if relatorio.ok else "REPROVADO")
