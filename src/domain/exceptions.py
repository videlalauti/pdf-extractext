"""Domain exceptions for business rule violations.

Las excepciones de validación/extracción de PDF se re-exportan desde
shared.domain.exceptions para mantener una única fuente de verdad.
"""

from shared.domain.exceptions import (
    DomainError,
    InvalidPdfFormatError,
    PdfExtractionError,
    PdfTooLargeError,
)

__all__ = [
    "DomainError",
    "InvalidPdfFormatError",
    "PdfExtractionError",
    "PdfTooLargeError",
    "ValidationError",
    "DocumentNotFoundError",
    "DuplicateDocumentError",
]


class ValidationError(DomainError):
    """Exception raised when validation of a domain entity fails."""

    def __init__(self, message: str = "Validation failed"):
        super().__init__(message)


class DocumentNotFoundError(DomainError):
    """Exception raised when a document does not exist."""

    def __init__(self, document_id: str):
        self.document_id = document_id
        super().__init__(f"Documento con ID {document_id} no encontrado")


class DuplicateDocumentError(DomainError):
    """Exception raised when a duplicate document is saved."""

    def __init__(self, checksum: str):
        self.checksum = checksum
        super().__init__(f"Documento con checksum {checksum} ya existe")
