"""Smoke tests to catch import/syntax errors before they reach production.

RED: test_app_imports will fail if the FastAPI app module has a
SyntaxError or unimportable dependency (Issue #1 regression).
"""


def test_app_imports():
    """El módulo HTTP principal debe importarse y exponer la app."""
    from src.interface_adapters.http.main import app

    assert app is not None


def test_domain_imports():
    """La entidad de dominio Document debe importarse correctamente."""
    from src.domain.entities.document import Document

    assert Document is not None