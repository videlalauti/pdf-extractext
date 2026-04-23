"""Adaptador de conexión asíncrona a MongoDB usando Motor.

Implementa el patrón Singleton para la gestión de conexiones
y sigue los principios de Clean Architecture.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from src.infrastructure.config.settings import settings


class MongoDBConnection:
    """Gestor de conexión asíncrona a MongoDB.

    Implementa el patrón Singleton para garantizar una única
    instancia de conexión a la base de datos.

    Attributes:
        _instance: Instancia única del gestor de conexión.
        _client: Cliente asíncrono de MongoDB.
        _database: Referencia a la base de datos.
    """

    _instance: Optional["MongoDBConnection"] = None
    _client: Optional[AsyncIOMotorClient] = None
    _database: Optional[AsyncIOMotorDatabase] = None

    def __new__(cls) -> "MongoDBConnection":
        """Crea o retorna la instancia única del gestor de conexión."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def is_connected(self) -> bool:
        """Verifica si existe una conexión activa."""
        return self._client is not None

    async def connect(self) -> None:
        """Establece la conexión con MongoDB.

        Raises:
            ConnectionError: Si falla la conexión a MongoDB.
        """
        if self.is_connected:
            return

        try:
            self._client = AsyncIOMotorClient(
                settings.mongodb_connection_string,
                maxPoolSize=50,
                minPoolSize=10,
                maxIdleTimeMS=45000,
                serverSelectionTimeoutMS=5000,
            )
            self._database = self._client[settings.MONGODB_DATABASE_NAME]

            # Verificar conexión con ping
            await self._client.admin.command("ping")

        except Exception as error:
            raise ConnectionError(f"Failed to connect to MongoDB: {error}") from error

    async def disconnect(self) -> None:
        """Cierra la conexión con MongoDB de forma segura."""
        if self._client is not None:
            self._client.close()
            self._client = None
            self._database = None

    def get_database(self) -> AsyncIOMotorDatabase:
        """Retorna la instancia de la base de datos.

        Returns:
            AsyncIOMotorDatabase: Instancia de la base de datos.

        Raises:
            RuntimeError: Si no existe conexión activa.
        """
        if self._database is None:
            raise RuntimeError("Database connection not established. Call connect() first.")
        return self._database

    def get_collection(self, collection_name: str):
        """Retorna una colección específica de la base de datos.

        Args:
            collection_name: Nombre de la colección.

        Returns:
            AsyncIOMotorCollection: Colección de MongoDB.
        """
        return self.get_database()[collection_name]


# Instancia global del gestor de conexión
mongodb_connection = MongoDBConnection()


@asynccontextmanager
async def get_db_connection() -> AsyncGenerator[AsyncIOMotorDatabase, None]:
    """Context manager para obtener conexión a la base de datos.

    Yields:
        AsyncIOMotorDatabase: Instancia de la base de datos.

    Example:
        async with get_db_connection() as db:
            await db.items.insert_one({"name": "example"})
    """
    if not mongodb_connection.is_connected:
        await mongodb_connection.connect()
    try:
        yield mongodb_connection.get_database()
    except Exception:
        await mongodb_connection.disconnect()
        raise


async def lifespan_handler():
    """Handler para gestionar el ciclo de vida de la conexión.

    Uso con FastAPI lifespan events.
    """
    await mongodb_connection.connect()
    try:
        yield
    finally:
        await mongodb_connection.disconnect()
