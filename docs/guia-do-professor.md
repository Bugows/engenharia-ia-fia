# Guia do professor

## 1. Publicação do repositório
1. Crie o repositório público `engenharia-ia-fia` na sua conta (ou organização) e envie este conteúdo.
2. Troque o marcador `PROFESSOR` pelo seu usuário (ou organização) do GitHub:
   ```bash
   grep -rl "PROFESSOR/engenharia-ia-fia" --exclude-dir=.venv --exclude=guia-do-professor.md . \
     | xargs sed -i 's#PROFESSOR/engenharia-ia-fia#seu-usuario-github/engenharia-ia-fia#g'
   ```
   Mantenha `SEU_USUARIO` onde aparecer (README, docs de Git, notebook do Colab): é o aluno quem substitui.
3. Em **Settings → Code security**, ative **Secret scanning** e **Push protection**.
4. Em **Settings → Actions → General**, mantenha "Require approval for all outside collaborators" para PRs de forks.
5. **Não** cadastre a sua chave como secret do repositório: ela não chega aos forks e, nos Codespaces
   em que chegasse, ficaria visível em texto puro.

## 2. Chaves da OpenAI para a turma (recomendado)
1. Em **platform.openai.com**, crie um **Project** `FIA-EngIA-TurmaX`.
2. Em **Limits** do projeto:
   - restrinja os modelos a `gpt-5.4-mini` e `text-embedding-3-small`;
   - em **Spend**, defina o limite mensal = `n_alunos x US$ 15` e ative o **hard limit**
     (ao atingir, a API devolve erro 429 `project_spend_limit_exceeded`);
   - configure alertas por e-mail em 50%, 75% e 90%.
3. Gere **uma chave por aluno** (nome `aluno-<nome>`): o painel de uso mostra o gasto por chave.
   Não existe teto rígido por chave dentro de um projeto; se precisar de teto individual, veja o item 4.
4. Distribua cada chave por **canal privado** (e-mail institucional, mensagem direta). Nunca em grupo ou slide.
5. Ao fim do curso, **revogue todas as chaves** e arquive o projeto.

### Teto individual por aluno (opcional)
- **Um Project por aluno**, cada um com hard limit de US$ 15. Manual, mas viável até ~40 alunos.
- **Proxy LiteLLM** com *virtual keys* (`max_budget`, `budget_duration`, `rpm_limit` por aluno). A chave real
  fica só no servidor; o aluno configura `OPENAI_API_KEY=<chave virtual>` e `OPENAI_BASE_URL=<url do proxy>`.
  Exige servidor e banco Postgres (sem banco, os orçamentos por chave não são aplicados).

### Alunos sem chave
O curso inteiro funciona em `MODO=fake`. Exemplos que dependem do modelo real (Aula 3: raciocínio e temperatura;
Aula 8: parâmetros de geração) avisam e encerram: faça-os em demonstração ao vivo.

## 3. Soluções dos exercícios
As soluções vêm separadas, na pasta `solucoes-professor/` (fora do repositório dos alunos), espelhando
os caminhos `aulas/aula_XX/exercicios/`. Estratégias de publicação:
- **Branch `solucoes`** no seu repositório, atualizada após cada aula:
  ```bash
  git switch -c solucoes
  cp -r ../solucoes-professor/aulas/aula_01_fundamentos/exercicios/* aulas/aula_01_fundamentos/exercicios/
  git commit -am "soluções da aula 1" && git push -u origin solucoes
  git switch main
  ```
- Ou mantenha as soluções num repositório **privado** e mostre em aula.

Todas as soluções passam na verificação automática:
```bash
for f in ../solucoes-professor/aulas/*/exercicios/*.py; do MODO=fake uv run python "$f"; done
```

## 4. Tags por aula
Prepare os marcos antes do curso (opcional, mas ajuda os alunos a voltarem a um ponto):
```bash
for n in 01 02 03 04 05 06 07 08; do git tag aula-$n-inicio; done   # no estado inicial
git push --tags
```
Se preferir liberar o conteúdo aula a aula, mantenha as pastas futuras numa branch `proximas-aulas`
e faça merge no `main` no dia de cada aula. Os alunos recebem com **Sync fork**.

## 5. Roteiro de cada encontro (6 horas)
| Bloco | Tempo | Atividade |
|---|---|---|
| Abertura | 10 min | `make chave` e `git pull`/Sync fork de todos |
| Teoria I | 75 min | Conceitos da aula (slides do curso) intercalando com exemplos `01`/`02` ao vivo |
| Intervalo | 15 min | |
| Teoria II | 75 min | Exemplos restantes, discutindo o código e o custo de cada chamada |
| Almoço | 60 min | |
| Prática | 90 min | Exercícios (verificação automática) em duplas |
| Desafio | 45 min | `desafio.md` em grupos, com apresentação relâmpago |
| Fechamento | 20 min | Checklist do README da aula, quiz e commit/push |

## 6. Checklist do primeiro dia
- [ ] Todos com fork, Codespace (ou ambiente local) e `make testar` verde.
- [ ] Chaves distribuídas; `make chave` mostra "MODO OPENAI" para quem recebeu.
- [ ] Rode com sua chave: `uv run pytest -m openai -q` (valida chat, temperatura e embeddings reais).
- [ ] Mostre o painel de uso do projeto OpenAI para a turma (transparência de custo).
- [ ] Combine a regra: chave vazada = aviso imediato.

## 7. Manutenção entre turmas
- Atualize preços em `src/assistente_ia/domain/custos.py`.
- Atualize dependências: `uv lock --upgrade && make testar`, depois rode os exemplos com chave.
- Confira na documentação da OpenAI o status do `gpt-5.4-mini` (novas versões, datas de descontinuação)
  e da plataforma de fine-tuning (Aula 6).
- Rode o workflow `Evals com OpenAI (manual)` no seu repositório (com o seu secret) para gerar o relatório-base.
- Atualize as versões dos hooks: `uv run pre-commit autoupdate`.

## 8. Pontos técnicos que costumam gerar dúvida
- **`temperature` sumiu?** No GPT-5.x ela só vale com `reasoning_effort="none"`. O LangChain remove em silêncio;
  o `criar_chat_openai` do curso bloqueia a combinação inválida com erro explicativo.
- **`write_todos` não aparece no deep agent?** Desde o deepagents 0.7 ele é opt-in: precisa do `TodoListMiddleware`.
- **`interrupt` não pausa?** O grafo precisa de `checkpointer` e a retomada usa `Command(resume=...)` com o mesmo `thread_id`.
- **Aprovação no `HumanInTheLoopMiddleware`:** a retomada é `Command(resume={"decisions": [{"type": "approve"}]})`
  (ou `reject`, `edit`, `respond`).
- **Tokenizador sem internet:** o `tiktoken` baixa o encoding na primeira execução; sem rede, o curso usa estimativa.
