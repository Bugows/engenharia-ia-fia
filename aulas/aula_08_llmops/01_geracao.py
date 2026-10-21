"""Aula 8 — Exemplo 1: os botões de controle da geração.

Como rodar (centavos):
    uv run python aulas/aula_08_llmops/01_geracao.py

Botões do gpt-5.4-mini que mais afetam custo e qualidade:
- max_tokens: teto da resposta (corta o texto e a conta);
- reasoning_effort: none | low | medium | high | xhigh;
- verbosity: low | medium | high (tamanho da resposta; via Responses API);
- temperature: só com reasoning_effort="none".
"""

from assistente_ia.config import descrever_ambiente
from assistente_ia.container import criar_chat_model, modo_fake
from assistente_ia.domain.custos import custo_usd

print(descrever_ambiente(), "\n")
if modo_fake():
    print("Este exemplo precisa do modelo real. Configure a chave e rode de novo.")
    raise SystemExit(0)

pergunta = "Explique para um cliente por que o pão francês da padaria sai em 3 fornadas por dia."

configuracoes = {
    "max_tokens=40": {"max_tokens": 40},
    "verbosity=low": {"verbosity": "low", "use_responses_api": True},
    "verbosity=high": {"verbosity": "high", "use_responses_api": True},
    "esforço=medium": {"reasoning_effort": "medium", "max_tokens": 1500},
}

for nome, ajustes in configuracoes.items():
    resposta = criar_chat_model(**ajustes).invoke(pergunta)
    uso = resposta.usage_metadata or {}
    texto = resposta.text if hasattr(resposta, "text") else str(resposta.content)
    custo = custo_usd("gpt-5.4-mini", uso.get("input_tokens", 0), uso.get("output_tokens", 0))
    print(f"[{nome:>15}] saída={uso.get('output_tokens', 0):>4} tok | US$ {custo:.5f} | {texto[:100]!r}")

print("\nQual configuração você usaria num WhatsApp? E num relatório para a diretoria?")
