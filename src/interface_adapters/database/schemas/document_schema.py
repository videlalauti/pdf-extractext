"""Esquema Pydantic para documentos en MongoDB."""

from pydantic import BaseModel, Field, field_validator


class DocumentMongoSchema(BaseModel):
    """Esquema Pydantic para persistir documentos en MongoDB.

    Attributes:
        id: Identificador único del documento (mapeado a _id en MongoDB).
        content: Texto extraído del archivo PDF.
        checksum: Checksum del archivo para verificar integridad.
    """

    id: str = Field(..., description="Identificador único del documento")
    content: str = Field(..., description="Texto extraído del PDF")
    checksum: str = Field(..., description="Checksum del archivo")

    @field_validator("checksum")
    @classmethod
    def checksum_must_not_be_empty(cls, v: str) -> str:
        """Valida que el checksum no esté vacío."""
        if not v or not v.strip():
            raise ValueError("checksum cannot be empty")
        return v

    def model_dump(self, **kwargs) -> dict:
        """Convierte el esquema a diccionario compatible con MongoDB.

        MongoDB usa _id como clave primaria, por lo que mapeamos
        el campo id a _id.

        Returns:
            dict: Diccionario con formato compatible con MongoDB.
        """
        data = super().model_dump(**kwargs)
        data["_id"] = data.pop("id")
        return data
