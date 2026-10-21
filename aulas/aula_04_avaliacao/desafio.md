# Desafio da Aula 4 — O Juiz do VAR

No futebol, o VAR revisa lances duvidosos. Vamos fazer o mesmo com o juiz LLM.

## Missão
1. Rode o `01_rodar_golden.py` e guarde as respostas.
2. Para cada resposta, peça a nota ao `JuizLLM` (exemplo `02_juiz_llm.py`).
3. **VAR**: toda resposta com nota 3 (lance duvidoso) é reavaliada por um segundo juiz com
   `reasoning_effort="medium"` (dica: `OpenAILLM.responder_estruturado` usa o modelo padrão;
   crie o seu juiz com `criar_chat_model(reasoning_effort="medium").with_structured_output(NotaJuiz)`).
4. Compare: em quantos casos o VAR mudou a nota? Quanto custou a revisão?

## Perguntas para o relatório
- O juiz concorda com a correção por palavra-chave? Onde discorda, quem está certo?
- Vale a pena pagar o VAR em todas as respostas ou só nas duvidosas?
- Como você detectaria um juiz "bonzinho" demais?
