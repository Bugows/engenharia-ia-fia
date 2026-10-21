# AI Project Charter — modelo

> Copie este arquivo, preencha e revise com o patrocinador ANTES de escrever código.

## 1. Identificação
- **Projeto:**
- **Patrocinador (quem paga e decide):**
- **Dono do produto:**
- **Equipe:**
- **Data:**

## 2. Problema e oportunidade
- Qual dor do negócio? (com número)
- Quanto ela custa hoje? (R$, horas, clientes perdidos)
- Por que IA e não uma regra fixa ou um formulário?

## 3. Escopo
| Dentro do escopo | Fora do escopo |
|---|---|
| | |

## 4. Solução proposta
- Tipo: [ ] chat simples [ ] RAG [ ] agente [ ] deep agent [ ] customização
- Modelo: `gpt-5.4-mini` (justificativa: custo/latência/qualidade)
- Dados usados e quem é o dono de cada um:
- Onde há humano no circuito (human-in-the-loop):

## 5. Métricas
| Tipo | Métrica | Meta | Como medir |
|---|---|---|---|
| Qualidade | Acerto no golden dataset | >= 80% | Aula 4 |
| Negócio | Tempo médio de atendimento | -30% | Relatório do WhatsApp |
| Custo | US$ por conversa | <= 0,005 | Observabilidade (Aula 8) |
| Segurança | Respostas com dado pessoal vazado | 0 | Guardrails (Aula 8) |

## 6. Riscos e mitigação
| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| Alucinação de preço | Média | Alto | RAG com fonte + golden dataset |
| Prompt injection | Média | Médio | Defesa em camadas (Aula 5) |
| Custo fora do controle | Baixa | Médio | Limites, cache, modelo mini |

## 7. Custos e ROI (use `02_roi.py`)
- Custo mensal estimado:
- Ganho mensal estimado:
- ROI esperado:
- Ponto de equilíbrio:

## 8. Marcos (go / no-go)
| Marco | Data | Critério para seguir |
|---|---|---|
| Prova de conceito | | acerto >= 60% no golden |
| Piloto com 1 loja | | acerto >= 80% e zero vazamento |
| Produção | | ROI positivo por 2 meses |

## 9. Plano B
Se a IA falhar ou sair do ar:
