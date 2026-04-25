"""Configuración de routers de la API."""

from fastapi import FastAPI

from src.interface_adapters.http.routes.documents_routes import router as documents_router
from src.interface_adapters.http.routes.health_routes import router as health_router
from src.interface_adapters.http.routes.items_routes import router as items_router

API_V1_PREFIX = "/api/v1"


def register_routers(app: FastAPI) -> None:
    """Registra todos los routers en la aplicación.

    Args:
        app: Instancia de FastAPI.
    """
    # Health check endpoint (sin prefijo)
    app.include_router(health_router)

    # API endpoints con prefijo
    app.include_router(items_router, prefix=API_V1_PREFIX)
    app.include_router(documents_router, prefix=API_V1_PREFIX)
