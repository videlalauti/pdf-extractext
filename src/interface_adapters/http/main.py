"""Punto de entrada principal de la aplicación FastAPI."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.infrastructure.config.logger import configure_logging, get_logger
from src.infrastructure.config.settings import settings
from src.interface_adapters.http.middleware.logging_middleware import (
    LoggingMiddleware,
)
from src.interface_adapters.http.router import register_routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestiona el ciclo de vida de la aplicación."""
    # Startup: configurar logging
    configure_logging()
    logger = get_logger(__name__)
    logger.info(f"Starting {settings.app_name} v{settings.version}")

    yield

    # Shutdown
    logger.info(f"Shutting down {settings.app_name}")


def create_application() -> FastAPI:
    """Crea y configura la instancia de FastAPI.

    Returns:
        FastAPI: Instancia configurada de la aplicación.
    """
    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        description=settings.description,
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        lifespan=lifespan,
    )

    # Agregar middleware de logging
    app.add_middleware(LoggingMiddleware)

    register_routers(app)

    return app


app = create_application()
