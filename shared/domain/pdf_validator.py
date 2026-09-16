"""Validación de PDF en memoria, compartida entre monolith y microservicios."""

from dataclasses import dataclass
from typing import Optional

from shared.domain.exceptions import InvalidPdfFormatError, PdfTooLargeError


@dataclass(frozen=True)
class PdfValidationResult:
    """Resultado sin excepciones: el caller decide cómo traducir el error."""

    is_valid: bool
    error: Optional[str] = None


class PdfValidator:
    """Valida bytes en memoria para no introducir I/O de disco en el pipeline."""

    PDF_MAGIC_NUMBER = b"%PDF-"

    def __init__(self, max_size_bytes: int) -> None:
        # Obligatorio: el límite lo decide el consumidor, nunca un default oculto
        self.max_size_bytes = max_size_bytes

    def validate(self, pdf_bytes: bytes) -> PdfValidationResult:
        """Retorna resultado sin lanzar, apto para endpoints que responden 200/400."""
        size_error = self._validate_size(pdf_bytes)
        if size_error:
            return PdfValidationResult(is_valid=False, error=size_error)

        format_error = self._validate_format(pdf_bytes)
        if format_error:
            return PdfValidationResult(is_valid=False, error=format_error)

        return PdfValidationResult(is_valid=True)

    def validate_or_raise(self, pdf_bytes: bytes) -> PdfValidationResult:
        """Lanza excepciones de dominio para flujos que requieren error 4xx."""
        size_error = self._validate_size(pdf_bytes)
        if size_error:
            raise PdfTooLargeError(
                max_size_bytes=self.max_size_bytes,
                actual_size_bytes=len(pdf_bytes),
            )

        format_error = self._validate_format(pdf_bytes)
        if format_error:
            raise InvalidPdfFormatError(format_error)

        return PdfValidationResult(is_valid=True)

    def _validate_size(self, pdf_bytes: bytes) -> Optional[str]:
        """Limitar el tamaño evita DoS por memoria en servicios sin backpressure."""
        if not pdf_bytes:
            return "El archivo está vacío"

        if len(pdf_bytes) > self.max_size_bytes:
            return f"El archivo excede el tamaño máximo de {self.max_size_bytes} bytes"

        return None

    def _validate_format(self, pdf_bytes: bytes) -> Optional[str]:
        """El magic number filtra archivos que pypdf no podría parsear."""
        if not pdf_bytes.startswith(self.PDF_MAGIC_NUMBER):
            return "El archivo no tiene un formato PDF válido"

        return None