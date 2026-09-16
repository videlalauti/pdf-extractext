"""Caso de uso para subir y procesar documentos PDF.

Este caso de uso orquesta el flujo completo de upload:
1. Validación del PDF (formato y tamaño)
2. Extracción del texto
3. Persistencia con verificación de duplicados (checksum)

Todo el procesamiento ocurre puramente en memoria: recibe los bytes
del PDF y no realiza operaciones de I/O en disco.
"""

import hashlib
from uuid import uuid4

from src.application.services.pdf_text_extractor import PdfTextExtractor
from src.application.services.pdf_validator import PdfValidator
from src.domain.entities.document import Document
from src.domain.exceptions import DuplicateDocumentError
from src.domain.repositories.document_repository import DocumentRepository


class UploadDocumentUseCase:
    """Caso de uso: Subir y procesar un documento PDF.

    Orquesta el flujo completo de procesamiento de PDFs, trabajando
    únicamente en memoria (sin archivos temporales en disco):
    - Valida el formato y tamaño del archivo
    - Extrae el texto usando el adaptador configurado
    - Genera checksum y verifica duplicados
    - Persiste el documento si no es duplicado

    Attributes:
        _repository: Repositorio de documentos inyectado.
        _extractor: Servicio de extracción de texto.
        _validator: Servicio de validación de PDFs (opcional).
    """

    def __init__(
        self,
        repository: DocumentRepository,
        extractor: PdfTextExtractor,
        validator: PdfValidator | None = None,
    ) -> None:
        """Inicializa el caso de uso con las dependencias requeridas.

        Args:
            repository: Repositorio para persistir documentos.
            extractor: Servicio para extraer texto de PDFs.
            validator: Servicio para validar PDFs (formato y tamaño).
        """
        self._repository = repository
        self._extractor = extractor
        self._validator = validator

    def _generate_checksum(self, pdf_bytes: bytes) -> str:
        """Genera checksum SHA-256 del contenido."""
        return hashlib.sha256(pdf_bytes).hexdigest()

    async def execute(self, pdf_bytes: bytes, filename: str = "") -> Document:
        """Ejecuta el flujo completo de upload de PDF, puramente en memoria.

        Args:
            pdf_bytes: Contenido binario del PDF a procesar.
            filename: Nombre del archivo subido (sin uso en la persistencia).

        Returns:
            Document: Documento persistido con el texto extraído.

        Raises:
            InvalidPdfFormatError: Si el archivo no es un PDF válido
            PdfTooLargeError: Si el archivo excede el tamaño máximo permitido
            DuplicateDocumentError: Si el checksum ya existe en el sistema
            PdfExtractionError: Si ocurre un error durante la extracción del texto
        """
        # Paso 1: Validar el PDF (formato y tamaño)
        if self._validator is not None:
            self._validator.validate_or_raise(pdf_bytes)

        # Paso 2: Extraer texto del PDF directamente desde bytes
        extracted_text = await self._extractor.extract_text_from_bytes(pdf_bytes)

        # Paso 3: Verificar duplicados por checksum
        checksum = self._generate_checksum(pdf_bytes)
        if await self._repository.exists_by_checksum(checksum):
            raise DuplicateDocumentError(checksum)

        # Paso 4: Persistir el documento
        document = Document(id=str(uuid4()), content=extracted_text, checksum=checksum)
        return await self._repository.save(document)
