# Configurando a sua chave da OpenAI

> Resumo: cada aluno usa uma **chave individual**, guardada como **Codespaces secret** (ou no `.env` local).
> Sem chave, o curso roda em **modo fake**, sem custo.

## Por que a chave do professor não vem junto com o fork?
- Segredos de um repositório **não são copiados para forks**, nem os de Codespaces nem os de GitHub Actions.
- Mesmo quando um segredo chega ao Codespace, ele vira uma **variável de ambiente em texto puro**:
  qualquer pessoa com acesso ao terminal consegue lê-lo. Compartilhar uma chave única com a turma
  seria o mesmo que entregá-la a todos.
- Por isso o professor gera **uma chave por aluno**, dentro de um projeto da OpenAI com **limite de gasto**.

## Opção 1 — GitHub Codespaces (recomendada)
1. Acesse **github.com/settings/codespaces**.
2. Em **Codespaces secrets**, clique em **New secret**.
3. Preencha:
   - **Name:** `OPENAI_API_KEY`
   - **Value:** a chave que você recebeu (começa com `sk-`)
   - **Repository access:** selecione o **seu fork** `engenharia-ia-fia`
4. Clique em **Add secret**.
5. Se o codespace já estava aberto, reinicie: `Ctrl+Shift+P` → **Codespaces: Rebuild Container**
   (ou pare e inicie de novo).
6. No terminal: `make chave`. Deve aparecer `MODO OPENAI (chave encontrada e oculta)`.

## Opção 2 — Computador local
```bash
cp .env.example .env
```
Abra o `.env` e cole a chave:
```dotenv
OPENAI_API_KEY=sk-...
```
O `.env` está no `.gitignore` e nunca deve ser commitado. Confira com `make chave`.

## Opção 3 — Sem chave (modo fake)
Deixe `OPENAI_API_KEY` vazio ou force:
```bash
MODO=fake uv run python aulas/aula_05_prompts_rag/03_rag_padaria.py
```
Os adaptadores simulados respondem com regras simples. É perfeito para estudar a arquitetura,
fazer os exercícios e rodar os testes. Os exemplos que só fazem sentido com o modelo real avisam e encerram.

## Os três modos (`MODO` no `.env`)
| Valor | Comportamento |
|---|---|
| `auto` (padrão) | Usa a OpenAI se houver chave válida; senão, modo fake |
| `openai` | Exige a chave; se faltar, mostra um erro com as instruções |
| `fake` | Sempre simulado, mesmo com chave |

## Se a turma usar um proxy (LiteLLM)
O professor pode distribuir uma "chave virtual" e um endereço. Configure as duas variáveis:
```dotenv
OPENAI_API_KEY=<chave virtual recebida do professor>
OPENAI_BASE_URL=https://proxy-da-turma.exemplo.com/v1
```

## Usando a chave no GitHub Actions (opcional)
O workflow manual `evals.yml` só roda se **você** cadastrar o secret no **seu fork**:
**Settings → Secrets and variables → Actions → New repository secret** → `OPENAI_API_KEY`.
O CI normal (`ci.yml`) nunca usa chave.

## Mensagens de erro comuns
| Erro | Significado | O que fazer |
|---|---|---|
| `Não encontrei sua OPENAI_API_KEY` | Variável ausente ou sem `sk-` | Refaça os passos acima |
| `401 Unauthorized` | Chave errada, expirada ou revogada | Peça uma nova ao professor |
| `429 ... project_spend_limit_exceeded` | Orçamento do projeto da turma acabou | Avise o professor |
| `429 ... rate limit` | Muitas chamadas por minuto | Espere alguns segundos |
| `Limite de US$ 0.50 desta sessão atingido` | Proteção do curso disparou | Revise o código (loop?) e rode de novo |

## Regras de segurança
1. Nunca escreva a chave em arquivo versionado, notebook, issue, print, slide ou mensagem.
2. Não rode `echo $OPENAI_API_KEY` em tela compartilhada.
3. Se vazou: avise o professor **na hora**. A chave será revogada e uma nova será gerada.
4. O GitHub tem *push protection*: se ele bloquear o seu push por detectar um segredo, não force.
