"""Caso de uso para eliminar un documento."""

from dataclasses import dataclass
from uuid import UUID

from src.domain.repositories.document_repository import DocumentRepository
from src.domain.exceptions import DomainError


class DocumentNotFoundError(DomainError):
    """Excepción cuando el documento no existe."""

    def __init__(self, document_id: str):
        self.document_id = document_id
        super().__init__(f"Documento con ID {document_id} no encontrado")


@dataclass
class DeleteDocumentOutput:
    """DTO de salida para el caso de uso."""

    deleted: bool


class DeleteDocumentUseCase:
    """Caso de uso: Eliminar documento."""

    def __init__(self, repository: DocumentRepository) -> None:
        """Inicializa el caso de uso con el repositorio.

        Args:
            repository: Implementación de DocumentRepository.
        """
        self._repository = repository

    async def execute(self, document_id: UUID) -> bool:
        """Ejecuta el caso de uso.

        Args:
            document_id: UUID del documento a eliminar.

        Returns:
            bool: True si se eliminó, False si no existía.

        Raises:
            DocumentNotFoundError: Si el documento no existe.
        """
        deleted = await self._repository.delete(document_id)
        if not deleted:
            raise DocumentNotFoundError(str(document_id))
        return True
