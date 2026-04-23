"""Proveedores de repositorios (singleton pattern)."""

from src.domain.repositories.item_repository import ItemRepository
from src.interface_adapters.database.in_memory_item_repository import InMemoryItemRepository

# Singleton instance
_item_repository_instance: ItemRepository | None = None


def get_item_repository() -> ItemRepository:
    """Provee el repositorio singleton de items.

    Returns:
        ItemRepository: Instancia única del repositorio.
    """
    global _item_repository_instance
    if _item_repository_instance is None:
        _item_repository_instance = InMemoryItemRepository()
    return _item_repository_instance


def reset_repository() -> None:
    """Resetea el repositorio (útil para tests)."""
    global _item_repository_instance
    _item_repository_instance = None
