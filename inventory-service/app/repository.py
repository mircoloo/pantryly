from . import schemas 
from . import models
from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from .database import get_db


def create_product(request: schemas.ProductCreate, db: Session):
    product = db.query(models.Product).filter(models.Product.name == request.name).first()
    if product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product named {request.name} already inserted"
        )
    new_product = models.Product(name=request.name, expiration_date=request.expiration_date, barcode=request.barcode)
    db.add(new_product)
    db.commit()
    db.flush(new_product)
    return new_product

def get_products(db: Session):
    return db.query(models.Product).all()

def get_product(id: int, db: Session):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product id {id} not found"
        )
    return product