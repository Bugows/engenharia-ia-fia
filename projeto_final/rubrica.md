# Rubrica do Projeto Final (100 pontos)

| Critério | Pontos | Excelente (100%) | Suficiente (60%) | Insuficiente (0–30%) |
|---|---|---|---|---|
| **Arquitetura** | 20 | Portas e adaptadores claros; aplicação sem import direto de OpenAI; container único | Portas usadas na maior parte | Código acoplado ao provedor |
| **Funcionalidade** | 25 | RAG, agente com aprovação, deep agent e API funcionando no caso escolhido | 3 de 4 componentes | Menos de 3 componentes |
| **Avaliação** | 20 | Golden com 20+ casos, ataques, fora do escopo; comparação de 2+ configurações com números | Golden com 10+ casos | Sem avaliação sistemática |
| **Segurança e custo** | 15 | PII, limite de chamadas, guardrail de saída, orçamento por sessão e projeção mensal | 2 guardrails e custo medido | Sem guardrails |
| **Testes e CI** | 10 | Testes fake do caso de uso; CI verde; nenhuma chave no histórico do git | Testes do template passando | CI vermelho ou chave commitada (zera o critério) |
| **Criatividade e negócio** | 10 | Problema real, ROI convincente, solução original | Caso genérico bem executado | Cópia do exemplo da padaria |

**Penalidade:** chave de API encontrada em qualquer commit = **-20 pontos** e revogação imediata da chave.
