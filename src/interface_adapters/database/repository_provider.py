"""Proveedores de repositorios (singleton pattern)."""

from src.domain.repositories.document_repository import DocumentRepository
from src.domain.repositories.item_repository import ItemRepository
from src.interface_adapters.database.in_memory_document_repository import InMemoryDocumentRepository
from src.interface_adapters.database.in_memory_item_repository import InMemoryItemRepository

# Singleton instances
_item_repository_instance: ItemRepository | None = None
_document_repository_instance: DocumentRepository | None = None


def get_item_repository() -> ItemRepository:
    """Provee el repositorio singleton de items.

    Returns:
        ItemRepository: Instancia única del repositorio.
    """
    global _item_repository_instance
    if _item_repository_instance is None:
        _item_repository_instance = InMemoryItemRepository()
    return _item_repository_instance


def get_document_repository() -> DocumentRepository:
    """Provee el repositorio singleton de documentos.

    Returns:
        DocumentRepository: Instancia única del repositorio.
    """
    global _document_repository_instance
    if _document_repository_instance is None:
        _document_repository_instance = InMemoryDocumentRepository()
    return _document_repository_instance


def reset_repository() -> None:
    """Resetea el repositorio (útil para tests)."""
    global _item_repository_instance, _document_repository_instance
    _item_repository_instance = None
    _document_repository_instance = None
