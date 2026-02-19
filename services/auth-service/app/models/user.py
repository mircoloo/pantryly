from sqlalchemy import Column, String, Integer
from ..db.schema import Base
class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    password_hashed = Column(String, nullable=False)