"""Interfaces de repositorios del dominio."""

from src.domain.repositories.document_repository import DocumentRepository
from src.domain.repositories.item_repository import ItemRepository

__all__ = ["DocumentRepository", "ItemRepository"]
