from datetime import date


from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

class Product(Base):
    """Product model for ORM."""

    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer)
    # user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True) For future implementation
    name: Mapped[str] = mapped_column(String)
    barcode: Mapped[str] = mapped_column(String)
    expiration_date: Mapped[date]
