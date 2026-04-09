from app.core.config import config
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

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
