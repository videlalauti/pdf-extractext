"""Configuración de la aplicación con Pydantic Settings - 12-Factor App."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración de la aplicación usando Pydantic Settings.

    Sigue el principio de 12-Factor App para configuración por entorno.
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

    # MongoDB Connection (12-Factor: config por variables de entorno)
    MONGODB_HOST: str = "localhost"
    MONGODB_PORT: int = 27017
    MONGODB_ROOT_USERNAME: str = ""
    MONGODB_ROOT_PASSWORD: str = ""
    MONGODB_DATABASE_NAME: str = "pdf_extractext"
    MONGODB_AUTH_SOURCE: str = "admin"

    # Legacy database config para compatibilidad
    DATABASE_URL: str = ""
    DATABASE_NAME: str = "pdf_extractext"

    # PDF Configuration
    MAX_PDF_SIZE_BYTES: int = 10 * 1024 * 1024  # 10MB default

    # Storage
    UPLOAD_PATH: str = "./uploads"

    @property
    def mongodb_connection_string(self) -> str:
        """Genera el connection string de MongoDB.

        Si DATABASE_URL está definida, la usa directamente.
        Si no, construye el string desde componentes individuales.
        """
        if self.DATABASE_URL:
            return self.DATABASE_URL

        if self.MONGODB_ROOT_USERNAME and self.MONGODB_ROOT_PASSWORD:
            return (
                f"mongodb://{self.MONGODB_ROOT_USERNAME}:{self.MONGODB_ROOT_PASSWORD}"
                f"@{self.MONGODB_HOST}:{self.MONGODB_PORT}"
                f"/{self.MONGODB_DATABASE_NAME}"
                f"?authSource={self.MONGODB_AUTH_SOURCE}"
            )

        return f"mongodb://{self.MONGODB_HOST}:{self.MONGODB_PORT}"

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
