"""Caso de uso para subir y procesar documentos PDF.

Este caso de uso orquesta el flujo completo de upload:
1. Validación del PDF (formato y tamaño)
2. Extracción del texto
3. Persistencia con verificación de duplicados (checksum)
"""

from dataclasses import dataclass

from src.application.services.pdf_text_extractor import PdfTextExtractor
from src.application.services.pdf_validator import PdfValidator
from src.application.use_cases.save_document import DuplicateDocumentError, SaveDocumentUseCase
from src.domain.entities.document import Document
from src.domain.exceptions import InvalidPdfFormatError, PdfTooLargeError


@dataclass
class UploadDocumentInput:
    """DTO de entrada para el caso de uso de upload."""

    pdf_bytes: bytes


@dataclass
class UploadDocumentOutput:
    """DTO de salida para el caso de uso de upload."""

    document: Document


class UploadDocumentUseCase:
    """Caso de uso: Subir y procesar un documento PDF.

    Orquesta el flujo completo de procesamiento de PDFs:
    - Valida el formato y tamaño del archivo
    - Extrae el texto usando el adaptador configurado
    - Genera checksum y verifica duplicados
    - Persiste el documento si no es duplicado

    Attributes:
        _validator: Servicio de validación de PDFs
        _extractor: Servicio de extracción de texto
        _save_use_case: Caso de uso para guardar documentos
    """

    def __init__(
        self,
        validator: PdfValidator,
        extractor: PdfTextExtractor,
        save_use_case: SaveDocumentUseCase,
    ) -> None:
        """Inicializa el caso de uso con las dependencias requeridas.

        Args:
            validator: Servicio para validar PDFs (formato y tamaño)
            extractor: Servicio para extraer texto de PDFs
            save_use_case: Caso de uso para persistir documentos
        """
        self._validator = validator
        self._extractor = extractor
        self._save_use_case = save_use_case

    async def execute(self, pdf_bytes: bytes) -> Document:
        """Ejecuta el flujo completo de upload de PDF.

        Args:
            pdf_bytes: Contenido binario del PDF a procesar

        Returns:
            Document: Documento persistido con el texto extraído

        Raises:
            InvalidPdfFormatError: Si el archivo no es un PDF válido
            PdfTooLargeError: Si el archivo excede el tamaño máximo permitido
            DuplicateDocumentError: Si el checksum ya existe en el sistema
            PdfExtractionError: Si ocurre un error durante la extracción del texto
        """
        # Paso 1: Validar el PDF (formato y tamaño)
        self._validator.validate_or_raise(pdf_bytes)

        # Paso 2: Extraer texto del PDF
        extracted_text = self._extractor.extract_text(pdf_bytes)

        # Paso 3: Guardar el documento (con verificación de duplicados)
        document = await self._save_use_case.execute(
            pdf_bytes=pdf_bytes,
            content=extracted_text,
        )

        return document
