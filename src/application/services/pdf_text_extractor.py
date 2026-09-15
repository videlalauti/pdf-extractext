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
    """Servicio de aplicación: Extraer texto plano de un documento PDF.

    Orquesta el flujo de extracción de texto manteniendo la lógica
    de negocio (dominio) separada de los detalles de implementación.
    Trabaja únicamente con bytes en memoria, sin I/O de disco.

    Attributes:
        _extractor_adapter: Adaptador que implementa TextExtractorPort

    Example:
        >>> from src.application.ports.text_extractor_port import TextExtractorPort
        >>> extractor = PdfTextExtractor(extractor_adapter=extractor_adapter)
        >>> text = await extractor.extract_text_from_bytes(pdf_bytes)
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

    async def extract_text_from_bytes(self, pdf_bytes: bytes) -> str:
        """Extrae texto plano de un PDF proporcionado como bytes.

        Este método:
        1. Delega la extracción al adaptador configurado
        2. Propaga errores de extracción como excepciones de dominio

        Args:
            pdf_bytes: Contenido binario del PDF.

        Returns:
            str: Texto plano extraído del documento. Retorna string vacío
                 si el PDF no contiene texto extraíble.

        Raises:
            PdfExtractionError: Si ocurre un error durante la extracción del texto.
        """
        try:
            return await self._extractor_adapter.extract_text_from_bytes(pdf_bytes)
        except Exception as error:
            raise PdfExtractionError(
                message=f"Error al extraer texto del PDF: {str(error)}",
                original_error=error,
            ) from error
