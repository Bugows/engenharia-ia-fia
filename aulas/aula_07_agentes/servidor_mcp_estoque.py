"""Servidor MCP de exemplo: o estoque da Padaria Peter Pão.

MCP (Model Context Protocol) é um padrão aberto para expor ferramentas a qualquer
agente compatível (Claude, ChatGPT, Cursor, LangChain...). Escreva uma vez, use em todos.

Este arquivo é iniciado automaticamente pelo exemplo 06_mcp_opcional.py.
"""

from mcp.server.fastmcp import FastMCP

servidor = FastMCP("estoque-padaria", log_level="WARNING")

ESTOQUE = {"pão de queijo": 120, "coxinha": 35, "sonho": 0, "bolo de rolo": 8, "pão francês": 400}


@servidor.tool()
def consultar_estoque(produto: str) -> str:
    """Quantidade disponível de um produto no estoque da padaria."""
    quantidade = ESTOQUE.get(produto.lower().strip())
    if quantidade is None:
        return f"Produto '{produto}' não cadastrado."
    return f"{produto}: {quantidade} unidades"


@servidor.tool()
def produtos_em_falta() -> str:
    """Lista os produtos com estoque zerado."""
    faltando = [nome for nome, qtd in ESTOQUE.items() if qtd == 0]
    return ", ".join(faltando) if faltando else "Nenhum produto em falta."


if __name__ == "__main__":
    servidor.run(transport="stdio")
