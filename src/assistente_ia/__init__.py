"""Assistente IA — projeto didático do curso Engenharia de Inteligência Artificial (FIA).

Organização (arquitetura hexagonal):

    domain/       regras do negócio em Python puro (não conhece OpenAI nem LangChain)
    ports/        contratos (Protocols) que o domínio e a aplicação precisam
    adapters/     implementações concretas das portas (OpenAI, fake, memória, arquivos...)
    application/  casos de uso que combinam portas (chat, RAG, avaliação, agentes)
    api/          entrada HTTP (FastAPI)
    container.py  "quadro de tomadas": decide qual adaptador ligar em cada porta
"""

__version__ = "1.0.0"
