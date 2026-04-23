"""Tests for PDF validator."""

import pytest

from src.application.services.pdf_validator import PdfValidator
from src.domain.exceptions import InvalidPdfFormatError, PdfTooLargeError


class TestPdfValidator:
    """Test cases for PDF validation service."""

    def test_should_validate_valid_pdf_file(self):
        """Test that a valid PDF file passes validation."""
        pdf_bytes = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n>>\nendobj\n%%EOF"
        max_size_bytes = 10 * 1024 * 1024  # 10MB

        validator = PdfValidator(max_size_bytes=max_size_bytes)

        result = validator.validate(pdf_bytes)

        assert result.is_valid is True
        assert result.error is None

    def test_should_reject_empty_file(self):
        """Test that empty file is rejected."""
        empty_bytes = b""
        max_size_bytes = 10 * 1024 * 1024

        validator = PdfValidator(max_size_bytes=max_size_bytes)

        result = validator.validate(empty_bytes)

        assert result.is_valid is False
        assert result.error is not None
        assert "vacío" in result.error.lower() or "empty" in result.error.lower()

    def test_should_reject_file_without_pdf_magic_number(self):
        """Test that file without PDF magic number is rejected."""
        fake_pdf = b"This is not a PDF file, just plain text"
        max_size_bytes = 10 * 1024 * 1024

        validator = PdfValidator(max_size_bytes=max_size_bytes)

        result = validator.validate(fake_pdf)

        assert result.is_valid is False
        assert result.error is not None
        assert "formato" in result.error.lower() or "format" in result.error.lower()

    def test_should_reject_file_with_wrong_extension_but_no_magic_number(self):
        """Test that file with wrong extension is rejected (checking magic numbers)."""
        fake_pdf_with_header = b"RIFF....fake content"
        max_size_bytes = 10 * 1024 * 1024

        validator = PdfValidator(max_size_bytes=max_size_bytes)

        result = validator.validate(fake_pdf_with_header)

        assert result.is_valid is False
        assert result.error is not None

    def test_should_reject_file_exceeding_max_size(self):
        """Test that file exceeding max size is rejected."""
        small_max_size = 100  # 100 bytes
        large_pdf = b"%PDF-1.4" + b"x" * 500  # Larger than 100 bytes

        validator = PdfValidator(max_size_bytes=small_max_size)

        result = validator.validate(large_pdf)

        assert result.is_valid is False
        assert result.error is not None
        assert "tamaño" in result.error.lower() or "size" in result.error.lower()

    def test_should_reject_file_exactly_at_max_size(self):
        """Test edge case: file exactly at max size limit."""
        max_size = 100
        pdf = b"%PDF-1.4" + b"x" * 92  # Exactly 100 bytes

        validator = PdfValidator(max_size_bytes=max_size)

        result = validator.validate(pdf)

        assert result.is_valid is True

    def test_should_validate_with_different_pdf_versions(self):
        """Test validation works with different PDF versions."""
        versions = [b"%PDF-1.0", b"%PDF-1.3", b"%PDF-1.4", b"%PDF-1.7", b"%PDF-2.0"]

        for version in versions:
            validator = PdfValidator(max_size_bytes=1024 * 1024)
            result = validator.validate(version)
            assert result.is_valid is True, f"Version {version} should be valid"

    def test_should_validate_minimal_valid_pdf(self):
        """Test that minimal PDF structure is accepted."""
        minimal_pdf = b"%PDF-1.4"

        validator = PdfValidator(max_size_bytes=1024)

        result = validator.validate(minimal_pdf)

        assert result.is_valid is True

    def test_should_raise_domain_exception_for_invalid_format(self):
        """Test that invalid format raises domain exception."""
        invalid_file = b"Not a PDF"

        validator = PdfValidator(max_size_bytes=1024 * 1024)

        with pytest.raises(InvalidPdfFormatError):
            validator.validate_or_raise(invalid_file)

    def test_should_raise_domain_exception_for_oversized_file(self):
        """Test that oversized file raises domain exception."""
        small_max_size = 50
        large_pdf = b"%PDF-1.4" + b"x" * 100

        validator = PdfValidator(max_size_bytes=small_max_size)

        with pytest.raises(PdfTooLargeError):
            validator.validate_or_raise(large_pdf)

    def test_should_not_raise_exception_for_valid_pdf(self):
        """Test that valid PDF does not raise exception."""
        valid_pdf = b"%PDF-1.4"

        validator = PdfValidator(max_size_bytes=1024)

        # Should not raise
        result = validator.validate_or_raise(valid_pdf)

        assert result.is_valid is True
