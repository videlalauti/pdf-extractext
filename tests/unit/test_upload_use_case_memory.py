from unittest.mock import AsyncMock

import pytest

from src.application.use_cases.upload_document import UploadDocumentUseCase


@pytest.mark.asyncio
async def test_upload_works_with_bytes_directly():
    mock_repo = AsyncMock()
    mock_repo.find_by_checksum.return_value = None
    mock_extractor = AsyncMock()
    mock_extractor.extract_text_from_bytes.return_value = "extracted text"
    use_case = UploadDocumentUseCase(mock_repo, mock_extractor)
    pdf_bytes = b"%PDF-1.4" + b"x" * 50
    result = await use_case.execute(pdf_bytes, "test.pdf")
    assert result.created is True
    assert result.document is not None
