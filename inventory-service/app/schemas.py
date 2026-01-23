from pydantic import BaseModel
from datetime import date
from typing import Optional, Union

class ProductCreate(BaseModel):
    name: str
    barcode: str
    expiration_date: Optional[date]
    
class ProductShow(BaseModel):
    name: str
    barcode: str
    expiration_date: Optional[date]