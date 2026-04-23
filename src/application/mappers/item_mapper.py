"""Mapper para convertir entre Item (domain) e ItemDTO (application)."""

from src.application.dtos.item_dto import ItemDTO
from src.domain.entities.item import Item


class ItemMapper:
    """Mapper para la entidad Item."""

    @staticmethod
    def to_dto(item: Item) -> ItemDTO:
        """Convierte una entidad Item a DTO.

        Args:
            item: Entidad del dominio.

        Returns:
            ItemDTO: DTO de aplicación.
        """
        return ItemDTO(
            id=item.id,
            name=item.name,
            description=item.description,
            created_at=item.created_at,
            updated_at=item.updated_at,
        )

    @staticmethod
    def to_dto_list(items: list[Item]) -> list[ItemDTO]:
        """Convierte una lista de entidades Item a DTOs.

        Args:
            items: Lista de entidades.

        Returns:
            list[ItemDTO]: Lista de DTOs.
        """
        return [ItemMapper.to_dto(item) for item in items]
