"""Punto de entrada para iniciar la aplicación."""

import uvicorn

from src.infrastructure.config.settings import settings

if __name__ == "__main__":
    uvicorn.run(
        "interface_adapters.http.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
