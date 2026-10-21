"""Aula 5 — Exemplo 3: RAG completo na arquitetura hexagonal.

Como rodar:
    uv run python aulas/aula_05_prompts_rag/03_rag_padaria.py
    MODO=fake uv run python aulas/aula_05_prompts_rag/03_rag_padaria.py

Pipeline: carregar arquivos -> dividir em pedaços -> gerar embeddings -> indexar
          -> buscar trechos parecidos -> montar prompt -> responder citando fontes.
"""

from assistente_ia.adapters.documentos.arquivos_locais import RepositorioArquivosLocais
from assistente_ia.application.rag import ServicoRAG
from assistente_ia.config import descrever_ambiente
from assistente_ia.container import criar_llm, criar_observabilidade, criar_vector_store

print(descrever_ambiente(), "\n")

# 1) Ingestão: arquivos -> pedaços (Documento)
documentos = RepositorioArquivosLocais(tamanho_pedaco=400, sobreposicao=60).carregar("padaria")
print(f"{len(documentos)} pedaços carregados de dados/padaria\n")

# 2) Indexação: pedaços -> vetores (VectorStorePort)
base = criar_vector_store()
base.adicionar(documentos)

# 3) Perguntas
rag = ServicoRAG(criar_llm(), base, criar_observabilidade(), k=3)
perguntas = [
    "Que horas vocês abrem no domingo?",
    "Tem opção sem glúten?",
    "Quanto custa um pão na chapa com café com leite?",
    "Vocês vendem pizza?",  # não está nos documentos: deve admitir que não sabe
]
for pergunta in perguntas:
    resposta = rag.perguntar(pergunta)
    print(f"\nPergunta: {pergunta}")
    for t in resposta.trechos:
        print(f"   trecho {t.pontuacao:.2f} [{t.documento.fonte}] {t.documento.texto[:60]!r}")
    print(f"Resposta: {resposta.resposta}")
