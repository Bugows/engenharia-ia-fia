"""Configurações centralizadas do curso.

Lê variáveis de ambiente e o arquivo `.env` da raiz do projeto.
A chave da OpenAI fica guardada como `SecretStr`: ela NUNCA aparece em print,
log ou mensagem de erro.

Teste rápido no terminal:

    uv run python -m assistente_ia.config
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# Raiz do repositório (onde estão pyproject.toml, dados/, aulas/...)
RAIZ_PROJETO = Path(os.getenv("RAIZ_PROJETO", Path(__file__).resolve().parents[2]))
PASTA_DADOS = RAIZ_PROJETO / "dados"
PASTA_SAIDAS = RAIZ_PROJETO / "saidas"

# Carrega o .env para os.environ (sem sobrescrever o que já existe).
# Isso permite que bibliotecas como LangSmith encontrem suas variáveis também.
load_dotenv(RAIZ_PROJETO / ".env", override=False)

Modo = Literal["auto", "openai", "fake"]
Esforco = Literal["none", "low", "medium", "high", "xhigh"]


class ChaveAusenteError(RuntimeError):
    """Erro amigável disparado quando o modo OpenAI é exigido e não há chave."""


MENSAGEM_SEM_CHAVE = """
Não encontrei sua OPENAI_API_KEY.

Como resolver:
  1) GitHub Codespaces: acesse github.com/settings/codespaces -> "New secret"
     Nome: OPENAI_API_KEY | Valor: sua chave | Repositório: o SEU fork.
     Depois, reinicie o codespace (Command Palette -> "Codespaces: Rebuild Container").
  2) Computador local: copie .env.example para .env e cole a chave na linha OPENAI_API_KEY=
  3) Ainda sem chave? Rode em modo simulado: MODO=fake

Guia completo: docs/00-configurando-a-chave.md
"""


class Configuracoes(BaseSettings):
    """Todas as configurações do curso em um único lugar."""

    model_config = SettingsConfigDict(
        env_file=RAIZ_PROJETO / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    openai_api_key: SecretStr | None = None
    openai_base_url: str | None = None  # só se a turma usar um proxy (ex.: LiteLLM)
    modelo_chat: str = "gpt-5.4-mini"
    modelo_embeddings: str = "text-embedding-3-small"
    esforco_raciocinio: Esforco = "none"
    max_tokens_saida: int = 800
    limite_custo_sessao_usd: float = 0.50
    modo: Modo = "auto"

    @property
    def tem_chave(self) -> bool:
        """True se existe uma chave com formato plausível (começa com 'sk-')."""
        if self.openai_api_key is None:
            return False
        return self.openai_api_key.get_secret_value().strip().startswith("sk-")

    @property
    def usar_fake(self) -> bool:
        """Decide se o projeto deve usar os adaptadores simulados (sem custo)."""
        if self.modo == "fake":
            return True
        if self.modo == "openai":
            self.exigir_chave()
            return False
        return not self.tem_chave  # modo "auto"

    def exigir_chave(self) -> str:
        """Devolve a chave ou dispara um erro com instruções claras."""
        if not self.tem_chave:
            raise ChaveAusenteError(MENSAGEM_SEM_CHAVE)
        return self.openai_api_key.get_secret_value().strip()  # type: ignore[union-attr]


@lru_cache
def obter_config() -> Configuracoes:
    """Configuração única (cacheada) para todo o projeto."""
    return Configuracoes()


def descrever_ambiente() -> str:
    """Resumo do ambiente SEM revelar a chave."""
    cfg = obter_config()
    if cfg.usar_fake:
        situacao = "MODO FAKE (respostas simuladas, custo zero)"
    else:
        situacao = "MODO OPENAI (chave encontrada e oculta)"
    proxy = f" | proxy={cfg.openai_base_url}" if cfg.openai_base_url else ""
    return (
        f"{situacao} | modelo={cfg.modelo_chat} | embeddings={cfg.modelo_embeddings} "
        f"| esforço={cfg.esforco_raciocinio} | max_tokens={cfg.max_tokens_saida}{proxy}"
    )


if __name__ == "__main__":
    try:
        print(descrever_ambiente())
    except ChaveAusenteError as erro:
        print(erro)
        raise SystemExit(1) from None
