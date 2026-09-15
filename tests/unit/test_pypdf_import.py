def test_pypdf_extractor_imports():
    from src.infrastructure.adapters.pypdf_text_extractor import PyPdfTextExtractor

    assert PyPdfTextExtractor is not None
