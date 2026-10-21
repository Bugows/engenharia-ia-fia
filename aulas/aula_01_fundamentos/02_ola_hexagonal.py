"""Aula 1 — Exemplo 2: a mesma conversa, agora com arquitetura hexagonal.

Como rodar:
    uv run python aulas/aula_01_fundamentos/02_ola_hexagonal.py
    MODO=fake uv run python aulas/aula_01_fundamentos/02_ola_hexagonal.py

O que observar:
- O código abaixo NÃO importa OpenAI nem LangChain.
- Ele conversa com uma PORTA (LLMPort). O container decide qual adaptador encaixar.
- Rode com e sem MODO=fake: o código da aplicação não muda uma vírgula.
"""

from assistente_ia.config import descrever_ambiente
from assistente_ia.container import criar_llm
from assistente_ia.domain.modelos import sistema, usuario

print(descrever_ambiente(), "\n")

llm = criar_llm()  # a "tomada": OpenAILLM ou FakeLLM

resposta = llm.responder(
    [
        sistema("Você é o atendente simpático da Padaria Peter Pão. Responda em até 2 frases."),
        usuario("Bom dia! Tem pão de queijo saindo agora?"),
    ]
)

print(f"Atendente: {resposta.texto}")
print(f"Modelo: {resposta.modelo} | entrada={resposta.tokens_entrada} saída={resposta.tokens_saida} tokens")
