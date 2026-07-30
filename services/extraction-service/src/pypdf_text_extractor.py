"""Adaptador de extracción de texto usando PyPDF."""

from io import BytesIO
from pypdf import PdfReader


class PdfExtractionError(Exception):
    def __init__(
        self,
        message: str = "Error al extraer texto del PDF",
        original_error: Exception | None = None,
    ):
        self.original_error = original_error
        super().__init__(message)


class PyPdfTextExtractor:
    def extract_text_from_bytes(self, pdf_bytes: bytes) -> str:
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
