"""Entidad Document del dominio.

Representa un documento procesado con su texto extraído y checksum.
"""

from dataclasses import dataclass

from src.domain.exceptions import ValidationError


@dataclass(frozen=True)
class Document:
    """Entidad de dominio que representa un documento procesado.

    Attributes:
        id: Identificador único del documento.
        content: Texto extraído del archivo PDF.
        checksum: Checksum del archivo para verificar integridad.

    Raises:
        ValidationError: Si el checksum está vacío.
    """

    id: str
    content: str
    checksum: str

    def __post_init__(self):
        if not self.checksum:
            raise ValidationError("checksum cannot be empty")
