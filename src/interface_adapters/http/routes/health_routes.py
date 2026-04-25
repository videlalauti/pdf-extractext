"""Rutas para el endpoint de health check."""

from fastapi import APIRouter, HTTPException
from starlette import status

from src.infrastructure.adapters.mongodb_connection import mongodb_connection

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    """Endpoint de health check que verifica la conexión a MongoDB.

    Returns:
        dict: Estado de salud del servicio.

    Raises:
        HTTPException: 503 si la base de datos no está disponible.
    """
    try:
        # Intentar hacer ping a la base de datos
        if mongodb_connection.is_connected:
            await mongodb_connection._client.admin.command("ping")
            return {"status": "ok"}
        else:
            # Intentar conectar si no está conectado
            await mongodb_connection.connect()
            return {"status": "ok"}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unavailable",
        )
