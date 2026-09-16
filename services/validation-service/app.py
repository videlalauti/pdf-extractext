"""Validation service: capa de aplicación, orquestación con servicios externos."""

import httpx
from fastapi import HTTPException
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    extraction_service_url: str = "http://extraction.localhost"


settings = Settings()


async def call_extraction_service(file_bytes: bytes, filename: str) -> dict:
    url = f"{settings.extraction_service_url}/extract"

    retries = 3
    for attempt in range(retries):
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                files = {"file": (filename, file_bytes, "application/pdf")}
                response = await client.post(url, files=files)
                response.raise_for_status()
                return response.json()
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            if attempt == retries - 1:
                raise HTTPException(
                    status_code=502, detail=f"Error communicating with extraction-service: {str(e)}"
                ) from e
    return {}
