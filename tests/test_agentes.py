from langchain_core.messages import AIMessage

from assistente_ia.adapters.ferramentas.langchain_tools import para_langchain
from assistente_ia.adapters.llm.fake_llm import FakeChatModel, FakeLLM
from assistente_ia.application.agente import AgenteLangChain
from assistente_ia.application.deep_agent import arquivos_gerados, criar_deep_agent_padaria
from assistente_ia.application.ferramentas import CalcularTotal, ConsultarPreco, ferramentas_padaria
from assistente_ia.application.grafo_atendimento import classificar_por_palavras, criar_grafo_atendimento
from assistente_ia.container import criar_servico_rag
from assistente_ia.ports import AgentePort, FerramentaPort


def test_ferramentas_encaixam_na_porta():
    assert all(isinstance(f, FerramentaPort) for f in ferramentas_padaria())


def test_ferramenta_vira_tool_langchain_com_esquema():
    tool = para_langchain(CalcularTotal())
    assert tool.name == "calcular_total"
    assert "itens" in tool.args
    assert tool.invoke({"itens": {"café": 2}}) == "Total do pedido: R$ 8,00"


def test_agente_usa_ferramenta_e_responde():
    roteiro = [
        AIMessage(content="", tool_calls=[{"name": "consultar_preco", "args": {"produto": "sonho"}, "id": "c1"}]),
        AIMessage(content="O sonho custa R$ 6,00."),
    ]
    agente = AgenteLangChain(FakeChatModel(roteiro=roteiro), [ConsultarPreco()])
    assert isinstance(agente, AgentePort)
    assert agente.conversar("Quanto custa o sonho?", "t1") == "O sonho custa R$ 6,00."
    mensagens = agente.historico("t1")
    assert any(getattr(m, "name", "") == "consultar_preco" for m in mensagens)


def test_agente_pausa_para_aprovacao_humana():
    roteiro = [
        AIMessage(
            content="",
            tool_calls=[
                {
                    "name": "registrar_encomenda",
                    "args": {"produto": "coxinha", "quantidade": 50, "data_retirada": "20/12"},
                    "id": "e1",
                }
            ],
        ),
        AIMessage(content="Encomenda registrada!"),
    ]
    agente = AgenteLangChain(FakeChatModel(roteiro=roteiro), ferramentas_padaria(), aprovar=["registrar_encomenda"])
    primeira = agente.conversar("Quero 50 coxinhas", "t2")
    assert primeira.startswith("[aguardando aprovação humana]")
    assert agente.decidir("t2", aprovar=True) == "Encomenda registrada!"


def test_classificador_por_palavras():
    assert classificar_por_palavras("Quero fazer uma encomenda") == "encomenda"
    assert classificar_por_palavras("O café veio frio, péssimo") == "reclamacao"
    assert classificar_por_palavras("Que horas abre?") == "duvida"


def test_grafo_duvida_e_encomenda():
    from langgraph.types import Command

    grafo = criar_grafo_atendimento(FakeLLM(), criar_servico_rag("padaria", llm=FakeLLM()))
    cfg = {"configurable": {"thread_id": "g1"}}
    resultado = grafo.invoke({"pergunta": "Aceitam pix?"}, cfg)
    assert resultado["categoria"] == "duvida" and resultado["fontes"]

    cfg2 = {"configurable": {"thread_id": "g2"}}
    pausa = grafo.invoke({"pergunta": "Quero encomendar 50 coxinhas"}, cfg2)
    assert "__interrupt__" in pausa
    final = grafo.invoke(Command(resume="aprovar"), cfg2)
    assert "aprovada" in final["resposta"]


def test_deep_agent_planeja_e_escreve_arquivo():
    roteiro = [
        AIMessage(content="", tool_calls=[{"name": "write_todos", "args": {"todos": [{"content": "calcular combo", "status": "in_progress"}]}, "id": "t1"}]),
        AIMessage(content="", tool_calls=[{"name": "write_file", "args": {"file_path": "/relatorio.md", "content": "# Relatório\nCombo: R$ 10,00"}, "id": "t2"}]),
        AIMessage(content="Relatório salvo em /relatorio.md."),
    ]
    agente = criar_deep_agent_padaria(FakeChatModel(roteiro=roteiro), ferramentas_padaria())
    resultado = agente.invoke({"messages": [{"role": "user", "content": "Monte um relatório"}]})
    assert resultado["todos"][0]["content"] == "calcular combo"
    assert "Combo" in arquivos_gerados(resultado)["/relatorio.md"]
