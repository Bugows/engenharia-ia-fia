# Aula 7 — Agentes de IA, Function Calling e Orquestração

> Um chatbot responde. Um agente **age**: decide, usa ferramentas, planeja e pede ajuda quando precisa.

## Objetivos
- Entender **function calling**: o modelo pede, o sistema executa.
- Criar um agente com **`create_agent`** (LangChain 1.x) e ferramentas do domínio.
- Desenhar um **workflow com LangGraph** (estado, nós, rotas condicionais, pausa humana).
- Usar **middleware**: aprovação humana, limite de chamadas e máscara de dados pessoais.
- Montar um **Deep Agent** (`deepagents`): planejamento, arquivos virtuais e subagentes.
- Conectar ferramentas via **MCP** (Model Context Protocol).

## Conceitos em 1 minuto
| Conceito | Em uma frase |
|---|---|
| Ferramenta (tool) | Função com nome, descrição e parâmetros tipados que o modelo pode pedir para executar |
| Agente | Loop: modelo decide → ferramenta executa → modelo lê o resultado → repete até responder |
| Workflow | Você desenha os passos; o modelo atua dentro de cada passo. Previsível e barato |
| Human-in-the-loop | O agente pausa antes de ações sensíveis e espera um humano aprovar |
| Deep agent | Agente para tarefas longas: planeja (todos), escreve arquivos e delega a subagentes |
| MCP | Padrão aberto para plugar ferramentas em qualquer agente compatível |

**Regra de ouro:** comece pelo workflow mais simples que resolve. Só suba para agente (e depois deep agent) quando os passos realmente não puderem ser previstos.

**Na arquitetura hexagonal:** as ferramentas são `FerramentaPort` (em `application/ferramentas.py`), as regras ficam no domínio (`domain/padaria.py`) e o adaptador `para_langchain` converte tudo para o LangChain.

## Passo a passo
```bash
uv run python aulas/aula_07_agentes/01_function_calling.py
uv run python aulas/aula_07_agentes/02_create_agent.py
uv run python aulas/aula_07_agentes/03_grafo_langgraph.py
uv run python aulas/aula_07_agentes/04_hitl_middleware.py
uv run python aulas/aula_07_agentes/05_deep_agent.py       # com chave: no máximo 3 execuções
uv run python aulas/aula_07_agentes/06_mcp_opcional.py
```
No modo fake, cada exemplo segue um **roteiro** (lista de `AIMessage`) que simula o modelo. Leia o roteiro: ele mostra exatamente o que o modelo real faria.

## Exercícios
| Arquivo | O que fazer |
|---|---|
| `exercicios/ex01_nova_ferramenta.py` | Criar a ferramenta `sugerir_acompanhamento` e usá-la no agente |
| `exercicios/ex02_rota_elogio.py` | Montar um grafo LangGraph do zero com a rota de elogios |

## Desafio criativo
`desafio.md`: **o Técnico Virtual da Várzea** (deep agent com subagentes).

## Cuidados de produção
- Sempre limite chamadas (`ModelCallLimitMiddleware`) e iterações.
- Ações irreversíveis (cobrar, enviar, apagar) **sempre** com aprovação humana.
- Resultados de ferramentas também podem conter injeção: trate como dados não confiáveis.
- No LangGraph, ao retomar após `interrupt`, o nó roda de novo desde o início: nada de efeitos colaterais antes da pausa.

## Checklist
- [ ] Sei explicar o ciclo do function calling.
- [ ] Sei quando usar workflow e quando usar agente.
- [ ] Implementei uma ferramenta nova que encaixa na porta.
- [ ] Montei um grafo com rota condicional.
- [ ] Rodei um deep agent e vi o plano e o arquivo gerado.
