"""Caso de uso: Crear un item."""

from dataclasses import dataclass

from src.domain.entities.item import Item
from src.domain.repositories.item_repository import ItemRepository


@dataclass
class CreateItemRequest:
    """Request para crear un item."""

    name: str
    description: str


@dataclass
class CreateItemResponse:
    """Response del caso de uso."""

    item: Item
    success: bool
    message: str


class CreateItemUseCase:
    """Caso de uso para crear un item."""

    def __init__(self, repository: ItemRepository) -> None:
        """Inicializa el caso de uso.

        Args:
            repository: Repositorio de items.
        """
        self._repository = repository

    def execute(self, request: CreateItemRequest) -> CreateItemResponse:
        """Ejecuta el caso de uso.

        Args:
            request: Datos del request.

        Returns:
            CreateItemResponse: Resultado del caso de uso.
        """
        if not request.name or not request.name.strip():
            return CreateItemResponse(
                item=None,  # type: ignore
                success=False,
                message="Item name cannot be empty",
            )

        item = Item(name=request.name, description=request.description)
        saved_item = self._repository.save(item)

        return CreateItemResponse(
            item=saved_item,
            success=True,
            message="Item created successfully",
        )
