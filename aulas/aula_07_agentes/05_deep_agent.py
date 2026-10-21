"""Aula 7 — Exemplo 5: Deep Agent (biblioteca deepagents) — o analista da padaria.

Como rodar (com chave: algumas dezenas de chamadas; rode no máximo 3 vezes):
    uv run python aulas/aula_07_agentes/05_deep_agent.py

Um deep agent é um agente com "equipamento extra" para tarefas longas:
  - write_todos: planeja e acompanha uma lista de tarefas;
  - sistema de arquivos VIRTUAL: ls, read_file, write_file, edit_file (fica no estado, não no disco);
  - task: delega partes do trabalho a SUBAGENTES especializados, com contexto limpo.
"""

from langchain_core.messages import AIMessage

from assistente_ia.application.deep_agent import arquivos_gerados, criar_deep_agent_padaria
from assistente_ia.application.ferramentas import ferramentas_padaria
from assistente_ia.config import PASTA_SAIDAS, descrever_ambiente
from assistente_ia.container import criar_chat_model

print(descrever_ambiente(), "\n")

relatorio_fake = "# Combos da semana\n\n| Combo | Preço cheio | Com 10% |\n|---|---|---|\n| Café + pão de queijo | R$ 8,50 | R$ 7,65 |\n"
roteiro = [  # usado só no modo fake
    AIMessage(content="", tool_calls=[{"name": "write_todos", "args": {"todos": [
        {"content": "Consultar preços do café e do pão de queijo", "status": "in_progress"},
        {"content": "Calcular combo com 10% de desconto", "status": "pending"},
        {"content": "Salvar /relatorio.md", "status": "pending"},
    ]}, "id": "t1"}]),
    AIMessage(content="", tool_calls=[{"name": "calcular_total", "args": {"itens": {"café": 1, "pão de queijo": 1}}, "id": "t2"}]),
    AIMessage(content="", tool_calls=[{"name": "write_file", "args": {"file_path": "/relatorio.md", "content": relatorio_fake}, "id": "t3"}]),
    AIMessage(content="Relatório pronto em /relatorio.md: o combo café + pão de queijo sai por R$ 7,65 com 10% de desconto."),
]

agente = criar_deep_agent_padaria(criar_chat_model(roteiro, reasoning_effort="low", max_tokens=1500), ferramentas_padaria())

tarefa = (
    "Monte uma proposta de 3 combos de café da manhã para a semana. Para cada combo, calcule o preço cheio "
    "e o preço com 10% de desconto usando as ferramentas. Salve uma tabela em /relatorio.md."
)
resultado = agente.invoke({"messages": [{"role": "user", "content": tarefa}]})

print("Plano (todos):")
for item in resultado.get("todos", []):
    print(f"  [{item['status']:>11}] {item['content']}")

arquivos = arquivos_gerados(resultado)
print(f"\nArquivos virtuais: {list(arquivos)}")
if "/relatorio.md" in arquivos:
    PASTA_SAIDAS.mkdir(exist_ok=True)
    (PASTA_SAIDAS / "aula07_relatorio.md").write_text(arquivos["/relatorio.md"], encoding="utf-8")
    print("Cópia salva em saidas/aula07_relatorio.md\n")
    print(arquivos["/relatorio.md"])

print(f"\nResumo do agente: {resultado['messages'][-1].content}")
print(f"Total de mensagens trocadas: {len(resultado['messages'])} (cada uma pode custar tokens!)")
