"""Schemas Pydantic para items."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from src.domain.entities.item import Item


class ItemCreateRequest(BaseModel):
    """DTO para creación de items.

    Attributes:
        name: Nombre del item (3-100 caracteres).
        description: Descripción del item (max 500 caracteres).
    """

    name: str = Field(..., min_length=3, max_length=100, description="Nombre del item")
    description: str = Field(
        ..., max_length=500, description="Descripción detallada del item"
    )


class ItemUpdateRequest(BaseModel):
    """DTO para actualización de items.

    Attributes:
        name: Nuevo nombre opcional.
        description: Nueva descripción opcional.
    """

    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class ItemResponse(BaseModel):
    """DTO para respuesta de items.

    Attributes:
        id: Identificador único.
        name: Nombre del item.
        description: Descripción del item.
        created_at: Fecha de creación.
        updated_at: Fecha de última actualización.
    """

    id: UUID = Field(..., description="Identificador único del item")
    name: str = Field(..., description="Nombre del item")
    description: str = Field(..., description="Descripción del item")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: Optional[datetime] = Field(
        None, description="Fecha de última actualización"
    )

    @classmethod
    def from_entity(cls, item: Item) -> "ItemResponse":
        """Crea un DTO de respuesta desde la entidad de dominio.

        Args:
            item: Entidad del dominio.

        Returns:
            ItemResponse: DTO de respuesta.
        """
        return cls(
            id=item.id,
            name=item.name,
            description=item.description,
            created_at=item.created_at,
            updated_at=item.updated_at,
        )
