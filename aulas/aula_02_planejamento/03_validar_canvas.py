"""Aula 2 — Exemplo 3: AI Canvas como código.

Como rodar:
    uv run python aulas/aula_02_planejamento/03_validar_canvas.py                 # canvas da padaria
    uv run python aulas/aula_02_planejamento/03_validar_canvas.py meu_canvas.yaml # o seu
"""

import sys
from pathlib import Path

import yaml

from assistente_ia.domain.canvas import validar_canvas

caminho = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "canvas_ia.yaml"
canvas = yaml.safe_load(caminho.read_text(encoding="utf-8"))

problemas = validar_canvas(canvas)
if problemas:
    print(f"Canvas '{caminho.name}' precisa de ajustes:")
    for p in problemas:
        print("  -", p)
    raise SystemExit(1)
print(f"Canvas '{canvas['projeto']}' completo. Pronto para virar Project Charter!")
