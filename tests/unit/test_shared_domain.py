def test_shared_validator_importable():
    from shared.domain.pdf_validator import PdfValidator

    assert PdfValidator is not None


def test_shared_extractor_importable():
    from shared.domain.pypdf_text_extractor import PyPdfTextExtractor

    assert PyPdfTextExtractor is not None


def test_shared_exceptions_importable():
    from shared.domain.exceptions import (
        InvalidPdfFormatError,
        PdfExtractionError,
        PdfTooLargeError,
    )

    assert PdfExtractionError and PdfTooLargeError and InvalidPdfFormatError


def test_max_pdf_size_constant_exists():
    from shared.domain.constants import MAX_PDF_SIZE_BYTES

    assert MAX_PDF_SIZE_BYTES == 10 * 1024 * 1024
