"""Servicio de aplicación para items."""

from typing import List, Optional
from uuid import UUID

from src.domain.entities.item import Item
from src.domain.repositories.item_repository import ItemRepository


class ItemService:
    """Servicio de aplicación que implementa la lógica de negocio para items.

    Mantiene las reglas de negocio y coordina las operaciones
    con el repositorio de datos.
    """

    def __init__(self, repository: ItemRepository) -> None:
        """Inicializa el servicio con su repositorio.

        Args:
            repository: Repositorio para persistencia.
        """
        self._repository = repository

    def create_item(self, name: str, description: str) -> Item:
        """Crea un nuevo item validando las reglas de negocio.

        Args:
            name: Nombre del item.
            description: Descripción del item.

        Returns:
            Item: Item creado y persistido.

        Raises:
            ValueError: Si el nombre está vacío.
        """
        self._validate_name(name)

        item = Item(name=name, description=description)
        return self._repository.save(item)

    def get_item(self, item_id: UUID) -> Optional[Item]:
        """Recupera un item por su ID.

        Args:
            item_id: UUID del item.

        Returns:
            Optional[Item]: Item encontrado o None.
        """
        return self._repository.find_by_id(item_id)

    def list_items(self) -> List[Item]:
        """Lista todos los items disponibles.

        Returns:
            List[Item]: Lista completa ordenada.
        """
        return self._repository.find_all()

    def update_item(
        self,
        item_id: UUID,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Optional[Item]:
        """Actualiza un item aplicando validaciones.

        Args:
            item_id: UUID del item.
            name: Nuevo nombre opcional.
            description: Nueva descripción opcional.

        Returns:
            Optional[Item]: Item actualizado o None.

        Raises:
            ValueError: Si el nombre está vacío.
        """
        existing_item = self._repository.find_by_id(item_id)
        if existing_item is None:
            return None

        if name is not None:
            self._validate_name(name)

        updated_item = existing_item.update(name=name, description=description)
        return self._repository.save(updated_item)

    def delete_item(self, item_id: UUID) -> bool:
        """Elimina un item del sistema.

        Args:
            item_id: UUID del item.

        Returns:
            bool: True si se eliminó.
        """
        return self._repository.delete(item_id)

    def _validate_name(self, name: str) -> None:
        """Valida que el nombre cumpla las reglas de negocio.

        Args:
            name: Nombre a validar.

        Raises:
            ValueError: Si el nombre está vacío o solo tiene espacios.
        """
        if not name or not name.strip():
            raise ValueError("Item name cannot be empty")
