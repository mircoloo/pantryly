from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    barcode: str = Field(min_length=1, max_length=50)
    expiration_date: Optional[date] = None

class ProductCreate(ProductBase):
    pass



class ProductShow(ProductBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
