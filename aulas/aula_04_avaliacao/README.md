# Aula 4 — Seleção, Avaliação e Comparação de Modelos e Pipelines

> "O que não se mede não se melhora." Sem avaliação, todo ajuste é palpite.

## Objetivos
- Montar e usar um **golden dataset** (gabarito) para o RAG da padaria.
- Corrigir respostas automaticamente por **regras** (palavras-chave, recusa).
- Usar um **LLM como juiz** com saída estruturada (nota de 1 a 5) e conhecer seus vieses.
- **Comparar configurações** (k, prompt, modelo) por acerto, latência e custo.

## Conceitos em 1 minuto
- **Golden dataset**: perguntas com resposta conhecida, incluindo casos difíceis, fora do escopo e ataques.
- **Avaliação offline**: roda antes de publicar (como teste automatizado). **Online**: mede em produção (Aula 8).
- **LLM-as-a-Judge**: um modelo dá nota às respostas. Rápido e barato, mas tem vieses (prefere textos longos, se autoelogia).
- **Benchmarks públicos** (MMLU, GPQA, SWE-Bench) ajudam a escolher modelo, mas **o seu golden dataset decide**.
- **Trade-off**: qualidade x latência x custo. Raramente o "melhor" ganha nos três.

## Passo a passo
```bash
uv run python aulas/aula_04_avaliacao/01_rodar_golden.py
uv run python aulas/aula_04_avaliacao/02_juiz_llm.py
uv run python aulas/aula_04_avaliacao/03_comparar_configs.py
```
Os relatórios ficam em `saidas/`. Rode tudo também com `MODO=fake` e compare: o acerto do modo fake é o seu "piso".

## Exercícios
| Arquivo | O que fazer |
|---|---|
| `exercicios/ex01_novos_casos.py` | Criar 4 casos novos (fácil, difícil, fora do escopo, ataque) |
| `exercicios/ex02_metrica_cita_fonte.py` | Criar a métrica "cita fonte válida" |

## Desafio criativo
`desafio.md`: **o Juiz do VAR**.

## Para ir além
- Avaliação com LangSmith: `from langsmith import evaluate` (requer conta gratuita).
- O workflow `.github/workflows/evals.yml` roda o golden dataset no GitHub Actions (com o SEU secret).

## Checklist
- [ ] Sei explicar por que o golden dataset precisa ter ataques e perguntas fora do escopo.
- [ ] Conheço 3 vieses do LLM-as-a-Judge.
- [ ] Comparei configurações com números e escolhi uma com justificativa.
