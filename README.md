# Engenharia de Inteligência Artificial — FIA

Repositório-base do curso de extensão **Engenharia de Inteligência Artificial** (FIA).
Em 8 aulas, você constrói, peça por peça, um **assistente corporativo** para a fictícia
**Padaria Peter Pão S.A.**, usando Python, LangChain, LangGraph, Deep Agents e arquitetura hexagonal.

Tudo funciona **sem chave** (modo fake, custo zero). Com uma chave da OpenAI, o mesmo código
passa a usar o `gpt-5.4-mini` e o `text-embedding-3-small`, sem mudar uma linha da aplicação.

---

## Mapa do curso

| Aula | Tema | Você vai construir | Pasta |
|---|---|---|---|
| 1 | Fundamentos e Arquitetura | Primeira chamada ao LLM e o primeiro adaptador | `aulas/aula_01_fundamentos` |
| 2 | Planejamento Estratégico | AI Canvas, calculadora de custo, ROI e TCO | `aulas/aula_02_planejamento` |
| 3 | Modelos de Fundação | Tokens, embeddings (aipim x mandioca x macaxeira), raciocínio | `aulas/aula_03_modelos` |
| 4 | Avaliação e Comparação | Golden dataset, juiz LLM, comparação de configurações | `aulas/aula_04_avaliacao` |
| 5 | Prompts e RAG | Atendente que responde citando o cardápio; defesa contra injeção | `aulas/aula_05_prompts_rag` |
| 6 | Customização e Fine-Tuning | Dataset "tom da Vovó", dados sintéticos, few-shot x zero-shot | `aulas/aula_06_customizacao` |
| 7 | Agentes e Orquestração | Garçom com ferramentas, LangGraph, aprovação humana, deep agent, MCP | `aulas/aula_07_agentes` |
| 8 | Otimização e LLMOps | Streaming, cache, fallback, custos, guardrails, API, Docker, CI | `aulas/aula_08_llmops` |
| Final | Projeto integrador | Assistente corporativo completo para um caso real | `projeto_final` |

Cada aula tem: `README.md` (roteiro), exemplos numerados (`01_...py`), `explorando.ipynb`,
`exercicios/` (com verificação automática) e `desafio.md` (desafio criativo).

---

## Como começar (passo a passo)

### 1. Faça o fork
Clique em **Fork** no canto superior direito desta página.

> Atenção: seu fork é **público**. Nunca coloque chaves em arquivos do repositório.

### 2. Abra o ambiente

**Opção A — GitHub Codespaces (recomendado, nada para instalar)**
1. No **seu fork**: botão verde **Code** → aba **Codespaces** → **Create codespace on main**.
2. Aguarde a instalação automática (2 a 4 minutos na primeira vez).
3. Ao terminar a aula, **pare o codespace** (github.com/codespaces → `...` → Stop).
   O plano gratuito tem 120 horas-núcleo por mês (cerca de 60 horas numa máquina de 2 núcleos).

**Opção B — No seu computador**
```bash
# 1. Instale o uv: https://docs.astral.sh/uv/getting-started/installation/
# 2. Clone o SEU fork
git clone https://github.com/SEU_USUARIO/engenharia-ia-fia.git
cd engenharia-ia-fia
# 3. Instale tudo (o uv baixa o Python certo sozinho)
make instalar            # sem make: uv sync && uv run pre-commit install
```
Prefere pip? `python -m venv .venv`, ative o ambiente e rode `pip install -r requirements.txt`
(requer Python 3.11 a 3.14; os comandos `uv run ...` viram `python ...`).

### 3. Configure a sua chave (do jeito seguro)
O professor envia uma **chave individual** por canal privado. Detalhes em
[`docs/00-configurando-a-chave.md`](docs/00-configurando-a-chave.md).

- **Codespaces:** github.com/settings/codespaces → **New secret** → nome `OPENAI_API_KEY`,
  valor = sua chave, repositório = o **seu fork** → reinicie o codespace.
- **Local:** `cp .env.example .env` e cole a chave na linha `OPENAI_API_KEY=`.

Confira (a chave nunca é exibida):
```bash
make chave               # sem make: uv run python -m assistente_ia.config
```

Sem chave? Tudo continua funcionando em **modo fake**:
```bash
MODO=fake uv run python aulas/aula_01_fundamentos/02_ola_hexagonal.py
```

### 4. Rode
```bash
make testar              # testes automatizados, grátis
make aula1               # exemplo principal da Aula 1
make ajuda               # todos os atalhos
```
Para rodar qualquer exemplo: `uv run python aulas/<pasta-da-aula>/<arquivo>.py`.
Notebooks: abra `explorando.ipynb` no VS Code/Codespaces e escolha o kernel `.venv`.

### 5. Receba as aulas novas
O professor publica o conteúdo aula a aula. Para trazer as novidades para o seu fork:
- No GitHub: botão **Sync fork** na página do seu fork; ou
- No terminal (uma vez): `git remote add upstream https://github.com/sergiogaiotto/engenharia-ia-fia.git`
  e depois, sempre que precisar: `git fetch upstream --tags && git merge upstream/main`.

Mais detalhes em [`docs/03-git-do-curso.md`](docs/03-git-do-curso.md).

---

## Arquitetura em uma imagem

