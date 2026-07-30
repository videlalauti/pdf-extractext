import os
import uuid
from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import FastAPI, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from pydantic import BaseModel, Field


class MongoDBConnection:
    _instance: Optional["MongoDBConnection"] = None
    _client: Optional[AsyncIOMotorClient] = None
    _database: Optional[AsyncIOMotorDatabase] = None

    def __new__(cls) -> "MongoDBConnection":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def is_connected(self) -> bool:
        return self._client is not None

    async def connect(self) -> None:
        if self.is_connected:
            return

        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            user = os.getenv("MONGODB_ROOT_USERNAME", "admin")
            password = os.getenv("MONGODB_ROOT_PASSWORD", "changeme")
            host = os.getenv("MONGODB_HOST", "mongo")
            port = os.getenv("MONGODB_PORT", "27017")
            db_name = os.getenv("MONGODB_DATABASE_NAME", "pdf_extractext")
            auth_source = os.getenv("MONGODB_AUTH_SOURCE", "admin")
            if user and password:
                db_url = f"mongodb://{user}:{password}@{host}:{port}/{db_name}?authSource={auth_source}"
            else:
                db_url = f"mongodb://{host}:{port}/{db_name}"

        db_name = os.getenv("MONGODB_DATABASE_NAME", "pdf_extractext")

        try:
            self._client = AsyncIOMotorClient(
                db_url,
                maxPoolSize=50,
                minPoolSize=10,
                maxIdleTimeMS=45000,
                serverSelectionTimeoutMS=5000,
            )
            self._database = self._client[db_name]
            await self._client.admin.command("ping")
        except Exception as error:
            raise ConnectionError(f"Failed to connect to MongoDB: {error}") from error

    async def disconnect(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None
            self._database = None

    def get_database(self) -> AsyncIOMotorDatabase:
        if self._database is None:
            raise RuntimeError("Database connection not established. Call connect() first.")
        return self._database

    def get_collection(self, collection_name: str = "documents") -> AsyncIOMotorCollection:
        return self.get_database()[collection_name]


mongodb_connection = MongoDBConnection()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await mongodb_connection.connect()
    yield
    await mongodb_connection.disconnect()


app = FastAPI(title="Document Persistence Service", version="1.0.0", lifespan=lifespan)


class DocumentCreate(BaseModel):
    id: Optional[str] = None
    content: str
    checksum: str


class DocumentUpdate(BaseModel):
    content: Optional[str] = None
    checksum: Optional[str] = None


class DocumentResponse(BaseModel):
    id: str
    content: str
    checksum: str


@app.post("/documents", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document(doc: DocumentCreate):
    collection = mongodb_connection.get_collection("documents")
    doc_id = doc.id or str(uuid.uuid4())
    doc_data = {
        "_id": doc_id,
        "content": doc.content,
        "checksum": doc.checksum,
    }
    await collection.insert_one(doc_data)
    return DocumentResponse(id=doc_id, content=doc.content, checksum=doc.checksum)


@app.get("/documents", response_model=List[DocumentResponse])
async def get_documents():
    collection = mongodb_connection.get_collection("documents")
    cursor = collection.find()
    documents = []
    async for item in cursor:
        documents.append(
            DocumentResponse(
                id=str(item["_id"]),
                content=item.get("content", ""),
                checksum=item.get("checksum", ""),
            )
        )
    return documents


@app.get("/documents/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: str):
    collection = mongodb_connection.get_collection("documents")
    data = await collection.find_one({"_id": document_id})
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    return DocumentResponse(
        id=str(data["_id"]),
        content=data.get("content", ""),
        checksum=data.get("checksum", ""),
    )


@app.put("/documents/{document_id}", response_model=DocumentResponse)
async def update_document(document_id: str, doc_update: DocumentUpdate):
    collection = mongodb_connection.get_collection("documents")
    update_data = {k: v for k, v in doc_update.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")

    result = await collection.update_one({"_id": document_id}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    data = await collection.find_one({"_id": document_id})
    return DocumentResponse(
        id=str(data["_id"]),
        content=data.get("content", ""),
        checksum=data.get("checksum", ""),
    )


@app.delete("/documents/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(document_id: str):
    collection = mongodb_connection.get_collection("documents")
    result = await collection.delete_one({"_id": document_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
