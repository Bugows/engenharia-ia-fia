"""Aula 5 — Exemplo 1: prompts como templates (e não como strings soltas).

Como rodar:
    uv run python aulas/aula_05_prompts_rag/01_templates.py

Boas práticas de prompt que este exemplo mostra:
- papel claro no "system"; formato de saída explícito; exemplos (few-shot); delimitadores.
"""

from langchain_core.prompts import ChatPromptTemplate

from assistente_ia.config import descrever_ambiente
from assistente_ia.container import criar_chat_model

print(descrever_ambiente(), "\n")

template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Você escreve mensagens de WhatsApp para a Padaria Peter Pão.\n"
            "Regras: no máximo 2 frases; tom {tom}; termine com uma pergunta ao cliente.\n"
            "Exemplo de mensagem boa: 'Oi, Rita! Seu bolo de rolo fica pronto às 15h. Quer que a gente separe um café também?'",
        ),
        ("user", "Cliente: {nome_cliente}\nSituação: <situacao>{situacao}</situacao>"),
    ]
)

# 1) Ver o prompt montado ANTES de gastar tokens (ótimo para depurar)
mensagens = template.format_messages(nome_cliente="Seu Jorge", tom="caloroso", situacao="encomenda de 20 coxinhas pronta")
for m in mensagens:
    print(f"--- {m.type} ---\n{m.content}\n")

# 2) Encadear template + modelo com o operador | (LCEL)
cadeia = template | criar_chat_model(max_tokens=150)
for tom in ("caloroso", "formal", "divertido"):
    resposta = cadeia.invoke({"nome_cliente": "Seu Jorge", "tom": tom, "situacao": "encomenda de 20 coxinhas pronta"})
    print(f"[{tom}] {resposta.content}")
