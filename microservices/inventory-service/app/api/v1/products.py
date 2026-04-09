from typing import List

from app.core.database import get_db
from app.repositories.repository import ProductRepository
from app.schemas import schemas
from app.services.service import ProductService
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session


router = APIRouter(tags=["Products"], prefix="/v1/products")


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    repo: ProductRepository = ProductRepository(db)
    return ProductService(repo)



@router.post(
    "", response_model=schemas.ProductShow, status_code=status.HTTP_201_CREATED
)
def create_product(
    request: schemas.ProductCreate,
    service: ProductService = Depends(get_product_service),
):

    return service.create_product(request)


@router.get(
    "", response_model=List[schemas.ProductShow], status_code=status.HTTP_200_OK
)
def list_products(
    user_id: int,
    service: ProductService = Depends(get_product_service),
):
    return service.get_all_products(user_id)


@router.get(
    "/{product_id}", response_model=schemas.ProductShow, status_code=status.HTTP_200_OK
)
def get_product_by_id(
    product_id: int,
    user_id: int,
    service: ProductService = Depends(get_product_service),
):
    
    product = service.get_product_by_id(product_id=product_id, user_id=user_id)
    if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    user_id: int,
    service: ProductService = Depends(get_product_service),
):
    return service.delete_product_by_id(user_id, product_id)
