"""Schemas Pydantic para documentos."""

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from src.domain.entities.document import Document


class DocumentUpdateRequest(BaseModel):
    """DTO para actualización de documentos.

    Attributes:
        content: Nuevo texto extraído del documento.
    """

    content: str = Field(
        ...,
        min_length=1,
        max_length=100000,
        description="Texto extraído del documento PDF",
    )


class DocumentResponse(BaseModel):
    """DTO para respuesta de documentos.

    Attributes:
        id: Identificador único.
        content: Texto extraído del documento.
        checksum: Checksum del archivo para verificar integridad.
    """

    id: UUID = Field(..., description="Identificador único del documento")
    content: str = Field(..., description="Texto extraído del documento")
    checksum: str = Field(..., description="Checksum SHA-256 del archivo PDF")

    @classmethod
    def from_entity(cls, document: Document) -> "DocumentResponse":
        """Crea un DTO de respuesta desde la entidad de dominio.

        Args:
            document: Entidad del dominio.

        Returns:
            DocumentResponse: DTO de respuesta.
        """
        return cls(
            id=UUID(document.id),
            content=document.content,
            checksum=document.checksum,
        )
