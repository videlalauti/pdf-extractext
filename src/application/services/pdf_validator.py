"""Re-export del validador de PDF desde el paquete compartido de dominio."""

from shared.domain.pdf_validator import PdfValidationResult, PdfValidator

__all__ = ["PdfValidationResult", "PdfValidator"]
