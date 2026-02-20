"""
Rotte REST per la gestione dei prodotti.

Ogni operazione è filtrata per user_id, estratto dall'header x-user-id
che il Gateway aggiunge dopo aver validato il JWT.

Flussi supportati:
  - POST   /v1/products       → crea un prodotto (per l'utente autenticato)
  - GET    /v1/products       → elenca i prodotti dell'utente
  - GET    /v1/products/{id}  → dettaglio prodotto (solo se dell'utente)
  - DELETE /v1/products/{id}  → elimina un prodotto (solo se dell'utente)
"""
from typing import List

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from .. import repository, schemas
from ..database import get_db

router = APIRouter(tags=["Products"], prefix="/v1/products")


def _get_user_id(x_user_id: str = Header(...)) -> int:
    """
    Dependency che estrae l'header x-user-id iniettato dal Gateway.
    Solleva 401 se l'header è assente o non numerico.
    """
    try:
        return int(x_user_id)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid x-user-id header",
        )


@router.post("", response_model=schemas.ProductShow, status_code=status.HTTP_201_CREATED)
def create_product(
    request: schemas.ProductCreate,
    user_id: int = Depends(_get_user_id),
    db: Session = Depends(get_db),
):
    """Crea un nuovo prodotto associato all'utente autenticato."""
    return repository.create_product(request, user_id, db)


@router.get("", response_model=List[schemas.ProductShow], status_code=status.HTTP_200_OK)
def list_products(
    user_id: int = Depends(_get_user_id),
    db: Session = Depends(get_db),
):
    """Elenca tutti i prodotti dell'utente autenticato."""
    return repository.get_products(user_id, db)


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
