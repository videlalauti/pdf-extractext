"""Tests for document CRUD use cases using InMemoryDocumentRepository."""

import pytest
from uuid import uuid4

from src.application.use_cases.delete_document import DeleteDocumentUseCase
from src.application.use_cases.get_document import GetDocumentUseCase
from src.application.use_cases.list_documents import ListDocumentsUseCase
from src.application.use_cases.update_document import UpdateDocumentUseCase
from src.domain.entities.document import Document
from src.domain.exceptions import DocumentNotFoundError
from src.interface_adapters.database.in_memory_document_repository import (
    InMemoryDocumentRepository,
)


@pytest.fixture
def repository():
    """Repositorio en memoria limpio para cada test."""
    return InMemoryDocumentRepository()


@pytest.fixture
def get_use_case(repository):
    return GetDocumentUseCase(repository)


@pytest.fixture
def list_use_case(repository):
    return ListDocumentsUseCase(repository)


@pytest.fixture
def update_use_case(repository):
    return UpdateDocumentUseCase(repository)


@pytest.fixture
def delete_use_case(repository):
    return DeleteDocumentUseCase(repository)


async def _save_document(repository, content="Original text", checksum="abc123"):
    """Guarda un documento de prueba y devuelve (id UUID, Document)."""
    doc_id = uuid4()
    doc = Document(id=str(doc_id), content=content, checksum=checksum)
    await repository.save(doc)
    return doc_id, doc


class TestUpdateDocumentUseCase:
    """Tests para UpdateDocumentUseCase."""

    @pytest.mark.asyncio
    async def test_update_document_success(self, repository, update_use_case):
        """Debe actualizar el contenido de un documento existente."""
        doc_id, doc = await _save_document(repository, content="Original text")

        updated = await update_use_case.execute(doc_id, "Updated text")

        assert updated.id == doc.id
        assert updated.content == "Updated text"
        assert updated.checksum == doc.checksum
        stored = await repository.find_by_id(doc_id)
        assert stored.content == "Updated text"

    @pytest.mark.asyncio
    async def test_update_document_not_found(self, update_use_case):
        """Debe lanzar DocumentNotFoundError si el documento no existe."""
        with pytest.raises(DocumentNotFoundError):
            await update_use_case.execute(uuid4(), "New content")


class TestDeleteDocumentUseCase:
    """Tests para DeleteDocumentUseCase."""

    @pytest.mark.asyncio
    async def test_delete_document_success(self, repository, delete_use_case):
        """Debe eliminar un documento existente."""
        doc_id, _ = await _save_document(repository)

        deleted = await delete_use_case.execute(doc_id)

        assert deleted is True
        assert await repository.find_by_id(doc_id) is None

    @pytest.mark.asyncio
    async def test_delete_document_not_found(self, delete_use_case):
        """Debe lanzar DocumentNotFoundError si el documento no existe."""
        with pytest.raises(DocumentNotFoundError):
            await delete_use_case.execute(uuid4())


class TestGetDocumentUseCase:
    """Tests para GetDocumentUseCase."""

    @pytest.mark.asyncio
    async def test_get_document_success(self, repository, get_use_case):
        """Debe recuperar un documento existente por ID."""
        doc_id, doc = await _save_document(repository, content="Get me")

        found = await get_use_case.execute(doc_id)

        assert found is not None
        assert found.id == doc.id
        assert found.content == "Get me"
        assert found.checksum == doc.checksum

    @pytest.mark.asyncio
    async def test_get_document_not_found(self, get_use_case):
        """Debe devolver None para un documento inexistente."""
        found = await get_use_case.execute(uuid4())

        assert found is None


class TestListDocumentsUseCase:
    """Tests para ListDocumentsUseCase."""

    @pytest.mark.asyncio
    async def test_list_documents_returns_list(self, repository, list_use_case):
        """Debe listar todos los documentos guardados."""
        await _save_document(repository, content="First")
        await _save_document(repository, content="Second")

        documents = await list_use_case.execute()

        assert isinstance(documents, list)
        assert len(documents) == 2