FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS dependencies

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project --no-dev

FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS builder

WORKDIR /app

COPY --from=dependencies /app/.venv ./.venv

COPY pyproject.toml uv.lock ./
COPY src ./src
COPY main.py ./

RUN uv sync --frozen --no-dev

FROM python:3.14-slim-bookworm AS production

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PATH="/app/.venv/bin:$PATH"

RUN groupadd -r appgroup && useradd -r -g appgroup appuser

WORKDIR /app

COPY --from=builder --chown=appuser:appgroup /app/.venv /app/.venv
COPY --from=builder --chown=appuser:appgroup /app/src ./src
COPY --from=builder --chown=appuser:appgroup /app/main.py ./

RUN rm -rf /root/.cache /tmp/* /var/cache/apt/archives/* /var/lib/apt/lists/*

USER appuser

EXPOSE 8000

CMD ["uvicorn", "src.interface_adapters.http.main:app", "--host", "0.0.0.0", "--port", "8000"]
