"""Entidad Item del dominio."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass(frozen=True)
class Item:
    """Entidad de dominio que representa un item.

    Attributes:
        id: Identificador único del item.
        name: Nombre descriptivo del item.
        description: Descripción detallada.
        created_at: Fecha de creación.
        updated_at: Fecha de última actualización.
    """

    name: str
    description: str
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    def update(
        self, name: Optional[str] = None, description: Optional[str] = None
    ) -> "Item":
        """Crea una nueva instancia con valores actualizados.

        Args:
            name: Nuevo nombre opcional.
            description: Nueva descripción opcional.

        Returns:
            Item: Nueva instancia con valores actualizados.
        """
        return Item(
            id=self.id,
            name=name if name is not None else self.name,
            description=description if description is not None else self.description,
            created_at=self.created_at,
            updated_at=datetime.utcnow(),
        )
