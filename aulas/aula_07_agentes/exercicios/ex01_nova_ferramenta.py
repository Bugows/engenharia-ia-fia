"""Aula 7 — Exercício 1: dê uma ferramenta nova ao garçom.

Crie a ferramenta `SugerirAcompanhamento`: dado um produto, sugere o que combina com ele.
Ela precisa encaixar na FerramentaPort (nome, descricao, executar) e funcionar no agente.

Rodar e verificar (modo fake, custo zero):
    MODO=fake uv run python aulas/aula_07_agentes/exercicios/ex01_nova_ferramenta.py
"""

from langchain_core.messages import AIMessage

from assistente_ia.adapters.ferramentas.langchain_tools import para_langchain
from assistente_ia.adapters.llm.fake_llm import FakeChatModel
from assistente_ia.application.agente import AgenteLangChain
from assistente_ia.exercicios import verificar
from assistente_ia.ports import FerramentaPort

COMBINACOES = {
    "café": "pão de queijo",
    "pão de queijo": "café com leite",
    "bolo de rolo": "café",
    "coxinha": "suco de laranja",
}


class SugerirAcompanhamento:
    # TODO 1: defina os atributos de classe `nome` e `descricao`.
    #         A descrição é o que o modelo lê para decidir usar a ferramenta: seja claro!

    def executar(self, produto: str) -> str:
        # TODO 2: procure em COMBINACOES (ignore maiúsculas e espaços extras).
        #         Achou: "Com {produto}, sugerimos {acompanhamento}."
        #         Não achou: "Não tenho sugestão para {produto}."
        raise NotImplementedError("Use COMBINACOES.get(produto.lower().strip())")


def checar_porta():
    ferramenta = SugerirAcompanhamento()
    if not hasattr(ferramenta, "nome"):
        raise NotImplementedError("Defina nome e descricao na classe.")
    assert isinstance(ferramenta, FerramentaPort), "Precisa ter nome, descricao e executar."
    assert ferramenta.nome == "sugerir_acompanhamento", "Use o nome 'sugerir_acompanhamento'."
    assert len(ferramenta.descricao) >= 20, "Escreva uma descrição útil (pelo menos 20 caracteres)."


def checar_execucao():
    ferramenta = SugerirAcompanhamento()
    assert ferramenta.executar("  CAFÉ ") == "Com café, sugerimos pão de queijo."
    assert ferramenta.executar("pizza") == "Não tenho sugestão para pizza."
    assert "produto" in para_langchain(ferramenta).args, "O parâmetro deve se chamar 'produto'."


def checar_no_agente():
    roteiro = [
        AIMessage(content="", tool_calls=[{"name": "sugerir_acompanhamento", "args": {"produto": "coxinha"}, "id": "x"}]),
        AIMessage(content="Com coxinha, que tal um suco de laranja?"),
    ]
    agente = AgenteLangChain(FakeChatModel(roteiro=roteiro), [SugerirAcompanhamento()])
    agente.conversar("O que combina com coxinha?", "ex1")
    resultados = [m.content for m in agente.historico("ex1") if m.type == "tool"]
    assert resultados == ["Com coxinha, sugerimos suco de laranja."], f"Resultado da ferramenta: {resultados}"


if __name__ == "__main__":
    verificar("Aula 7 — Exercício 1", checar_porta, checar_execucao, checar_no_agente)
