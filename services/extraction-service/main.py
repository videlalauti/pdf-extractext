"""Extraction service FastAPI application."""

from fastapi import FastAPI, HTTPException, UploadFile
from pydantic import BaseModel

from src.pypdf_text_extractor import PdfExtractionError, PyPdfTextExtractor


class ExtractionResponse(BaseModel):
    text: str


app = FastAPI(title="PDF Extraction Service", version="1.0.0")

extractor = PyPdfTextExtractor()


@app.post("/extract", response_model=ExtractionResponse)
async def extract_text(file: UploadFile) -> ExtractionResponse:
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="El archivo debe tener extensión .pdf")

    try:
        content = await file.read()
        text = extractor.extract_text_from_bytes(content)
        return ExtractionResponse(text=text)
    except PdfExtractionError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
