# Imagem da API do assistente (Aula 8)
# Build:  docker build -t assistente-ia .
# Rodar:  docker run -p 8000:8000 -e OPENAI_API_KEY=$OPENAI_API_KEY assistente-ia
#         (sem a chave, a API sobe em modo fake)
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    RAIZ_PROJETO=/app

WORKDIR /app
RUN pip install --no-cache-dir uv

# Dependências primeiro (melhor uso do cache de camadas)
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev --no-install-project

# Código e dados
COPY src ./src
COPY dados ./dados
RUN uv sync --frozen --no-dev

# Nunca rode como root em produção
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

EXPOSE 8000
CMD ["uv", "run", "--no-sync", "uvicorn", "assistente_ia.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
