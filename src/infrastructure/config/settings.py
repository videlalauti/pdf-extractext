"""Configuración de la aplicación con Pydantic Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración de la aplicación usando Pydantic Settings.

    Carga valores desde variables de entorno y archivo .env.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Application
    APP_NAME: str = "PDF ExtractExt"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "API para extracción y procesamiento de PDFs"
    DEBUG: bool = False

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database (ejemplo para MongoDB)
    DATABASE_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "pdf_extractext"

    # Storage
    UPLOAD_PATH: str = "./uploads"

    @property
    def app_name(self) -> str:
        """Nombre de la aplicación."""
        return self.APP_NAME

    @property
    def version(self) -> str:
        """Versión de la aplicación."""
        return self.VERSION

    @property
    def description(self) -> str:
        """Descripción de la aplicación."""
        return self.DESCRIPTION

    @property
    def debug(self) -> bool:
        """Modo de depuración."""
        return self.DEBUG


# Instancia singleton de configuración
settings = Settings()
