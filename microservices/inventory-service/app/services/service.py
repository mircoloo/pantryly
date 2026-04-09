from app.repositories.repository import ProductRepository
from app.schemas import ProductCreate, ProductShow


class ProductAlreadyExistsError(Exception):
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        super().__init__(field, value)


class ProductNotFoundError(Exception):
    pass


class ProductService:
    def __init__(self, repo: ProductRepository):
        self.repo: ProductRepository = repo

    def create_product(self, request: ProductCreate) -> ProductShow:
        existing_by_barcode = self.repo.get_product_by_barcode(request.barcode, request.user_id)
        if existing_by_barcode:
            raise ProductAlreadyExistsError("barcode", request.barcode)
        existing_by_name = self.repo.get_product_by_name(request.name, request.user_id)
        if existing_by_name:
            raise ProductAlreadyExistsError("name", request.name)
        return ProductShow.model_validate(self.repo.create_product(request))

    def get_all_products(self, user_id: int) -> list[ProductShow]:
        products = self.repo.get_products(user_id=user_id)
        return [ProductShow.model_validate(p) for p in products]

    def get_product_by_id(self, user_id: int, product_id: int) -> ProductShow:
        product = self.repo.get_product_by_id(product_id, user_id)
        if not product:
            raise ProductNotFoundError()
        return ProductShow.model_validate(product)

    def get_product_by_name(self, user_id: int, product_name: str) -> ProductShow:
        product = self.repo.get_product_by_name(product_name, user_id)
        if not product:
            raise ProductNotFoundError()
        return ProductShow.model_validate(product)

    def get_product_by_barcode(self, user_id: int, product_barcode: str) -> ProductShow:
        product = self.repo.get_product_by_barcode(product_barcode, user_id)
        if not product:
            raise ProductNotFoundError()
        return ProductShow.model_validate(product)

    def delete_product_by_id(self, user_id: int, product_id: int) -> None:
        self.get_product_by_id(user_id, product_id)
        self.repo.delete_product(product_id, user_id)
