"""Interfaz del servicio de items."""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.models.item import Item


class ItemServiceInterface(ABC):
    """Contrato para operaciones de negocio sobre items.

    Define los casos de uso disponibles para gestionar items.
    """

    @abstractmethod
    def create_item(self, name: str, description: str) -> Item:
        """Crea un nuevo item.

        Args:
            name: Nombre del item.
            description: Descripción del item.

        Returns:
            Item: Item creado.

        Raises:
            ValueError: Si el nombre está vacío.
        """
        pass

    @abstractmethod
    def get_item(self, item_id: UUID) -> Optional[Item]:
        """Obtiene un item por su ID.

        Args:
            item_id: UUID del item.

        Returns:
            Optional[Item]: Item encontrado o None.
        """
        pass

    @abstractmethod
    def list_items(self) -> List[Item]:
        """Lista todos los items.

        Returns:
            List[Item]: Lista de items.
        """
        pass

    @abstractmethod
    def update_item(
        self,
        item_id: UUID,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Optional[Item]:
        """Actualiza un item existente.

        Args:
            item_id: UUID del item a actualizar.
            name: Nuevo nombre opcional.
            description: Nueva descripción opcional.

        Returns:
            Optional[Item]: Item actualizado o None si no existe.

        Raises:
            ValueError: Si el nombre proporcionado está vacío.
        """
        pass

    @abstractmethod
    def delete_item(self, item_id: UUID) -> bool:
        """Elimina un item.

        Args:
            item_id: UUID del item a eliminar.

        Returns:
            bool: True si se eliminó, False si no existía.
        """
        pass
