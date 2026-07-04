"""PDF validation service."""

from dataclasses import dataclass
from typing import Optional


MAX_PDF_SIZE_BYTES = 10 * 1024 * 1024


@dataclass(frozen=True)
class PdfValidationResult:
    is_valid: bool
    error: Optional[str] = None


class PdfValidator:
    PDF_MAGIC_NUMBER = b"%PDF-"

    def __init__(self, max_size_bytes: Optional[int] = None):
        self.max_size_bytes = max_size_bytes or MAX_PDF_SIZE_BYTES

    def validate(self, file_content: bytes) -> PdfValidationResult:
        size_error = self._validate_size(file_content)
        if size_error:
            return PdfValidationResult(is_valid=False, error=size_error)

        format_error = self._validate_format(file_content)
        if format_error:
            return PdfValidationResult(is_valid=False, error=format_error)

        return PdfValidationResult(is_valid=True)

    def _validate_size(self, file_content: bytes) -> Optional[str]:
        if not file_content:
            return "El archivo está vacío"

        if len(file_content) > self.max_size_bytes:
            return f"El archivo excede el tamaño máximo de {self.max_size_bytes} bytes"

        return None

    def _validate_format(self, file_content: bytes) -> Optional[str]:
        if not file_content.startswith(self.PDF_MAGIC_NUMBER):
            return "El archivo no tiene un formato PDF válido"

        return None
