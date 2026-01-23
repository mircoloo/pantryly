
from fastapi import APIRouter, HTTPException, Depends, status
from .. import schemas, models, repository
from ..database import get_db
from typing import List
from sqlalchemy.orm import Session

router = APIRouter(tags=['Products'], prefix="/v1/products")




@router.post("", response_model=schemas.ProductShow, status_code=status.HTTP_201_CREATED)
def create_product(request: schemas.ProductCreate, db: Session = Depends(get_db)):
    return repository.create_product(request, db)


@router.get("", response_model=List[schemas.ProductShow], status_code=status.HTTP_200_OK)
def get_products(db: Session = Depends(get_db)):
    return repository.get_products(db)

@router.get("/{id}", response_model=schemas.ProductShow, status_code=status.HTTP_200_OK)
def get_products(id: int, db: Session = Depends(get_db)):
    return repository.get_product(id, db)



@router.delete("/{id}")
def delte_products(id: int, db: Session = Depends(get_db)):
    to_delete = db.query(models.Product).filter(models.Product.id == id).first()
    if not to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    db.delete(to_delete)
    db.commit()
    return {"ok": True}