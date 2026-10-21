"""Aula 8 — Exercício 2: um adaptador "decorator" com fallback.

Crie o LLMComFallback: ele ENCAIXA na LLMPort e embrulha dois outros LLMs.
Se o principal falhar (exceção), usa o reserva e anota a falha.
A aplicação não percebe nada: esse é o poder da arquitetura hexagonal.

Rodar e verificar (custo zero):
    uv run python aulas/aula_08_llmops/exercicios/ex02_fallback.py
"""

from assistente_ia.adapters.llm.fake_llm import FakeLLM
from assistente_ia.domain.modelos import Mensagem, RespostaLLM
from assistente_ia.exercicios import verificar
from assistente_ia.ports import LLMPort


class LLMForaDoAr:
    """Simula um provedor caído."""

    def responder(self, mensagens, *, esforco=None) -> RespostaLLM:
        raise ConnectionError("timeout")

    def transmitir(self, mensagens):
        raise ConnectionError("timeout")

    def responder_estruturado(self, mensagens, esquema):
        raise ConnectionError("timeout")


class LLMComFallback:
    def __init__(self, principal: LLMPort, reserva: LLMPort) -> None:
        self.principal = principal
        self.reserva = reserva
        self.falhas: list[str] = []  # guarde aqui o nome da exceção de cada falha

    def responder(self, mensagens: list[Mensagem], *, esforco: str | None = None) -> RespostaLLM:
        # TODO 1: tente o principal; se der exceção, anote type(erro).__name__ em self.falhas e use o reserva
        raise NotImplementedError("try: ... except Exception as erro: ...")

    def transmitir(self, mensagens: list[Mensagem]):
        # TODO 2: mesma ideia, mas para streaming (dica: monte a lista de pedaços do principal antes de devolver)
        raise NotImplementedError("try: pedacos = list(self.principal.transmitir(...)) ...")

    def responder_estruturado(self, mensagens, esquema):
        # TODO 3: mesma ideia para saída estruturada
        raise NotImplementedError("try/except chamando responder_estruturado")


def checar_porta():
    assert isinstance(LLMComFallback(FakeLLM(), FakeLLM()), LLMPort)


def checar_fallback():
    llm = LLMComFallback(LLMForaDoAr(), FakeLLM())
    resposta = llm.responder([Mensagem("user", "Aceitam pix?")])
    assert "pix" in resposta.texto.lower(), "O reserva deveria ter respondido."
    assert llm.falhas == ["ConnectionError"], f"Falhas anotadas: {llm.falhas}"
    assert "".join(llm.transmitir([Mensagem("user", "Aceitam pix?")])).strip(), "Streaming também precisa de fallback."
    assert len(llm.falhas) == 2


def checar_sem_falha():
    llm = LLMComFallback(FakeLLM(), LLMForaDoAr())
    llm.responder([Mensagem("user", "oi")])
    assert llm.falhas == [], "Se o principal funcionar, nenhuma falha deve ser anotada."


if __name__ == "__main__":
    verificar("Aula 8 — Exercício 2", checar_porta, checar_fallback, checar_sem_falha)
