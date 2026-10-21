"""Adaptadores SIMULADOS: funcionam sem internet, sem chave e sem custo.

- FakeLLM: implementa a LLMPort com regras simples (bom para aulas e testes).
- FakeChatModel: um modelo de chat do LangChain que segue um "roteiro"
  de mensagens. Usado para demonstrar agentes sem gastar tokens.
"""

from __future__ import annotations

import re
import types
from collections.abc import Iterator
from enum import Enum
from typing import Any, Literal, Union, get_args, get_origin

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from pydantic import BaseModel, Field, PrivateAttr

from assistente_ia.domain.modelos import Mensagem, RespostaLLM
from assistente_ia.ports.llm import EsquemaT

PREFIXO_FAKE = "[modo fake]"
_COMUNS = {"a", "o", "as", "os", "de", "da", "do", "e", "em", "que", "qual", "quanto", "voces", "tem", "um", "uma", "para", "com"}


def _radicais(texto: str) -> list[str]:
    """Palavras sem acento, sem as muito comuns, cortadas em 5 letras."""
    import unicodedata

    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()
    return [p[:5] for p in re.findall(r"[a-z0-9]+", sem_acento) if p not in _COMUNS and len(p) > 1]


class FakeLLM:
    """Responde com regras fixas. Ótimo para testar a arquitetura sem gastar nada."""

    REGRAS: dict[str, str] = {
        "pão de queijo": "Temos pão de queijo quentinho saindo às 7h, por R$ 4,50.",
        "horário": "Abrimos de segunda a sexta das 6h às 20h, sábado das 6h às 18h e domingo das 7h às 13h.",
        "abre": "Abrimos de segunda a sexta das 6h às 20h, sábado das 6h às 18h e domingo das 7h às 13h.",
        "pix": "Aceitamos pix, cartão de débito, crédito e dinheiro.",
        "encomenda": "Encomendas precisam de 24 horas de antecedência.",
        "entrega": "Entregamos num raio de 3 km, com taxa de R$ 5,00.",
    }

    def __init__(self, nome_modelo: str = "fake") -> None:
        self.nome_modelo = nome_modelo
        self.chamadas: list[list[Mensagem]] = []

    def responder(self, mensagens: list[Mensagem], *, esforco: str | None = None) -> RespostaLLM:
        self.chamadas.append(list(mensagens))
        ultima = mensagens[-1].conteudo if mensagens else ""
        texto = self._responder_rag(ultima) or self._responder_por_regra(ultima)
        return RespostaLLM(
            texto=texto,
            modelo=self.nome_modelo,
            tokens_entrada=sum(len(m.conteudo.split()) for m in mensagens),
            tokens_saida=len(texto.split()),
        )

    def _responder_rag(self, prompt: str) -> str | None:
        """Se houver <documentos> no prompt, escolhe a frase mais parecida com a pergunta e cita a fonte."""
        bloco = re.search(r"<documentos>(.*?)</documentos>(.*)", prompt, flags=re.S)
        if not bloco:
            return None
        documentos, pergunta = bloco.group(1), bloco.group(2)
        palavras_pergunta = set(_radicais(pergunta))
        melhor: tuple[int, str, str] = (0, "", "")
        for fonte, texto in re.findall(r"\[([^\]]+)\] (.*?)(?=\n\n\[[^\]]+\] |\Z)", documentos.strip(), flags=re.S):
            for frase in re.split(r"\n|(?<=\.) ", texto):
                frase = frase.strip(" -#")
                pontos = len(palavras_pergunta & set(_radicais(frase)))
                if frase and pontos > melhor[0]:
                    melhor = (pontos, fonte, frase)
        if melhor[0] == 0:
            return f"{PREFIXO_FAKE} Não tenho essa informação, vou confirmar com a equipe."
        return f"{PREFIXO_FAKE} Segundo [{melhor[1]}]: {melhor[2]}"

    def _responder_por_regra(self, pergunta: str) -> str:
        minuscula = pergunta.lower()
        for chave, resposta in self.REGRAS.items():
            if chave in minuscula:
                return f"{PREFIXO_FAKE} {resposta}"
        return f"{PREFIXO_FAKE} Entendi! Configure a OPENAI_API_KEY para respostas reais."

    def transmitir(self, mensagens: list[Mensagem]) -> Iterator[str]:
        for palavra in self.responder(mensagens).texto.split():
            yield palavra + " "

    def responder_estruturado(self, mensagens: list[Mensagem], esquema: type[EsquemaT]) -> EsquemaT:
        self.chamadas.append(list(mensagens))
        return preencher_esquema_fake(esquema)


