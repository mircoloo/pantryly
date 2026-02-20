"""
Repository per la tabella Products.

Accesso diretto al DB – nessuna logica di business qui.
Tutte le query sono filtrate per user_id (multi-tenancy):
l'utente vede e gestisce solo i propri prodotti.
"""
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas


def create_product(
    request: schemas.ProductCreate, user_id: int, db: Session
) -> models.Product:
    """
    Crea un nuovo prodotto per l'utente specificato.
    Solleva 400 se l'utente ha già un prodotto con lo stesso nome.
    """
    existing = (
        db.query(models.Product)
        .filter(
            models.Product.user_id == user_id,
            models.Product.name == request.name,
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product named '{request.name}' already inserted",
        )

    new_product = models.Product(
        user_id=user_id,
        name=request.name,
        expiration_date=request.expiration_date,
        barcode=request.barcode,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def get_products(user_id: int, db: Session) -> list[models.Product]:
    """Restituisce tutti i prodotti dell'utente."""
    return (
        db.query(models.Product)
        .filter(models.Product.user_id == user_id)
        .all()
    )


def get_product(id: int, user_id: int, db: Session) -> models.Product:
    """
    Restituisce un prodotto per id, solo se appartiene all'utente.
    Solleva 404 se non trovato o non di proprietà dell'utente.
    """
    product = (
        db.query(models.Product)
        .filter(
            models.Product.id == id,
            models.Product.user_id == user_id,
        )
        .first()
    )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product id {id} not found",
        )
    return product


def delete_product(id: int, user_id: int, db: Session) -> None:
    """
    Elimina un prodotto per id, solo se appartiene all'utente.
    Solleva 404 se non trovato o non di proprietà dell'utente.
    """
    product = (
        db.query(models.Product)
        .filter(
            models.Product.id == id,
            models.Product.user_id == user_id,
        )
        .first()
    )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    db.delete(product)
    db.commit()
