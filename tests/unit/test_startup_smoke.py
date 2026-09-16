"""Smoke test: verify the application can be imported without errors."""


def test_main_app_imports():
    from src.interface_adapters.http.main import app

    assert app is not None


def test_domain_imports():
    from src.domain.entities.document import Document
    from src.domain.exceptions import DomainError

    assert Document is not None
    assert DomainError is not None


def test_application_imports():
    from src.application.ports.text_extractor_port import TextExtractorPort
    from src.application.services.pdf_validator import PdfValidator

    assert TextExtractorPort is not None
    assert PdfValidator is not None


def test_infrastructure_imports():
    from src.infrastructure.adapters.pypdf_text_extractor import PyPdfTextExtractor
    from src.infrastructure.config.settings import settings

    assert PyPdfTextExtractor is not None
    assert settings is not None