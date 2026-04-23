"""Tests de integración para endpoints de documentos."""

from http import HTTPStatus
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from src.domain.entities.document import Document
from src.interface_adapters.database.repository_provider import (
    get_document_repository,
    reset_repository,
)
from src.interface_adapters.http.main import app


@pytest.fixture(autouse=True)
def reset_state():
    """Resetea el estado antes de cada test."""
    reset_repository()


@pytest.fixture
def client():
    """Provee un cliente de test."""
    return TestClient(app)


@pytest.fixture
async def sample_document():
    """Crea un documento de prueba."""
    repo = get_document_repository()
    doc = Document(
        id=str(uuid4()),
        content="Sample extracted text from PDF",
        checksum="abc123def456",
    )
    await repo.save(doc)
    return doc


class TestDocumentsApi:
    """Tests de integración para la API de documentos."""

    def test_list_documents_empty(self, client):
        """GET /documents debe retornar lista vacía inicialmente."""
        response = client.get("/api/v1/documents")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == []

    def test_get_document_not_found(self, client):
        """GET /documents/{id} debe retornar 404 para ID inexistente."""
        response = client.get(f"/api/v1/documents/{uuid4()}")

        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_update_document_not_found(self, client):
        """PUT /documents/{id} debe retornar 404 para ID inexistente."""
        response = client.put(
            f"/api/v1/documents/{uuid4()}",
            json={"content": "New content"},
        )

        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_delete_document_not_found(self, client):
        """DELETE /documents/{id} debe retornar 404 para ID inexistente."""
        response = client.delete(f"/api/v1/documents/{uuid4()}")

        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_full_document_lifecycle(self, client):
        """Flujo completo: crear, obtener, actualizar, eliminar."""
        import asyncio

        # Create document directly via repository
        repo = get_document_repository()
        doc_id = str(uuid4())
        doc = Document(
            id=doc_id,
            content="Original text",
            checksum="original_checksum",
        )
        asyncio.run(repo.save(doc))

        # Get - verify exists
        get_response = client.get(f"/api/v1/documents/{doc_id}")
        assert get_response.status_code == HTTPStatus.OK
        data = get_response.json()
        assert data["content"] == "Original text"
        assert data["checksum"] == "original_checksum"

        # List - verify appears in list
        list_response = client.get("/api/v1/documents")
        assert list_response.status_code == HTTPStatus.OK
        assert len(list_response.json()) == 1

        # Update
        update_response = client.put(
            f"/api/v1/documents/{doc_id}",
            json={"content": "Updated text content"},
        )
        assert update_response.status_code == HTTPStatus.OK
        updated_data = update_response.json()
        assert updated_data["content"] == "Updated text content"
        # Checksum should remain the same (not updating the file)
        assert updated_data["checksum"] == "original_checksum"

        # Get again - verify update
        get_after_update = client.get(f"/api/v1/documents/{doc_id}")
        assert get_after_update.status_code == HTTPStatus.OK
        assert get_after_update.json()["content"] == "Updated text content"

        # Delete
        delete_response = client.delete(f"/api/v1/documents/{doc_id}")
        assert delete_response.status_code == HTTPStatus.NO_CONTENT

        # Verify deletion
        get_after_delete = client.get(f"/api/v1/documents/{doc_id}")
        assert get_after_delete.status_code == HTTPStatus.NOT_FOUND
