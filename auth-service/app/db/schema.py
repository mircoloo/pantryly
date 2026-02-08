from sqlalchemy import String, create_engine

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from app.core.config import config

engine = create_engine(config.DB_URL)

LocalSession = sessionmaker(bind=engine, autoflush=False)

Base = DeclarativeBase()

def create_db_and_tables():
    Base.metadata.create_all(engine)

async def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()