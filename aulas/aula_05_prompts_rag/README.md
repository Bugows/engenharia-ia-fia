# Aula 5 — Engenharia Avançada de Prompts e RAG

> O modelo não conhece a sua empresa. RAG é como entregar a ele o manual certo, na hora certa.

## Objetivos
- Escrever prompts como **templates** (papel, regras, formato, exemplos, delimitadores).
- Obter **saída estruturada** (Pydantic) em vez de texto livre.
- Construir um **RAG completo**: ingestão, chunking, embeddings, busca, geração com citação.
- Fazer o mesmo RAG com os componentes prontos do **LangChain** (InMemoryVectorStore, retriever, LCEL).
- Entender **prompt injection** direta e indireta e montar **defesa em camadas**.

## Conceitos em 1 minuto
- **RAG** = Retrieval (buscar trechos) + Augmented (colocar no prompt) + Generation (responder).
- **Chunking**: dividir documentos em pedaços (aqui, 400–500 caracteres com sobreposição).
- **k**: quantos trechos entram no prompt. Mais trechos = mais contexto, mais custo, mais ruído.
- **Citação de fonte**: permite auditar e reduz alucinação.
- **Injeção indireta**: a ordem maliciosa vem de um documento, não do usuário.

```
 arquivos -> pedaços -> embeddings -> [vector store]
                                           |
 pergunta -> embedding -> busca top-k -----+-> prompt com <documentos> -> LLM -> resposta [fonte]
```

## Passo a passo
```bash
uv run python aulas/aula_05_prompts_rag/01_templates.py
uv run python aulas/aula_05_prompts_rag/02_saida_estruturada.py
uv run python aulas/aula_05_prompts_rag/03_rag_padaria.py
uv run python aulas/aula_05_prompts_rag/04_rag_langchain.py
uv run python aulas/aula_05_prompts_rag/05_injecao.py
```

## Exercícios
| Arquivo | O que fazer |
|---|---|
| `exercicios/ex01_extrair_reclamacao.py` | Criar o esquema Pydantic de reclamação e extrair |
| `exercicios/ex02_rag_varzea.py` | Montar um RAG para o regulamento da Copa da Várzea |

## Desafio criativo
`desafio.md`: **caça ao tesouro da injeção** (red team).

## Checklist
- [ ] Sei montar um prompt com papel, regras, formato e exemplo.
- [ ] Sei extrair dados com saída estruturada.
- [ ] Sei explicar cada etapa do RAG e o efeito do `k`.
- [ ] Conheço 4 camadas de defesa contra prompt injection.
