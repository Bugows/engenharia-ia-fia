"""Divisão de textos em pedaços (chunking) para RAG.

Por que dividir? Modelos de embedding representam melhor textos curtos e focados,
e o prompt fica mais barato quando enviamos só os pedaços relevantes.
"""

from __future__ import annotations


def dividir_em_pedacos(texto: str, tamanho: int = 500, sobreposicao: int = 80) -> list[str]:
    """Divide o texto em pedaços de até `tamanho` caracteres.

    - Tenta respeitar parágrafos e não cortar palavras no meio.
    - `sobreposicao` repete o final de um pedaço no início do próximo,
      para não perder contexto na fronteira.
    """
    if tamanho <= 0:
        raise ValueError("O tamanho precisa ser positivo.")
    if not 0 <= sobreposicao < tamanho:
        raise ValueError("A sobreposição deve ser >= 0 e menor que o tamanho.")

    texto = texto.strip()
    if not texto:
        return []
    if len(texto) <= tamanho:
        return [texto]

    pedacos: list[str] = []
    inicio = 0
    while inicio < len(texto):
        fim = min(inicio + tamanho, len(texto))
        if fim < len(texto):
            # Prefere cortar no fim de um parágrafo, depois de uma frase, depois num espaço.
            for separador in ("\n\n", "\n", ". ", " "):
                posicao = texto.rfind(separador, inicio + tamanho // 2, fim)
                if posicao != -1:
                    fim = posicao + len(separador)
                    break
        pedaco = texto[inicio:fim].strip()
        if pedaco:
            pedacos.append(pedaco)
        if fim >= len(texto):
            break
        proximo = max(fim - sobreposicao, inicio + 1)
        # Não começa o próximo pedaço no meio de uma palavra
        if 0 < proximo < len(texto) and not texto[proximo - 1].isspace():
            espaco = texto.find(" ", proximo, fim)
            if espaco != -1:
                proximo = espaco + 1
        inicio = proximo
    return pedacos
