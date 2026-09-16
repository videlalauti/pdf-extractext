"""Persistence service: endpoints HTTP CRUD delegando en DocumentRepository."""

from fastapi import APIRouter, status
from persistence.mongodb_connection import MongoDBConnection
from persistence.repository import DocumentRepository
from pydantic import BaseModel

router = APIRouter()


class DocumentCreate(BaseModel):
    id: str | None = None
    content: str
    checksum: str


class DocumentUpdate(BaseModel):
    content: str | None = None
    checksum: str | None = None


class DocumentResponse(BaseModel):
    id: str
    content: str
    checksum: str


repository = DocumentRepository(MongoDBConnection())


@router.post("/documents", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document(doc: DocumentCreate) -> DocumentResponse:
    return DocumentResponse(**await repository.create(doc.id, doc.content, doc.checksum))


@router.get("/documents", response_model=list[DocumentResponse])
async def get_documents() -> list[DocumentResponse]:
    return [DocumentResponse(**document) for document in await repository.list_all()]


@router.get("/documents/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: str) -> DocumentResponse:
    return DocumentResponse(**await repository.get(document_id))


@router.put("/documents/{document_id}", response_model=DocumentResponse)
async def update_document(document_id: str, doc_update: DocumentUpdate) -> DocumentResponse:
    return DocumentResponse(
        **await repository.update(document_id, doc_update.content, doc_update.checksum)
    )


@router.delete("/documents/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(document_id: str) -> None:
    await repository.delete(document_id)
