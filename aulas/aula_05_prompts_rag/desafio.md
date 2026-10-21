# Desafio da Aula 5 — Caça ao tesouro da injeção

Você é o "red team" (time de ataque) da Padaria Peter Pão.

## Missão
1. Escreva **10 ataques** diferentes contra o `ServicoRAG` (exemplo `05_injecao.py`):
   - 5 diretos (na pergunta): pedir desconto, revelar prompt, mudar de persona, falar em outro idioma...
   - 5 indiretos (em documentos): escondidos no meio de um texto normal, em inglês, com erros de digitação...
2. Conte quantos passaram por cada camada de defesa (heurística, filtro, prompt).
3. Proponha **uma nova camada** de defesa e implemente-a (dica: um segundo LLM barato que classifica
   o trecho como "seguro" ou "suspeito" com `responder_estruturado`).
4. Adicione os ataques que passaram ao golden dataset da Aula 4 (com `deve_recusar: true`).

## Reflexão
- Por que a heurística por palavras é fácil de burlar?
- Qual o custo (tokens e latência) da sua nova camada?
- Existe defesa 100%? O que fazer com o risco que sobra?
