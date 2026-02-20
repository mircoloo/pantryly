"""
Inventory Service – Microservizio per la gestione dei prodotti Pantryly.

Gestisce:
  - CRUD prodotti (nome, barcode, scadenza)
  - Consultazione inventario
"""
import logging

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, status

from .database import create_db_and_tables
from .routes import products

# Logging strutturato
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s – %(message)s",
)
logger = logging.getLogger("inventory")

# Creazione tabelle al primo avvio
create_db_and_tables()

app = FastAPI(
    title="Pantryly Inventory Service",
    version="1.0.0",
)


@app.get("/", status_code=status.HTTP_200_OK, tags=["Health"])
def health_check():
    """Endpoint di health-check."""
    return {"status": "ok"}


app.include_router(products.router)

logger.info("Inventory service avviato")
