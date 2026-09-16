"""Fixtures compartidas para tests de integración de microservicios."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

VALIDATION_DIR = str(PROJECT_ROOT / "services" / "validation-service")
EXTRACTION_DIR = str(PROJECT_ROOT / "services" / "extraction-service")
PERSISTENCE_DIR = str(PROJECT_ROOT / "services" / "persistence-service")


def _add_to_sys_path(directory: str) -> None:
    if directory not in sys.path:
        sys.path.insert(0, directory)


@pytest.fixture
def validation_client():
    """TestClient para validation-service."""
    _add_to_sys_path(VALIDATION_DIR)
    from services.validation_service.main import app as validation_app

    return TestClient(validation_app)


@pytest.fixture
def extraction_client():
    """TestClient para extraction-service (mock persistence HTTP)."""
    _add_to_sys_path(EXTRACTION_DIR)

    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"id": "mock-doc-001", "content": "", "checksum": "abc"}
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.AsyncClient.post", return_value=mock_response):
        from services.extraction_service.main import app as extraction_app

        return TestClient(extraction_app)


@pytest.fixture
def persistence_client():
    """TestClient para persistence-service (mock MongoDB)."""
    _add_to_sys_path(PERSISTENCE_DIR)

    with (
        patch("persistence.mongodb_connection.MongoDBConnection") as mock_conn_cls,
        patch("persistence.repository.DocumentRepository") as mock_repo_cls,
    ):
        mock_conn_cls.return_value = MagicMock()
        mock_repo = MagicMock()
        mock_repo_cls.return_value = mock_repo

        # In-memory store keyed by doc_id
        _store: dict[str, dict] = {}

        def _create(doc_id, content, checksum):
            from uuid import uuid4

            did = doc_id or str(uuid4())
            doc = {"id": did, "content": content, "checksum": checksum}
            _store[did] = doc
            return doc

        def _get(doc_id):
            if doc_id not in _store:
                from fastapi import HTTPException

                raise HTTPException(status_code=404, detail="Document not found")
            return _store[doc_id]

        def _list_all():
            return list(_store.values())

        def _update(doc_id, content=None, checksum=None):
            if doc_id not in _store:
                from fastapi import HTTPException

                raise HTTPException(status_code=404, detail="Document not found")
            doc = _store[doc_id]
            if content is not None:
                doc["content"] = content
            if checksum is not None:
                doc["checksum"] = checksum
            return doc

        def _delete(doc_id):
            if doc_id not in _store:
                from fastapi import HTTPException

                raise HTTPException(status_code=404, detail="Document not found")
            del _store[doc_id]

        mock_repo.create = MagicMock(side_effect=_create)
        mock_repo.get = MagicMock(side_effect=_get)
        mock_repo.list_all = MagicMock(side_effect=_list_all)
        mock_repo.update = MagicMock(side_effect=_update)
        mock_repo.delete = MagicMock(side_effect=_delete)

        from services.persistence_service.main import app as persistence_app

        client = TestClient(persistence_app)
        yield client
        _store.clear()
