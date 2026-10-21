"""Aula 5 — Exemplo 4: o mesmo RAG, agora com os componentes prontos do LangChain.

Como rodar:
    uv run python aulas/aula_05_prompts_rag/04_rag_langchain.py

Compare com o exemplo 3: InMemoryVectorStore + retriever + LCEL fazem o que
escrevemos à mão. Em produção, você troca o InMemoryVectorStore por pgvector,
Qdrant ou Chroma mudando UMA linha.
"""

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import InMemoryVectorStore

from assistente_ia.adapters.documentos.arquivos_locais import RepositorioArquivosLocais
from assistente_ia.application.rag import PROMPT_RAG
from assistente_ia.config import descrever_ambiente
from assistente_ia.container import criar_chat_model, criar_embeddings, modo_fake

print(descrever_ambiente(), "\n")

# 1) Documentos do domínio -> Documents do LangChain
pedacos = RepositorioArquivosLocais().carregar("padaria")
documentos = [Document(page_content=p.texto, metadata={"fonte": p.fonte}) for p in pedacos]

# 2) Vector store do LangChain (com o mesmo embedding do container)
vector_store = InMemoryVectorStore(embedding=criar_embeddings().langchain)
vector_store.add_documents(documentos)
retriever = vector_store.as_retriever(search_kwargs={"k": 3})


def formatar(docs: list[Document]) -> str:
    return "\n\n".join(f"[{d.metadata['fonte']}] {d.page_content}" for d in docs)


prompt = ChatPromptTemplate.from_messages(
    [("system", PROMPT_RAG), ("user", "<documentos>\n{contexto}\n</documentos>\n\nPergunta do cliente: {pergunta}")]
)

# 3) A "cadeia" LCEL: pergunta -> {contexto, pergunta} -> prompt -> modelo -> texto
cadeia = (
    {"contexto": retriever | formatar, "pergunta": RunnablePassthrough()}
    | prompt
    | criar_chat_model(max_tokens=300)
    | StrOutputParser()
)

pergunta = "Fazem entrega? Quanto custa?"
print("Trechos recuperados:")
for doc in retriever.invoke(pergunta):
    print(f"  [{doc.metadata['fonte']}] {doc.page_content[:70]!r}")
print(f"\nResposta: {cadeia.invoke(pergunta)}")
if modo_fake():
    print("\n(No modo fake o modelo não lê o contexto; com a chave, ele responde citando as fontes.)")
