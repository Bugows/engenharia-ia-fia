"""Aula 6 — Exercício 1: conserte o dataset.

O arquivo dados/finetune/tom_vovo_com_erros.jsonl tem 7 linhas e vários problemas.
Escreva a função `corrigir` para transformar a lista de exemplos abaixo (já carregada
como dicionários) em uma lista válida.

Rodar e verificar (custo zero):
    uv run python aulas/aula_06_customizacao/exercicios/ex01_corrigir_dataset.py
"""

import json

from assistente_ia.config import PASTA_DADOS
from assistente_ia.domain.dataset import validar_linhas
from assistente_ia.domain.seguranca import mascarar_dados_pessoais
from assistente_ia.exercicios import verificar


def carregar_exemplos() -> list[dict]:
    """Carrega as linhas que são JSON válido (as quebradas são descartadas)."""
    exemplos = []
    for linha in (PASTA_DADOS / "finetune" / "tom_vovo_com_erros.jsonl").read_text(encoding="utf-8").splitlines():
        try:
            exemplos.append(json.loads(linha))
        except json.JSONDecodeError:
            continue
    return exemplos


def corrigir(exemplos: list[dict]) -> list[dict]:
    """Devolva uma nova lista em que:
    1. papéis inválidos (ex.: 'cliente') viram 'user';
    2. exemplos com alguma mensagem vazia são descartados;
    3. dados pessoais são mascarados (use mascarar_dados_pessoais);
    4. exemplos cuja ÚLTIMA mensagem não é 'assistant' são descartados;
    5. duplicatas são removidas (mantenha a primeira).
    """
    # TODO
    raise NotImplementedError("Percorra os exemplos aplicando as 5 regras.")


def checar():
    corrigidos = corrigir(carregar_exemplos())
    linhas = [json.dumps(e, ensure_ascii=False) for e in corrigidos]
    relatorio = validar_linhas(linhas)
    assert relatorio.ok, " | ".join(relatorio.erros)
    assert len(corrigidos) == 3, f"Esperava 3 exemplos válidos depois da limpeza, ficaram {len(corrigidos)}."


if __name__ == "__main__":
    verificar("Aula 6 — Exercício 1", checar)
    _ = mascarar_dados_pessoais  # use na sua solução
