"""Tests de integración para extraction-service."""


def _simple_pdf() -> bytes:
    return b"""%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj
2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj
3 0 obj
<<
/Type /Page
/Parent 2 0 R
/MediaBox [0 0 612 792]
/Resources <<
/Font <<
/F1 4 0 R
>>
>>
/Contents 5 0 R
>>
endobj
4 0 obj
<<
/Type /Font
/Subtype /Type1
/BaseFont /Helvetica
>>
endobj
5 0 obj
<<
/Length 44
>>
stream
BT
/F1 12 Tf
100 700 Td
(Hello World) Tj
ET
endstream
endobj
xref
0 6
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000266 00000 n 
0000000345 00000 n 
trailer
<<
/Size 6
/Root 1 0 R
>>
startxref
439
%%EOF"""


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
