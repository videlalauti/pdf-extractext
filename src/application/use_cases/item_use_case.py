"""Casos de uso para la gestión de items.

Implementan la lógica de negocio para crear, listar, obtener,
actualizar y eliminar items, delegando la persistencia al repositorio.
"""

from typing import List, Optional
from uuid import UUID

from src.domain.entities.item import Item
from src.domain.exceptions import ValidationError
from src.domain.repositories.item_repository import ItemRepository


class CreateItemUseCase:
    """Caso de uso: Crear un nuevo item con validación de reglas de negocio."""

    def __init__(self, repository: ItemRepository) -> None:
        self._repository = repository

    def execute(self, name: str, description: str) -> Item:
        self._validate_name(name)
        item = Item(name=name, description=description)
        return self._repository.save(item)

    def _validate_name(self, name: str) -> None:
        if not name or not name.strip():
            raise ValidationError("Item name cannot be empty")


class ListItemsUseCase:
    """Caso de uso: Listar todos los items."""

    def __init__(self, repository: ItemRepository) -> None:
        self._repository = repository

    def execute(self) -> List[Item]:
        return self._repository.find_all()


class GetItemUseCase:
    """Caso de uso: Obtener un item por su ID."""

    def __init__(self, repository: ItemRepository) -> None:
        self._repository = repository

    def execute(self, item_id: UUID) -> Optional[Item]:
        return self._repository.find_by_id(item_id)


class UpdateItemUseCase:
    """Caso de uso: Actualizar un item existente aplicando validaciones."""

    def __init__(self, repository: ItemRepository) -> None:
        self._repository = repository

    def execute(
        self,
        item_id: UUID,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Optional[Item]:
        existing_item = self._repository.find_by_id(item_id)
        if existing_item is None:
            return None

        if name is not None:
            self._validate_name(name)

        updated_item = existing_item.update(name=name, description=description)
        return self._repository.save(updated_item)

    def _validate_name(self, name: str) -> None:
        if not name or not name.strip():
            raise ValidationError("Item name cannot be empty")


class DeleteItemUseCase:
    """Caso de uso: Eliminar un item del sistema."""

    def __init__(self, repository: ItemRepository) -> None:
        self._repository = repository

    def execute(self, item_id: UUID) -> bool:
        return self._repository.delete(item_id)
