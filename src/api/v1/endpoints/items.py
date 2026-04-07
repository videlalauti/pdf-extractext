"""Endpoints para gestión de items."""

from http import HTTPStatus
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from src.api.v1.schemas.item import ItemCreateRequest, ItemResponse, ItemUpdateRequest
from src.repositories.interfaces.item_repository import ItemRepositoryInterface
from src.repositories.providers import get_item_repository
from src.services.implementations.item_service import ItemService
from src.services.interfaces.item_service import ItemServiceInterface

router = APIRouter(prefix="/items", tags=["items"])


def get_item_service(
    repository: ItemRepositoryInterface = Depends(get_item_repository),
) -> ItemServiceInterface:
    """Proveedor de dependencia para el servicio.

    Args:
        repository: Repositorio inyectado.

    Returns:
        ItemServiceInterface: Servicio configurado.
    """
    return ItemService(repository)


@router.get("", response_model=List[ItemResponse])
async def list_items(
    service: ItemServiceInterface = Depends(get_item_service),
) -> List[ItemResponse]:
    """Lista todos los items.

    Returns:
        List[ItemResponse]: Lista de items.
    """
    items = service.list_items()
    return [ItemResponse.from_model(item) for item in items]


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: UUID,
    service: ItemServiceInterface = Depends(get_item_service),
) -> ItemResponse:
    """Obtiene un item por su ID.

    Args:
        item_id: UUID del item.
        service: Servicio de items.

    Returns:
        ItemResponse: Item encontrado.

    Raises:
        HTTPException: 404 si no existe.
    """
    item = service.get_item(item_id)
    if item is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Item with id {item_id} not found",
        )
    return ItemResponse.from_model(item)


@router.post("", response_model=ItemResponse, status_code=HTTPStatus.CREATED)
async def create_item(
    request: ItemCreateRequest,
    service: ItemServiceInterface = Depends(get_item_service),
) -> ItemResponse:
    """Crea un nuevo item.

    Args:
        request: Datos del item a crear.
        service: Servicio de items.

    Returns:
        ItemResponse: Item creado.

    Raises:
        HTTPException: 400 si los datos son inválidos.
    """
    try:
        item = service.create_item(
            name=request.name,
            description=request.description,
        )
        return ItemResponse.from_model(item)
    except ValueError as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e),
        )


@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: UUID,
    request: ItemUpdateRequest,
    service: ItemServiceInterface = Depends(get_item_service),
) -> ItemResponse:
    """Actualiza un item existente.

    Args:
        item_id: UUID del item.
        request: Datos a actualizar.
        service: Servicio de items.

    Returns:
        ItemResponse: Item actualizado.

    Raises:
        HTTPException: 404 si no existe, 400 si los datos son inválidos.
    """
    try:
        item = service.update_item(
            item_id=item_id,
            name=request.name,
            description=request.description,
        )
        if item is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Item with id {item_id} not found",
            )
        return ItemResponse.from_model(item)
    except ValueError as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e),
        )


@router.delete("/{item_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_item(
    item_id: UUID,
    service: ItemServiceInterface = Depends(get_item_service),
) -> None:
    """Elimina un item.

    Args:
        item_id: UUID del item.
        service: Servicio de items.

    Raises:
        HTTPException: 404 si no existe.
    """
    deleted = service.delete_item(item_id)
    if not deleted:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Item with id {item_id} not found",
        )
