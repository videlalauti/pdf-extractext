"""Implementación en memoria del repositorio de documentos."""

from uuid import UUID

from src.domain.entities.document import Document
from src.domain.repositories.document_repository import DocumentRepository


class InMemoryDocumentRepository(DocumentRepository):
    """Implementación en memoria para pruebas y desarrollo.

    Almacena los documentos en un diccionario en memoria.
    Sin persistencia entre reinicios.
    """

    def __init__(self) -> None:
        """Inicializa el repositorio vacío."""
        self._documents: dict[str, Document] = {}
        self._by_checksum: dict[str, Document] = {}

    async def save(self, document: Document) -> Document:
        """Guarda o actualiza un documento.

        Args:
            document: Entidad a persistir.

        Returns:
            Document: Documento guardado.
        """
        self._documents[document.id] = document
        self._by_checksum[document.checksum] = document
        return document

    async def find_by_id(self, document_id: UUID) -> Document | None:
        """Busca un documento por UUID.

        Args:
            document_id: UUID del documento.

        Returns:
            Optional[Document]: Documento encontrado o None.
        """
        return self._documents.get(str(document_id))

    async def find_all(self) -> list[Document]:
        """Recupera todos los documentos.

        Returns:
            List[Document]: Lista de todos los documentos.
        """
        return list(self._documents.values())

    async def delete(self, document_id: UUID) -> bool:
        """Elimina un documento.

        Args:
            document_id: UUID del documento a eliminar.

        Returns:
            bool: True si existía y se eliminó.
        """
        doc_id = str(document_id)
        if doc_id in self._documents:
            document = self._documents.pop(doc_id)
            if document.checksum in self._by_checksum:
                del self._by_checksum[document.checksum]
            return True
        return False

    async def exists_by_checksum(self, checksum: str) -> bool:
        """Verifica si existe un documento con el checksum dado.

        Args:
            checksum: Checksum a verificar.

        Returns:
            bool: True si existe documento con ese checksum.
        """
        return checksum in self._by_checksum

    async def find_by_checksum(self, checksum: str) -> Document | None:
        """Retorna el documento con el checksum dado, si existe.

        Args:
            checksum: Checksum del archivo a buscar.

        Returns:
            Optional[Document]: Documento encontrado o None.
        """
        return self._by_checksum.get(checksum)
