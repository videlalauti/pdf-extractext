"""Composition root: ensambla los casos de uso con sus dependencias concretas."""

from fastapi import Depends

from src.application.services.pdf_text_extractor import PdfTextExtractor
from src.application.services.pdf_validator import PdfValidator
from src.application.use_cases.delete_document import DeleteDocumentUseCase
from src.application.use_cases.get_document import GetDocumentUseCase
from src.application.use_cases.list_documents import ListDocumentsUseCase
from src.application.use_cases.update_document import UpdateDocumentUseCase
from src.application.use_cases.upload_document import UploadDocumentUseCase
from src.domain.repositories.document_repository import DocumentRepository
from src.infrastructure.adapters.pypdf_text_extractor import PyPdfTextExtractor
from src.infrastructure.config.settings import settings
from src.interface_adapters.database.repository_provider import get_document_repository


def get_list_use_case(
    repository: DocumentRepository = Depends(get_document_repository),
) -> ListDocumentsUseCase:
    """Proveedor de dependencia para el caso de uso de listar."""
    return ListDocumentsUseCase(repository)


def get_get_use_case(
    repository: DocumentRepository = Depends(get_document_repository),
) -> GetDocumentUseCase:
    """Proveedor de dependencia para el caso de uso de obtener."""
    return GetDocumentUseCase(repository)


def get_update_use_case(
    repository: DocumentRepository = Depends(get_document_repository),
) -> UpdateDocumentUseCase:
    """Proveedor de dependencia para el caso de uso de actualizar."""
    return UpdateDocumentUseCase(repository)


def get_delete_use_case(
    repository: DocumentRepository = Depends(get_document_repository),
) -> DeleteDocumentUseCase:
    """Proveedor de dependencia para el caso de uso de eliminar."""
    return DeleteDocumentUseCase(repository)


def get_upload_use_case(
    repository: DocumentRepository = Depends(get_document_repository),
) -> UploadDocumentUseCase:
    """Proveedor de dependencia para el caso de uso de subir documentos."""
    validator = PdfValidator(max_size_bytes=settings.MAX_PDF_SIZE_BYTES)
    extractor_adapter = PyPdfTextExtractor()
    extractor = PdfTextExtractor(extractor_adapter=extractor_adapter)
    return UploadDocumentUseCase(
        repository=repository,
        extractor=extractor,
        validator=validator,
    )