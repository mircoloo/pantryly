"""
Flussi supportati:
  - POST   /v1/products       → crea un prodotto (per l'utente autenticato)
  - GET    /v1/products       → elenca i prodotti dell'utente
  - GET    /v1/products/{id}  → dettaglio prodotto (solo se dell'utente)
  - DELETE /v1/products/{id}  → elimina un prodotto (solo se dell'utente)
"""
from typing import List

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from app.repository import ProductRepository
from app.service import ProductService
from app import repository, schemas
from app.core.database import get_db

router = APIRouter(tags=["Products"], prefix="/v1/products")

def get_product_service(db: Session = Depends(get_db)):
    repo = ProductRepository(db)
    return ProductService(repo)

def _get_user_id(x_user_id: str = Header(...)) -> int:
    try:
        return int(x_user_id)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid x-user-id header",
        )


@router.post("", response_model=schemas.ProductShow, status_code=status.HTTP_201_CREATED)
def create_product(request: schemas.ProductCreate, user_id: int = Depends(_get_user_id), service: ProductService = Depends(get_product_service)):
    return service.create_product(request, user_id)


@router.get("", response_model=List[schemas.ProductShow], status_code=status.HTTP_200_OK)
def list_products(user_id: int = Depends(_get_user_id), service: ProductService = Depends(get_product_service)):
    """Elenca tutti i prodotti dell'utente autenticato."""
    return service.get_all_products(user_id)


@router.get("/{product_id}", response_model=schemas.ProductShow, status_code=status.HTTP_200_OK)
def get_product(
    product_id: int,
    user_id: int = Depends(_get_user_id),
    db: Session = Depends(get_db),
):
    """Recupera un prodotto per id (solo se dell'utente)."""
    return repository.get_product(product_id, user_id, db)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    user_id: int = Depends(_get_user_id),
    db: Session = Depends(get_db),
):
    """Elimina un prodotto per id (solo se dell'utente)."""
    repository.delete_product(product_id, user_id, db)
