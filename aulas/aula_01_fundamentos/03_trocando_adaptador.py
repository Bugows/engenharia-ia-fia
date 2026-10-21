"""Aula 1 — Exemplo 3: provando que a porta funciona com QUALQUER adaptador.

Como rodar:
    uv run python aulas/aula_01_fundamentos/03_trocando_adaptador.py

Criamos um adaptador novo (EcoLLM) com 6 linhas. Ele não é inteligente,
mas encaixa na porta — e a função `atender` funciona com ele sem alteração.
"""

from assistente_ia.adapters.llm.fake_llm import FakeLLM
from assistente_ia.container import criar_llm
from assistente_ia.domain.modelos import Mensagem, RespostaLLM, sistema, usuario
from assistente_ia.ports import LLMPort


class EcoLLM:
    """Adaptador de brinquedo: devolve a pergunta em maiúsculas."""

    def responder(self, mensagens: list[Mensagem], *, esforco=None) -> RespostaLLM:
        return RespostaLLM(texto=mensagens[-1].conteudo.upper(), modelo="eco")

    def transmitir(self, mensagens):
        yield self.responder(mensagens).texto

    def responder_estruturado(self, mensagens, esquema):
        raise NotImplementedError("O EcoLLM não sabe gerar saída estruturada.")


def atender(llm: LLMPort, pergunta: str) -> str:
    """Regra da aplicação: só conhece a porta."""
    return llm.responder([sistema("Atendente da Padaria Peter Pão."), usuario(pergunta)]).texto


pergunta = "Vocês aceitam pix?"
for adaptador in (EcoLLM(), FakeLLM(), criar_llm()):
    print(f"{type(adaptador).__name__:>10} | encaixa na porta? {isinstance(adaptador, LLMPort)} | {atender(adaptador, pergunta)}")
