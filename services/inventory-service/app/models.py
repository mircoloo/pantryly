"""
Modello SQLAlchemy per i prodotti.

Ogni prodotto è associato a un utente tramite user_id.
L'utente può vedere e gestire solo i propri prodotti (multi-tenancy).
"""
from sqlalchemy import Column, Date, Integer, String

from .database import Base


class Product(Base):
    """Rappresenta un prodotto nell'inventario di un utente."""
    __tablename__ = "products"

    id: int = Column(Integer, primary_key=True, index=True)
    # ID dell'utente proprietario (ricevuto dal gateway via header x-user-id)
    user_id: int = Column(Integer, nullable=False, index=True)
    name: str = Column(String, index=True, nullable=False)
    barcode: str = Column(String, index=True)
    expiration_date = Column(Date, nullable=True)
