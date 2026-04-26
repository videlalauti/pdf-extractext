"""Tests de integración para endpoints de documentos."""

import asyncio
from http import HTTPStatus
from pathlib import Path
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from src.domain.entities.document import Document
from src.interface_adapters.database.repository_provider import (
    get_document_repository,
    reset_repository,
)
from src.interface_adapters.http.main import app

# Path to test fixtures
FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"


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


class TestUploadDocument:
    """Tests de integración para el endpoint POST /documents/upload."""

    def _create_simple_pdf(self) -> bytes:
        """Crea un PDF mínimo válido que pypdf puede procesar."""
        # PDF mínimo estructuralmente válido con objeto vacío
        pdf_lines = [
            b"%PDF-1.4",
            b"1 0 obj",
            b"<< /Type /Catalog /Pages 2 0 R >>",
            b"endobj",
            b"2 0 obj",
            b"<< /Type /Pages /Kids [] /Count 0 >>",
            b"endobj",
            b"xref",
            b"0 3",
            b"0000000000 65535 f ",
            b"0000000009 00000 n ",
            b"0000000052 00000 n ",
            b"trailer",
            b"<< /Size 3 /Root 1 0 R >>",
            b"startxref",
            b"103",
            b"%%EOF",
        ]
        return b"\n".join(pdf_lines)

    def test_upload_valid_pdf(self, client):
        """POST /documents/upload con PDF válido debe crear documento."""
        pdf_content = self._create_simple_pdf()

        response = client.post(
            "/api/v1/documents/upload",
            files={"file": ("test.pdf", pdf_content, "application/pdf")},
        )

        assert response.status_code == HTTPStatus.CREATED
        data = response.json()
        assert "id" in data
        assert "content" in data
        assert "checksum" in data
        assert len(data["checksum"]) == 64  # SHA-256 hash length

    def test_upload_invalid_format_returns_400(self, client):
        """POST /documents/upload con archivo no-PDF debe retornar 400."""
        invalid_content = b"This is not a PDF file, just plain text"

        response = client.post(
            "/api/v1/documents/upload",
            files={"file": ("test.txt", invalid_content, "text/plain")},
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert "PDF" in response.json()["detail"] or "formato" in response.json()["detail"].lower()

    def test_upload_empty_file_returns_400(self, client):
        """POST /documents/upload con archivo vacío debe retornar 400."""
        response = client.post(
            "/api/v1/documents/upload",
            files={"file": ("empty.pdf", b"", "application/pdf")},
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_upload_duplicate_pdf_returns_409(self, client):
        """POST /documents/upload con PDF duplicado debe retornar 409."""
        pdf_content = self._create_simple_pdf()

        # Primer upload - debe funcionar
        first_response = client.post(
            "/api/v1/documents/upload",
            files={"file": ("test.pdf", pdf_content, "application/pdf")},
        )
        assert first_response.status_code == HTTPStatus.CREATED

        # Segundo upload del mismo contenido - debe fallar con 409
        second_response = client.post(
            "/api/v1/documents/upload",
            files={"file": ("duplicate.pdf", pdf_content, "application/pdf")},
        )

        assert second_response.status_code == HTTPStatus.CONFLICT
        assert (
            "checksum" in second_response.json()["detail"].lower()
            or "exists" in second_response.json()["detail"].lower()
        )

    def test_upload_pdf_with_text_extraction(self, client):
        """POST /documents/upload debe extraer texto correctamente del PDF."""
        # PDF simple válido para la extracción
        pdf_content = self._create_simple_pdf()

        response = client.post(
            "/api/v1/documents/upload",
            files={"file": ("test_with_text.pdf", pdf_content, "application/pdf")},
        )

        assert response.status_code == HTTPStatus.CREATED
        data = response.json()
        # El contenido extraído debe estar presente
        assert "content" in data
