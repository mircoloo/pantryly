from .database import Base
from sqlalchemy import Column, Integer, String, Date

class Product(Base):
    __tablename__ = "Products"
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, unique=True, index=True, nullable=False)
    barcode: str = Column(String, unique=True, index=True)
    expiration_date = Column(Date, nullable=True)