from datetime import date
from typing import Optional

from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    user_id: int
    barcode: str
    expiration_date: Optional[date] = None


class ProductShow(BaseModel):
    id: int
    user_id: int
    name: str
    barcode: str
    expiration_date: Optional[date] = None

    class ConfigDict:
        from_attributes = True  # ORM support → Pydantic
