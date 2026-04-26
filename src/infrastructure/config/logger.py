"""Configuración de logging estructurado - Factor XI 12-Factor App.

Emite logs a stdout (salida estándar), nunca a archivos físicos.
Los logs son capturados por el entorno de ejecución (contenedor/orquestador).
"""

import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any

from src.infrastructure.config.settings import settings


class StructuredLogFormatter(logging.Formatter):
    """Formateador de logs en JSON para consumo estructurado.

    Cumple con 12-Factor App Factor XI: Logs como flujo de eventos.
    """

    def format(self, record: logging.LogRecord) -> str:
        """Formatea el registro de log como JSON estructurado."""
        log_entry: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "service": settings.APP_NAME,
            "version": settings.VERSION,
        }

        # Agregar campos opcionales si existen
        if hasattr(record, "request_id"):
            log_entry["request_id"] = record.request_id

        if hasattr(record, "method"):
            log_entry["method"] = record.method

        if hasattr(record, "path"):
            log_entry["path"] = record.path

        if hasattr(record, "status_code"):
            log_entry["status_code"] = record.status_code

        if hasattr(record, "duration_ms"):
            log_entry["duration_ms"] = record.duration_ms

        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry, ensure_ascii=False)


def configure_logging() -> None:
    """Configura el logging estructurado para la aplicación.

    Configura el logger raíz para emitir a stdout en formato JSON.
    Cumple 12-Factor: los logs fluyen a stdout, no a archivos.
    """
    # Configurar logger raíz
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

    # Limpiar handlers existentes
    root_logger.handlers.clear()

    # Handler para stdout (salida estándar)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

    # Usar formato estructurado JSON en producción, simple en desarrollo
    if settings.DEBUG:
        simple_formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
        )
        stdout_handler.setFormatter(simple_formatter)
    else:
        structured_formatter = StructuredLogFormatter()
        stdout_handler.setFormatter(structured_formatter)

    root_logger.addHandler(stdout_handler)

    # Redirigir logs de librerías externas
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Retorna un logger configurado.

    Args:
        name: Nombre del logger (generalmente __name__).

    Returns:
        logging.Logger: Instancia del logger configurado.
    """
    return logging.getLogger(name)


# Configurar logging al importar el módulo
configure_logging()
