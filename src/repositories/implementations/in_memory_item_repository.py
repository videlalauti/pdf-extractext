"""Implementación en memoria del repositorio de items."""

from typing import Dict, List, Optional
from uuid import UUID

from src.models.item import Item
from src.repositories.interfaces.item_repository import ItemRepositoryInterface


class InMemoryItemRepository(ItemRepositoryInterface):
    """Implementación en memoria para pruebas y desarrollo.

    Almacena los items en un diccionario en memoria.
    No persistencia entre reinicios.
    """

    def __init__(self) -> None:
        """Inicializa el repositorio vacío."""
        self._items: Dict[UUID, Item] = {}

    def save(self, item: Item) -> Item:
        """Guarda o actualiza un item.

        Args:
            item: Entidad a persistir.

        Returns:
            Item: Item guardado.
        """
        self._items[item.id] = item
        return item

    def find_by_id(self, item_id: UUID) -> Optional[Item]:
        """Busca un item por UUID.

        Args:
            item_id: UUID del item.

        Returns:
            Optional[Item]: Item encontrado o None.
        """
        return self._items.get(item_id)

    def find_all(self) -> List[Item]:
        """Recupera todos los items.

        Returns:
            List[Item]: Lista de items ordenada por fecha de creación.
        """
        return sorted(
            self._items.values(),
            key=lambda item: item.created_at,
        )

    def delete(self, item_id: UUID) -> bool:
        """Elimina un item.

        Args:
            item_id: UUID del item a eliminar.

        Returns:
            bool: True si existía y se eliminó.
        """
        if item_id in self._items:
            del self._items[item_id]
            return True
        return False
