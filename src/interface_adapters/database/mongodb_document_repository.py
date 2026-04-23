"""Adaptador de repositorio MongoDB para documentos.

Implementa la interfaz DocumentRepository para persistir
documentos en MongoDB usando Motor (driver asincrono).
"""

from typing import List, Optional
from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorCollection

from src.domain.entities.document import Document
from src.domain.repositories.document_repository import DocumentRepository
from src.interface_adapters.database.schemas.document_schema import DocumentMongoSchema
from src.infrastructure.adapters.mongodb_connection import mongodb_connection


class MongoDBDocumentRepository(DocumentRepository):
    """Repositorio MongoDB para entidades Document.

    Implementa el patron Repository de Domain-Driven Design,
    abstrayendo la persistencia en MongoDB.

    Attributes:
        _collection_name: Nombre de la coleccion en MongoDB.
    """

    COLLECTION_NAME = "documents"

    def __init__(self) -> None:
        """Inicializa el repositorio con conexion a MongoDB."""
        self._collection: Optional[AsyncIOMotorCollection] = None

    def _get_collection(self) -> AsyncIOMotorCollection:
        """Obtiene la coleccion de documentos.

        Returns:
            AsyncIOMotorCollection: Coleccion de MongoDB.

        Raises:
            RuntimeError: Si no hay conexion activa.
        """
        if self._collection is None:
            self._collection = mongodb_connection.get_collection(self.COLLECTION_NAME)
        return self._collection

    def _to_schema(self, document: Document) -> dict:
        """Convierte entidad a esquema MongoDB.

        Args:
            document: Entidad del dominio.

        Returns:
            dict: Diccionario compatible con MongoDB.
        """
        schema = DocumentMongoSchema(
            id=document.id, content=document.content, checksum=document.checksum
        )
        return schema.model_dump()

    def _to_entity(self, data: dict) -> Document:
        """Convierte documento MongoDB a entidad del dominio.

        Args:
            data: Documento de MongoDB.

        Returns:
            Document: Entidad del dominio.
        """
        return Document(
            id=str(data.get("_id")),
            content=data.get("content", ""),
            checksum=data.get("checksum", ""),
        )

    async def save(self, document: Document) -> Document:
        """Guarda un documento en MongoDB.

        Args:
            document: Entidad a persistir.

        Returns:
            Document: Documento persistido.
        """
        collection = self._get_collection()
        document_data = self._to_schema(document)

        await collection.insert_one(document_data)
        return document

    async def find_by_id(self, document_id: UUID) -> Optional[Document]:
        """Busca un documento por su ID.

        Args:
            document_id: UUID del documento.

        Returns:
            Optional[Document]: Documento encontrado o None.
        """
        collection = self._get_collection()
        data = await collection.find_one({"_id": str(document_id)})

        if data is None:
            return None
        return self._to_entity(data)

    async def find_all(self) -> List[Document]:
        """Recupera todos los documentos.

        Returns:
            List[Document]: Lista de documentos.
        """
        collection = self._get_collection()
        cursor = collection.find()
        documents = []

        async for data in cursor:
            documents.append(self._to_entity(data))

        return documents

    async def find_by_filename(self, filename: str) -> Optional[Document]:
        """Busca documento por nombre de archivo.

        Nota: Este repositorio no almacena filenames,
        por lo que siempre retorna None.

        Args:
            filename: Nombre del archivo.

        Returns:
            Optional[Document]: None (no implementado).
        """
        return None

    async def delete(self, document_id: UUID) -> bool:
        """Elimina un documento por su ID.

        Args:
            document_id: UUID del documento a eliminar.

        Returns:
            bool: True si se elimino, False si no existia.
        """
        collection = self._get_collection()
        result = await collection.delete_one({"_id": str(document_id)})
        return result.deleted_count > 0

    async def exists_by_checksum(self, checksum: str) -> bool:
        """Verifica si existe un documento con el checksum dado.

        Args:
            checksum: Checksum a verificar.

        Returns:
            bool: True si existe documento con ese checksum.
        """
        collection = self._get_collection()
        count = await collection.count_documents({"checksum": checksum})
        return count > 0
