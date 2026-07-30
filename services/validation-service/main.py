"""Validation service FastAPI application."""

import os
import httpx
from fastapi import FastAPI, HTTPException, UploadFile
from pydantic import BaseModel

from src.pdf_validator import PdfValidator


class ValidationResponse(BaseModel):
    valid: bool
    error: str | None = None


app = FastAPI(title="PDF Validation Service", version="1.0.0")

validator = PdfValidator()


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "validation-service"}


async def call_extraction_service(file_bytes: bytes, filename: str) -> dict:
    base_url = os.getenv("EXTRACTION_SERVICE_URL", "http://extraction.localhost")
    url = f"{base_url}/extract"

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
                raise HTTPException(status_code=502, detail=f"Error communicating with extraction-service: {str(e)}")
    return {}


@app.post("/validate", response_model=ValidationResponse)
async def validate_pdf(file: UploadFile) -> ValidationResponse:
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        return ValidationResponse(valid=False, error="El archivo debe tener extensión .pdf")

    content = await file.read()
    result = validator.validate(content)

    return ValidationResponse(valid=result.is_valid, error=result.error)
