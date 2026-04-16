"""
Repository per la tabella Products.

Accesso diretto al DB – nessuna logica di business qui.
Tutte le query sono filtrate per user_id (multi-tenancy):
l'utente vede e gestisce solo i propri prodotti.
"""

from sqlalchemy.orm import Session

from app.models import Product
from app.schemas import ProductCreate


class ProductRepository:
    def __init__(self, db: Session):
        self.db: Session = db

    def create_product(
        self, request: ProductCreate, user_id: int
    ) -> Product:
        """Crea un nuovo prodotto associato all'utente. Solleva 400 se nome o barcode già esistono per l'utente."""
        new_product = Product(
            user_id=user_id,
            name=request.name,
            expiration_date=request.expiration_date,
            barcode=request.barcode,
        )
        self.db.add(new_product)
        self.db.commit()
        self.db.refresh(new_product)
        return new_product

    def get_products(self, user_id: int) -> list[Product]:
        return (
            self.db.query(Product)
            .filter(Product.user_id == user_id)
            .all()
        )

    def get_product_by_id(self, id: int, user_id: int) -> Product | None:
        product = (
            self.db.query(Product)
            .filter(
                Product.id == id,
                Product.user_id == user_id,
            )
            .first()
        )
        return product

    def get_product_by_barcode(self, barcode: str, user_id: int) -> Product | None:
        product = (
            self.db.query(Product)
            .filter(
                Product.user_id == user_id, Product.barcode == barcode
            )
            .first()
        )
        return product

    def get_product_by_name(self, name: str, user_id: int) -> Product | None:
        product = (
            self.db.query(Product)
            .filter(
                Product.user_id == user_id,
                Product.name == name,
            )
            .first()
        )
        return product

    def delete_product(self, id: int, user_id: int) -> None:
        product = (
            self.db.query(Product)
            .filter(
                Product.id == id,
                Product.user_id == user_id,
            )
            .first()
        )
        self.db.delete(product)
        self.db.commit()
