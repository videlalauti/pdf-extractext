"""Tests unitarios para los casos de uso de items."""

from uuid import uuid4

import pytest

from src.application.use_cases.item_use_case import (
    CreateItemUseCase,
    DeleteItemUseCase,
    GetItemUseCase,
    ListItemsUseCase,
    UpdateItemUseCase,
)
from src.domain.entities.item import Item
from src.interface_adapters.database.in_memory_item_repository import InMemoryItemRepository


def test_create_item_use_case_exists():
    assert hasattr(CreateItemUseCase, "execute")


def test_list_items_use_case_exists():
    assert hasattr(ListItemsUseCase, "execute")


class TestItemUseCases:
    """Tests para la lógica de negocio de items vía use cases."""

    @pytest.fixture
    def repository(self):
        """Provee un repositorio limpio para cada test."""
        return InMemoryItemRepository()

    @pytest.fixture
    def create_use_case(self, repository):
        """Provee el caso de uso de crear items."""
        return CreateItemUseCase(repository)

    @pytest.fixture
    def get_use_case(self, repository):
        """Provee el caso de uso de obtener items."""
        return GetItemUseCase(repository)

    @pytest.fixture
    def list_use_case(self, repository):
        """Provee el caso de uso de listar items."""
        return ListItemsUseCase(repository)

    @pytest.fixture
    def update_use_case(self, repository):
        """Provee el caso de uso de actualizar items."""
        return UpdateItemUseCase(repository)

    @pytest.fixture
    def delete_use_case(self, repository):
        """Provee el caso de uso de eliminar items."""
        return DeleteItemUseCase(repository)

    def test_create_item_success(self, create_use_case):
        """Debe crear un item con datos válidos."""
        item = create_use_case.execute(name="Test Item", description="A test item")

        assert item.name == "Test Item"
        assert item.description == "A test item"
        assert item.id is not None
        assert item.created_at is not None

    def test_create_item_empty_name_raises_error(self, create_use_case):
        """Debe rechazar nombres vacíos."""
        with pytest.raises(ValueError, match="cannot be empty"):
            create_use_case.execute(name="", description="Description")

    def test_create_item_whitespace_name_raises_error(self, create_use_case):
        """Debe rechazar nombres con solo espacios."""
        with pytest.raises(ValueError, match="cannot be empty"):
            create_use_case.execute(name="   ", description="Description")

    def test_get_existing_item(self, create_use_case, get_use_case):
        """Debe recuperar un item existente."""
        created = create_use_case.execute(name="Existing", description="Item")

        found = get_use_case.execute(created.id)

        assert found is not None
        assert found.id == created.id
        assert found.name == "Existing"

    def test_get_nonexistent_item_returns_none(self, get_use_case):
        """Debe retornar None para item inexistente."""
        found = get_use_case.execute(uuid4())

        assert found is None

    def test_list_items_returns_ordered_results(self, create_use_case, list_use_case):
        """Debe listar items ordenados por creación."""
        create_use_case.execute(name="First", description="1")
        create_use_case.execute(name="Second", description="2")

        items = list_use_case.execute()

        assert len(items) == 2
        assert items[0].name == "First"
        assert items[1].name == "Second"

    def test_update_item_success(self, create_use_case, update_use_case):
        """Debe actualizar un item existente."""
        created = create_use_case.execute(name="Original", description="Original desc")

        updated = update_use_case.execute(
            created.id, name="Updated", description="New desc"
        )

        assert updated is not None
        assert updated.name == "Updated"
        assert updated.description == "New desc"
        assert updated.created_at == created.created_at
        assert updated.updated_at is not None

    def test_update_nonexistent_item_returns_none(self, update_use_case):
        """Debe retornar None al actualizar item inexistente."""
        updated = update_use_case.execute(uuid4(), name="New Name")

        assert updated is None

    def test_delete_existing_item(self, create_use_case, delete_use_case, get_use_case):
        """Debe eliminar un item existente."""
        created = create_use_case.execute(name="To Delete", description="Delete me")

        deleted = delete_use_case.execute(created.id)

        assert deleted is True
        assert get_use_case.execute(created.id) is None

    def test_delete_nonexistent_item_returns_false(self, delete_use_case):
        """Debe retornar False al eliminar item inexistente."""
        deleted = delete_use_case.execute(uuid4())

        assert deleted is False