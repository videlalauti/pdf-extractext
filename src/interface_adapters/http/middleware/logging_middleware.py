"""Middleware de logging para FastAPI - Factor XI 12-Factor App.

Intercepta todas las peticiones HTTP y registra información estructurada.
"""

import time
import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from src.infrastructure.config.logger import get_logger

logger = get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware que registra todas las peticiones HTTP.

    Captura método, ruta, status code y tiempo de procesamiento.
    Cumple con 12-Factor App Factor XI: Logs como flujo de eventos.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Procesa la petición y registra métricas.

        Args:
            request: Petición HTTP entrante.
            call_next: Función para continuar con el procesamiento.

        Returns:
            Response: Respuesta HTTP generada.
        """
        # Generar ID único para la petición
        request_id = str(uuid.uuid4())[:8]
        request.state.request_id = request_id

        # Capturar tiempo de inicio
        start_time = time.perf_counter()

        # Extraer información de la petición
        method = request.method
        path = request.url.path
        client_host = request.client.host if request.client else "unknown"

        # Log de inicio de petición
        logger.info(
            f"Request started: {method} {path}",
            extra={
                "request_id": request_id,
                "method": method,
                "path": path,
                "client_host": client_host,
            },
        )

        try:
            # Procesar la petición
            response = await call_next(request)

            # Calcular duración
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            status_code = response.status_code

            # Log de completitud
            logger.info(
                f"Request completed: {method} {path} {status_code} in {duration_ms}ms",
                extra={
                    "request_id": request_id,
                    "method": method,
                    "path": path,
                    "status_code": status_code,
                    "duration_ms": duration_ms,
                    "client_host": client_host,
                },
            )

            # Agregar headers de trazabilidad
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Response-Time"] = f"{duration_ms}ms"

            return response

        except Exception as exc:
            # Calcular duración incluso en error
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

            # Log de error
            logger.error(
                f"Request failed: {method} {path} in {duration_ms}ms",
                extra={
                    "request_id": request_id,
                    "method": method,
                    "path": path,
                    "duration_ms": duration_ms,
                    "client_host": client_host,
                    "error": str(exc),
                },
                exc_info=True,
            )
            raise
