"""Tests para el servicio de extracción de texto de PDFs.

Siguiendo TDD (Test-Driven Development):
- Tests primero, implementación después
- Tests de comportamiento, no de implementación
- Cada test describe una capacidad observable del sistema
"""

import pytest
from io import BytesIO
from unittest.mock import Mock, create_autospec
from typing import Protocol, runtime_checkable

from src.application.services.pdf_text_extractor import PdfTextExtractor
from src.domain.exceptions import InvalidPdfFormatError, PdfExtractionError


class TestPdfTextExtractor:
    """Tests para el caso de uso de extracción de texto."""

    @pytest.fixture
    def valid_pdf_bytes(self) -> bytes:
        """PDF mínimo válido en memoria con texto simple.

        Este es un PDF de 1 página con texto "Hello World" embebido.
        Usamos un PDF real pero mínimo para testing.
        """
        # PDF mínimo válido con texto "Hello"
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

    @pytest.fixture
    def extractor(self):
        """Instancia del extractor usando pypdf real."""
        from src.infrastructure.adapters.pypdf_text_extractor import PyPdfTextExtractor

        return PdfTextExtractor(extractor_adapter=PyPdfTextExtractor())

    def test_extract_text_from_valid_pdf_returns_text(self, extractor, valid_pdf_bytes):
        """Dado un PDF válido en memoria, extrae y retorna el texto contenido."""
        result = extractor.extract_text(valid_pdf_bytes)

        assert result is not None
        assert isinstance(result, str)
        assert "Hello" in result or "World" in result

    def test_extract_text_returns_empty_string_for_pdf_without_text(self, extractor):
        """Dado un PDF válido sin contenido textual, retorna string vacío."""
        # PDF sin texto (solo estructura)
        pdf_without_text = b"""%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj
2 0 obj
<<
/Type /Pages
/Kids []
/Count 0
>>
endobj
trailer
<<
/Size 3
/Root 1 0 R
>>
startxref
105
%%EOF"""

        result = extractor.extract_text(pdf_without_text)

        assert result == ""

    def test_extract_text_from_corrupted_pdf_raises_extraction_error(self, extractor):
        """Dado un PDF corrupto (no parseable), lanza PdfExtractionError."""
        corrupted_bytes = b"%PDF-1.4\nINCOMPLETE DATA"

        with pytest.raises(PdfExtractionError):
            extractor.extract_text(corrupted_bytes)

    def test_extract_text_with_empty_bytes_raises_value_error(self, extractor):
        """Dado bytes vacíos, lanza ValueError."""
        with pytest.raises(ValueError, match="Los bytes del PDF no pueden estar vacíos"):
            extractor.extract_text(b"")

    def test_extract_text_processing_is_pure_in_memory(self, extractor, valid_pdf_bytes):
        """Verifica que el procesamiento ocurre puramente en memoria sin I/O de disco."""
        import tempfile
        import os

        # Monitorear que no se crean archivos temporales
        temp_dir_before = set(
            os.listdir(tempfile.gettempdir()) if os.path.exists(tempfile.gettempdir()) else []
        )

        result = extractor.extract_text(valid_pdf_bytes)

        temp_dir_after = set(
            os.listdir(tempfile.gettempdir()) if os.path.exists(tempfile.gettempdir()) else []
        )

        # No deberían haberse creado archivos nuevos
        assert temp_dir_before == temp_dir_after or len(temp_dir_after - temp_dir_before) == 0
        assert result is not None


class TestPdfTextExtractorInterface:
    """Tests para verificar que el extractor sigue el principio de Inversión de Dependencias."""

    def test_extractor_uses_adapter_interface(self):
        """El extractor debe depender de una abstracción, no de implementación concreta."""
        from src.application.ports.text_extractor_port import TextExtractorPort
        from src.application.services.pdf_text_extractor import PdfTextExtractor

        # Crear mock que cumple con el protocolo
        mock_adapter = Mock(spec=TextExtractorPort)
        mock_adapter.extract_text_from_bytes.return_value = "Texto de prueba"

        extractor = PdfTextExtractor(extractor_adapter=mock_adapter)
        result = extractor.extract_text(b"dummy bytes")

        mock_adapter.extract_text_from_bytes.assert_called_once_with(b"dummy bytes")
        assert result == "Texto de prueba"

    def test_adapter_can_be_swapped(self):
        """Verifica que podemos intercambiar implementaciones del adaptador."""
        from src.application.ports.text_extractor_port import TextExtractorPort
        from src.application.services.pdf_text_extractor import PdfTextExtractor

        class MockAdapter:
            def extract_text_from_bytes(self, pdf_bytes: bytes) -> str:
                return "MOCKED TEXT"

        extractor = PdfTextExtractor(extractor_adapter=MockAdapter())
        result = extractor.extract_text(b"any bytes")

        assert result == "MOCKED TEXT"
