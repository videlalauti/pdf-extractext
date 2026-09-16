"""Integration smoke test: verify the full app can respond to HTTP."""

import pytest
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_app_starts_and_health_responds():
    from src.interface_adapters.http.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code in (200, 503)