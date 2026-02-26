
from app.repository import ProductRepository
from app.schemas import ProductCreate, ProductShow
from fastapi import status, HTTPException


class ProductService():
    def __init__(self, repo: ProductRepository):
        self.repo: ProductRepository = repo

    def create_product(self, request: ProductCreate, user_id: int) -> ProductShow:
        print(f"{request=}")
        existing_by_barcode = self.repo.get_product_by_barcode(request.barcode, user_id) 
        print(f"{existing_by_barcode}")
        if existing_by_barcode:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product with barcode {request.barcode} already exists",
            )
        existing_by_name = self.repo.get_product_by_name(request.name, user_id)
        if existing_by_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product with name {request.name} already exists"
            )
        return self.repo.create_product(request, user_id)
    
    def get_all_products(self, user_id: int) -> list[ProductShow]:
        return self.repo.get_products(user_id)