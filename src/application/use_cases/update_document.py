"""Caso de uso para actualizar el contenido de un documento."""

from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from src.domain.entities.document import Document
from src.domain.repositories.document_repository import DocumentRepository
from src.domain.exceptions import DomainError


class DocumentNotFoundError(DomainError):
    """Excepción cuando el documento no existe."""

    def __init__(self, document_id: str):
        self.document_id = document_id
        super().__init__(f"Documento con ID {document_id} no encontrado")


@dataclass
class UpdateDocumentInput:
    """DTO de entrada para el caso de uso."""

    document_id: UUID
    content: str


@dataclass
class UpdateDocumentOutput:
    """DTO de salida para el caso de uso."""

    document: Document


class UpdateDocumentUseCase:
    """Caso de uso: Actualizar contenido de documento."""

    def __init__(self, repository: DocumentRepository) -> None:
        """Inicializa el caso de uso con el repositorio.

        Args:
            repository: Implementación de DocumentRepository.
        """
        self._repository = repository

    async def execute(self, document_id: UUID, content: str) -> Document:
        """Ejecuta el caso de uso.

        Args:
            document_id: UUID del documento a actualizar.
            content: Nuevo contenido del documento.

        Returns:
            Document: Documento actualizado.

        Raises:
            DocumentNotFoundError: Si el documento no existe.
        """
        existing = await self._repository.find_by_id(document_id)
        if existing is None:
            raise DocumentNotFoundError(str(document_id))

        # Como Document es inmutable, creamos uno nuevo con el mismo ID y checksum
        updated = Document(
            id=existing.id,
            content=content,
            checksum=existing.checksum,
        )

        return await self._repository.save(updated)
