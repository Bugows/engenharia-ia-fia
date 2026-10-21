"""Caso de uso: conversa simples com memória curta (histórico)."""

from __future__ import annotations

from assistente_ia.domain.modelos import Mensagem
from assistente_ia.ports.llm import LLMPort
from assistente_ia.ports.observabilidade import ObservabilidadePort

PERSONA_PADARIA = (
    "Você é o atendente virtual da Padaria Pão Nosso, em São Paulo. "
    "Seja simpático, objetivo (no máximo 3 frases) e responda em português do Brasil. "
    "Se não souber algo, diga que vai confirmar com a equipe."
)


class ServicoChat:
    """Mantém o histórico e conversa com qualquer LLMPort."""

    def __init__(
        self,
        llm: LLMPort,
        persona: str = PERSONA_PADARIA,
        observabilidade: ObservabilidadePort | None = None,
        max_historico: int = 10,
    ) -> None:
        self.llm = llm
        self.persona = persona
        self.observabilidade = observabilidade
        self.max_historico = max_historico
        self.historico: list[Mensagem] = []

    def perguntar(self, texto: str) -> str:
        self.historico.append(Mensagem("user", texto))
        recentes = self.historico[-self.max_historico :]  # memória curta = economia de tokens
        resposta = self.llm.responder([Mensagem("system", self.persona), *recentes])
        if self.observabilidade:
            self.observabilidade.registrar_uso(resposta, "chat")
        self.historico.append(Mensagem("assistant", resposta.texto))
        return resposta.texto

    def limpar(self) -> None:
        self.historico.clear()
