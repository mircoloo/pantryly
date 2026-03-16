from app.repositories.repository import ProductRepository
from app.schemas.schemas import ProductCreate, ProductShow
from fastapi import HTTPException, status


class ProductService:
    def __init__(self, repo: ProductRepository):
        self.repo: ProductRepository = repo

    def create_product(self, request: ProductCreate, user_id: int) -> ProductShow:
        """
        create the product into the database if not found, otherwise it raises 400 BAD REQUEST exception
        """
        existing_by_barcode = self.repo.get_product_by_barcode(request.barcode, user_id)
        if existing_by_barcode:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product with barcode {request.barcode} already exists",
            )
        existing_by_name = self.repo.get_product_by_name(request.name, user_id)
        if existing_by_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product with name {request.name} already exists",
            )
        return self.repo.create_product(request, user_id)

    def get_all_products(self, user_id: int) -> list[ProductShow]:
        return self.repo.get_products(user_id)

    def get_product_by_id(self, user_id, product_id):
        product = self.repo.get_product_by_id(product_id, user_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )
        return product

    def get_product_by_name(self, user_id, product_name):
        product = self.repo.get_product_by_name(product_name, user_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )
        return product

    def get_product_by_barcode(self, user_id, product_barcode):
        product = self.repo.get_product_by_barcode(product_barcode, user_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )
        return product

    def delete_product_by_id(self, user_id: int, product_id: int):
        try:
            self.get_product_by_id(user_id, product_id)
        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product to delete not found",
            )
        self.repo.delete_product(product_id, user_id)
