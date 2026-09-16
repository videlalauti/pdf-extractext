"""Tests de integración para validation-service."""


def test_health_check(validation_client):
    resp = validation_client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "healthy"
    assert body["service"] == "validation-service"


def test_validate_valid_pdf_returns_valid(validation_client):
    pdf = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\n%%EOF"
    resp = validation_client.post(
        "/validate",
        files={"file": ("test.pdf", pdf, "application/pdf")},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["valid"] is True
    assert body["error"] is None


def test_validate_non_pdf_file_returns_invalid(validation_client):
    resp = validation_client.post(
        "/validate",
        files={"file": ("test.txt", b"not a pdf", "text/plain")},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["valid"] is False
    assert body["error"] is not None


def test_validate_empty_file_returns_invalid(validation_client):
    resp = validation_client.post(
        "/validate",
        files={"file": ("empty.pdf", b"", "application/pdf")},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["valid"] is False
    assert body["error"] is not None
