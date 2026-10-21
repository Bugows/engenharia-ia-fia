"""Aula 2 — Exemplo 2: o projeto se paga? (ROI)

Como rodar (custo zero):
    uv run python aulas/aula_02_planejamento/02_roi.py
"""

from pathlib import Path

import yaml

from assistente_ia.domain.custos import custo_usd, formatar_brl, roi

canvas = yaml.safe_load((Path(__file__).parent / "canvas_ia.yaml").read_text(encoding="utf-8"))
n = canvas["numeros"]

# Ganho: horas de atendente economizadas
horas_economizadas = n["conversas_por_mes"] * n["minutos_economizados_por_conversa"] / 60
ganho_mensal = horas_economizadas * n["custo_hora_atendente_brl"]

# Custo: tokens + custo fixo
custo_tokens_brl = (
    custo_usd("gpt-5.4-mini", n["tokens_entrada_por_conversa"], n["tokens_saida_por_conversa"])
    * n["conversas_por_mes"]
    * n["cotacao_dolar"]
)
custo_mensal = custo_tokens_brl + n["custo_fixo_mensal_brl"]

print(f"Horas economizadas por mês: {horas_economizadas:.0f} h")
print(f"Ganho mensal:  {formatar_brl(ganho_mensal)}")
print(f"Custo mensal:  {formatar_brl(custo_mensal)} (tokens {formatar_brl(custo_tokens_brl)} + fixo {formatar_brl(n['custo_fixo_mensal_brl'])})")
print(f"ROI mensal:    {roi(ganho_mensal, custo_mensal):.0%}")

# Análise de sensibilidade: e se a IA economizar menos tempo do que o esperado?
print("\nSensibilidade (minutos economizados por conversa):")
for minutos in (0.5, 1, 2, 3, 5):
    ganho = n["conversas_por_mes"] * minutos / 60 * n["custo_hora_atendente_brl"]
    print(f"  {minutos:>4} min -> ROI {roi(ganho, custo_mensal):>7.0%}")
print("\nPergunta para discutir: qual é o 'ponto de equilíbrio' (ROI = 0%)?")
