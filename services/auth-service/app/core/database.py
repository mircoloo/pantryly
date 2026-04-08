from app.core.config import config
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

engine = create_engine(config.DATABASE_URL)

LocalSession = sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase):
    pass


def create_db_and_tables():
    Base.metadata.create_all(bind=engine)


async def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()
