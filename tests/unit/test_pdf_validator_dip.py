from src.application.services.pdf_validator import PdfValidator


def test_pdf_validator_works_without_infrastructure_import():
    validator = PdfValidator(max_size_bytes=1024)
    assert validator.max_size_bytes == 1024


def test_pdf_validator_rejects_oversized_pdf():
    validator = PdfValidator(max_size_bytes=100)
    pdf = b"%PDF-1.4" + b"x" * 200
    result = validator.validate(pdf)
    assert result.is_valid is False
