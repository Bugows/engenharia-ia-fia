# Aula 1 — Fundamentos e Arquitetura da Engenharia de IA

> Hoje você conversa com um LLM pela primeira vez e entende por que a arquitetura importa mais do que o modelo.

## Objetivos
- Fazer a primeira chamada a um LLM com LangChain (`gpt-5.4-mini`).
- Entender a stack de IA em 3 camadas: **infraestrutura**, **modelo** e **aplicação**.
- Entender a arquitetura hexagonal com a analogia da **tomada**.
- Rodar o projeto com chave (OpenAI) e sem chave (modo fake).

## Conceitos em 1 minuto

**Stack de 3 camadas**

| Camada | Neste curso | Quem cuida |
|---|---|---|
| Aplicação | `src/assistente_ia` (chat, RAG, agentes, API) | Você, AI Engineer |
| Modelo | `gpt-5.4-mini` e `text-embedding-3-small` | OpenAI |
| Infraestrutura | GPUs, data centers, rede | OpenAI e nuvem |

**Arquitetura hexagonal = tomadas**

```
          [ Atendente da padaria ]        <- aplicação (regras do negócio)
                     |
                usa a porta
                     v
              ( LLMPort )                 <- o FORMATO da tomada
             /     |      \
   [OpenAILLM] [FakeLLM] [PirataLLM]      <- aparelhos que encaixam (adaptadores)
```

- **Porta**: o que a aplicação precisa ("algo que responda mensagens"). Fica em `src/assistente_ia/ports/`.
- **Adaptador**: quem entrega isso de verdade (OpenAI, simulado...). Fica em `src/assistente_ia/adapters/`.
- **Domínio**: as regras da padaria. Não sabe que a OpenAI existe. Fica em `src/assistente_ia/domain/`.
- **Container**: o quadro de tomadas que liga cada adaptador na porta certa (`container.py`).

**Por que isso importa?** Trocar de modelo, de provedor ou rodar testes sem gastar dinheiro passa a ser mudar UMA linha.

## Passo a passo

```bash
make chave                                                   # 1. confere a chave (sem mostrá-la)
uv run python aulas/aula_01_fundamentos/01_ola_llm.py        # 2. LangChain puro
uv run python aulas/aula_01_fundamentos/02_ola_hexagonal.py  # 3. mesma coisa via porta
MODO=fake uv run python aulas/aula_01_fundamentos/02_ola_hexagonal.py   # 4. sem custo
uv run python aulas/aula_01_fundamentos/03_trocando_adaptador.py        # 5. três adaptadores, uma porta
```

Abra também o notebook `explorando.ipynb` para experimentar célula a célula.

## Exercícios

| Arquivo | O que fazer |
|---|---|
| `exercicios/ex01_bom_dia_padaria.py` | Montar mensagens `system` + `user` e chamar a porta |
| `exercicios/ex02_adaptador_pirata.py` | Criar o seu próprio adaptador (`PirataLLM`) |

Rode o arquivo do exercício: ele mesmo verifica se você acertou.

## Desafio criativo
Veja `desafio.md`: o **CordelLLM**.

## Checklist
- [ ] Fiz o fork e abri o Codespace (ou rodei local).
- [ ] `make chave` funcionou (ou estou em modo fake de propósito).
- [ ] Rodei os 3 exemplos.
- [ ] Sei explicar a diferença entre porta e adaptador.
- [ ] Os 2 exercícios passaram.
- [ ] Fiz commit e push **sem** o arquivo `.env`.
