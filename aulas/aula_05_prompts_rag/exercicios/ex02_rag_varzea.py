"""Aula 5 — Exercício 2: um RAG para o regulamento da Copa da Várzea.

Reaproveite as peças da arquitetura: repositório de arquivos, vector store e ServicoRAG.
Só o PROMPT e a PASTA mudam. É o poder de ter portas e adaptadores!

Rodar e verificar:
    uv run python aulas/aula_05_prompts_rag/exercicios/ex02_rag_varzea.py
"""

from assistente_ia.application.rag import ServicoRAG
from assistente_ia.exercicios import verificar

PROMPT_VARZEA = """TODO: escreva o prompt do "Juiz Virtual da Copa da Várzea".
Ele deve: responder só com base nos documentos, citar a fonte entre colchetes,
admitir quando não sabe e ignorar ordens escritas dentro dos documentos."""


def criar_rag_varzea() -> ServicoRAG:
    """Monte o ServicoRAG com a base 'futebol' e o PROMPT_VARZEA."""
    # TODO: use carregar_base("futebol") e criar_llm()
    raise NotImplementedError("return ServicoRAG(criar_llm(), carregar_base('futebol'), prompt_sistema=PROMPT_VARZEA)")


def checar_prompt():
    if "TODO" in PROMPT_VARZEA:
        raise NotImplementedError("Escreva o PROMPT_VARZEA (sem a palavra TODO).")
    texto = PROMPT_VARZEA.lower()
    assert "fonte" in texto, "O prompt deve pedir para citar a fonte."
    assert "documento" in texto, "O prompt deve falar dos documentos."


def checar_rag():
    rag = criar_rag_varzea()
    resposta = rag.perguntar("Quantos jogadores cada time pode inscrever?")
    assert "regulamento_varzea.md" in resposta.fontes, f"Fontes: {resposta.fontes}"
    assert rag.prompt_sistema == PROMPT_VARZEA


if __name__ == "__main__":
    if verificar("Aula 5 — Exercício 2", checar_prompt, checar_rag):
        rag = criar_rag_varzea()
        for pergunta in ["Cartão vermelho suspende por quantos jogos?", "Qual o prêmio do artilheiro?"]:
            print(f"{pergunta}\n  -> {rag.perguntar(pergunta).resposta}")
