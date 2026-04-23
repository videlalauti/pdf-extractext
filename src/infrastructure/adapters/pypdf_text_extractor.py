"""Adaptador de extracción de texto usando PyPDF.

Este adaptador implementa el puerto TextExtractorPort utilizando la librería
pypdf para extraer texto de documentos PDF. Funciona puramente en memoria,
sin persistir archivos temporalmente en disco.

Patrón: Adapter (Infrastructure Layer)
Librería externa: pypdf
"""

from io import BytesIO

from pypdf import PdfReader

from src.application.ports.text_extractor_port import TextExtractorPort
from src.domain.exceptions import PdfExtractionError


class PyPdfTextExtractor:
    """Adaptador concreto para extracción de texto usando pypdf.

    Este adaptador implementa el protocolo TextExtractorPort y permite
    extraer texto de PDFs utilizando la librería pypdf. El procesamiento
    se realiza completamente en memoria usando BytesIO.

    Attributes:
        None (stateless)

    Example:
        >>> extractor = PyPdfTextExtractor()
        >>> with open("documento.pdf", "rb") as f:
        ...     text = extractor.extract_text_from_bytes(f.read())
        >>> print(text)
        'Contenido del PDF...'

    Note:
        Este adaptador procesa el PDF puramente en memoria utilizando
        BytesIO, sin crear archivos temporales en disco.
    """

    def extract_text_from_bytes(self, pdf_bytes: bytes) -> str:
        """Extrae texto plano de un PDF proporcionado como bytes.

        Utiliza pypdf.PdfReader para procesar el documento en memoria
        y extraer todo el texto contenido en todas las páginas.

        Args:
            pdf_bytes: Contenido binario del PDF.

        Returns:
            str: Texto plano extraído del documento. Si el PDF no contiene
                 texto o está compuesto solo de imágenes, retorna string vacío.

        Raises:
            PdfExtractionError: Si el PDF está corrupto, malformado, o si
                               ocurre cualquier error durante la extracción.
            ValueError: Si pdf_bytes es None o vacío (delegado a pypdf).

        Implementation Details:
            - Usa BytesIO para mantener el procesamiento en memoria
            - Extrae texto de todas las páginas concatenándolas con salto de línea
            - Maneja excepciones específicas de pypdf y las convierte a excepciones de dominio
        """
        if not pdf_bytes:
            raise ValueError("Los bytes del PDF no pueden estar vacíos")

        try:
            # Procesamiento puramente en memoria usando BytesIO
            pdf_stream = BytesIO(pdf_bytes)
            reader = PdfReader(pdf_stream)

            # Extraer texto de todas las páginas
            extracted_texts = []
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    extracted_texts.append(page_text)

            # Unir todo el texto con saltos de línea entre páginas
            return "\n".join(extracted_texts)

        except Exception as error:
            # Convertimos excepciones de pypdf a excepciones de dominio
            # para mantener la independencia de la infraestructura
            raise PdfExtractionError(
                message=f"Error al extraer texto con pypdf: {str(error)}",
                original_error=error,
            ) from error
