from app.core.config import config
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
import os 

DATABASE_URL = config.DATABASE_URL

class Base(DeclarativeBase):
    """Classe base per tutti i modelli SQLAlchemy."""


def create_db_and_tables():
    """Create db and tables if not exists."""
    Base.metadata.create_all(engine)
    
def get_db():
    db: Session = LocalSession()
    try:
        yield db
    finally:
        db.close()

# check_same_thread serve solo per SQLite
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
