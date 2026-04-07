"""Configuración de la aplicación."""

import os
from dataclasses import dataclass, field


@dataclass(frozen=True)
class ApplicationConfig:
    """Configuración inmutable de la aplicación.

    Attributes:
        app_name: Nombre de la aplicación.
        version: Versión actual.
        description: Descripción de la aplicación.
        debug: Modo de depuración activado.
    """

    app_name: str = "PDF ExtractExt"
    version: str = "0.1.0"
    description: str = "API para extracción y procesamiento de PDFs"
    debug: bool = field(
        default_factory=lambda: os.getenv("DEBUG", "false").lower() == "true"
    )
