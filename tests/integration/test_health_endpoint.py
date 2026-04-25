"""Tests de integración para el endpoint de health check."""

from http import HTTPStatus
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from src.interface_adapters.http.main import app
from src.infrastructure.adapters.mongodb_connection import MongoDBConnection


@pytest.fixture
def client():
    """Provee un cliente de test."""
    return TestClient(app)


class TestHealthEndpoint:
    """Tests para el endpoint /health."""

    def test_health_check_success(self, client):
        """GET /health debe retornar 200 cuando la DB está disponible."""
        mock_client = AsyncMock()
        mock_client.admin.command = AsyncMock(return_value=True)

        # Crear instancia mock de MongoDBConnection
        mock_conn = MongoDBConnection.__new__(MongoDBConnection)
        mock_conn._client = mock_client

        with patch(
            "src.interface_adapters.http.routes.health_routes.mongodb_connection",
            mock_conn,
        ):
            response = client.get("/health")

            assert response.status_code == HTTPStatus.OK
            assert response.json() == {"status": "ok"}

    def test_health_check_database_failure(self, client):
        """GET /health debe retornar 503 cuando la DB no responde."""
        mock_client = AsyncMock()
        mock_client.admin.command = AsyncMock(side_effect=Exception("Connection refused"))

        # Crear instancia mock de MongoDBConnection
        mock_conn = MongoDBConnection.__new__(MongoDBConnection)
        mock_conn._client = mock_client

        with patch(
            "src.interface_adapters.http.routes.health_routes.mongodb_connection",
            mock_conn,
        ):
            response = client.get("/health")

            assert response.status_code == HTTPStatus.SERVICE_UNAVAILABLE
            assert response.json() == {"detail": "Database unavailable"}
