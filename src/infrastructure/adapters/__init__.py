"""Adaptadores de la capa de infraestructura.

Los adaptadores implementan los puertos definidos por la capa de aplicación,
permitiendo que la lógica de negocio permanezca independiente de las
librerías y tecnologías externas.
"""

from .mongodb_connection import (
    MongoDBConnection,
    get_db_connection,
    lifespan_handler,
    mongodb_connection,
)
from .pypdf_text_extractor import PyPdfTextExtractor

__all__ = [
    "PyPdfTextExtractor",
    "MongoDBConnection",
    "mongodb_connection",
    "get_db_connection",
    "lifespan_handler",
]
