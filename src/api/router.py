"""Configuración de routers de la API."""

from fastapi import FastAPI

from src.api.v1.endpoints.items import router as items_router

API_V1_PREFIX = "/api/v1"


def register_routers(app: FastAPI) -> None:
    """Registra todos los routers en la aplicación.

    Args:
        app: Instancia de FastAPI.
    """
    app.include_router(items_router, prefix=API_V1_PREFIX)
