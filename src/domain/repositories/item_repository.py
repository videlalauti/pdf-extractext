"""Interfaz del repositorio de items."""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.entities.item import Item


class ItemRepository(ABC):
    """Contrato para el acceso a datos de items.

    Esta interfaz define las operaciones disponibles para
    persistir y recuperar entidades Item.
    """

    @abstractmethod
    def save(self, item: Item) -> Item:
        """Guarda un item en el repositorio.

        Args:
            item: Entidad a persistir.

        Returns:
            Item: Item persistido.
        """
        pass

    @abstractmethod
    def find_by_id(self, item_id: UUID) -> Optional[Item]:
        """Busca un item por su identificador.

        Args:
            item_id: UUID del item.

        Returns:
            Optional[Item]: Item encontrado o None.
        """
        pass

    @abstractmethod
    def find_all(self) -> List[Item]:
        """Recupera todos los items.

        Returns:
            List[Item]: Lista de todos los items.
        """
        pass

    @abstractmethod
    def delete(self, item_id: UUID) -> bool:
        """Elimina un item por su identificador.

        Args:
            item_id: UUID del item a eliminar.

        Returns:
            bool: True si se eliminó, False si no existía.
        """
        pass
