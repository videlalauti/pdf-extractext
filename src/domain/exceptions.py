"""Domain exceptions for business rule violations."""


class DomainError(Exception):
    """Base exception for domain errors."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class InvalidPdfFormatError(DomainError):
    """Exception raised when a file is not a valid PDF."""

    def __init__(self, message: str = "El archivo no tiene un formato PDF válido"):
        super().__init__(message)


class PdfTooLargeError(DomainError):
    """Exception raised when a PDF exceeds maximum allowed size."""

    def __init__(
        self,
        max_size_bytes: int = 0,
        actual_size_bytes: int = 0,
        message: str = "El archivo PDF excede el tamaño máximo permitido",
    ):
        self.max_size_bytes = max_size_bytes
        self.actual_size_bytes = actual_size_bytes
        super().__init__(message)
