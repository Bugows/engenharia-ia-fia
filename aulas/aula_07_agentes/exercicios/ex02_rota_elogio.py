"""Aula 7 — Exercício 2: seu primeiro grafo LangGraph do zero.

Monte um mini-fluxo de atendimento com 3 rotas: duvida, reclamacao e ELOGIO.
Elogios devem ser agradecidos e registrados no "mural de elogios" da padaria.

Rodar e verificar (custo zero):
    uv run python aulas/aula_07_agentes/exercicios/ex02_rota_elogio.py
"""

from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from assistente_ia.exercicios import verificar

MURAL_DE_ELOGIOS: list[str] = []


class Estado(TypedDict, total=False):
    mensagem: str
    rota: str
    resposta: str


def classificar(estado: Estado) -> Estado:
    estado["mensagem"].lower()
    # TODO 1: se tiver "parabéns", "adorei", "maravilhoso" ou "melhor" -> rota "elogio"
    #         se tiver "frio", "atrasou" ou "ruim" -> rota "reclamacao"
    #         senão -> rota "duvida"
    raise NotImplementedError("Devolva {'rota': ...}")


def responder_duvida(estado: Estado) -> Estado:
    return {"resposta": "Vou verificar e já te respondo!"}


def tratar_reclamacao(estado: Estado) -> Estado:
    return {"resposta": "Sentimos muito! A Dona Cida vai falar com você em até 1 hora."}


def agradecer_elogio(estado: Estado) -> Estado:
    # TODO 2: acrescente a mensagem ao MURAL_DE_ELOGIOS e devolva uma resposta de agradecimento
    raise NotImplementedError("MURAL_DE_ELOGIOS.append(...) e devolva {'resposta': ...}")


def montar_grafo():
    grafo = StateGraph(Estado)
    grafo.add_node("classificar", classificar)
    grafo.add_node("responder_duvida", responder_duvida)
    grafo.add_node("tratar_reclamacao", tratar_reclamacao)
    # TODO 3: adicione o nó "agradecer_elogio"
    grafo.add_edge(START, "classificar")
    grafo.add_conditional_edges(
        "classificar",
        lambda estado: estado["rota"],
        {
            "duvida": "responder_duvida",
            "reclamacao": "tratar_reclamacao",
            # TODO 4: mapeie a rota "elogio" para o nó "agradecer_elogio"
        },
    )
    for no in ("responder_duvida", "tratar_reclamacao"):  # TODO 5: inclua "agradecer_elogio"
        grafo.add_edge(no, END)
    return grafo.compile()


def checar():
    MURAL_DE_ELOGIOS.clear()
    app = montar_grafo()
    assert app.invoke({"mensagem": "Que horas abre?"})["rota"] == "duvida"
    assert app.invoke({"mensagem": "O café veio frio"})["rota"] == "reclamacao"
    resultado = app.invoke({"mensagem": "Parabéns, o melhor sonho da cidade!"})
    assert resultado["rota"] == "elogio", f"Rota recebida: {resultado['rota']}"
    assert MURAL_DE_ELOGIOS == ["Parabéns, o melhor sonho da cidade!"], "O elogio deve ir para o mural."
    assert "obrigad" in resultado["resposta"].lower(), "A resposta deve agradecer (obrigado/obrigada)."


if __name__ == "__main__":
    if verificar("Aula 7 — Exercício 2", checar):
        print(montar_grafo().get_graph().draw_mermaid())
