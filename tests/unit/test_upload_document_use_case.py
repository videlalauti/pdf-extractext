"""Tests for UploadDocumentUseCase (TDD, Issue #5 refactor).

RED: each test was written first; the use case was already implemented
during the Issue #5 refactor, so they should pass (GREEN).
Mocks: DocumentRepository and TextExtractorPort.
"""

import hashlib
from unittest.mock import AsyncMock, create_autospec

import pytest

from src.application.ports.text_extractor_port import TextExtractorPort
from src.application.services.pdf_validator import PdfValidator
from src.application.use_cases.upload_document import UploadDocumentUseCase
from src.domain.entities.document import Document
from src.domain.exceptions import DuplicateDocumentError, InvalidPdfFormatError
from src.domain.repositories.document_repository import DocumentRepository


@pytest.fixture
def repository():
    """Mock del repositorio de documentos."""
    return create_autospec(DocumentRepository, instance=True)


@pytest.fixture
def extractor():
    """Mock del puerto de extracción de texto."""
    return create_autospec(TextExtractorPort, instance=True)


def make_use_case(repository, extractor, validator=None):
    """Construye el caso de uso con las dependencias inyectadas."""
    return UploadDocumentUseCase(
        repository=repository,
        extractor=extractor,
        validator=validator,
    )


@pytest.mark.asyncio
async def test_upload_valid_pdf_returns_document(repository, extractor):
    """Un PDF válido debe persistirse y devolverse como Document."""
    extractor.extract_text_from_bytes = AsyncMock(return_value="texto extraido")
    repository.exists_by_checksum = AsyncMock(return_value=False)

    async def fake_save(document: Document) -> Document:
        return document

    repository.save = AsyncMock(side_effect=fake_save)

    use_case = make_use_case(repository, extractor)
    pdf_bytes = b"%PDF-1.4" + b"x" * 50

    result = await use_case.execute(pdf_bytes, "test.pdf")

    assert isinstance(result, Document)
    assert result.content == "texto extraido"
    assert result.checksum == hashlib.sha256(pdf_bytes).hexdigest()
    repository.save.assert_called_once()


@pytest.mark.asyncio
async def test_upload_duplicate_checksum_raises_error(repository, extractor):
    """Un checksum existente debe lanzar DuplicateDocumentError."""
    extractor.extract_text_from_bytes = AsyncMock(return_value="texto extraido")
    repository.exists_by_checksum = AsyncMock(return_value=True)

    use_case = make_use_case(repository, extractor)

    with pytest.raises(DuplicateDocumentError):
        await use_case.execute(b"%PDF-1.4" + b"y" * 50, "duplicate.pdf")

    repository.save.assert_not_called()


@pytest.mark.asyncio
async def test_upload_invalid_pdf_format_raises_error(repository, extractor):
    """Un archivo que no es PDF debe lanzar InvalidPdfFormatError."""
    validator = PdfValidator(max_size_bytes=1024 * 1024)
    use_case = make_use_case(repository, extractor, validator=validator)

    with pytest.raises(InvalidPdfFormatError):
        await use_case.execute(b"not a pdf at all", "test.txt")

    extractor.extract_text_from_bytes.assert_not_called()
    repository.save.assert_not_called()
