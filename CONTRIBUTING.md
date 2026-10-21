# Como trabalhar neste repositório

## Fluxo do aluno
1. Trabalhe no **seu fork**, na branch `main` ou numa branch por aula (`git switch -c aula-03`).
2. Antes de cada commit:
   ```bash
   make testar      # testes em modo fake
   make lint        # estilo
   ```
3. Commits pequenos e com mensagem clara, por exemplo: `aula 5: exercício 2 do RAG da várzea`.
4. O `pre-commit` roda sozinho: se ele bloquear o commit por causa de uma chave, **não force**.
   Remova a chave do arquivo e use o `.env` ou o Codespaces secret.

## Encontrou um erro no material?
Abra uma *issue* no repositório **do professor** com:
- aula e arquivo;
- o comando que você rodou;
- a mensagem de erro (sem chaves ou dados pessoais!);
- se estava em modo fake ou openai (`make chave`).

Correções por pull request são bem-vindas. O CI precisa ficar verde (ele roda em modo fake, sem chave).

## Convenções do código
- Domínio (`src/assistente_ia/domain`) em Python puro: nada de OpenAI, LangChain ou FastAPI.
- Toda dependência externa entra por uma **porta** (`ports/`) e um **adaptador** (`adapters/`).
- Todo adaptador real precisa de um equivalente **fake** para os testes.
- Textos, comentários e mensagens em português do Brasil; nomes técnicos consagrados podem ficar em inglês.
- Nada de `print` de chaves, nem em depuração.
