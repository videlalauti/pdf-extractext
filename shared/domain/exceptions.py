"""Excepciones de dominio compartidas entre el monolith y los microservicios."""


class DomainError(Exception):
    """Base para errores de dominio; permite al caller tratar reglas de negocio."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class InvalidPdfFormatError(DomainError):
    """El input no parece un PDF; evita que bytes arbitrarios avancen al pipeline."""

    def __init__(self, message: str = "El archivo no tiene un formato PDF válido"):
        super().__init__(message)


class PdfTooLargeError(DomainError):
    """El PDF excede el límite configurado; protege memoria y ancho de banda."""

    def __init__(
        self,
        max_size_bytes: int = 0,
        actual_size_bytes: int = 0,
        message: str = "El archivo PDF excede el tamaño máximo permitido",
    ):
        self.max_size_bytes = max_size_bytes
        self.actual_size_bytes = actual_size_bytes
        super().__init__(message)


class PdfExtractionError(DomainError):
    """No se pudo extraer texto; conserva la causa original para diagnóstico."""

    def __init__(
        self,
        message: str = "Error al extraer texto del PDF",
        original_error: Exception | None = None,
    ):
        self.original_error = original_error
        super().__init__(message)