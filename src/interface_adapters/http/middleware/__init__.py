"""Middlewares de la capa de interface adapters HTTP.

Middlewares para interceptar y procesar requests/responses.
"""

from .logging_middleware import LoggingMiddleware

__all__ = ["LoggingMiddleware"]
