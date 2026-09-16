"""Repositorio CRUD sobre la colección documents; toda la lógica de persistencia."""

import uuid
from typing import List, Optional

from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorCollection

from persistence.mongodb_connection import MongoDBConnection


class DocumentRepository:
    """Encapsula el acceso a Mongo; la colección se resuelve una sola vez en __init__."""

    COLLECTION_NAME = "documents"

    def __init__(self, connection: MongoDBConnection) -> None:
        self._collection = self.get_collection(connection, self.COLLECTION_NAME)

    @staticmethod
    def get_collection(connection: MongoDBConnection, collection_name: str) -> AsyncIOMotorCollection:
        return connection.get_database()[collection_name]

    async def create(self, doc_id: Optional[str], content: str, checksum: str) -> dict:
        document_id = doc_id or str(uuid.uuid4())
        await self._collection.insert_one(
            {"_id": document_id, "content": content, "checksum": checksum}
        )
        return {"id": document_id, "content": content, "checksum": checksum}

    async def list_all(self) -> List[dict]:
        documents = []
        async for item in self._collection.find():
            documents.append(self._to_dict(item))
        return documents

    async def get(self, document_id: str) -> dict:
        data = await self._collection.find_one({"_id": document_id})
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
        return self._to_dict(data)

    async def update(self, document_id: str, content: Optional[str], checksum: Optional[str]) -> dict:
        update_data = {k: v for k, v in {"content": content, "checksum": checksum}.items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")

        result = await self._collection.update_one({"_id": document_id}, {"$set": update_data})
        if result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

        data = await self._collection.find_one({"_id": document_id})
        return self._to_dict(data)

    async def delete(self, document_id: str) -> None:
        result = await self._collection.delete_one({"_id": document_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    @staticmethod
    def _to_dict(data) -> dict:
        return {
            "id": str(data["_id"]),
            "content": data.get("content", ""),
            "checksum": data.get("checksum", ""),
        }