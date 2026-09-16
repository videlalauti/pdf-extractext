"""Tests de higiene: YAGNI/KISS y decisiones de arquitectura."""

from pathlib import Path


def test_main_py_uses_src_prefix():
    code = Path("main.py").read_text()
    assert "src.interface_adapters.http.main:app" in code


def test_no_services_external_dir():
    assert not Path("src/interface_adapters/services_external").exists()


def test_no_application_dtos_dir():
    assert not Path("src/application/dtos").exists()


def test_no_application_mappers_dir():
    assert not Path("src/application/mappers").exists()


def test_no_dead_dtos_in_use_cases():
    for uc in Path("src/application/use_cases").glob("*.py"):
        content = uc.read_text()
        assert "class UploadDocumentInput" not in content
        assert "class UploadDocumentOutput" not in content
        assert "class SaveDocumentInput" not in content
        assert "class SaveDocumentOutput" not in content
        assert "class UpdateDocumentInput" not in content
        assert "class UpdateDocumentOutput" not in content
        assert "class GetDocumentOutput" not in content
        assert "class ListDocumentsOutput" not in content
        assert "class DeleteDocumentOutput" not in content


def test_item_use_case_raises_domain_error():
    import pytest

    from src.application.use_cases.item_use_case import CreateItemUseCase
    from src.domain.exceptions import ValidationError
    from src.interface_adapters.database.in_memory_item_repository import InMemoryItemRepository

    repo = InMemoryItemRepository()
    with pytest.raises(ValidationError):
        CreateItemUseCase(repo).execute(name="", description="")


def test_no_utcnow_in_item_entity():
    code = Path("src/domain/entities/item.py").read_text()
    assert "utcnow" not in code


def test_no_dead_exports_in_adapters_init():
    code = Path("src/infrastructure/adapters/__init__.py").read_text()
    assert "get_db_connection" not in code
    assert "lifespan_handler" not in code
