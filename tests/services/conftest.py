"""Fixtures compartidas para tests de integración de microservicios."""

import importlib.util
import sys
import types
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

VALIDATION_DIR = PROJECT_ROOT / "services" / "validation-service"
EXTRACTION_DIR = PROJECT_ROOT / "services" / "extraction-service"
PERSISTENCE_DIR = PROJECT_ROOT / "services" / "persistence-service"


def _load_module(module_name: str, file_path: Path) -> types.ModuleType:
    """Carga un archivo .py como módulo con nombre único, sin tocar sys.path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _load_app(service_dir: Path, tag: str) -> "FastAPI":
    """Carga main.py de un servicio resolviendo sus imports internos por sys.modules."""
    main_path = service_dir / "main.py"
    return _load_module(f"{tag}_main", main_path).app


def _register(name: str, module) -> None:
    sys.modules[name] = module


def _session_cleanup(service_dir: Path, *names) -> None:
    sys.path = [p for p in sys.path if p != str(service_dir)]
    for name in names:
        sys.modules.pop(name, None)


@pytest.fixture
def validation_client():
    from shared.domain.pdf_validator import PdfValidator

    _register("routes", _load_module("validation_routes", VALIDATION_DIR / "routes.py"))
    app = _load_app(VALIDATION_DIR, "validation")
    client = TestClient(app)
    yield client
    _session_cleanup(VALIDATION_DIR, "routes", "validation_main")


@pytest.fixture
def extraction_client():
    """TestClient para extraction-service (mock de la llamada HTTP a persistence)."""

    _register("app", _load_module("extraction_app", EXTRACTION_DIR / "app.py"))
    _register("routes", _load_module("extraction_routes", EXTRACTION_DIR / "routes.py"))

    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"id": "mock-doc-001", "content": "", "checksum": "abc"}
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.AsyncClient.post", new=AsyncMock(return_value=mock_response)):
        app = _load_app(EXTRACTION_DIR, "extraction")
        client = TestClient(app)
        yield client
    _session_cleanup(EXTRACTION_DIR, "app", "routes", "extraction_main")


@pytest.fixture
def persistence_client():
    """TestClient para persistence-service con módulos de Mongo fabricados (sin conexión real)."""

    mock_connection = MagicMock()
    mock_connection.connect = AsyncMock()
    mock_connection.disconnect = AsyncMock()

    fake_conn_module = types.ModuleType("persistence.mongodb_connection")
    fake_conn_module.MongoDBConnection = MagicMock()
    fake_conn_module.mongodb_connection = mock_connection

    mock_repo = MagicMock()
    _store: dict[str, dict] = {}

    def _create(doc_id, content, checksum):
        from uuid import uuid4

        did = doc_id or str(uuid4())
        doc = {"id": did, "content": content, "checksum": checksum}
        _store[did] = doc
        return doc

    def _get(doc_id):
        if doc_id not in _store:
            from fastapi import HTTPException

            raise HTTPException(status_code=404, detail="Document not found")
        return _store[doc_id]

    def _list_all():
        return list(_store.values())

    def _update(doc_id, content=None, checksum=None):
        if doc_id not in _store:
            from fastapi import HTTPException

            raise HTTPException(status_code=404, detail="Document not found")
        doc = _store[doc_id]
        if content is not None:
            doc["content"] = content
        if checksum is not None:
            doc["checksum"] = checksum
        return doc

    def _delete(doc_id):
        if doc_id not in _store:
            from fastapi import HTTPException

            raise HTTPException(status_code=404, detail="Document not found")
        del _store[doc_id]

    mock_repo.create = AsyncMock(side_effect=_create)
    mock_repo.get = AsyncMock(side_effect=_get)
    mock_repo.list_all = AsyncMock(side_effect=_list_all)
    mock_repo.update = AsyncMock(side_effect=_update)
    mock_repo.delete = AsyncMock(side_effect=_delete)

    fake_repo_cls = MagicMock(return_value=mock_repo)
    fake_repo_module = types.ModuleType("persistence.repository")
    fake_repo_module.DocumentRepository = fake_repo_cls

    _register("persistence", types.ModuleType("persistence"))
    _register("persistence.mongodb_connection", fake_conn_module)
    _register("persistence.repository", fake_repo_module)
    _register("routes", _load_module("persistence_routes", PERSISTENCE_DIR / "routes.py"))

    app = _load_app(PERSISTENCE_DIR, "persistence")
    client = TestClient(app)
    yield client
    _store.clear()
    _session_cleanup(
        PERSISTENCE_DIR,
        "persistence",
        "persistence.mongodb_connection",
        "persistence.repository",
        "routes",
        "persistence_main",
    )