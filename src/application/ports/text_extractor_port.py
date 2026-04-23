"""Puerto (interfaz) para extracción de texto de documentos.

Siguiendo el patrón de Arquitectura Limpia y Hexagonal,
este puerto define el contrato que cualquier adaptador de extracción
debe cumplir, permitiendo que la capa de aplicación permanezca
independiente de las implementaciones concretas de extracción.
"""

from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable


@runtime_checkable
class TextExtractorPort(Protocol):
    """Protocolo que define la interfaz para extracción de texto.

    Cualquier adaptador que implemente este protocolo puede ser usado
    por el servicio de aplicación para extraer texto de documentos.

    Ejemplo:
        >>> class PyPdfAdapter:
        ...     def extract_text_from_bytes(self, pdf_bytes: bytes) -> str:
        ...         # Implementación con pypdf
        ...         return "texto extraído"
        >>>
        >>> adapter = PyPdfAdapter()
        >>> isinstance(adapter, TextExtractorPort)
        True
    """

    def extract_text_from_bytes(self, pdf_bytes: bytes) -> str:
        """Extrae texto plano de un documento en formato bytes.

        Args:
            pdf_bytes: Contenido binario del documento PDF.

        Returns:
            str: Texto plano extraído del documento.

        Raises:
            PdfExtractionError: Si ocurre un error durante la extracción.
            ValueError: Si el input es inválido.
        """
        ...


class AbstractTextExtractor(ABC):
    """Clase abstracta base para adaptadores de extracción.

    Proporciona una implementación de referencia para casos donde
    se prefiere herencia sobre protocolos.
    """

    @abstractmethod
    def extract_text_from_bytes(self, pdf_bytes: bytes) -> str:
        """Extrae texto plano de un documento en formato bytes.

        Args:
            pdf_bytes: Contenido binario del documento PDF.

        Returns:
            str: Texto plano extraído del documento.

        Raises:
            PdfExtractionError: Si ocurre un error durante la extracción.
            ValueError: Si el input es inválido.
        """
        pass
