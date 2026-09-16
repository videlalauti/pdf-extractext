"""Tests de acoplamiento: rutas HTTP no dependen de adaptadores concretos ni anti-patrones TDD."""

from pathlib import Path


def test_mongodb_connection_has_public_ping():
    from src.infrastructure.adapters.mongodb_connection import MongoDBConnection

    assert hasattr(MongoDBConnection, "ping")


def test_health_route_does_not_use_underscore_client():
    code = Path("src/interface_adapters/http/routes/health_routes.py").read_text()
    assert "_client" not in code


def test_upload_document_test_does_not_use_call_str():
    code = Path("tests/unit/test_upload_document_use_case.py").read_text()
    assert "str(call)" not in code


def test_documents_api_has_no_asyncio_run():
    code = Path("tests/integration/test_documents_api.py").read_text()
    assert "asyncio.run" not in code


def test_composition_is_not_in_documents_routes():
    code = Path("src/interface_adapters/http/routes/documents_routes.py").read_text()
    assert "PyPdfTextExtractor()" not in code
    assert "PdfValidator(" not in code
