# Desafio da Aula 3 — O mapa do Brasil em embeddings

O Brasil tem muitos nomes para a mesma coisa. Vamos ver se o modelo sabe disso.

## Missão
1. Monte grupos de sinônimos regionais (pelo menos 4 grupos com 3 palavras):
   - aipim / mandioca / macaxeira
   - pão francês / cacetinho / pão de sal
   - bolacha / biscoito / ...
   - semáforo / sinaleira / farol
2. Adapte o `02_embeddings_aipim.py` para calcular a **similaridade média dentro de cada grupo**
   e a **similaridade média entre grupos diferentes**.
3. Responda: o embedding real "conhece" o português regional? Algum grupo surpreendeu?
4. Rode o mesmo código em modo fake e explique, com suas palavras, por que o resultado é tão diferente.

## Bônus
Teste `text-embedding-3-large` (mude `MODELO_EMBEDDINGS` no `.env`). Ficou melhor? Quanto custaria em 1 milhão de textos?
