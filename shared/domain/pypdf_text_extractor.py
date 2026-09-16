"""Extracción de texto con pypdf, compartida entre monolith y microservicios."""

from io import BytesIO

from pypdf import PdfReader

from shared.domain.exceptions import PdfExtractionError


class PyPdfTextExtractor:
    """Procesa el PDF en memoria con BytesIO, sin crear archivos temporales."""

    async def extract_text_from_bytes(self, pdf_bytes: bytes) -> str:
        """Extrae texto de todas las páginas, o vacío si no hay texto extraíble."""
        if not pdf_bytes:
            raise ValueError("Los bytes del PDF no pueden estar vacíos")

        try:
            pdf_stream = BytesIO(pdf_bytes)
            reader = PdfReader(pdf_stream)

            extracted_texts = []
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    extracted_texts.append(page_text)

            return "\n".join(extracted_texts)
        except Exception as error:
            raise PdfExtractionError(
                message=f"Error al extraer texto con pypdf: {str(error)}",
                original_error=error,
            ) from error