"""DTOs para items en la capa de aplicación."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class ItemDTO:
    """DTO para transferir datos de items entre capas."""

    id: UUID
    name: str
    description: str
    created_at: datetime
    updated_at: Optional[datetime] = None
