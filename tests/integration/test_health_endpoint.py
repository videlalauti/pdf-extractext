"""Tests de integración para el endpoint de health check."""

from http import HTTPStatus
from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi.testclient import TestClient

from src.interface_adapters.http.main import app


@pytest.fixture
def client():
    """Provee un cliente de test."""
    return TestClient(app)


@pytest.fixture
def mock_db_command():
    """Mockea la dependencia mongodb_connection de la ruta /health.

    Solo se configura el contrato público de la conexión (is_connected y el
    ping a la DB), sin tocar atributos privados de la implementación real.
    """
    command = AsyncMock(return_value=True)

    connection = Mock()
    connection.is_connected = True
    connection.configure_mock(**{"_client.admin.command": command})

    with patch(
        "src.interface_adapters.http.routes.health_routes.mongodb_connection",
        connection,
    ):
        yield command


class TestHealthEndpoint:
    """Tests para el endpoint /health."""

    def test_health_check_success(self, client, mock_db_command):
        """GET /health debe retornar 200 cuando la DB está disponible."""
        response = client.get("/health")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {"status": "ok"}
        mock_db_command.assert_awaited_once_with("ping")

    def test_health_check_database_failure(self, client, mock_db_command):
        """GET /health debe retornar 503 cuando la DB no responde."""
        mock_db_command.side_effect = Exception("Connection refused")

        response = client.get("/health")

        assert response.status_code == HTTPStatus.SERVICE_UNAVAILABLE
        assert response.json() == {"detail": "Database unavailable"}
        mock_db_command.assert_awaited_once_with("ping")