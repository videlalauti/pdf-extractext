"""Validation service FastAPI application."""

from fastapi import FastAPI, HTTPException, UploadFile
from pydantic import BaseModel

from src.pdf_validator import PdfValidator


class ValidationResponse(BaseModel):
    valid: bool
    error: str | None = None


app = FastAPI(title="PDF Validation Service", version="1.0.0")

validator = PdfValidator()


@app.post("/validate", response_model=ValidationResponse)
async def validate_pdf(file: UploadFile) -> ValidationResponse:
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        return ValidationResponse(valid=False, error="El archivo debe tener extensión .pdf")

    content = await file.read()
    result = validator.validate(content)

    return ValidationResponse(valid=result.is_valid, error=result.error)
