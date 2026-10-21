# Aula 3 — Modelos de Fundação e Dinâmica Interna

> Abrir o capô: tokens, embeddings, raciocínio e temperatura.

## Objetivos
- Entender **tokens** e por que o português custa mais.
- Entender **embeddings** como "coordenadas de significado" e medir similaridade de cosseno.
- Comparar níveis de **raciocínio** (`reasoning_effort`) em qualidade, tempo e custo.
- Entender **temperatura** e a regra do GPT-5.x.

## Conceitos em 1 minuto
- **Modelo de fundação**: treinado em uma montanha de texto para prever o próximo token; depois ajustado para seguir instruções.
- **Token**: a unidade que o modelo lê e gera. ~1 token ≈ 3 a 4 caracteres em português.
- **Embedding**: vetor de números que representa o significado de um texto. Textos parecidos ficam próximos.
- **Cosseno**: mede o ângulo entre dois vetores (1 = iguais, 0 = nada a ver).
- **Raciocínio**: o modelo "pensa" em tokens escondidos antes de responder. Ajuda em lógica e contas, mas custa saída.
- **Temperatura**: controla a aleatoriedade. No GPT-5.x, só funciona com `reasoning_effort="none"`.

## Passo a passo
```bash
uv run python aulas/aula_03_modelos/01_tokens.py               # custo zero
uv run python aulas/aula_03_modelos/02_embeddings_aipim.py     # quase zero
uv run python aulas/aula_03_modelos/03_esforco_raciocinio.py   # centavos
uv run python aulas/aula_03_modelos/04_temperatura.py          # centavos
```
O mapa de calor fica em `saidas/aula03_similaridade.png`. O notebook `explorando.ipynb` repete tudo de forma interativa.

## Exercícios
| Arquivo | O que fazer |
|---|---|
| `exercicios/ex01_detetive_tokens.py` | Medir tokens por palavra e achar a frase mais "cara" |
| `exercicios/ex02_cosseno_na_mao.py` | Implementar o cosseno e uma busca vetorial do zero |

## Desafio criativo
`desafio.md`: **o mapa do Brasil em embeddings**.

## Checklist
- [ ] Sei explicar token, embedding e cosseno para alguém de fora da área.
- [ ] Vi o custo dos tokens de raciocínio na prática.
- [ ] Sei quando usar `reasoning_effort` maior que `none`.
- [ ] Implementei o cosseno à mão.
