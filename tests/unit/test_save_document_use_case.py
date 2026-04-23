"""Tests para el caso de uso SaveDocumentUseCase.

Aplica TDD con mocks para verificar la logica de negocio
antes de implementar el repositorio real.
"""

import hashlib
import pytest
from unittest.mock import AsyncMock, create_autospec
from uuid import UUID, uuid4

from src.domain.entities.document import Document
from src.domain.repositories.document_repository import DocumentRepository
from src.domain.exceptions import DomainError


class TestSaveDocumentUseCase:
    """Tests para el caso de uso de guardar documento con validacion de duplicados."""

    @pytest.mark.asyncio
    async def test_genera_checksum_sha256_correctamente(self):
        """Test: Debe generar SHA-256 del contenido del archivo."""
        from src.application.use_cases.save_document import SaveDocumentUseCase

        mock_repo = create_autospec(DocumentRepository, instance=True)
        mock_repo.exists_by_checksum = AsyncMock(return_value=False)

        pdf_bytes = b"contenido de prueba del PDF"
        expected_checksum = hashlib.sha256(pdf_bytes).hexdigest()

        expected_document = Document(
            id=str(uuid4()), content="texto extraido", checksum=expected_checksum
        )
        mock_repo.save = AsyncMock(return_value=expected_document)

        use_case = SaveDocumentUseCase(repository=mock_repo)
        result = await use_case.execute(pdf_bytes=pdf_bytes, content="texto extraido")

        assert result.checksum == expected_checksum

    @pytest.mark.asyncio
    async def test_rechaza_documento_duplicado_por_checksum(self):
        """Test: Debe rechazar si el checksum ya existe en el repositorio."""
        from src.application.use_cases.save_document import (
            SaveDocumentUseCase,
            DuplicateDocumentError,
        )

        mock_repo = create_autospec(DocumentRepository, instance=True)
        mock_repo.exists_by_checksum = AsyncMock(return_value=True)

        use_case = SaveDocumentUseCase(repository=mock_repo)
        pdf_bytes = b"contenido duplicado"

        with pytest.raises(DuplicateDocumentError) as exc_info:
            await use_case.execute(pdf_bytes=pdf_bytes, content="texto extraido")

        assert (
            "ya existe" in str(exc_info.value).lower() or "duplicate" in str(exc_info.value).lower()
        )
        mock_repo.exists_by_checksum.assert_called_once()

    @pytest.mark.asyncio
    async def test_guarda_documento_nuevo_cuando_no_existe(self):
        """Test: Debe guardar el documento cuando no existe duplicado."""
        from src.application.use_cases.save_document import SaveDocumentUseCase

        mock_repo = create_autospec(DocumentRepository, instance=True)
        mock_repo.exists_by_checksum = AsyncMock(return_value=False)

        saved_document = Document(id=str(uuid4()), content="texto extraido", checksum="abc123")
        mock_repo.save = AsyncMock(return_value=saved_document)

        use_case = SaveDocumentUseCase(repository=mock_repo)
        pdf_bytes = b"contenido nuevo"

        result = await use_case.execute(pdf_bytes=pdf_bytes, content="texto extraido")

        mock_repo.save.assert_called_once()
        assert result.content == "texto extraido"

    @pytest.mark.asyncio
    async def test_repositorio_recibe_documento_con_checksum_correcto(self):
        """Test: El repositorio debe recibir documento con checksum SHA-256."""
        from src.application.use_cases.save_document import SaveDocumentUseCase

        mock_repo = create_autospec(DocumentRepository, instance=True)
        mock_repo.exists_by_checksum = AsyncMock(return_value=False)
        mock_repo.save = AsyncMock(
            return_value=Document(id=str(uuid4()), content="texto", checksum="dummy")
        )

        use_case = SaveDocumentUseCase(repository=mock_repo)
        pdf_bytes = b"contenido especifico"

        await use_case.execute(pdf_bytes=pdf_bytes, content="texto extraido")

        call_args = mock_repo.save.call_args[0][0]
        assert isinstance(call_args, Document)
        assert len(call_args.checksum) == 64
        assert all(c in "0123456789abcdef" for c in call_args.checksum)

    @pytest.mark.asyncio
    async def test_consulta_checksum_antes_de_insertar(self):
        """Test: Debe consultar exists_by_checksum antes de intentar guardar."""
        from src.application.use_cases.save_document import SaveDocumentUseCase

        mock_repo = create_autospec(DocumentRepository, instance=True)
        mock_repo.exists_by_checksum = AsyncMock(return_value=False)
        mock_repo.save = AsyncMock(
            return_value=Document(id=str(uuid4()), content="texto", checksum="hash123")
        )

        use_case = SaveDocumentUseCase(repository=mock_repo)
        await use_case.execute(pdf_bytes=b"contenido", content="texto")

        assert mock_repo.exists_by_checksum.called
        assert mock_repo.save.called
        call_order = [
            call
            for call in mock_repo.method_calls
            if "exists_by_checksum" in str(call) or "save" in str(call)
        ]
        assert "exists_by_checksum" in str(call_order[0])
