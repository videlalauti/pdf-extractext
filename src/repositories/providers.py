"""Proveedores de repositorios (singleton pattern)."""

from src.repositories.implementations.in_memory_item_repository import (
    InMemoryItemRepository,
)
from src.repositories.interfaces.item_repository import ItemRepositoryInterface

# Singleton instance
_item_repository_instance: ItemRepositoryInterface | None = None


def get_item_repository() -> ItemRepositoryInterface:
    """Provee el repositorio singleton de items.

    Returns:
        ItemRepositoryInterface: Instancia única del repositorio.
    """
    global _item_repository_instance
    if _item_repository_instance is None:
        _item_repository_instance = InMemoryItemRepository()
    return _item_repository_instance


def reset_repository() -> None:
    """Resetea el repositorio (útil para tests)."""
    global _item_repository_instance
    _item_repository_instance = None
