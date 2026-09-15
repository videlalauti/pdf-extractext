import pytest


def test_create_item_use_case_removed():
    with pytest.raises(ImportError):
        from src.application.use_cases.create_item import CreateItemUseCase  # noqa: F401


def test_item_mapper_removed():
    with pytest.raises(ImportError):
        from src.application.mappers.item_mapper import ItemMapper  # noqa: F401


def test_item_dto_removed():
    with pytest.raises(ImportError):
        from src.application.dtos.item_dto import ItemDTO  # noqa: F401
