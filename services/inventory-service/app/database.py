"""
Configurazione database per l'inventory-service.

In sviluppo usa SQLite; in produzione basta cambiare DATABASE_URL
nel file .env per puntare a PostgreSQL/MySQL.
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# check_same_thread serve solo per SQLite
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)


class Base(DeclarativeBase):
    """Classe base per tutti i modelli SQLAlchemy."""
    pass


LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_db_and_tables():
    """Crea tutte le tabelle definite nei modelli (idempotente)."""
    Base.metadata.create_all(engine)


def get_db():
    """
    Dependency FastAPI che fornisce una sessione DB per ogni request.
    La sessione viene chiusa automaticamente al termine della request.
    """
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

