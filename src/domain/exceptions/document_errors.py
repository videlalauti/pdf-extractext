from .base import ProblemDetailsException


class DuplicateDocumentError(ProblemDetailsException):
    def __init__(self, *, instance: str = None):
        super().__init__(
            type_uri="https://api/errors/duplicate-document",
            title="Documento Duplicado",
            status=409,
            detail="Ya existe un documento con este contenido.",
            instance=instance,
        )
