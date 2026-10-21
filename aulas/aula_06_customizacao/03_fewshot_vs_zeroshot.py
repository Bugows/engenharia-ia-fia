"""Aula 6 — Exemplo 3: customizar SEM treinar — few-shot vs zero-shot.

Como rodar:
    uv run python aulas/aula_06_customizacao/03_fewshot_vs_zeroshot.py

Antes de pensar em fine-tuning, teste few-shot: colocar exemplos do comportamento
desejado dentro do prompt. Muitas vezes resolve, e muda em segundos.
Custo: os exemplos vão em TODA chamada (mais tokens de entrada — mas o cache ajuda).
"""

import json

from pydantic import BaseModel, Field

from assistente_ia.config import PASTA_DADOS, descrever_ambiente
from assistente_ia.container import criar_llm
from assistente_ia.domain.custos import custo_usd
from assistente_ia.domain.modelos import Mensagem, sistema, usuario

print(descrever_ambiente(), "\n")
llm = criar_llm()

exemplos = [json.loads(linha) for linha in (PASTA_DADOS / "finetune" / "tom_vovo.jsonl").read_text(encoding="utf-8").splitlines()]
persona = exemplos[0]["messages"][0]["content"]

# Few-shot: 4 pares (user, assistant) do dataset viram "conversa de exemplo"
few_shot: list[Mensagem] = []
for exemplo in exemplos[:4]:
    for m in exemplo["messages"][1:]:
        few_shot.append(Mensagem(m["role"], m["content"]))


class NotaTom(BaseModel):
    nota: int = Field(ge=1, le=5, description="1 = nada a ver com a Vovó; 5 = é a Vovó Lurdes falando")
    motivo: str


def avaliar_tom(resposta: str) -> NotaTom:
    return llm.responder_estruturado(
        [sistema(f"Avalie o quanto a resposta soa como esta persona: {persona}"), usuario(resposta)], NotaTom
    )


perguntas = ["Tem bolo de rolo hoje?", "O pão de queijo está caro, hein?", "Vocês abrem no feriado?"]
totais = {"zero-shot": [0, 0.0], "few-shot": [0, 0.0]}

for pergunta in perguntas:
    print(f"\nPergunta: {pergunta}")
    for nome, mensagens in [
        ("zero-shot", [sistema(persona), usuario(pergunta)]),
        ("few-shot", [sistema(persona), *few_shot, usuario(pergunta)]),
    ]:
        resposta = llm.responder(mensagens)
        nota = avaliar_tom(resposta.texto)
        custo = custo_usd(resposta.modelo, resposta.tokens_entrada, resposta.tokens_saida)
        totais[nome][0] += nota.nota
        totais[nome][1] += custo
        print(f"  [{nome:>9}] nota {nota.nota} | entrada {resposta.tokens_entrada:>4} tok | {resposta.texto[:90]}")

print("\nResumo:")
for nome, (soma_notas, custo) in totais.items():
    print(f"  {nome:>9}: nota média {soma_notas / len(perguntas):.1f} | custo US$ {custo:.5f}")
print("\nQuando valeria a pena treinar (fine-tuning) em vez de few-shot? Discuta: volume, latência, privacidade, estabilidade.")
