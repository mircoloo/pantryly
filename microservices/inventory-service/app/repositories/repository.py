from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Product
from app.schemas import ProductCreate

from app import models
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

    def get_products(self, user_id: int) -> list[models.Product]:
        
        return list(self.db.execute( 
                                    select(models.Product).where(models.Product.user_id == user_id) 
                                    )
                    .scalars()
                    .all())
        # return (
            # self.db.query(Product)
            # .filter(Product.user_id == user_id)
            # .all()
            # )

    def get_product_by_id(self, id: int, user_id: int) -> models.Product | None:
        product = (
            self.db.query(models.Product)
            .filter(
                models.Product.id == id,
                models.Product.user_id == user_id,
            )
            .first()
        )
        return product

    def get_product_by_barcode(self, barcode: str, user_id: int) -> models.Product | None:
        product = (
            self.db.query(models.Product)
            .filter(
                models.Product.user_id == user_id, models.Product.barcode == barcode
            )
            .first()
        )
        return product

    def get_product_by_name(self, name: str, user_id: int) -> models.Product | None:
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
