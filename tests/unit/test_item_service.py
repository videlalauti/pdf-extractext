"""Tests unitarios para ItemService."""

from uuid import uuid4

import pytest

from src.application.services.item_service import ItemService
from src.domain.entities.item import Item
from src.interface_adapters.database.in_memory_item_repository import InMemoryItemRepository


class TestItemService:
    """Tests para la lógica de negocio de items."""

    @pytest.fixture
    def repository(self):
        """Provee un repositorio limpio para cada test."""
        return InMemoryItemRepository()

    @pytest.fixture
    def service(self, repository):
        """Provee un servicio configurado para cada test."""
        return ItemService(repository)

    def test_create_item_success(self, service):
        """Debe crear un item con datos válidos."""
        item = service.create_item(name="Test Item", description="A test item")

        assert item.name == "Test Item"
        assert item.description == "A test item"
        assert item.id is not None
        assert item.created_at is not None

    def test_create_item_empty_name_raises_error(self, service):
        """Debe rechazar nombres vacíos."""
        with pytest.raises(ValueError, match="cannot be empty"):
            service.create_item(name="", description="Description")

    def test_create_item_whitespace_name_raises_error(self, service):
        """Debe rechazar nombres con solo espacios."""
        with pytest.raises(ValueError, match="cannot be empty"):
            service.create_item(name="   ", description="Description")

    def test_get_existing_item(self, service):
        """Debe recuperar un item existente."""
        created = service.create_item(name="Existing", description="Item")

        found = service.get_item(created.id)

        assert found is not None
        assert found.id == created.id
        assert found.name == "Existing"

    def test_get_nonexistent_item_returns_none(self, service):
        """Debe retornar None para item inexistente."""
        found = service.get_item(uuid4())

        assert found is None

    def test_list_items_returns_ordered_results(self, service):
        """Debe listar items ordenados por creación."""
        service.create_item(name="First", description="1")
        service.create_item(name="Second", description="2")

        items = service.list_items()

        assert len(items) == 2
        assert items[0].name == "First"
        assert items[1].name == "Second"

    def test_update_item_success(self, service):
        """Debe actualizar un item existente."""
        created = service.create_item(name="Original", description="Original desc")

        updated = service.update_item(created.id, name="Updated", description="New desc")

        assert updated is not None
        assert updated.name == "Updated"
        assert updated.description == "New desc"
        assert updated.created_at == created.created_at
        assert updated.updated_at is not None

    def test_update_nonexistent_item_returns_none(self, service):
        """Debe retornar None al actualizar item inexistente."""
        updated = service.update_item(uuid4(), name="New Name")

        assert updated is None

    def test_delete_existing_item(self, service):
        """Debe eliminar un item existente."""
        created = service.create_item(name="To Delete", description="Delete me")

        deleted = service.delete_item(created.id)

        assert deleted is True
        assert service.get_item(created.id) is None

    def test_delete_nonexistent_item_returns_false(self, service):
        """Debe retornar False al eliminar item inexistente."""
        deleted = service.delete_item(uuid4())

        assert deleted is False
