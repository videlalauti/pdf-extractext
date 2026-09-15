"""Puertos de la capa de aplicación.

Los puertos definen las interfaces que la capa de aplicación expone
para que la infraestructura las implemente, siguiendo el principio de
Inversión de Dependencias (SOLID).
"""

from .text_extractor_port import TextExtractorPort

__all__ = ["TextExtractorPort"]
