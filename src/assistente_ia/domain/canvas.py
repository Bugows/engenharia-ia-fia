"""AI Canvas como código (Aula 2): um projeto de IA bem definido antes de escrever prompt."""

from __future__ import annotations

CAMPOS_OBRIGATORIOS = {
    "projeto": "Nome curto do projeto",
    "problema": "Qual dor do negócio será resolvida (com número, se possível)",
    "usuarios": "Quem usa (lista)",
    "dados": "Quais dados/documentos alimentam a IA (lista)",
    "tarefa_da_ia": "O que exatamente a IA faz",
    "metrica_sucesso": "Como saber se deu certo (número + prazo)",
    "riscos": "O que pode dar errado (lista)",
    "plano_b_sem_ia": "Como resolver se a IA falhar",
}


def validar_canvas(canvas: dict) -> list[str]:
    """Lista os problemas do canvas (lista vazia = canvas completo)."""
    problemas = []
    for campo, explicacao in CAMPOS_OBRIGATORIOS.items():
        valor = canvas.get(campo)
        if valor in (None, "", [], "TODO") or (isinstance(valor, str) and "TODO" in valor):
            problemas.append(f"Preencha '{campo}': {explicacao}.")
    for campo_lista in ("usuarios", "dados", "riscos"):
        valor = canvas.get(campo_lista)
        if valor and not isinstance(valor, list):
            problemas.append(f"'{campo_lista}' deve ser uma lista.")
    riscos = canvas.get("riscos")
    if isinstance(riscos, list) and 0 < len(riscos) < 3:
        problemas.append("Liste pelo menos 3 riscos.")
    metrica = str(canvas.get("metrica_sucesso", ""))
    if metrica and not any(c.isdigit() for c in metrica):
        problemas.append("A métrica de sucesso precisa ter um número (ex.: '80% de acerto em 30 dias').")
    return problemas
