"""Re-export del extractor pypdf desde el paquete compartido de dominio."""

from shared.domain.pypdf_text_extractor import PyPdfTextExtractor

__all__ = ["PyPdfTextExtractor"]
