# Desafio da Aula 8 — Plantão de sexta-feira

É sexta-feira, 18h. O assistente da padaria vai ao ar no WhatsApp amanhã às 6h.
Você é a pessoa de plantão. Prepare o sistema para sobreviver ao primeiro dia.

## Missão
1. **Painel do dono**: adicione à API (`src/assistente_ia/api/main.py`) um endpoint `GET /painel` com:
   chamadas, custo em reais, custo médio por conversa e projeção mensal (use `domain/custos.py`).
2. **Plano de contingência**: use o `LLMComFallback` do exercício 2 no container, com um reserva
   (pode ser o `FakeLLM` respondendo "Estamos com instabilidade, um atendente vai te responder.").
3. **Guardrail de saída**: no `ServicoRAG`, quando `precos_desconhecidos` encontrar preço fora do
   cardápio, troque a resposta por uma mensagem segura e registre o alerta.
4. **Docker**: construa a imagem e suba a API em modo fake (`docker run -p 8000:8000 assistente-ia`).
5. **Runbook**: escreva `docs/runbook.md` com 5 situações (custo disparou, OpenAI fora do ar,
   cliente reclamou de resposta errada, tentativa de injeção, chave vazou) e o que fazer em cada uma.

## Critério
O sistema precisa continuar respondendo (mesmo que de forma degradada) com a chave inválida,
e o CI precisa continuar verde.
