"""Endpoints para gestión de items."""

from http import HTTPStatus
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from src.application.use_cases.item_use_case import (
    CreateItemUseCase,
    DeleteItemUseCase,
    GetItemUseCase,
    ListItemsUseCase,
    UpdateItemUseCase,
)
from src.domain.exceptions import ValidationError
from src.domain.repositories.item_repository import ItemRepository
from src.interface_adapters.database.repository_provider import get_item_repository
from src.interface_adapters.http.schemas.item_schemas import (
    ItemCreateRequest,
    ItemResponse,
    ItemUpdateRequest,
)

router = APIRouter(prefix="/items", tags=["items"])


def get_list_use_case(
    repository: ItemRepository = Depends(get_item_repository),
) -> ListItemsUseCase:
    """Proveedor de dependencia para el caso de uso de listar."""
    return ListItemsUseCase(repository)


def get_get_use_case(
    repository: ItemRepository = Depends(get_item_repository),
) -> GetItemUseCase:
    """Proveedor de dependencia para el caso de uso de obtener."""
    return GetItemUseCase(repository)


def get_create_use_case(
    repository: ItemRepository = Depends(get_item_repository),
) -> CreateItemUseCase:
    """Proveedor de dependencia para el caso de uso de crear."""
    return CreateItemUseCase(repository)


def get_update_use_case(
    repository: ItemRepository = Depends(get_item_repository),
) -> UpdateItemUseCase:
    """Proveedor de dependencia para el caso de uso de actualizar."""
    return UpdateItemUseCase(repository)


def get_delete_use_case(
    repository: ItemRepository = Depends(get_item_repository),
) -> DeleteItemUseCase:
    """Proveedor de dependencia para el caso de uso de eliminar."""
    return DeleteItemUseCase(repository)


@router.get("", response_model=List[ItemResponse])
async def list_items(
    use_case: ListItemsUseCase = Depends(get_list_use_case),
) -> List[ItemResponse]:
    """Lista todos los items.

    Returns:
        List[ItemResponse]: Lista de items.
    """
    items = use_case.execute()
    return [ItemResponse.from_entity(item) for item in items]


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: UUID,
    use_case: GetItemUseCase = Depends(get_get_use_case),
) -> ItemResponse:
    """Obtiene un item por su ID.

    Args:
        item_id: UUID del item.
        use_case: Caso de uso de obtener items.

    Returns:
        ItemResponse: Item encontrado.

    Raises:
        HTTPException: 404 si no existe.
    """
    item = use_case.execute(item_id)
    if item is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Item with id {item_id} not found",
        )
    return ItemResponse.from_entity(item)


@router.post("", response_model=ItemResponse, status_code=HTTPStatus.CREATED)
async def create_item(
    request: ItemCreateRequest,
    use_case: CreateItemUseCase = Depends(get_create_use_case),
) -> ItemResponse:
    """Crea un nuevo item.

    Args:
        request: Datos del item a crear.
        use_case: Caso de uso de crear items.

    Returns:
        ItemResponse: Item creado.

    Raises:
        HTTPException: 400 si los datos son inválidos.
    """
    try:
        item = use_case.execute(
            name=request.name,
            description=request.description,
        )
        return ItemResponse.from_entity(item)
    except ValidationError as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e),
        )


@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: UUID,
    request: ItemUpdateRequest,
    use_case: UpdateItemUseCase = Depends(get_update_use_case),
) -> ItemResponse:
    """Actualiza un item existente.

    Args:
        item_id: UUID del item.
        request: Datos a actualizar.
        use_case: Caso de uso de actualizar items.

    Returns:
        ItemResponse: Item actualizado.

    Raises:
        HTTPException: 404 si no existe, 400 si los datos son inválidos.
    """
    try:
        item = use_case.execute(
            item_id=item_id,
            name=request.name,
            description=request.description,
        )
        if item is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Item with id {item_id} not found",
            )
        return ItemResponse.from_entity(item)
    except ValidationError as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e),
        )


@router.delete("/{item_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_item(
    item_id: UUID,
    use_case: DeleteItemUseCase = Depends(get_delete_use_case),
) -> None:
    """Elimina un item.

    Args:
        item_id: UUID del item.
        use_case: Caso de uso de eliminar items.

    Raises:
        HTTPException: 404 si no existe.
    """
    deleted = use_case.execute(item_id)
    if not deleted:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Item with id {item_id} not found",
        )
