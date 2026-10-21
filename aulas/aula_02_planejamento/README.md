# Aula 2 — Planejamento Estratégico de Aplicações de IA

> Antes do prompt, a pergunta certa: **este problema precisa de IA, e ela se paga?**

## Objetivos
- Descrever um projeto de IA com o **AI Canvas** (versionado como código, em YAML).
- Estimar **tokens e custo mensal** com o `tiktoken`.
- Calcular **ROI**, ponto de equilíbrio e **TCO de 12 meses**.
- Escrever um **AI Project Charter** com métricas, riscos, marcos e plano B.

## Conceitos em 1 minuto
- **Token**: pedaço de palavra. Você paga por token de entrada e de saída. No `gpt-5.4-mini`: US$ 0,75 por milhão de entrada e US$ 4,50 por milhão de saída.
- **Tokens de raciocínio** contam como saída: custam 6x mais que a entrada.
- **Cache de prompt**: entrada repetida no início do prompt custa 10x menos (US$ 0,075 por milhão).
- **ROI** = (ganho − custo) / custo. **TCO** = setup + 12 x custo mensal completo (tokens, infraestrutura, manutenção humana).
- **Métrica de sucesso** sem número não é métrica.

## Passo a passo (nenhum exemplo usa a API: custo zero)
```bash
uv run python aulas/aula_02_planejamento/01_calculadora_custos.py
uv run python aulas/aula_02_planejamento/02_roi.py
uv run python aulas/aula_02_planejamento/03_validar_canvas.py
```
Depois, leia `canvas_ia.yaml` e `project_charter.md`.

## Exercícios
| Arquivo | O que fazer |
|---|---|
| `exercicios/ex01_canvas_varzea.py` | Preencher o AI Canvas do Técnico Virtual de Várzea |
| `exercicios/ex02_tco_12_meses.py` | Implementar o cálculo de custo de tokens e TCO |

## Desafio criativo
`desafio.md`: **Shark Tank da IA**.

## Checklist
- [ ] Entendi por que tokens de saída e raciocínio pesam mais na conta.
- [ ] Sei calcular custo mensal, ROI e TCO.
- [ ] Meu canvas passa no validador.
- [ ] Preenchi um Project Charter para um caso real.
