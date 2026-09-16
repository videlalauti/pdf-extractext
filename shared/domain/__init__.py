"""Paquete compartido: dominio puro reutilizable entre monolith y microservicios."""

from shared.domain.constants import MAX_PDF_SIZE_BYTES
from shared.domain.exceptions import (
    DomainError,
    InvalidPdfFormatError,
    PdfExtractionError,
    PdfTooLargeError,
)
from shared.domain.pdf_validator import PdfValidationResult, PdfValidator
from shared.domain.pypdf_text_extractor import PyPdfTextExtractor

__all__ = [
    "DomainError",
    "InvalidPdfFormatError",
    "MAX_PDF_SIZE_BYTES",
    "PdfExtractionError",
    "PdfTooLargeError",
    "PdfValidationResult",
    "PdfValidator",
    "PyPdfTextExtractor",
]