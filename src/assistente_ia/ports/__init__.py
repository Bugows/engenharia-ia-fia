"""Portas: os "formatos de tomada" que a aplicação precisa.

Cada porta é um `Protocol`: diz O QUE precisa existir, nunca COMO é feito.
Qualquer classe com os mesmos métodos "encaixa" na porta (duck typing com tipos).
"""

from assistente_ia.ports.agente import AgentePort
from assistente_ia.ports.documentos import RepositorioDocumentosPort
from assistente_ia.ports.embeddings import EmbeddingsPort
from assistente_ia.ports.ferramentas import FerramentaPort
from assistente_ia.ports.llm import LLMPort
from assistente_ia.ports.observabilidade import ObservabilidadePort
from assistente_ia.ports.vector_store import VectorStorePort

__all__ = [
    "AgentePort",
    "EmbeddingsPort",
    "FerramentaPort",
    "LLMPort",
    "ObservabilidadePort",
    "RepositorioDocumentosPort",
    "VectorStorePort",
]
