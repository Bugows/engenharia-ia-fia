# Projeto Final — Assistente Corporativo

> Junte tudo o que você construiu em um assistente que resolve um problema real.

## O que entregar
Um assistente para **um caso de uso à sua escolha** (sua empresa, uma ONG, um negócio do bairro)
ou para a **Pão Nosso S.A.** (rede com 5 lojas), construído sobre a arquitetura hexagonal do curso.

### Requisitos obrigatórios
1. **AI Canvas + Project Charter** (Aula 2) com custo mensal estimado e ROI.
2. **RAG com citação de fontes** sobre uma base própria em `dados/<seu_caso>/` (Aula 5).
3. **Agente com pelo menos 3 ferramentas** (`FerramentaPort`), sendo pelo menos 1 com **aprovação humana** (Aula 7).
4. **Deep agent** que gera um relatório em arquivo virtual, com planejamento (`write_todos`) e 1 subagente (Aula 7).
5. **Golden dataset com pelo menos 20 casos** (incluindo 3 ataques e 3 fora do escopo) e relatório de avaliação (Aula 4).
6. **Guardrails**: máscara de dados pessoais, limite de chamadas e pelo menos 1 guardrail de saída (Aula 8).
7. **Observabilidade**: custo por sessão e projeção mensal (Aula 8).
8. **API FastAPI** com pelo menos 3 endpoints (Aula 8).
9. **Testes em modo fake** cobrindo o seu caso, com o **CI verde** (Aula 8).
10. Tudo atrás das **portas**: a aplicação não importa OpenAI diretamente.

### Bônus
Customização com few-shot medida contra zero-shot (Aula 6) · Servidor MCP próprio (Aula 7) ·
Tracing no LangSmith (Aula 8) · Imagem Docker publicada.

## Por onde começar
```bash
uv run python projeto_final/app.py
```
O `app.py` já funciona com a padaria. Procure os comentários `PROJETO:` e adapte.

## Entrega
1. Tag no seu fork: `git tag projeto-final-entrega && git push origin projeto-final-entrega`.
2. Vídeo de até 3 minutos: problema, demonstração e números (acerto, custo, ROI).
3. Arquivo `projeto_final/RELATORIO.md` (até 2 páginas) com decisões de arquitetura e lições aprendidas.

Rubrica: `rubrica.md`.
