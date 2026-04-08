from typing import List

from app.core.database import get_db
from app.repositories import repository
from app.repositories.repository import ProductRepository
from app.schemas import schemas
from app.services.service import ProductService
from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(tags=["Products"], prefix="/v1/products")


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    repo: ProductRepository = ProductRepository(db)
    return ProductService(repo)


def _get_user_id(x_user_id: str = Header(...)) -> int:
    try:
        return int(x_user_id)
    except (ValueError, TypeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid x-user-id header",
        ) from exc


@router.post(
    "", response_model=schemas.ProductShow, status_code=status.HTTP_201_CREATED
)
def create_product(
    request: schemas.ProductCreate,
    user_id: int = Depends(_get_user_id),
    service: ProductService = Depends(get_product_service),
):
    """
    Creates a proucts using the specified service

    Args:
        request: the request schema of the product
        user_id: the user id issuing the request
        service: the service used to create the product

    Returns:
        Returns the Product created if successfull
    """

    return service.create_product(request, user_id)


@router.get(
    "", response_model=List[schemas.ProductShow], status_code=status.HTTP_200_OK
)
def list_products(
    user_id: int = Depends(_get_user_id),
    service: ProductService = Depends(get_product_service),
):
    """Elenca tutti i prodotti dell'utente autenticato."""
    return service.get_all_products(user_id)


@router.get(
    "/{product_id}", response_model=schemas.ProductShow, status_code=status.HTTP_200_OK
)
def get_product_by_id(
    product_id: int,
    user_id: int = Depends(_get_user_id),
    service: ProductService = Depends(get_product_service),
):
    return service.get_product_by_id(product_id=product_id, user_id=user_id)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    user_id: int = Depends(_get_user_id),
    service: ProductService = Depends(get_product_service),
):
    return service.delete_product_by_id(user_id, product_id)
