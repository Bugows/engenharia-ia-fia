"""Aula 8 — Exemplo 6 (opcional): rastreamento (tracing) com LangSmith.

Como rodar:
    1) Crie uma conta gratuita em https://smith.langchain.com (plano Developer: 5.000 traces/mês).
    2) Gere uma API key e coloque no .env (ou Codespaces secret):
         LANGSMITH_TRACING=true
         LANGSMITH_API_KEY=lsv2_...
         LANGSMITH_PROJECT=fia-engenharia-ia
    3) uv run python aulas/aula_08_llmops/06_langsmith_opcional.py

Não precisa mudar NENHUMA linha do código: LangChain, LangGraph e deepagents enviam
os traces automaticamente quando as variáveis estão definidas.
Alternativa open source e auto-hospedável: Langfuse (https://langfuse.com).
"""

import os

from assistente_ia.config import descrever_ambiente
from assistente_ia.container import criar_agente_garcom

print(descrever_ambiente(), "\n")

if os.getenv("LANGSMITH_TRACING", "").lower() != "true" or not os.getenv("LANGSMITH_API_KEY"):
    print("LangSmith não configurado. Siga os passos do topo deste arquivo.")
    raise SystemExit(0)

agente = criar_agente_garcom()
print(agente.conversar("Quanto ficam 2 cafés com leite e 1 misto quente?", "trace-demo"))
print(f"\nAbra https://smith.langchain.com, projeto '{os.getenv('LANGSMITH_PROJECT', 'default')}', e veja cada passo do agente.")
