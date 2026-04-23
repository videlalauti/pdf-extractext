"""Tests para la entidad Document del dominio."""

import pytest
from dataclasses import FrozenInstanceError


class TestDocument:
    """Tests para la entidad Document."""

    def test_document_creacion_con_valores_minimos(self):
        """Test: Debe crear un Document con id, content y checksum."""
        # Arrange & Act
        from src.domain.entities.document import Document

        document = Document(id="doc-001", content="Texto extraído del PDF", checksum="abc123def456")

        # Assert
        assert document.id == "doc-001"
        assert document.content == "Texto extraído del PDF"
        assert document.checksum == "abc123def456"

    def test_document_requiere_checksum_no_vacio(self):
        """Test: Debe rechazar checksum vacío."""
        from src.domain.entities.document import Document
        from src.domain.exceptions import ValidationError

        with pytest.raises(ValidationError, match="checksum cannot be empty"):
            Document(id="doc-002", content="Texto del documento", checksum="")

    def test_document_es_inmutable(self):
        """Test: Los documentos deben ser inmutables (frozen dataclass)."""
        from src.domain.entities.document import Document

        document = Document(id="doc-003", content="Texto", checksum="hash123")

        with pytest.raises(FrozenInstanceError):
            document.content = "Nuevo texto"


class TestDocumentMongoSchema:
    """Tests para el esquema MongoDB de Document."""

    def test_schema_crea_documento_valido(self):
        """Test: El esquema debe crear un documento válido para MongoDB."""
        from src.interface_adapters.database.schemas.document_schema import DocumentMongoSchema

        schema = DocumentMongoSchema(
            id="doc-mongo-001", content="Texto extraído del PDF", checksum="sha256:abc123"
        )

        assert schema.id == "doc-mongo-001"
        assert schema.content == "Texto extraído del PDF"
        assert schema.checksum == "sha256:abc123"

    def test_schema_rechaza_checksum_vacio(self):
        """Test: El esquema debe rechazar checksum vacío."""
        from src.interface_adapters.database.schemas.document_schema import DocumentMongoSchema
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            DocumentMongoSchema(id="doc-mongo-002", content="Texto", checksum="")

    def test_schema_convierte_a_diccionario(self):
        """Test: El esquema debe poder convertirse a diccionario para MongoDB."""
        from src.interface_adapters.database.schemas.document_schema import DocumentMongoSchema

        schema = DocumentMongoSchema(
            id="doc-mongo-003", content="Contenido del PDF", checksum="md5:xyz789"
        )

        data = schema.model_dump()

        assert data["_id"] == "doc-mongo-003"
        assert data["content"] == "Contenido del PDF"
        assert data["checksum"] == "md5:xyz789"
