from datetime import date
from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class Product(Base):
    """Product model for ORM."""

    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    name: Mapped[str]
    barcode: Mapped[str]
    expiration_date: Mapped[date]
