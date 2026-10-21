"""Observabilidade simples no terminal: tokens, custo acumulado e limite por sessão."""

from __future__ import annotations

from dataclasses import dataclass, field

from assistente_ia.domain.custos import custo_usd
from assistente_ia.domain.modelos import RespostaLLM


class LimiteDeCustoAtingido(RuntimeError):
    """Disparado quando a sessão passa do orçamento definido."""


@dataclass
class RegistroUso:
    etapa: str
    modelo: str
    entrada: int
    saida: int
    raciocinio: int
    custo_usd: float


@dataclass
class ObservabilidadeConsole:
    """Implementa a ObservabilidadePort imprimindo no terminal."""

    limite_usd: float = 0.50
    silencioso: bool = False
    registros: list[RegistroUso] = field(default_factory=list)

    def registrar_uso(self, resposta: RespostaLLM, etapa: str) -> None:
        custo = custo_usd(resposta.modelo, resposta.tokens_entrada, resposta.tokens_saida, resposta.tokens_cache)
        self.registros.append(
            RegistroUso(etapa, resposta.modelo, resposta.tokens_entrada, resposta.tokens_saida,
                        resposta.tokens_raciocinio, custo)
        )
        if not self.silencioso:
            print(
                f"[uso] {etapa}: {resposta.tokens_entrada} tokens de entrada -> "
                f"{resposta.tokens_saida} de saída (raciocínio={resposta.tokens_raciocinio}) "
                f"| acumulado US$ {self.custo_total_usd():.5f}"
            )
        if self.custo_total_usd() > self.limite_usd:
            raise LimiteDeCustoAtingido(
                f"Limite de US$ {self.limite_usd:.2f} desta sessão atingido. "
                "Revise o código antes de continuar (loop? prompt gigante?)."
            )

    def custo_total_usd(self) -> float:
        return sum(r.custo_usd for r in self.registros)

    def resumo(self) -> dict:
        return {
            "chamadas": len(self.registros),
            "tokens_entrada": sum(r.entrada for r in self.registros),
            "tokens_saida": sum(r.saida for r in self.registros),
            "custo_usd": round(self.custo_total_usd(), 6),
        }
