"""Aula 2 — Exercício 1: o AI Canvas do Técnico Virtual de Várzea.

Contexto: o time "Unidos da Vila" quer um assistente que responda dúvidas sobre o
regulamento da Copa da Várzea (dados/futebol/regulamento_varzea.md) e ajude o técnico
a montar a escalação.

Preencha todos os campos marcados com TODO.

Rodar e verificar:
    uv run python aulas/aula_02_planejamento/exercicios/ex01_canvas_varzea.py
"""

from assistente_ia.domain.canvas import validar_canvas
from assistente_ia.exercicios import verificar

CANVAS_VARZEA = {
    "projeto": "Técnico Virtual do Unidos da Vila",
    "problema": "TODO: qual dor? Ex.: o técnico perde X horas por semana respondendo dúvidas no grupo",
    "usuarios": [],  # TODO: lista com pelo menos 2 tipos de usuário
    "dados": ["dados/futebol/regulamento_varzea.md"],
    "tarefa_da_ia": "TODO: o que a IA faz exatamente?",
    "metrica_sucesso": "TODO: precisa ter um número e um prazo",
    "riscos": [],  # TODO: pelo menos 3 riscos
    "plano_b_sem_ia": "TODO: e se a IA falhar?",
}


def checar_canvas():
    problemas = validar_canvas(CANVAS_VARZEA)
    if any("TODO" in str(v) for v in CANVAS_VARZEA.values()) or not CANVAS_VARZEA["usuarios"]:
        raise NotImplementedError("Ainda há campos com TODO ou listas vazias no CANVAS_VARZEA.")
    assert not problemas, " | ".join(problemas)


if __name__ == "__main__":
    verificar("Aula 2 — Exercício 1", checar_canvas)
