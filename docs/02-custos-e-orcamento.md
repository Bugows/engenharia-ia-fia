# Custos e orçamento

## Preços de referência (out/2026, confira antes de cada turma)
| Modelo | Entrada (US$/1M tokens) | Entrada em cache | Saída |
|---|---|---|---|
| `gpt-5.4-mini` | 0,75 | 0,075 | 4,50 |
| `text-embedding-3-small` | 0,02 | — | — |
| `text-embedding-3-large` | 0,13 | — | — |

Os preços ficam em `src/assistente_ia/domain/custos.py`. Atualize ali quando mudarem.

## O que pesa na conta
1. **Saída custa 6x a entrada.** Respostas longas e tokens de **raciocínio** (que contam como saída) pesam.
2. **Contexto grande em toda chamada.** RAG com `k` alto, histórico longo, few-shot com muitos exemplos.
3. **Agentes fazem várias chamadas por pergunta.** Um deep agent pode fazer dezenas.
4. **Loops.** Um erro de lógica pode chamar o modelo centenas de vezes.

## Proteções embutidas no projeto
| Proteção | Onde | Padrão |
|---|---|---|
| Esforço de raciocínio mínimo | `.env` → `ESFORCO_RACIOCINIO` | `none` |
| Teto de tokens de saída | `.env` → `MAX_TOKENS_SAIDA` | 800 |
| Orçamento por sessão | `.env` → `LIMITE_CUSTO_SESSAO_USD` | US$ 0,50 |
| Limite de chamadas do agente | `ModelCallLimitMiddleware` | 8 (agente), 15 (deep agent) |
| Modo fake | `.env` → `MODO` | `auto` |
| Cache de prompt | Prompt de sistema fixo no início | automático na OpenAI |

## Estimativa por aluno no curso
Premissas: ~1.600 chamadas no curso (cerca de 200 por aula), média de 2.000 tokens de entrada e 800 de saída.

| Item | Conta | Custo |
|---|---|---|
| Entrada | 3,2 milhões x US$ 0,75 | US$ 2,40 |
| Saída | 1,28 milhão x US$ 4,50 | US$ 5,76 |
| Embeddings | — | < US$ 0,05 |
| **Total** | | **≈ US$ 8,20** |

Com folga para agentes e experimentos: **orce US$ 12 a 15 por aluno**.

## Calculando o custo do seu projeto
```bash
uv run python aulas/aula_02_planejamento/01_calculadora_custos.py
uv run python aulas/aula_02_planejamento/02_roi.py
```
Ou direto no Python:
```python
from assistente_ia.domain.custos import custo_usd, custo_brl, formatar_brl
usd = custo_usd("gpt-5.4-mini", entrada=2500, saida=300) * 3000   # 3.000 conversas/mês
print(formatar_brl(custo_brl(usd)))
```

## Dicas de economia
- Teste em `MODO=fake`; ligue a chave só quando o código estiver pronto.
- Mantenha o prompt de sistema **fixo e no início** (aproveita o cache: entrada 10x mais barata).
- Use `k` pequeno no RAG (3 costuma bastar).
- Corte o histórico do chat (o `ServicoChat` guarda só as últimas 10 mensagens).
- Use `reasoning_effort` maior só onde há conta ou lógica difícil (e meça o ganho na Aula 4).
