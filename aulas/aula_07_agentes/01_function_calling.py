"""Aula 7 — Exemplo 1: function calling "na unha" (sem framework de agente).

Como rodar:
    uv run python aulas/aula_07_agentes/01_function_calling.py

O ciclo que todo agente repete:
  1) o modelo recebe a pergunta + a LISTA de ferramentas (nome, descrição, parâmetros);
  2) ele decide chamar uma ferramenta e devolve um "tool_call" (nome + argumentos);
  3) NÓS executamos a ferramenta e devolvemos o resultado (ToolMessage);
  4) o modelo escreve a resposta final.
O modelo NUNCA executa nada sozinho: ele só pede.
"""

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage

from assistente_ia.adapters.ferramentas.langchain_tools import para_langchain_lista
from assistente_ia.application.ferramentas import CalcularTotal, ConsultarPreco
from assistente_ia.config import descrever_ambiente
from assistente_ia.container import criar_chat_model

print(descrever_ambiente(), "\n")

ferramentas = {t.name: t for t in para_langchain_lista([ConsultarPreco(), CalcularTotal()])}

# Roteiro usado só no modo fake (simula o que o modelo real faria)
roteiro = [
    AIMessage(content="", tool_calls=[{"name": "calcular_total", "args": {"itens": {"café": 2, "sonho": 1}}, "id": "chamada_1"}]),
    AIMessage(content="Dois cafés e um sonho ficam R$ 14,00."),
]
modelo = criar_chat_model(roteiro, max_tokens=300).bind_tools(list(ferramentas.values()))

print("Esquema que o modelo recebe para a ferramenta 'calcular_total':")
print(ferramentas["calcular_total"].args, "\n")

conversa = [
    SystemMessage("Você é o caixa da Padaria Peter Pão. Use as ferramentas para valores."),
    HumanMessage("Quanto fica 2 cafés e 1 sonho?"),
]

for passo in range(1, 5):  # limite de segurança: nunca deixe um loop sem teto
    resposta = modelo.invoke(conversa)
    conversa.append(resposta)
    if not resposta.tool_calls:
        print(f"Passo {passo} - resposta final: {resposta.content}")
        break
    for chamada in resposta.tool_calls:
        print(f"Passo {passo} - o modelo pediu: {chamada['name']}({chamada['args']})")
        resultado = ferramentas[chamada["name"]].invoke(chamada["args"])
        print(f"          nós executamos e devolvemos: {resultado}")
        conversa.append(ToolMessage(content=resultado, tool_call_id=chamada["id"]))
