# Etapa de construcción
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS builder

# Configurar uv
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

# Directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY pyproject.toml uv.lock ./

# Instalar dependencias en un directorio virtual
RUN uv sync --frozen --no-install-project --no-dev

# Copiar el código fuente
COPY src ./src
COPY main.py ./

# Instalar el proyecto
RUN uv sync --frozen --no-dev

# Etapa de producción
FROM python:3.11-slim-bookworm AS production

# Configurar Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

# Crear usuario no root
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Directorio de trabajo
WORKDIR /app

# Copiar solo el entorno virtual desde el builder
COPY --from=builder --chown=appuser:appgroup /app/.venv /app/.venv
COPY --from=builder --chown=appuser:appgroup /app/src ./src
COPY --from=builder --chown=appuser:appgroup /app/main.py ./

# Agregar el entorno virtual al PATH
ENV PATH="/app/.venv/bin:$PATH"

# Cambiar al usuario no root
USER appuser

# Exponer el puerto
EXPOSE 8000

# Comando para ejecutar la aplicacion
CMD ["uvicorn", "src.interface_adapters.http.main:app", "--host", "0.0.0.0", "--port", "8000"]
