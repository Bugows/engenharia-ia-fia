"""Aula 3 — Exemplo 1: o modelo não lê palavras, lê TOKENS.

Como rodar (custo zero):
    uv run python aulas/aula_03_modelos/01_tokens.py
"""

from assistente_ia.adapters.tokenizador import contar_tokens, pedacos_de_tokens

frases = [
    "pão de queijo",
    "cheese bread",
    "paralelepípedo",
    "inconstitucionalissimamente",
    "Bom dia! Tem coxinha?",
    "Good morning! Do you have coxinha?",
    "🥖☕🧀",
    "R$ 4,50",
    "12345678901234567890",
]

print(f"{'texto':<36} {'tokens':>6}  pedaços")
for frase in frases:
    pedacos = pedacos_de_tokens(frase)
    print(f"{frase:<36} {contar_tokens(frase):>6}  {pedacos}")

print("\nPara discutir:")
print("- Português costuma gastar mais tokens que inglês para a mesma ideia. Isso vira custo.")
print("- Emojis e números longos também são caros.")
print("- O limite de contexto (400 mil tokens no gpt-5.4-mini) é medido em tokens, não em palavras.")
