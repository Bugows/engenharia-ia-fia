# Aula 8 — Controle, Otimização da Geração e LLMOps

> Fazer funcionar é a metade. A outra metade é funcionar **todo dia**, com custo previsível e sem surpresas.

## Objetivos
- Controlar a geração: `max_tokens`, `reasoning_effort`, `verbosity`, `temperature`, streaming.
- Otimizar: **cache**, **rate limit**, **retry** e **fallback**.
- Observar: tokens, custo, latência e **orçamento por sessão**; tracing com LangSmith (opcional).
- Proteger: **guardrails** de entrada (PII, injeção), processo (limite de chamadas) e saída (preço inventado).
- Publicar: **API FastAPI**, **Docker** e **CI** no GitHub Actions rodando em modo fake.

## Conceitos em 1 minuto
| Tema | O que é | Onde está no projeto |
|---|---|---|
| TTFT | Tempo até a primeira palavra | `02_streaming.py` |
| Cache | Mesma entrada, resposta guardada, custo zero | `03_cache_retry_rate.py` |
| Rate limit | Teto de chamadas por segundo | `03_cache_retry_rate.py` |
| Fallback | Plano B automático quando o provedor falha | `03_cache_retry_rate.py`, exercício 2 |
| Observabilidade | Medir uso, custo e qualidade em produção | `adapters/observabilidade/console.py` |
| Guardrails | Regras antes, durante e depois do modelo | `05_guardrails.py`, `application/agente.py` |
| LLMOps | Ciclo: medir → avaliar → ajustar → publicar → monitorar | Aulas 4 + 8 + CI |

## Passo a passo
```bash
uv run python aulas/aula_08_llmops/01_geracao.py          # precisa de chave
uv run python aulas/aula_08_llmops/02_streaming.py
uv run python aulas/aula_08_llmops/03_cache_retry_rate.py
uv run python aulas/aula_08_llmops/04_custos.py
uv run python aulas/aula_08_llmops/05_guardrails.py
uv run python aulas/aula_08_llmops/06_langsmith_opcional.py   # opcional
```

### A API do assistente
```bash
make api        # ou: uv run uvicorn assistente_ia.api.main:app --reload
```
Abra `http://localhost:8000/docs` (no Codespaces, use a aba **Ports**, porta 8000) e teste:
- `GET /saude` — modo atual (fake/openai);
- `POST /perguntar` — RAG com fontes: `{"texto": "Aceitam pix?"}`;
- `POST /conversar` — agente garçom: `{"texto": "Quero 50 coxinhas para 20/12", "sessao": "ana"}`;
- `POST /aprovar` — aprova a encomenda pendente: `{"sessao": "ana", "aprovar": true}`;
- `GET /custos` — tokens e custo acumulados.

### Docker
```bash
docker build -t assistente-ia .
docker run -p 8000:8000 assistente-ia                                   # modo fake
docker run -p 8000:8000 -e OPENAI_API_KEY="$OPENAI_API_KEY" assistente-ia   # modo real
```

### CI
`.github/workflows/ci.yml` roda lint e testes em **modo fake** a cada push: verde sem gastar um centavo.
`.github/workflows/evals.yml` (manual) roda o golden dataset com a SUA chave, se você cadastrar o secret no seu fork.

## Exercícios
| Arquivo | O que fazer |
|---|---|
| `exercicios/ex01_endpoint_cardapio.py` | Publicar o cardápio em dois endpoints FastAPI |
| `exercicios/ex02_fallback.py` | Criar um adaptador decorator com fallback |

## Desafio criativo
`desafio.md`: **plantão de sexta-feira**.

## Checklist
- [ ] Sei quais parâmetros reduzem custo e latência.
- [ ] Sei explicar cache, rate limit, retry e fallback.
- [ ] Vi o orçamento por sessão interromper um gasto fora do controle.
- [ ] Conheço guardrails de entrada, processo e saída.
- [ ] Subi a API e testei os endpoints.
- [ ] Meu CI está verde.
