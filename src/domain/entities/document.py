"""Entidad Document del dominio.

Representa un documento PDF con su contenido y metadatos.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass(frozen=True)
class Document:
    """Entidad de dominio que representa un documento PDF.

    Attributes:
        id: Identificador único del documento.
        filename: Nombre del archivo.
        content: Contenido extraído del PDF (texto).
        file_path: Ruta donde se almacena el archivo físico.
        uploaded_at: Fecha de subida.
        processed_at: Fecha de procesamiento (extracción de texto).
    """

    filename: str
    file_path: str
    id: UUID = field(default_factory=uuid4)
    content: str = ""
    uploaded_at: datetime = field(default_factory=datetime.utcnow)
    processed_at: Optional[datetime] = None

    def process(self, extracted_text: str) -> "Document":
        """Crea una nueva instancia con el texto procesado.

        Args:
            extracted_text: Texto extraído del PDF.

        Returns:
            Document: Nueva instancia con el contenido procesado.
        """
        return Document(
            id=self.id,
            filename=self.filename,
            file_path=self.file_path,
            content=extracted_text,
            uploaded_at=self.uploaded_at,
            processed_at=datetime.utcnow(),
        )

    def is_processed(self) -> bool:
        """Verifica si el documento ya fue procesado.

        Returns:
            bool: True si tiene contenido procesado.
        """
        return self.processed_at is not None and bool(self.content)
