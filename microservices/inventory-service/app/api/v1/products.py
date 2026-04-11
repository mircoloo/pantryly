from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.repository import ProductRepository
from app.schemas import schemas
from app.services.service import (ProductAlreadyExistsError,
                                  ProductNotFoundError, ProductService)

router = APIRouter(tags=["Products"], prefix="/v1/products")


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    repo: ProductRepository = ProductRepository(db)
    return ProductService(repo)


def _to_http_exception(exc: Exception) -> HTTPException:
    if isinstance(exc, ProductAlreadyExistsError):
        if exc.field == "barcode":
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product with barcode {exc.value} already exists",
            )
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product with name {exc.value} already exists",
        )
    if isinstance(exc, ProductNotFoundError):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Unexpected server error",
    )


@router.post(
    "", response_model=schemas.ProductShow, status_code=status.HTTP_201_CREATED
)
def create_product(
    request: schemas.ProductCreate,
    service: ProductService = Depends(get_product_service),
):
    try:
        return service.create_product(request)
    except ProductAlreadyExistsError as exc:
        raise _to_http_exception(exc) from exc


@router.get(
    "", response_model=List[schemas.ProductShow], status_code=status.HTTP_200_OK
)
def list_products_for_user(
    user_id: int,
    service: ProductService = Depends(get_product_service),
):
    return service.get_all_products(user_id)


@router.get(
    "/by-name/{product_name}",
    response_model=schemas.ProductShow,
    status_code=status.HTTP_200_OK,
)
def get_product_by_name(
    product_name: str,
    user_id: int,
    service: ProductService = Depends(get_product_service),
):
    try:
        return service.get_product_by_name(user_id=user_id, product_name=product_name)
    except ProductNotFoundError as exc:
        raise _to_http_exception(exc) from exc


@router.get(
    "/by-barcode/{product_barcode}",
    response_model=schemas.ProductShow,
    status_code=status.HTTP_200_OK,
)
def get_product_by_barcode(
    product_barcode: str,
    user_id: int,
    service: ProductService = Depends(get_product_service),
):
    try:
        return service.get_product_by_barcode(
            user_id=user_id,
            product_barcode=product_barcode,
        )
    except ProductNotFoundError as exc:
        raise _to_http_exception(exc) from exc


@router.get(
    "/{product_id}", response_model=schemas.ProductShow, status_code=status.HTTP_200_OK
)
def get_product_by_id(
    product_id: int,
    user_id: int,
    service: ProductService = Depends(get_product_service),
):
    try:
        return service.get_product_by_id(product_id=product_id, user_id=user_id)
    except ProductNotFoundError as exc:
        raise _to_http_exception(exc) from exc


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_for_user(
    product_id: int,
    user_id: int,
    service: ProductService = Depends(get_product_service),
):
    try:
        service.delete_product_by_id(user_id, product_id)
    except ProductNotFoundError as exc:
        raise _to_http_exception(exc) from exc
