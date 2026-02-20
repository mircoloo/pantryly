"""
Schemi Pydantic per l'inventory-service.

ProductCreate: validazione input per la creazione (user_id viene dall'header, non dal body).
ProductShow: serializzazione output (include id e user_id).
"""
from datetime import date
from typing import Optional

from pydantic import BaseModel


class ProductCreate(BaseModel):
    """Schema per la creazione di un nuovo prodotto (user_id arriva dall'header)."""
    name: str
    barcode: str
    expiration_date: Optional[date] = None


class ProductShow(BaseModel):
    """Schema per la risposta: include id e user_id."""
    id: int
    user_id: int
    name: str
    barcode: str
    expiration_date: Optional[date] = None

    class Config:
        from_attributes = True  # supporto ORM → Pydantic
