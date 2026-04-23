"""Caso de uso para listar todos los documentos."""

from dataclasses import dataclass
from typing import List

from src.domain.entities.document import Document
from src.domain.repositories.document_repository import DocumentRepository


@dataclass
class ListDocumentsOutput:
    """DTO de salida para el caso de uso."""

    documents: List[Document]


class ListDocumentsUseCase:
    """Caso de uso: Listar todos los documentos."""

    def __init__(self, repository: DocumentRepository) -> None:
        """Inicializa el caso de uso con el repositorio.

        Args:
            repository: Implementación de DocumentRepository.
        """
        self._repository = repository

    async def execute(self) -> List[Document]:
        """Ejecuta el caso de uso.

        Returns:
            List[Document]: Lista de todos los documentos.
        """
        return await self._repository.find_all()
