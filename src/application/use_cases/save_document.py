"""Caso de uso para guardar documentos con validacion de duplicados.

Implementa la logica de negocio para persistir documentos PDF,
generando checksum SHA-256 y evitando duplicados.
"""

import hashlib
from dataclasses import dataclass
from typing import Optional
from uuid import uuid4

from src.domain.entities.document import Document
from src.domain.repositories.document_repository import DocumentRepository
from src.domain.exceptions import DomainError


class DuplicateDocumentError(DomainError):
    """Excepcion cuando se intenta guardar un documento duplicado."""

    def __init__(self, checksum: str):
        self.checksum = checksum
        super().__init__(f"Documento con checksum {checksum} ya existe")


@dataclass
class SaveDocumentInput:
    """DTO de entrada para el caso de uso."""

    pdf_bytes: bytes
    content: str


@dataclass
class SaveDocumentOutput:
    """DTO de salida para el caso de uso."""

    document: Document


class SaveDocumentUseCase:
    """Caso de uso: Guardar documento con validacion de duplicados.

    Responsabilidades:
    - Generar checksum SHA-256 del archivo PDF
    - Verificar duplicados antes de persistir
    - Crear entidad Document y persistirla

    Attributes:
        _repository: Repositorio de documentos inyectado.
    """

    def __init__(self, repository: DocumentRepository) -> None:
        """Inicializa el caso de uso con el repositorio.

        Args:
            repository: Implementacion de DocumentRepository.
        """
        self._repository = repository

    def _generate_checksum(self, pdf_bytes: bytes) -> str:
        """Genera checksum SHA-256 del contenido.

        Args:
            pdf_bytes: Contenido binario del PDF.

        Returns:
            str: Hash SHA-256 en hexadecimal.
        """
        return hashlib.sha256(pdf_bytes).hexdigest()

    async def execute(self, pdf_bytes: bytes, content: str) -> Document:
        """Ejecuta el caso de uso.

        Args:
            pdf_bytes: Contenido binario del PDF.
            content: Texto extraido del documento.

        Returns:
            Document: Documento persistido.

        Raises:
            DuplicateDocumentError: Si el checksum ya existe.
        """
        checksum = self._generate_checksum(pdf_bytes)

        if await self._repository.exists_by_checksum(checksum):
            raise DuplicateDocumentError(checksum)

        document = Document(id=str(uuid4()), content=content, checksum=checksum)

        return await self._repository.save(document)
