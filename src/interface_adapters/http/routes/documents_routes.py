"""Endpoints para gestión de documentos PDF."""

from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, UploadFile

from src.application.use_cases.delete_document import DeleteDocumentUseCase
from src.application.use_cases.get_document import GetDocumentUseCase
from src.application.use_cases.list_documents import ListDocumentsUseCase
from src.application.use_cases.update_document import UpdateDocumentUseCase
from src.application.use_cases.upload_document import UploadDocumentUseCase
from src.domain.exceptions import (
    DocumentNotFoundError,
    InvalidPdfFormatError,
    PdfTooLargeError,
)
from src.interface_adapters.http.providers import (
    get_delete_use_case,
    get_get_use_case,
    get_list_use_case,
    get_update_use_case,
    get_upload_use_case,
)
from src.interface_adapters.http.schemas.document_schemas import (
    DocumentResponse,
    DocumentUpdateRequest,
)

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile,
    response: Response,
    use_case: UploadDocumentUseCase = Depends(get_upload_use_case),
) -> DocumentResponse:
    """Sube y procesa un archivo PDF.

    Orquesta el flujo completo:
    1. Detecta duplicados por checksum antes de procesar (cache)
    2. Valida formato y tamaño del PDF
    3. Extrae texto del documento
    4. Genera checksum y verifica duplicados
    5. Persiste el documento

    Args:
        file: Archivo PDF subido por el usuario
        response: Response para fijar el status code dinámico (200/201)

    Returns:
        DocumentResponse: Documento procesado y guardado

    Raises:
        HTTPException: 400 si el PDF es inválido o excede tamaño
        HTTPException: 500 si ocurre un error en el procesamiento
    """
    content = await file.read()

    try:
        result = await use_case.execute(content, file.filename)
        response.status_code = (
            HTTPStatus.CREATED if result.created else HTTPStatus.OK
        )
        return DocumentResponse.from_entity(result.document)
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


@router.get("", response_model=list[DocumentResponse])
async def list_documents(
    use_case: ListDocumentsUseCase = Depends(get_list_use_case),
) -> list[DocumentResponse]:
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
    except DocumentNotFoundError as error:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Document with id {document_id} not found",
        ) from error


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
    except DocumentNotFoundError as error:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Document with id {document_id} not found",
        ) from error
