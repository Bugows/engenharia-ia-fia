"""Carrega arquivos .md e .txt de uma pasta e divide em pedaços."""

from __future__ import annotations

from pathlib import Path

from assistente_ia.config import PASTA_DADOS
from assistente_ia.domain.chunking import dividir_em_pedacos
from assistente_ia.domain.modelos import Documento


class RepositorioArquivosLocais:
    """Implementa a RepositorioDocumentosPort lendo arquivos do disco."""

    EXTENSOES = {".md", ".txt"}

    def __init__(self, tamanho_pedaco: int = 500, sobreposicao: int = 80) -> None:
        self.tamanho_pedaco = tamanho_pedaco
        self.sobreposicao = sobreposicao

    def carregar(self, pasta: str | Path) -> list[Documento]:
        caminho = Path(pasta)
        if not caminho.is_absolute() and not caminho.exists():
            caminho = PASTA_DADOS / caminho  # permite carregar("padaria")
        if not caminho.exists():
            raise FileNotFoundError(f"Pasta não encontrada: {caminho}")

        documentos: list[Documento] = []
        for arquivo in sorted(caminho.rglob("*")):
            if arquivo.suffix.lower() not in self.EXTENSOES:
                continue
            texto = arquivo.read_text(encoding="utf-8")
            pedacos = dividir_em_pedacos(texto, self.tamanho_pedaco, self.sobreposicao)
            for i, pedaco in enumerate(pedacos):
                documentos.append(
                    Documento(
                        id=f"{arquivo.stem}-{i}",
                        texto=pedaco,
                        fonte=arquivo.name,
                        metadados={"caminho": str(arquivo), "pedaco": i},
                    )
                )
        return documentos
