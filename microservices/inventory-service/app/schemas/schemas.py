from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict

class ProductBase(BaseModel):
    name: str
    barcode: str
    expiration_date: Optional[date] = None

class ProductCreate(ProductBase):
    user_id: int



class ProductShow(ProductBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
