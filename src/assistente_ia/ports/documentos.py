"""Porta para carregar documentos de alguma origem (pasta, Drive, Notion...)."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol, runtime_checkable

from assistente_ia.domain.modelos import Documento


@runtime_checkable
class RepositorioDocumentosPort(Protocol):
    def carregar(self, pasta: str | Path) -> list[Documento]:
        """Lê os documentos e devolve já divididos em pedaços."""
        ...
