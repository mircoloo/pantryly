from datetime import date

from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Product(Base):
    """Product model for ORM."""

    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] 
    name: Mapped[str] 
    barcode: Mapped[str] 
    expiration_date: Mapped[date]
