"""Tests para la validación compartida de extensión de archivo."""

from shared.domain.filename import has_pdf_extension


def test_accepts_lowercase_pdf():
    assert has_pdf_extension("document.pdf") is True


def test_accepts_uppercase_extensions():
    assert has_pdf_extension("DOCUMENT.PDF") is True


def test_rejects_other_extensions():
    assert has_pdf_extension("document.txt") is False


def test_rejects_almost_pdf_extension():
    assert has_pdf_extension("document.pdfx") is False


def test_rejects_none():
    assert has_pdf_extension(None) is False


def test_rejects_empty_string():
    assert has_pdf_extension("") is False
