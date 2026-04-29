"""PDF validation service."""

from dataclasses import dataclass
from typing import Optional

from src.domain.exceptions import InvalidPdfFormatError, PdfTooLargeError
from src.infrastructure.config.settings import settings


@dataclass(frozen=True)
class PdfValidationResult:
    """Result of PDF validation.

    Attributes:
        is_valid: Whether the file is a valid PDF
        error: Error message if validation failed, None otherwise
    """

    is_valid: bool
    error: Optional[str] = None


class PdfValidator:
    """Service for validating PDF files in memory.

    Validates:
    - Magic numbers (file signature)
    - Maximum file size
    """

    PDF_MAGIC_NUMBER = b"%PDF-"

    def __init__(self, max_size_bytes: Optional[int] = None):
        """Initialize validator with size limit.

        Args:
            max_size_bytes: Maximum allowed file size (default from settings)
        """
        self.max_size_bytes = max_size_bytes or settings.MAX_PDF_SIZE_BYTES

    def validate(self, file_content: bytes) -> PdfValidationResult:
        """Validate PDF file content without raising exceptions.

        Args:
            file_content: Raw bytes of the file to validate

        Returns:
            PdfValidationResult with validation status
        """
        size_error = self._validate_size(file_content)
        if size_error:
            return PdfValidationResult(is_valid=False, error=size_error)

        format_error = self._validate_format(file_content)
        if format_error:
            return PdfValidationResult(is_valid=False, error=format_error)

        return PdfValidationResult(is_valid=True)

    def validate_or_raise(self, file_content: bytes) -> PdfValidationResult:
        """Validate PDF and raise domain exception on failure.

        Args:
            file_content: Raw bytes of the file to validate

        Returns:
            PdfValidationResult if valid

        Raises:
            PdfTooLargeError: If file exceeds max size
            InvalidPdfFormatError: If file is not a valid PDF
        """
        size_error = self._validate_size(file_content)
        if size_error:
            raise PdfTooLargeError(
                max_size_bytes=self.max_size_bytes,
                actual_size_bytes=len(file_content),
            )

        format_error = self._validate_format(file_content)
        if format_error:
            raise InvalidPdfFormatError(format_error)

        return PdfValidationResult(is_valid=True)

    def _validate_size(self, file_content: bytes) -> Optional[str]:
        """Check if file size is within limits.

        Args:
            file_content: Raw bytes of the file

        Returns:
            Error message if too large, None otherwise
        """
        if not file_content:
            return "El archivo está vacío"

        if len(file_content) > self.max_size_bytes:
            return f"El archivo excede el tamaño máximo de {self.max_size_bytes} bytes"

        return None

    def _validate_format(self, file_content: bytes) -> Optional[str]:
        """Check if file has valid PDF magic number.

        Args:
            file_content: Raw bytes of the file

        Returns:
            Error message if invalid format, None otherwise
        """
        if not file_content.startswith(self.PDF_MAGIC_NUMBER):
            return "El archivo no tiene un formato PDF válido"

        return None
