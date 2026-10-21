"""Porta de observabilidade: registrar uso, custo e eventos."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from assistente_ia.domain.modelos import RespostaLLM


@runtime_checkable
class ObservabilidadePort(Protocol):
    def registrar_uso(self, resposta: RespostaLLM, etapa: str) -> None:
        """Contabiliza tokens e custo de uma chamada."""
        ...

    def custo_total_usd(self) -> float:
        """Custo acumulado na sessão."""
        ...
