"""Punto de entrada principal de la aplicación."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.router import register_routers
from src.config import ApplicationConfig


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestiona el ciclo de vida de la aplicación."""
    # Startup
    yield
    # Shutdown


def create_application() -> FastAPI:
    """Crea y configura la instancia de FastAPI.

    Returns:
        FastAPI: Instancia configurada de la aplicación.
    """
    config = ApplicationConfig()

    app = FastAPI(
        title=config.app_name,
        version=config.version,
        description=config.description,
        docs_url="/docs" if config.debug else None,
        redoc_url="/redoc" if config.debug else None,
        lifespan=lifespan,
    )

    register_routers(app)

    return app


app = create_application()
