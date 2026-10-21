# Desafio da Aula 7 — O Técnico Virtual da Várzea

O Unidos da Vila quer um deep agent que ajude o técnico antes de cada rodada.

## Missão
Crie `aulas/aula_07_agentes/desafio_tecnico.py` com um deep agent (`create_deep_agent`) que tenha:

1. **Ferramentas** (implemente como `FerramentaPort` e converta com `para_langchain_lista`):
   - `consultar_regulamento(pergunta)`: usa o RAG da várzea da Aula 5;
   - `listar_elenco()`: devolve 14 jogadores fictícios, com posição e cartões amarelos;
   - `verificar_suspensao(jogador)`: aplica a regra do regulamento (2 amarelos = suspenso).
2. **Dois subagentes**:
   - `escalador`: monta o time titular (1 goleiro, 4 defensores, 4 meias, 2 atacantes) sem suspensos;
   - `analista-adversario`: escreve 3 pontos de atenção sobre o adversário (dados fictícios).
3. **Planejamento** com `TodoListMiddleware` e **arquivo final** `/escalacao.md`.
4. **Aprovação humana** antes de "publicar a escalação no grupo" (`interrupt_on`).

## Regras de custo
- Teste tudo em modo fake com roteiro antes de usar a chave.
- `ModelCallLimitMiddleware(run_limit=20)` é obrigatório.
- Anote quantas chamadas e quanto custou cada execução real.

## Apresentação
Mostre o plano (`todos`), o arquivo gerado e explique: por que usar subagentes em vez de um agente só?
