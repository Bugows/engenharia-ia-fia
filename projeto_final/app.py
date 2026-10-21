"""Projeto Final — ponto de partida: o Assistente Corporativo Pão Nosso S.A. no terminal.

Como rodar:
    uv run python projeto_final/app.py
    MODO=fake uv run python projeto_final/app.py

Este esqueleto JÁ FUNCIONA juntando o que foi construído no curso.
Sua missão (veja README.md): adaptá-lo ao SEU caso de uso e cumprir os requisitos da rubrica.
Procure os comentários "PROJETO:" para saber onde estender.
"""

from langchain_core.messages import AIMessage
from rich.console import Console
from rich.markup import escape
from rich.prompt import Prompt

from assistente_ia.application.avaliacao import avaliar, carregar_golden
from assistente_ia.application.deep_agent import arquivos_gerados, criar_deep_agent_padaria
from assistente_ia.application.ferramentas import ferramentas_padaria
from assistente_ia.config import PASTA_DADOS, descrever_ambiente
from assistente_ia.container import (
    criar_agente_garcom,
    criar_chat_model,
    criar_observabilidade,
    criar_servico_rag,
)

console = Console()

# PROJETO: troque a pasta "padaria" pela base de conhecimento do seu caso de uso.
observabilidade = criar_observabilidade(silencioso=True)
rag = criar_servico_rag("padaria", observabilidade=observabilidade)
# PROJETO: troque/acrescente ferramentas em application/ferramentas.py
agente = criar_agente_garcom()


def opcao_rag() -> None:
    pergunta = Prompt.ask("Pergunta")
    resposta = rag.perguntar(pergunta)
    console.print(f"[bold]Resposta:[/] {escape(resposta.resposta)}\n[dim]Fontes: {resposta.fontes}[/]")


def opcao_agente() -> None:
    sessao = Prompt.ask("Nome da sessão (cliente)", default="cliente")
    mensagem = Prompt.ask("Mensagem")
    resposta = agente.conversar(mensagem, sessao)
    console.print(f"[bold]Agente:[/] {escape(resposta)}")
    if resposta.startswith("[aguardando aprovação humana]"):
        aprovado = Prompt.ask("Aprovar a ação?", choices=["s", "n"], default="n") == "s"
        console.print(f"[bold]Agente:[/] {escape(agente.decidir(sessao, aprovado))}")


def opcao_relatorio() -> None:
    # PROJETO: escreva o roteiro fake do SEU relatório para testar sem custo.
    roteiro = [
        AIMessage(content="", tool_calls=[{"name": "write_file", "args": {
            "file_path": "/relatorio_semanal.md", "content": "# Relatório semanal\n(modo fake)"}, "id": "r1"}]),
        AIMessage(content="Relatório semanal salvo em /relatorio_semanal.md."),
    ]
    deep = criar_deep_agent_padaria(criar_chat_model(roteiro, reasoning_effort="low", max_tokens=1500), ferramentas_padaria())
    resultado = deep.invoke({"messages": [{"role": "user", "content": (
        "Gere o relatório semanal da padaria: 3 sugestões de combos com preço e desconto de 10%. "
        "Salve em /relatorio_semanal.md."
    )}]})
    for caminho, conteudo in arquivos_gerados(resultado).items():
        console.print(f"[bold]{caminho}[/]\n{escape(conteudo)}")
    console.print(escape(str(resultado["messages"][-1].content)))


def opcao_avaliacao() -> None:
    # PROJETO: crie o seu golden dataset com pelo menos 20 casos.
    casos = carregar_golden(PASTA_DADOS / "golden" / "padaria_golden.jsonl")
    relatorio = avaliar("projeto", lambda p: rag.perguntar(p).resposta, casos)
    console.print(f"Acerto: [bold]{relatorio.taxa_acerto:.0%}[/] em {len(casos)} casos")
    for erro in relatorio.erros():
        console.print(f"  [red]x[/] {erro.caso.id}: {escape(erro.caso.pergunta)}")


def opcao_custos() -> None:
    console.print(observabilidade.resumo())


MENU = {
    "1": ("Perguntar à base de conhecimento (RAG)", opcao_rag),
    "2": ("Conversar com o agente (ferramentas + aprovação)", opcao_agente),
    "3": ("Gerar relatório com o deep agent", opcao_relatorio),
    "4": ("Rodar a avaliação (golden dataset)", opcao_avaliacao),
    "5": ("Ver custos da sessão", opcao_custos),
}

if __name__ == "__main__":
    console.print(f"[bold]Assistente Corporativo Pão Nosso S.A.[/]\n[dim]{descrever_ambiente()}[/]\n")
    while True:
        for chave, (rotulo, _) in MENU.items():
            console.print(f"  {chave}) {rotulo}")
        escolha = Prompt.ask("Escolha (ou 'sair')", default="sair")
        if escolha == "sair":
            break
        if escolha in MENU:
            MENU[escolha][1]()
        console.print()
