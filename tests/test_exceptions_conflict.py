def test_domain_exceptions_is_file_not_package():
    import inspect

    import src.domain.exceptions as exc

    # exceptions.py is a module file, not a package directory
    assert inspect.ismodule(exc)
    assert hasattr(exc, "DomainError")


def test_problem_details_not_importable():
    import pytest

    with pytest.raises((ImportError, ModuleNotFoundError)):
        from src.domain.exceptions.base import ProblemDetailsException  # noqa: F401
