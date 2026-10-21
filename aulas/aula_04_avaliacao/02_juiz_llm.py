"""Aula 4 — Exemplo 2: LLM-as-a-Judge (um modelo avaliando outro).

Como rodar:
    uv run python aulas/aula_04_avaliacao/02_juiz_llm.py

Por que usar um juiz? Palavras-chave não captam respostas certas escritas de outro jeito.
Cuidados: o juiz também erra, tem preferência por respostas longas e, se for o mesmo
modelo avaliado, tende a ser "bonzinho" consigo mesmo (viés de autoavaliação).
"""

from assistente_ia.application.avaliacao import JuizLLM
from assistente_ia.config import descrever_ambiente
from assistente_ia.container import criar_llm

print(descrever_ambiente(), "\n")
juiz = JuizLLM(criar_llm())

referencia = "Aos sábados a padaria abre das 6h às 18h."
candidatas = {
    "correta": "No sábado abrimos às 6h e fechamos às 18h.",
    "incompleta": "Abrimos às 6h.",
    "errada": "No sábado abrimos às 8h e fechamos às 22h.",
    "inventada": "No sábado abrimos às 6h às 18h e temos música ao vivo com sorteio de bolo.",
}

for nome, resposta in candidatas.items():
    nota = juiz.avaliar("Que horas a padaria funciona no sábado?", referencia, resposta)
    print(f"[{nome:>10}] nota {nota.nota} — {nota.justificativa}")

print("\nO juiz concordou com a sua intuição? Em qual caso você daria outra nota?")
