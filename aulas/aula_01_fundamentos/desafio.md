# Desafio da Aula 1 — CordelLLM

A Padaria Pão Nosso vai participar da Festa Junina do bairro e quer um atendente que responda em **versos de cordel**.

## Missão
1. Crie a classe `CordelLLM` (em um arquivo novo, `aulas/aula_01_fundamentos/desafio_cordel.py`).
2. Ela deve **encaixar na `LLMPort`** e, por dentro, usar outro LLM (o que vier do `criar_llm()`), acrescentando
   uma instrução de sistema: "responda sempre em uma estrofe de cordel, com 6 versos rimados".
3. Mostre que a função `atender(llm, pergunta)` do exemplo 3 funciona com o `CordelLLM` sem alteração.

## Dica de arquitetura
Esse padrão (um adaptador que "embrulha" outro e acrescenta comportamento) se chama **decorator**.
É assim que, na Aula 8, vamos acrescentar cache, retry e limite de custo sem mexer na aplicação.

## Critérios
- Encaixa na porta (`isinstance(CordelLLM(...), LLMPort)` é `True`).
- Funciona em modo fake (rode com `MODO=fake`).
- Bônus: um parâmetro `tema` ("São João", "futebol", "pão de queijo").
