"""Adaptadores de la capa de infraestructura.

Los adaptadores implementan los puertos definidos por la capa de aplicación,
permitiendo que la lógica de negocio permanezca independiente de las
librerías y tecnologías externas.
"""

from .pypdf_text_extractor import PyPdfTextExtractor

__all__ = ["PyPdfTextExtractor"]
