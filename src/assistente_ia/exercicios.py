"""Ajudante para os exercícios: roda as verificações e mostra o resultado de forma amigável.

Uso dentro de um exercício:

    from assistente_ia.exercicios import verificar

    def checar():
        assert minha_funcao(2) == 4, "minha_funcao(2) deveria devolver 4"

    if __name__ == "__main__":
        verificar("Exercício 1", checar)
"""

from __future__ import annotations

from collections.abc import Callable

from rich.console import Console
from rich.markup import escape
from rich.panel import Panel

_console = Console()


def verificar(nome: str, *checagens: Callable[[], None]) -> bool:
    """Executa as checagens. Mostra PASSOU ou a dica do que falta."""
    for checagem in checagens:
        try:
            checagem()
        except NotImplementedError as erro:
            _console.print(Panel(f"Ainda falta completar um TODO.\n\nDica: {escape(str(erro))}", title=f"{nome}: EM ANDAMENTO", style="yellow"))
            return False
        except AssertionError as erro:
            _console.print(Panel(f"Quase lá! {escape(str(erro))}", title=f"{nome}: AINDA NÃO", style="red"))
            return False
        except Exception as erro:  # noqa: BLE001
            _console.print(Panel(f"{type(erro).__name__}: {escape(str(erro))}", title=f"{nome}: ERRO", style="red"))
            return False
    _console.print(Panel("Todas as verificações passaram. Faça um commit!", title=f"{nome}: PASSOU", style="green"))
    return True
