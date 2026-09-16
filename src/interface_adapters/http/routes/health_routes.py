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
        if await mongodb_connection.ping():
            return {"status": "ok"}
        await mongodb_connection.connect()
        return {"status": "ok"}
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unavailable",
        ) from error
