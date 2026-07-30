"""Extraction service FastAPI application."""

import hashlib
import os
import httpx
from fastapi import FastAPI, HTTPException, UploadFile
from pydantic import BaseModel

from src.pypdf_text_extractor import PdfExtractionError, PyPdfTextExtractor


class ExtractionResponse(BaseModel):
    text: str
    document_id: str | None = None


app = FastAPI(title="PDF Extraction Service", version="1.0.0")

extractor = PyPdfTextExtractor()


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "extraction-service"}


async def save_to_persistence(content: str, checksum: str) -> dict:
    base_url = os.getenv("PERSISTENCE_SERVICE_URL", "http://persistence.localhost")
    url = f"{base_url}/documents"
    payload = {
        "content": content,
        "checksum": checksum,
    }

    retries = 3
    for attempt in range(retries):
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                return response.json()
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            if attempt == retries - 1:
                raise HTTPException(status_code=502, detail=f"Error communicating with persistence-service: {str(e)}")
    return {}


@app.post("/extract", response_model=ExtractionResponse)
async def extract_text(file: UploadFile) -> ExtractionResponse:
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="El archivo debe tener extensión .pdf")

    try:
        content = await file.read()
        text = extractor.extract_text_from_bytes(content)

        checksum = hashlib.sha256(content).hexdigest()
        persistence_response = await save_to_persistence(text, checksum)
        doc_id = persistence_response.get("id")

        return ExtractionResponse(text=text, document_id=doc_id)
    except PdfExtractionError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
