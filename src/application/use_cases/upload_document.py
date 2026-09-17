"""Caso de uso para subir y procesar documentos PDF.

Este caso de uso orquesta el flujo completo de upload:
1. Validación del PDF (formato y tamaño)
2. Extracción del texto
3. Persistencia con verificación de duplicados (checksum)

Todo el procesamiento ocurre puramente en memoria: recibe los bytes
del PDF y no realiza operaciones de I/O en disco.
"""

import hashlib
from dataclasses import dataclass
from uuid import uuid4

from src.application.services.pdf_text_extractor import PdfTextExtractor
from src.application.services.pdf_validator import PdfValidator
from src.domain.entities.document import Document
from src.domain.repositories.document_repository import DocumentRepository


@dataclass(frozen=True)
class UploadDocumentResult:
    """Resultado del upload: documento resultante y si fue creado o cacheado.

    Attributes:
        document: Documento persistido o existente (cache hit).
        created: True si se creó en este request, False si ya existía.
    """

    document: Document
    created: bool


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

    async def execute(self, pdf_bytes: bytes, filename: str = "") -> UploadDocumentResult:
        """Ejecuta el flujo completo de upload de PDF, puramente en memoria.

        Los repetidos se resuelven antes de extraer: el checksum se calcula
        primero y, si el documento ya existe, se devuelve el cacheado sin
        volver a validar, extraer ni persistir.

        Args:
            pdf_bytes: Contenido binario del PDF a procesar.
            filename: Nombre del archivo subido (sin uso en la persistencia).

        Returns:
            UploadDocumentResult: Documento resultante e indicador de si fue creado.

        Raises:
            InvalidPdfFormatError: Si el archivo no es un PDF válido
            PdfTooLargeError: Si el archivo excede el tamaño máximo permitido
            PdfExtractionError: Si ocurre un error durante la extracción del texto
        """
        # Paso 1: Verificar duplicados por checksum (el repositorio actúa como cache)
        checksum = self._generate_checksum(pdf_bytes)
        existing = await self._repository.find_by_checksum(checksum)
        if existing is not None:
            return UploadDocumentResult(document=existing, created=False)

        # Paso 2: Validar el PDF (formato y tamaño)
        if self._validator is not None:
            self._validator.validate_or_raise(pdf_bytes)

        # Paso 3: Extraer texto del PDF directamente desde bytes
        extracted_text = await self._extractor.extract_text_from_bytes(pdf_bytes)

        # Paso 4: Persistir el documento
        document = Document(id=str(uuid4()), content=extracted_text, checksum=checksum)
        saved = await self._repository.save(document)
        return UploadDocumentResult(document=saved, created=True)
