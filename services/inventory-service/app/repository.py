"""
Repository per la tabella Products.

Accesso diretto al DB – nessuna logica di business qui.
Tutte le query sono filtrate per user_id (multi-tenancy):
l'utente vede e gestisce solo i propri prodotti.
"""
from sqlalchemy.orm import Session
from app import models, schemas

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_product(self, request: schemas.ProductCreate, user_id: int) -> models.Product:
        """ Crea un nuovo prodotto associato all'utente. Solleva 400 se nome o barcode già esistono per l'utente. """
        new_product = models.Product(
        user_id=user_id,
        name=request.name,
        expiration_date=request.expiration_date,
        barcode=request.barcode,
    )
        self.db.add(new_product)
        self.db.commit()
        self.db.refresh(new_product)
        return new_product


    def get_products(self,user_id: int) -> list[models.Product]:
        return (
            self.db.query(models.Product)
            .filter(models.Product.user_id == user_id)
            .all()
        )


    def get_product_by_id(self, id: int, user_id: int) -> models.Product:
        product = (
            self.db.query(models.Product)
            .filter(
                models.Product.id == id,
                models.Product.user_id == user_id,
            )
            .first()
        )
        return product
    
    def get_product_by_barcode(self, barcode: str, user_id: int) -> models.Product:
        product = self.db.query(models.Product).filter(models.Product.user_id == user_id, models.Product.barcode == barcode).first()
        return product
    
    def get_product_by_name(self, name: str, user_id: int) -> models.Product:
        product = (
            self.db.query(models.Product)
            .filter(
                models.Product.user_id == user_id,
                models.Product.name == name,
            )
            .first()
        )
        return product


    def delete_product(self, id: int, user_id: int) -> None:
        product = (
            self.db.query(models.Product)
            .filter(
                models.Product.id == id,
                models.Product.user_id == user_id,
            )
            .first()
        )
        self.db.delete(product)
        self.db.commit()