# ---------------------------------------------------------------------------
# Preenchimento automático de esquemas Pydantic (para saídas estruturadas fake)
# ---------------------------------------------------------------------------
def _valor_fake(nome: str, anotacao: Any, metadados: list[Any]) -> Any:
    origem = get_origin(anotacao)
    argumentos = get_args(anotacao)

    if origem in (Union, types.UnionType):  # Optional[X] ou X | None
        nao_nulos = [a for a in argumentos if a is not type(None)]
        return _valor_fake(nome, nao_nulos[0], metadados) if nao_nulos else None
    if origem is Literal:
        return argumentos[0]
    if origem in (list, tuple, set):
        return []
    if origem is dict:
        return {}
    if isinstance(anotacao, type) and issubclass(anotacao, Enum):
        return next(iter(anotacao))
    if isinstance(anotacao, type) and issubclass(anotacao, BaseModel):
        return preencher_esquema_fake(anotacao)
    if anotacao is bool:
        return True
    if anotacao in (int, float):
        minimo = next((m.ge for m in metadados if getattr(m, "ge", None) is not None), None)
        maximo = next((m.le for m in metadados if getattr(m, "le", None) is not None), None)
        if minimo is not None and maximo is not None:
            return anotacao((minimo + maximo) // 2)  # ponto médio: ex. nota 3 numa escala 1-5
        if minimo is None:
            maior_que = next((m.gt for m in metadados if getattr(m, "gt", None) is not None), None)
            minimo = (maior_que + 1) if maior_que is not None else 1
        return anotacao(minimo)
    return f"{PREFIXO_FAKE} {nome}"


def preencher_esquema_fake(esquema: type[EsquemaT]) -> EsquemaT:
    """Cria uma instância plausível de qualquer esquema Pydantic simples."""
    valores = {
        nome: _valor_fake(nome, campo.annotation, list(campo.metadata))
        for nome, campo in esquema.model_fields.items()
    }
    try:
        return esquema.model_validate(valores)
    except Exception:  # noqa: BLE001 - em último caso, cria sem validar
        return esquema.model_construct(**valores)


# ---------------------------------------------------------------------------
# Modelo de chat LangChain simulado (para agentes, grafos e deep agents)
# ---------------------------------------------------------------------------
def _texto_de(mensagem: BaseMessage) -> str:
    conteudo = mensagem.content
    return conteudo if isinstance(conteudo, str) else str(conteudo)


class FakeChatModel(BaseChatModel):
    """Modelo de chat que segue um ROTEIRO de respostas.

    Exemplo de roteiro para um agente com ferramenta:
        [
          AIMessage(content="", tool_calls=[{"name": "consultar_preco",
                                             "args": {"produto": "café"}, "id": "1"}]),
          AIMessage(content="O café custa R$ 4,00."),
        ]
    Quando o roteiro acaba, devolve uma resposta padrão.
    """

    roteiro: list[AIMessage] = Field(default_factory=list)
    resposta_padrao: str = f"{PREFIXO_FAKE} Configure a OPENAI_API_KEY para respostas reais."
    _posicao: int = PrivateAttr(default=0)

    @property
    def _llm_type(self) -> str:
        return "fake-chat-curso-fia"

    def bind_tools(self, tools: Any, *, tool_choice: Any = None, **kwargs: Any) -> FakeChatModel:  # type: ignore[override]
        """Aceita ferramentas (como um modelo real), mas segue o roteiro."""
        return self

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: Any = None,
        **kwargs: Any,
    ) -> ChatResult:
        if self._posicao < len(self.roteiro):
            resposta = self.roteiro[self._posicao]
            self._posicao += 1
        else:
            resposta = AIMessage(content=self.resposta_padrao)
        uso = {
            "input_tokens": sum(len(_texto_de(m).split()) for m in messages),
            "output_tokens": max(1, len(_texto_de(resposta).split())),
        }
        uso["total_tokens"] = uso["input_tokens"] + uso["output_tokens"]
        resposta = resposta.model_copy(update={"usage_metadata": uso})
        return ChatResult(generations=[ChatGeneration(message=resposta)])
