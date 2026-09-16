"""Caso de uso para eliminar un documento."""

from uuid import UUID

from src.domain.exceptions import DocumentNotFoundError
from src.domain.repositories.document_repository import DocumentRepository


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
