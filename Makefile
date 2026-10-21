# Atalhos do curso. Sem "make"? Copie o comando da direita e rode no terminal.
.PHONY: ajuda instalar chave testar lint api notebook limpar aula1 aula2 aula3 aula4 aula5 aula6 aula7 aula8

ajuda:  ## lista os comandos
	@grep -E '^[a-z0-9]+:.*##' Makefile | awk -F':.*## ' '{printf "  make %-10s %s\n", $$1, $$2}'

instalar:  ## instala Python, dependências e proteções de commit
	uv sync
	uv run pre-commit install

chave:  ## verifica a chave SEM mostrá-la
	uv run python -m assistente_ia.config

testar:  ## roda os testes em modo fake (grátis)
	MODO=fake uv run pytest -m "not openai" -q

lint:  ## verifica o estilo do código
	uv run ruff check .

api:  ## sobe a API em http://localhost:8000/docs
	uv run uvicorn assistente_ia.api.main:app --reload

notebook:  ## abre o Jupyter
	uv run jupyter lab

limpar:  ## apaga arquivos gerados
	rm -rf saidas/* .pytest_cache .ruff_cache && touch saidas/.gitkeep

aula1:  ## exemplo principal da Aula 1
	uv run python aulas/aula_01_fundamentos/02_ola_hexagonal.py
aula2:
	uv run python aulas/aula_02_planejamento/01_calculadora_custos.py
aula3:
	uv run python aulas/aula_03_modelos/01_tokens.py
aula4:
	uv run python aulas/aula_04_avaliacao/01_rodar_golden.py
aula5:
	uv run python aulas/aula_05_prompts_rag/03_rag_padaria.py
aula6:
	uv run python aulas/aula_06_customizacao/01_validar_jsonl.py
aula7:
	uv run python aulas/aula_07_agentes/02_create_agent.py
aula8:
	uv run python aulas/aula_08_llmops/04_custos.py