```
                        ┌──────────────────────────────┐
   aulas/, api/,  ───>  │   application/  (casos de uso)│  chat, RAG, avaliação,
   projeto_final/       │   rag.py  agente.py  ...      │  grafo, agente, deep agent
                        └──────────────┬───────────────┘
                                       │ usa somente PORTAS
                        ┌──────────────▼───────────────┐
                        │   ports/  (contratos)         │  LLMPort, EmbeddingsPort,
                        │                               │  VectorStorePort, FerramentaPort...
                        └──────────────┬───────────────┘
                     ┌─────────────────┼─────────────────┐
             ┌───────▼──────┐  ┌───────▼──────┐  ┌───────▼──────┐
             │ OpenAI       │  │ Fake         │  │ Memória,     │   adapters/
             │ (LangChain)  │  │ (custo zero) │  │ arquivos...  │
             └──────────────┘  └──────────────┘  └──────────────┘
                        domain/  = regras da padaria em Python puro
                        container.py = decide qual adaptador ligar em cada porta
```
Explicação completa: [`docs/01-arquitetura-hexagonal.md`](docs/01-arquitetura-hexagonal.md).

---

## Estrutura de pastas

```
.
├── aulas/                    # uma pasta por aula (roteiro, exemplos, exercícios, desafio)
├── projeto_final/            # requisitos, rubrica e ponto de partida do projeto integrador
├── src/assistente_ia/        # o "produto": código reutilizado por todas as aulas
│   ├── domain/               # regras de negócio (padaria, custos, chunking, segurança, datasets)
│   ├── ports/                # contratos (Protocols)
│   ├── adapters/             # OpenAI, fake, banco vetorial em memória, arquivos, tools, observabilidade
│   ├── application/          # chat, RAG, avaliação, grafo LangGraph, agente, deep agent, ferramentas
│   ├── api/                  # API FastAPI
│   ├── config.py             # configurações (a chave fica oculta)
│   └── container.py          # liga os adaptadores às portas
├── dados/                    # base de conhecimento da padaria, várzea, golden dataset, datasets de ajuste
├── tests/                    # testes (rodam sem chave)
├── docs/                     # guias: chave, arquitetura, custos, git, professor
├── saidas/                   # arquivos gerados pelos exemplos (não versionados)
└── .devcontainer/ .github/   # Codespaces e CI
```

---

## Custos e regras de ouro

- Modelo padrão: `gpt-5.4-mini` (US$ 0,75 por milhão de tokens de entrada e US$ 4,50 de saída, out/2026).
- Padrões econômicos: `ESFORCO_RACIOCINIO=none` e `MAX_TOKENS_SAIDA=800`.
- Cada sessão de terminal para sozinha ao passar de **US$ 0,50** (configurável no `.env`).
- Teste primeiro em modo fake; use a chave quando o código estiver pronto.
- O curso inteiro custa, em média, **menos de US$ 15 por aluno**. Detalhes em [`docs/02-custos-e-orcamento.md`](docs/02-custos-e-orcamento.md).

### Segurança da chave
- **Nunca** cole a chave em código, notebook, issue, print, slide ou grupo da turma.
- O `pre-commit` bloqueia commits que contenham chave (`sk-...`); o `.gitignore` ignora o `.env`.
- Vazou? Avise o professor imediatamente para revogar e gerar outra.

---

## Stack

| Peça | Para quê |
|---|---|
| [uv](https://docs.astral.sh/uv/) | Instala Python e dependências com versões travadas (`uv.lock`) |
| [LangChain 1.x](https://docs.langchain.com/oss/python/langchain/overview) | Modelos, prompts, ferramentas, `create_agent`, middleware |
| [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview) | Fluxos com estado, rotas condicionais e pausa para aprovação humana |
| [Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview) | Agentes com planejamento, arquivos virtuais e subagentes |
| [langchain-mcp-adapters](https://github.com/langchain-ai/langchain-mcp-adapters) | Ferramentas via Model Context Protocol |
| [FastAPI](https://fastapi.tiangolo.com/) | API HTTP do assistente |
| OpenAI `gpt-5.4-mini` e `text-embedding-3-small` | Modelo de chat e embeddings |

---

## Problemas comuns

| Sintoma | Solução |
|---|---|
| `Não encontrei sua OPENAI_API_KEY` | Veja `docs/00-configurando-a-chave.md` ou rode com `MODO=fake` |
| Criei o secret mas o Codespace não vê | Reinicie o codespace (Command Palette → *Codespaces: Rebuild Container*) |
| `Error code: 429 ... project_spend_limit_exceeded` | O orçamento da turma acabou: avise o professor |
| `Error code: 401` | Chave errada ou revogada |
| Aviso sobre "tokenizador o200k_base" | Sem internet para baixar o tokenizador; o curso usa uma estimativa |
| `make: command not found` (Windows) | Rode o comando equivalente indicado no `Makefile` |
| Notebook não acha `assistente_ia` | Selecione o kernel `.venv` no canto superior direito |

Dúvidas sobre como contribuir: [`CONTRIBUTING.md`](CONTRIBUTING.md). Professor: [`docs/guia-do-professor.md`](docs/guia-do-professor.md).

---

Licença MIT. Conteúdo didático do curso de extensão Engenharia de Inteligência Artificial — FIA.
