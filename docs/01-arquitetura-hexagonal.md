# Arquitetura hexagonal (portas e adaptadores) no curso

## A analogia da tomada
Seu notebook não sabe se a energia vem de uma hidrelétrica, de um painel solar ou de um gerador.
Ele só conhece o **formato da tomada**. Trocar a fonte de energia não exige trocar o notebook.

Aqui é igual:
- a **aplicação** (atendente da padaria) só conhece o formato da tomada: a **porta**;
- a OpenAI, o modelo simulado ou qualquer outro provedor são **adaptadores** que encaixam nela;
- o **container** é o quadro de tomadas: decide o que fica ligado em cada porta.

## As camadas
| Camada | Pasta | Pode importar | Exemplo |
|---|---|---|---|
| Domínio | `domain/` | Só Python padrão | `padaria.total_do_pedido`, `custos.custo_usd`, `seguranca.parece_injecao` |
| Portas | `ports/` | Domínio | `LLMPort`, `EmbeddingsPort`, `VectorStorePort`, `FerramentaPort` |
| Aplicação | `application/` | Domínio, portas (e LangGraph/LangChain para orquestrar) | `ServicoRAG`, `AgenteLangChain`, `criar_grafo_atendimento` |
| Adaptadores | `adapters/` | Tudo (OpenAI, LangChain, arquivos) | `OpenAILLM`, `FakeLLM`, `VectorStoreMemoria` |
| Entrada | `api/`, `aulas/`, `projeto_final/` | Container e aplicação | API FastAPI, scripts das aulas |
| Composição | `container.py` | Tudo | `criar_llm()`, `criar_servico_rag()` |

**Regra da dependência:** as setas apontam para dentro. O domínio não conhece ninguém; os adaptadores conhecem todos.

## As portas do projeto
| Porta | Métodos | Adaptadores disponíveis |
|---|---|---|
| `LLMPort` | `responder`, `transmitir`, `responder_estruturado` | `OpenAILLM`, `FakeLLM` (e os seus: `PirataLLM`, `LLMComFallback`) |
| `EmbeddingsPort` | `vetorizar_textos`, `vetorizar_consulta` | `OpenAIEmbeddingsAdapter`, `FakeEmbeddings` |
| `VectorStorePort` | `adicionar`, `buscar` | `VectorStoreMemoria` |
| `RepositorioDocumentosPort` | `carregar` | `RepositorioArquivosLocais` |
| `FerramentaPort` | `nome`, `descricao`, `executar` | `ConsultarPreco`, `CalcularTotal`, `RacharConta`, `VerHorario`, `RegistrarEncomenda` |
| `ObservabilidadePort` | `registrar_uso`, `custo_total_usd` | `ObservabilidadeConsole` |
| `AgentePort` | `conversar` | `AgenteLangChain` |

As portas são `Protocol`s com `@runtime_checkable`: qualquer classe com os mesmos métodos encaixa,
e dá para conferir com `isinstance(objeto, LLMPort)`.

## E o LangChain/LangGraph? Não "vazam" para a aplicação?
Um pouco, de propósito. Agentes, grafos e deep agents **são** orquestração, e reescrever o LangGraph
não faz sentido. A estratégia do curso:
- **regras de negócio** ficam no domínio (puro);
- **ferramentas** são `FerramentaPort` e viram tools do LangChain por um adaptador (`para_langchain`);
- o **modelo** chega pronto do container (`criar_chat_model()`), real ou fake;
- quem usa o agente de fora enxerga só a `AgentePort`.

Assim, trocar de provedor de modelo, de banco vetorial ou rodar testes sem custo continua sendo
mudar o container, e não a aplicação.

## Por que isso vale ouro em projetos de IA
1. **Testes sem custo**: tudo roda com adaptadores fake (o CI nunca gasta um centavo).
2. **Troca de modelo em minutos**: o mercado de modelos muda a cada trimestre.
3. **Decorators**: cache, fallback, limite de custo e logs entram "embrulhando" um adaptador,
   sem tocar na aplicação (veja o `LLMComFallback` da Aula 8).
4. **Auditoria**: as regras de negócio ficam num lugar só, legíveis e testáveis.

## Fluxo de uma pergunta no RAG
```
aula/api ──> container.criar_servico_rag()
               ├─ criar_llm()            -> OpenAILLM | FakeLLM
               ├─ criar_embeddings()     -> OpenAIEmbeddingsAdapter | FakeEmbeddings
               └─ carregar_base("padaria") -> RepositorioArquivosLocais + VectorStoreMemoria
ServicoRAG.perguntar(pergunta)
   1. seguranca.parece_injecao(pergunta)       (domínio)
   2. vector_store.buscar(pergunta, k)         (porta)
   3. filtra trechos suspeitos                 (domínio)
   4. llm.responder([system, user+documentos]) (porta)
   5. observabilidade.registrar_uso(...)       (porta)
```
