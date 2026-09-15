from src.domain.exceptions import DomainError, DuplicateDocumentError, DocumentNotFoundError


def test_domain_error_is_base():
    assert issubclass(DuplicateDocumentError, DomainError)


def test_document_not_found_is_domain_error():
    assert issubclass(DocumentNotFoundError, DomainError)


def test_exceptions_are_importable_from_single_location():
    from src.domain.exceptions import DuplicateDocumentError, DocumentNotFoundError
    assert DuplicateDocumentError is not None
    assert DocumentNotFoundError is not None