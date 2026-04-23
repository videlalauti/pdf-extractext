"""Caso de uso para obtener un documento por ID."""

from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from src.domain.entities.document import Document
from src.domain.repositories.document_repository import DocumentRepository


@dataclass
class GetDocumentOutput:
    """DTO de salida para el caso de uso."""

    document: Optional[Document]


class GetDocumentUseCase:
    """Caso de uso: Obtener documento por ID."""

    def __init__(self, repository: DocumentRepository) -> None:
        """Inicializa el caso de uso con el repositorio.

        Args:
            repository: Implementación de DocumentRepository.
        """
        self._repository = repository

    async def execute(self, document_id: UUID) -> Optional[Document]:
        """Ejecuta el caso de uso.

        Args:
            document_id: UUID del documento a buscar.

        Returns:
            Optional[Document]: Documento encontrado o None.
        """
        return await self._repository.find_by_id(document_id)
