"""Extraction service: endpoints HTTP delegando en extractor y lógica de aplicación."""

from app import compute_checksum, save_to_persistence
from fastapi import APIRouter, HTTPException, UploadFile
from pydantic import BaseModel

from shared.domain.exceptions import PdfExtractionError
from shared.domain.filename import has_pdf_extension
from shared.domain.pypdf_text_extractor import PyPdfTextExtractor

router = APIRouter()


class ExtractionResponse(BaseModel):
    text: str
    document_id: str | None = None


extractor = PyPdfTextExtractor()


@router.post("/extract", response_model=ExtractionResponse)
async def extract_text(file: UploadFile) -> ExtractionResponse:
    if not has_pdf_extension(file.filename):
        raise HTTPException(status_code=400, detail="El archivo debe tener extensión .pdf")

    try:
        content = await file.read()
        text = await extractor.extract_text_from_bytes(content)

        checksum = compute_checksum(content)
        persistence_response = await save_to_persistence(text, checksum)
        doc_id = persistence_response.get("id")

        return ExtractionResponse(text=text, document_id=doc_id)
    except PdfExtractionError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}") from e
