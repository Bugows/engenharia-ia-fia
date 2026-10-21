"""Contagem de tokens com tiktoken (encoding o200k_base, usado pela família GPT-5).

Na primeira vez, o tiktoken baixa o arquivo do encoding da internet. Se a rede bloquear,
caímos numa estimativa (1 token ~ 3,5 caracteres em português) e avisamos.
O número OFICIAL de tokens sempre vem do `usage_metadata` da resposta da API.
"""

from __future__ import annotations

import warnings
from functools import lru_cache


@lru_cache
def _encoding():
    try:
        import tiktoken

        return tiktoken.get_encoding("o200k_base")
    except Exception:  # noqa: BLE001 - sem internet, proxy corporativo etc.
        warnings.warn(
            "Não consegui carregar o tokenizador o200k_base (sem acesso à internet?). "
            "Usando estimativa de 3,5 caracteres por token.",
            stacklevel=2,
        )
        return None


def tokenizador_disponivel() -> bool:
    return _encoding() is not None


def contar_tokens(texto: str) -> int:
    encoding = _encoding()
    if encoding is None:
        return max(1, round(len(texto) / 3.5))
    return len(encoding.encode(texto))


def pedacos_de_tokens(texto: str) -> list[str]:
    """Mostra como o texto é fatiado em tokens (ou fatias de 4 letras, na estimativa)."""
    encoding = _encoding()
    if encoding is None:
        return [texto[i : i + 4] for i in range(0, len(texto), 4)]
    return [encoding.decode([t]) for t in encoding.encode(texto)]
