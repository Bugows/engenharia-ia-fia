# Aula 6 — Customização e Fine-Tuning de Modelos

> Antes de treinar, pergunte: prompt e RAG já não resolvem? Se não, o segredo é o **dataset**.

## Objetivos
- Entender a escada da customização: **prompt → few-shot → RAG → fine-tuning → modelo próprio**.
- Montar e **validar datasets** no formato de conversa (JSONL).
- Gerar **dados sintéticos** com o modelo e fazer **curadoria humana**.
- Comparar **few-shot x zero-shot** com nota e custo.
- Conhecer o caminho do **fine-tuning com LoRA** em modelo aberto (opcional, Colab).

## Conceitos em 1 minuto
| Técnica | Muda o quê? | Quando usar |
|---|---|---|
| Prompt / few-shot | O que o modelo lê | Primeiro sempre. Rápido e barato de mudar |
| RAG | O conhecimento disponível | Fatos que mudam (preço, política, estoque) |
| Fine-tuning | Os pesos do modelo | Estilo/formato muito consistente, alto volume, prompt gigante |
| LoRA | Só "adaptadores" pequenos | Fine-tuning barato em modelos abertos |

**Realidade em 2026:** a OpenAI não oferece fine-tuning para a família GPT-5.4 e anunciou o encerramento da plataforma de fine-tuning para novos usuários. Confirme o estado atual na documentação oficial antes de planejar. Por isso esta aula ensina o **processo** (dataset, validação, avaliação), que vale para qualquer provedor ou modelo aberto.

**Formato do dataset (uma linha por exemplo):**
```json
{"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
```

## Passo a passo
```bash
uv run python aulas/aula_06_customizacao/01_validar_jsonl.py
uv run python aulas/aula_06_customizacao/02_dados_sinteticos.py
uv run python aulas/aula_06_customizacao/02_dados_sinteticos.py --converter   # depois de revisar o CSV
uv run python aulas/aula_06_customizacao/03_fewshot_vs_zeroshot.py
```
Opcional: `colab_lora_opcional.ipynb` no Google Colab com GPU.

## Exercícios
| Arquivo | O que fazer |
|---|---|
| `exercicios/ex01_corrigir_dataset.py` | Limpar um dataset com 5 tipos de erro |
| `exercicios/ex02_dataset_narrador.py` | Criar o dataset do "Galvão da Várzea" |

## Desafio criativo
`desafio.md`: **a receita secreta da Vovó**.

## Checklist
- [ ] Sei explicar quando NÃO fazer fine-tuning.
- [ ] Sei validar um JSONL e conheço os erros mais comuns (papel inválido, vazio, PII, duplicata).
- [ ] Entendi que dado sintético precisa de revisão humana.
- [ ] Comparei few-shot e zero-shot com números.
