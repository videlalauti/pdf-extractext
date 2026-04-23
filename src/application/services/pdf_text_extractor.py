"""Servicio de aplicación para extracción de texto de PDFs.

Este servicio orquesta la extracción de texto asegurando que:
- Los inputs sean validados antes del procesamiento
- El procesamiento ocurra puramente en memoria
- Las excepciones del dominio sean propagadas adecuadamente

Aplica el principio de Inversión de Dependencias (SOLID) al depender
únicamente de la abstracción TextExtractorPort, no de implementaciones concretas.
"""

from src.application.ports.text_extractor_port import TextExtractorPort
from src.domain.exceptions import PdfExtractionError


class PdfTextExtractor:
    """Caso de uso: Extraer texto plano de un documento PDF.

    Este servicio representa un caso de uso de la capa de aplicación
    que orquesta el flujo de extracción de texto manteniendo la lógica
    de negocio (dominio) separada de los detalles de implementación.

    Attributes:
        _extractor_adapter: Adaptador que implementa TextExtractorPort

    Example:
        >>> from src.infrastructure.adapters.pypdf_text_extractor import PyPdfTextExtractor
        >>> extractor = PdfTextExtractor(extractor_adapter=PyPdfTextExtractor())
        >>> text = extractor.extract_text(pdf_bytes)
    """

    def __init__(self, extractor_adapter: TextExtractorPort) -> None:
        """Inicializa el servicio con un adaptador de extracción.

        Args:
            extractor_adapter: Implementación concreta del puerto de extracción.
                              Puede ser PyPDF, pdfplumber, o cualquier otro adaptador
                              que cumpla con el protocolo TextExtractorPort.

        Note:
            Siguiendo el principio de Inversión de Dependencias (DIP), este servicio
            depende de la abstracción TextExtractorPort, no de una implementación concreta.
        """
        self._extractor_adapter = extractor_adapter

    def extract_text(self, pdf_bytes: bytes) -> str:
        """Extrae texto plano de un PDF proporcionado como bytes.

        Este método:
        1. Valida que los bytes no estén vacíos (validación básica)
        2. Delega la extracción al adaptador configurado
        3. Propaga errores de extracción como excepciones de dominio

        Args:
            pdf_bytes: Contenido binario del PDF. Debe ser previamente validado
                      como PDF válido (ej: por PdfValidator) antes de llamar
                      este método.

        Returns:
            str: Texto plano extraído del documento. Retorna string vacío
                 si el PDF no contiene texto extraíble.

        Raises:
            ValueError: Si pdf_bytes está vacío o es None.
            PdfExtractionError: Si ocurre un error durante la extracción del texto.

        Note:
            El procesamiento es estrictamente en memoria. El documento nunca
            se persiste temporalmente en disco durante este proceso.
        """
        if not pdf_bytes:
            raise ValueError("Los bytes del PDF no pueden estar vacíos")

        try:
            return self._extractor_adapter.extract_text_from_bytes(pdf_bytes)
        except Exception as error:
            # Envolvemos la excepción en una excepción de dominio
            # para mantener la independencia de la capa de aplicación
            raise PdfExtractionError(
                message=f"Error al extraer texto del PDF: {str(error)}",
                original_error=error,
            ) from error
