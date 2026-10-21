"""Aula 8 — Exemplo 3: cache, limite de requisições e fallback.

Como rodar:
    uv run python aulas/aula_08_llmops/03_cache_retry_rate.py

Três técnicas que todo sistema em produção usa:
1) CACHE: a mesma pergunta não paga duas vezes;
2) RATE LIMIT: no máximo N chamadas por segundo (protege a conta e a cota);
3) FALLBACK: se o modelo principal falhar, usa um reserva automaticamente.
(Retry com espera exponencial já vem embutido no ChatOpenAI: max_retries=2.)
"""

import time

from langchain_core.caches import InMemoryCache
from langchain_core.globals import set_llm_cache
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_core.runnables import RunnableLambda

from assistente_ia.config import descrever_ambiente
from assistente_ia.container import criar_chat_model

print(descrever_ambiente(), "\n")

# 1) Cache em memória (em produção: Redis, SQLite...)
set_llm_cache(InMemoryCache())
modelo = criar_chat_model(max_tokens=60)
pergunta = "Em uma frase: qual a diferença entre pão francês e pão de forma?"
for tentativa in (1, 2):
    inicio = time.perf_counter()
    modelo.invoke(pergunta)
    print(f"Cache - chamada {tentativa}: {time.perf_counter() - inicio:.3f}s")
print("A segunda chamada veio do cache: custo zero.\n")
set_llm_cache(None)

# 2) Rate limiter: no máximo 2 chamadas por segundo
limitador = InMemoryRateLimiter(requests_per_second=2, check_every_n_seconds=0.05, max_bucket_size=1)
modelo_limitado = criar_chat_model(rate_limiter=limitador, max_tokens=20)
inicio = time.perf_counter()
for i in range(4):
    modelo_limitado.invoke(f"Responda só com o número {i}")
    print(f"Rate limit - chamada {i + 1} concluída em {time.perf_counter() - inicio:.2f}s")
print("Repare no espaçamento de ~0,5s entre as chamadas.\n")


# 3) Fallback: o principal falha (simulamos uma queda) e o reserva assume
def principal_fora_do_ar(_entrada):
    raise ConnectionError("Provedor principal indisponível (simulação)")


robusto = RunnableLambda(principal_fora_do_ar).with_fallbacks([criar_chat_model(max_tokens=60)])
resposta = robusto.invoke("Diga 'olá' em uma palavra.")
print(f"Fallback - resposta do modelo reserva: {resposta.content}")
