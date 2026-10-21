# Desafio da Aula 6 — A receita secreta da Vovó

A Dona Cida quer que o assistente fale como a Vovó Lurdes em TODAS as mensagens.

## Missão
1. Gere 20 exemplos sintéticos com `02_dados_sinteticos.py`, revise e aprove só os bons.
2. Junte com os 12 exemplos de `dados/finetune/tom_vovo.jsonl` e valide com `01_validar_jsonl.py`.
3. Rode o `03_fewshot_vs_zeroshot.py` usando 4, 8 e 12 exemplos no few-shot.
   Monte uma tabela: nº de exemplos x nota média de tom x custo por mil conversas.
4. Escreva uma recomendação de 1 página para a Dona Cida: **few-shot, fine-tuning ou um modelo aberto com LoRA?**
   Considere custo, manutenção, privacidade e o fato de que a plataforma de fine-tuning da OpenAI não está
   disponível para a família GPT-5.4.

## Bônus (opcional, fora da nota)
Rode o notebook `colab_lora_opcional.ipynb` no Google Colab (GPU T4 gratuita) e ajuste um modelo aberto
pequeno com LoRA usando o seu dataset. Compare a resposta antes e depois.
