"""Interfaz del repositorio de documentos PDF.

Esta interfaz define el contrato para la persistencia de documentos,
permitiendo diferentes implementaciones (MongoDB, filesystem, etc).
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.entities.document import Document


class DocumentRepository(ABC):
    """Contrato para el acceso a datos de documentos PDF.

    Esta interfaz define las operaciones disponibles para
    persistir y recuperar entidades Document.
    """

    @abstractmethod
    def save(self, document: Document) -> Document:
        """Guarda un documento en el repositorio.

        Args:
            document: Entidad a persistir.

        Returns:
            Document: Documento persistido.
        """
        pass

    @abstractmethod
    def find_by_id(self, document_id: UUID) -> Optional[Document]:
        """Busca un documento por su identificador.

        Args:
            document_id: UUID del documento.

        Returns:
            Optional[Document]: Documento encontrado o None.
        """
        pass

    @abstractmethod
    def find_all(self) -> List[Document]:
        """Recupera todos los documentos.

        Returns:
            List[Document]: Lista de todos los documentos.
        """
        pass

    @abstractmethod
    def find_by_filename(self, filename: str) -> Optional[Document]:
        """Busca un documento por su nombre de archivo.

        Args:
            filename: Nombre del archivo.

        Returns:
            Optional[Document]: Documento encontrado o None.
        """
        pass

    @abstractmethod
    def delete(self, document_id: UUID) -> bool:
        """Elimina un documento por su identificador.

        Args:
            document_id: UUID del documento a eliminar.

        Returns:
            bool: True si se eliminó, False si no existía.
        """
        pass
