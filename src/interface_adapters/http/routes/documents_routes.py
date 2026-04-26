"""Endpoints para gestión de documentos PDF."""

from http import HTTPStatus
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, UploadFile

from src.application.services.pdf_text_extractor import PdfTextExtractor
from src.application.services.pdf_validator import PdfValidator
from src.application.use_cases.delete_document import (
    DeleteDocumentUseCase,
    DocumentNotFoundError,
)
from src.application.use_cases.get_document import GetDocumentUseCase
from src.application.use_cases.list_documents import ListDocumentsUseCase
from src.application.use_cases.save_document import (
    DuplicateDocumentError,
    SaveDocumentUseCase,
)
from src.application.use_cases.update_document import (
    UpdateDocumentUseCase,
    DocumentNotFoundError as UpdateNotFoundError,
)
from src.application.use_cases.upload_document import UploadDocumentUseCase
from src.domain.exceptions import InvalidPdfFormatError, PdfTooLargeError
from src.domain.repositories.document_repository import DocumentRepository
from src.infrastructure.adapters.pypdf_text_extractor import PyPdfTextExtractor
from src.interface_adapters.database.repository_provider import get_document_repository
from src.interface_adapters.http.schemas.document_schemas import (
    DocumentResponse,
    DocumentUpdateRequest,
)

router = APIRouter(prefix="/documents", tags=["documents"])


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
    """Proveedor de dependencia para el caso de uso de subir documentos.

    Configura el flujo completo de upload con:
    - Validador de PDFs
    - Extractor de texto (PyPDF)
    - Caso de uso de guardado con verificación de duplicados
    """
    validator = PdfValidator()
    extractor_adapter = PyPdfTextExtractor()
    extractor = PdfTextExtractor(extractor_adapter=extractor_adapter)
    save_use_case = SaveDocumentUseCase(repository=repository)
    return UploadDocumentUseCase(
        validator=validator,
        extractor=extractor,
        save_use_case=save_use_case,
    )


@router.post("/upload", response_model=DocumentResponse, status_code=HTTPStatus.CREATED)
async def upload_document(
    file: UploadFile,
    use_case: UploadDocumentUseCase = Depends(get_upload_use_case),
) -> DocumentResponse:
    """Sube y procesa un archivo PDF.

    Orquesta el flujo completo:
    1. Valida formato y tamaño del PDF
    2. Extrae texto del documento
    3. Genera checksum y verifica duplicados
    4. Persiste el documento

    Args:
        file: Archivo PDF subido por el usuario

    Returns:
        DocumentResponse: Documento procesado y guardado

    Raises:
        HTTPException: 400 si el PDF es inválido o excede tamaño
        HTTPException: 409 si el documento ya existe (checksum duplicado)
        HTTPException: 500 si ocurre un error en el procesamiento
    """
    content = await file.read()

    try:
        document = await use_case.execute(content)
        return DocumentResponse.from_entity(document)
    except InvalidPdfFormatError as error:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(error),
        ) from error
    except PdfTooLargeError as error:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(error),
        ) from error
    except DuplicateDocumentError as error:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=f"Document already exists with checksum: {error.checksum}",
        ) from error


@router.get("", response_model=List[DocumentResponse])
async def list_documents(
    use_case: ListDocumentsUseCase = Depends(get_list_use_case),
) -> List[DocumentResponse]:
    """Lista todos los documentos.

    Returns:
        List[DocumentResponse]: Lista de documentos.
    """
    documents = await use_case.execute()
    return [DocumentResponse.from_entity(doc) for doc in documents]


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: UUID,
    use_case: GetDocumentUseCase = Depends(get_get_use_case),
) -> DocumentResponse:
    """Obtiene un documento por su ID.

    Args:
        document_id: UUID del documento.

    Returns:
        DocumentResponse: Documento encontrado.

    Raises:
        HTTPException: 404 si no existe.
    """
    document = await use_case.execute(document_id)
    if document is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Document with id {document_id} not found",
        )
    return DocumentResponse.from_entity(document)


@router.put("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: UUID,
    request: DocumentUpdateRequest,
    use_case: UpdateDocumentUseCase = Depends(get_update_use_case),
) -> DocumentResponse:
    """Actualiza el contenido de un documento.

    Args:
        document_id: UUID del documento.
        request: Datos a actualizar.

    Returns:
        DocumentResponse: Documento actualizado.

    Raises:
        HTTPException: 404 si no existe, 400 si datos inválidos.
    """
    try:
        document = await use_case.execute(document_id, request.content)
        return DocumentResponse.from_entity(document)
    except UpdateNotFoundError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Document with id {document_id} not found",
        )


@router.delete("/{document_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_document(
    document_id: UUID,
    use_case: DeleteDocumentUseCase = Depends(get_delete_use_case),
) -> None:
    """Elimina un documento.

    Args:
        document_id: UUID del documento.

    Raises:
        HTTPException: 404 si no existe.
    """
    try:
        await use_case.execute(document_id)
    except DocumentNotFoundError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Document with id {document_id} not found",
        )
