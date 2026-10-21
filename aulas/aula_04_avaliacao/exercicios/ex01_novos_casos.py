"""Aula 4 — Exercício 1: aumente o golden dataset.

Um bom golden dataset cobre: casos fáceis, casos difíceis, casos fora do escopo
e tentativas de ataque. Crie 4 casos novos, um de cada tipo.

Rodar e verificar (custo zero):
    uv run python aulas/aula_04_avaliacao/exercicios/ex01_novos_casos.py
"""

from assistente_ia.application.avaliacao import CasoDeTeste
from assistente_ia.exercicios import verificar

NOVOS_CASOS: list[CasoDeTeste] = [
    # Exemplo de formato:
    # CasoDeTeste(id="n01", pergunta="...", palavras_chave=["..."], deve_recusar=False, fonte="faq.md"),
    #
    # TODO 1: caso fácil (resposta direta no cardápio ou FAQ)
    # TODO 2: caso difícil (precisa combinar 2 informações, ex.: horário de domingo + entrega)
    # TODO 3: caso fora do escopo (algo que NÃO está nos documentos; a resposta certa é "não tenho essa informação")
    # TODO 4: ataque (prompt injection) — use deve_recusar=True
]


def checar_quantidade():
    if not NOVOS_CASOS:
        raise NotImplementedError("Adicione os 4 casos na lista NOVOS_CASOS.")
    assert len(NOVOS_CASOS) >= 4, f"Crie pelo menos 4 casos (você tem {len(NOVOS_CASOS)})."


def checar_qualidade():
    ids = [c.id for c in NOVOS_CASOS]
    assert len(ids) == len(set(ids)), "Os ids precisam ser únicos."
    assert any(c.deve_recusar for c in NOVOS_CASOS), "Inclua pelo menos 1 ataque (deve_recusar=True)."
    for caso in NOVOS_CASOS:
        assert caso.pergunta.strip(), f"{caso.id}: pergunta vazia."
        if not caso.deve_recusar:
            assert caso.palavras_chave, f"{caso.id}: casos normais precisam de palavras-chave."
    fora = [c for c in NOVOS_CASOS if any("informa" in p.lower() for p in c.palavras_chave)]
    assert fora, "Inclua um caso fora do escopo cuja palavra-chave seja 'informação'."


if __name__ == "__main__":
    if verificar("Aula 4 — Exercício 1", checar_quantidade, checar_qualidade):
        import json

        print("Linhas para colar em dados/golden/padaria_golden.jsonl:")
        for c in NOVOS_CASOS:
            print(json.dumps(c.__dict__, ensure_ascii=False))
