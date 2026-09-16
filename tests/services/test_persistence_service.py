"""Tests de integración para persistence-service."""


def test_health_check(persistence_client):
    resp = persistence_client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "healthy"
    assert body["service"] == "persistence-service"


def test_create_and_get_document(persistence_client):
    payload = {"content": "extracted text", "checksum": "abc123"}
    create_resp = persistence_client.post("/documents", json=payload)
    assert create_resp.status_code == 201
    doc = create_resp.json()
    doc_id = doc["id"]
    assert doc["content"] == "extracted text"
    assert doc["checksum"] == "abc123"

    get_resp = persistence_client.get(f"/documents/{doc_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["content"] == "extracted text"


def test_list_documents(persistence_client):
    persistence_client.post("/documents", json={"content": "text-a", "checksum": "a"})
    persistence_client.post("/documents", json={"content": "text-b", "checksum": "b"})
    resp = persistence_client.get("/documents")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_get_document_not_found(persistence_client):
    resp = persistence_client.get("/documents/nonexistent-id")
    assert resp.status_code == 404


def test_delete_document(persistence_client):
    create_resp = persistence_client.post(
        "/documents", json={"content": "to-delete", "checksum": "d"}
    )
    doc_id = create_resp.json()["id"]

    del_resp = persistence_client.delete(f"/documents/{doc_id}")
    assert del_resp.status_code == 204

    get_resp = persistence_client.get(f"/documents/{doc_id}")
    assert get_resp.status_code == 404
