"""Validaciones de nombre de archivo compartidas por todos los servicios."""


def has_pdf_extension(filename: str | None) -> bool:
    """True si el nombre termina en .pdf, sin diferenciar mayúsculas."""
    return bool(filename) and filename.lower().endswith(".pdf")
