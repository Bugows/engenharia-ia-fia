"""Aula 3 — Exemplo 3: modelos que "pensam antes de responder".

Como rodar (usa a API: alguns centavos):
    uv run python aulas/aula_03_modelos/03_esforco_raciocinio.py

O gpt-5.4-mini aceita reasoning_effort: none (padrão), low, medium, high, xhigh.
Mais esforço = mais tokens de raciocínio (cobrados como SAÍDA) e mais tempo.
"""

import time

from assistente_ia.config import descrever_ambiente
from assistente_ia.container import criar_chat_model, modo_fake
from assistente_ia.domain.custos import custo_usd

print(descrever_ambiente(), "\n")
if modo_fake():
    print("Este exemplo só faz sentido com o modelo real. Configure a chave e rode de novo.")
    raise SystemExit(0)

problema = (
    "Na Padaria Peter Pão, o sonho custa R$ 6,00 e o café R$ 4,00. O combo sonho + café tem 15% de desconto. "
    "Uma família pediu 2 combos e mais 1 café avulso, e vai dividir a conta entre 3 pessoas com 10% de gorjeta. "
    "Quanto cada pessoa paga? Responda só o valor final."
)
# Resposta correta: (2 * 10 * 0,85 + 4) * 1,10 / 3 = R$ 7,70

for esforco in ["none", "low", "medium"]:
    modelo = criar_chat_model(reasoning_effort=esforco, max_tokens=2000)
    inicio = time.perf_counter()
    resposta = modelo.invoke(problema)
    segundos = time.perf_counter() - inicio
    uso = resposta.usage_metadata or {}
    raciocinio = (uso.get("output_token_details") or {}).get("reasoning", 0)
    custo = custo_usd("gpt-5.4-mini", uso.get("input_tokens", 0), uso.get("output_tokens", 0))
    print(f"[{esforco:>6}] {segundos:5.1f}s | raciocínio={raciocinio:>4} tok | US$ {custo:.5f} | {str(resposta.content)[:80]}")

print("\nResposta correta: R$ 7,70. Qual esforço acertou? Qual o melhor custo-benefício?")
