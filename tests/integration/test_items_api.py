"""Tests de integración para endpoints de items."""

from http import HTTPStatus
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from src.infrastructure.config.settings import settings
from src.interface_adapters.database.repository_provider import reset_repository
from src.interface_adapters.http.main import app


@pytest.fixture(autouse=True)
def reset_state():
    """Resetea el estado antes de cada test."""
    reset_repository()


@pytest.fixture
def client():
    """Provee un cliente de test."""
    return TestClient(app)


class TestItemsApi:
    """Tests de integración para la API de items."""

    def test_create_item_success(self, client):
        """POST /items debe crear un item."""
        response = client.post(
            "/api/v1/items",
            json={"name": "Integration Test", "description": "Test description"},
        )

        assert response.status_code == HTTPStatus.CREATED
        data = response.json()
        assert data["name"] == "Integration Test"
        assert data["description"] == "Test description"
        assert "id" in data

    def test_create_item_validation_error(self, client):
        """POST /items debe rechazar datos inválidos."""
        response = client.post(
            "/api/v1/items",
            json={"name": "ab", "description": "Test"},  # Nombre muy corto
        )

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_list_items_empty(self, client):
        """GET /items debe retornar lista vacía inicialmente."""
        response = client.get("/api/v1/items")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == []

    def test_get_item_not_found(self, client):
        """GET /items/{id} debe retornar 404 para ID inexistente."""
        response = client.get(f"/api/v1/items/{uuid4()}")

        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_full_item_lifecycle(self, client):
        """Flujo completo: crear, obtener, actualizar, eliminar."""
        # Create
        create_response = client.post(
            "/api/v1/items",
            json={"name": "Lifecycle Test", "description": "Original"},
        )
        assert create_response.status_code == HTTPStatus.CREATED
        item_id = create_response.json()["id"]

        # Get
        get_response = client.get(f"/api/v1/items/{item_id}")
        assert get_response.status_code == HTTPStatus.OK
        assert get_response.json()["name"] == "Lifecycle Test"

        # Update
        update_response = client.put(
            f"/api/v1/items/{item_id}",
            json={"name": "Updated Name", "description": "Updated"},
        )
        assert update_response.status_code == HTTPStatus.OK
        assert update_response.json()["name"] == "Updated Name"

        # Delete
        delete_response = client.delete(f"/api/v1/items/{item_id}")
        assert delete_response.status_code == HTTPStatus.NO_CONTENT

        # Verify deletion
        get_after_delete = client.get(f"/api/v1/items/{item_id}")
        assert get_after_delete.status_code == HTTPStatus.NOT_FOUND
