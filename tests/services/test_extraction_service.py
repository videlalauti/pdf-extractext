"""Tests de integración para extraction-service."""


def _simple_pdf() -> bytes:
    return b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [] /Count 0 >>\nendobj\n%%EOF"


def test_health_check(extraction_client):
    resp = extraction_client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "healthy"
    assert body["service"] == "extraction-service"


def test_extract_valid_pdf_returns_text(extraction_client):
    pdf = _simple_pdf()
    resp = extraction_client.post(
        "/extract",
        files={"file": ("doc.pdf", pdf, "application/pdf")},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert "text" in body
    assert isinstance(body["text"], str)


def test_extract_non_pdf_returns_400(extraction_client):
    resp = extraction_client.post(
        "/extract",
        files={"file": ("doc.txt", b"not a pdf", "text/plain")},
    )
    assert resp.status_code == 400
