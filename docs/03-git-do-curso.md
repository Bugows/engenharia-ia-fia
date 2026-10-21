# Git no curso: fork, sincronização e entregas

## Conceitos
- **Repositório do professor (upstream):** onde o material é publicado aula a aula.
- **Seu fork (origin):** sua cópia, onde você faz os exercícios e o projeto.
- **Tags:** marcos do curso (`aula-01-inicio`, `aula-01-fim`, ..., `projeto-final-inicio`).

## Primeira vez
```bash
git clone https://github.com/SEU_USUARIO/engenharia-ia-fia.git
cd engenharia-ia-fia
git remote add upstream https://github.com/sergiogaiotto/engenharia-ia-fia.git
git remote -v        # deve listar origin (você) e upstream (professor)
```

## A cada aula: trazer o conteúdo novo
**Pelo GitHub:** página do seu fork → **Sync fork** → **Update branch**. Depois, no terminal: `git pull`.

**Pelo terminal:**
```bash
git fetch upstream --tags
git merge upstream/main
git push
```

### Deu conflito?
Acontece quando você e o professor mexeram no mesmo trecho (por exemplo, um exercício que você resolveu
e que o professor corrigiu). O VS Code mostra as duas versões lado a lado:
- **Accept Current** mantém a sua versão;
- **Accept Incoming** pega a do professor.
Depois: `git add .` → `git commit` → `git push`.

## Salvando o seu trabalho
```bash
git status
git add aulas/aula_03_modelos/exercicios/
git commit -m "aula 3: exercícios de tokens e cosseno"
git push
```

## Voltando a um ponto do curso
```bash
git tag                          # lista os marcos
git switch -c revisao aula-05-inicio   # cria uma branch a partir do início da Aula 5
```

## Entrega do projeto final
```bash
git tag projeto-final-entrega
git push origin projeto-final-entrega
```

## Nunca faça
- `git add .env` (o `.gitignore` bloqueia, mas não force com `-f`).
- `git push --force` no `main` sem saber o que está fazendo.
- Commitar notebooks com saída contendo chave (o `nbstripout` limpa as saídas automaticamente).
