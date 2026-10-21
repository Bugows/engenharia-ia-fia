"""Aula 6 — Exemplo 2: gerar dados sintéticos com o próprio modelo (e revisar como humano!).

Como rodar:
    uv run python aulas/aula_06_customizacao/02_dados_sinteticos.py

Gera saidas/sinteticos_para_revisao.csv com uma coluna "aprovado" vazia.
Abra o CSV, marque "sim" nos exemplos bons e depois rode:
    uv run python aulas/aula_06_customizacao/02_dados_sinteticos.py --converter
para transformar os aprovados em JSONL validado.
"""

import csv
import json
import sys

from pydantic import BaseModel, Field

from assistente_ia.config import PASTA_SAIDAS, descrever_ambiente
from assistente_ia.container import criar_llm, modo_fake
from assistente_ia.domain.dataset import validar_linhas
from assistente_ia.domain.modelos import sistema, usuario

PERSONA = (
    "Você é a Vovó Lurdes, fundadora da Padaria Peter Pão. Fale com carinho, use 'meu bem' e conte "
    "pequenas lembranças de Recife, sem perder a informação correta."
)
CSV = PASTA_SAIDAS / "sinteticos_para_revisao.csv"
JSONL = PASTA_SAIDAS / "sinteticos_aprovados.jsonl"


class Exemplo(BaseModel):
    pergunta: str = Field(description="Pergunta curta e realista de um cliente de padaria")
    resposta: str = Field(description="Resposta no tom da Vovó Lurdes, com no máximo 3 frases")


class Lote(BaseModel):
    exemplos: list[Exemplo]


def gerar(quantidade: int = 8) -> list[Exemplo]:
    lote = criar_llm().responder_estruturado(
        [
            sistema(
                f"Gere {quantidade} exemplos variados de conversa para treinar um atendente. Persona: {PERSONA} "
                "Varie os temas: preço, horário, encomenda, alergia, entrega, reclamação. "
                "Preço do pão de queijo R$ 4,50; café R$ 4,00; sonho R$ 6,00; bolo de rolo R$ 9,00."
            ),
            usuario("Gere os exemplos."),
        ],
        Lote,
    )
    if not lote.exemplos and modo_fake():
        return [Exemplo(pergunta=f"[fake] pergunta {i}", resposta=f"[fake] resposta, meu bem {i}") for i in range(3)]
    return lote.exemplos


def salvar_csv(exemplos: list[Exemplo]) -> None:
    PASTA_SAIDAS.mkdir(exist_ok=True)
    with CSV.open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["pergunta", "resposta", "aprovado"])
        for e in exemplos:
            escritor.writerow([e.pergunta, e.resposta, ""])


def converter_aprovados() -> None:
    linhas = []
    with CSV.open(encoding="utf-8") as arquivo:
        for linha in csv.DictReader(arquivo):
            if linha["aprovado"].strip().lower() == "sim":
                exemplo = {"messages": [
                    {"role": "system", "content": PERSONA},
                    {"role": "user", "content": linha["pergunta"]},
                    {"role": "assistant", "content": linha["resposta"]},
                ]}
                linhas.append(json.dumps(exemplo, ensure_ascii=False))
    relatorio = validar_linhas(linhas)
    JSONL.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(f"{relatorio.validos} exemplos aprovados e válidos salvos em {JSONL}")
    for erro in relatorio.erros:
        print("  ERRO", erro)


if __name__ == "__main__":
    print(descrever_ambiente(), "\n")
    if "--converter" in sys.argv:
        converter_aprovados()
    else:
        exemplos = gerar()
        salvar_csv(exemplos)
        for e in exemplos:
            print(f"- {e.pergunta}\n  {e.resposta}")
        print(f"\n{len(exemplos)} exemplos em {CSV}. Revise e marque 'sim' na coluna 'aprovado'.")
        print("Atenção: dado sintético herda os erros do modelo que o gerou. A revisão humana NÃO é opcional.")
