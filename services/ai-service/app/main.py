"""
AI Service – Microservizio AI di Pantryly.

Gestisce:
  - Generazione ricette a partire dai prodotti in inventario
  - Categorizzazione automatica dei prodotti
  - Chat libera con l'assistente AI

Comunica con l'inventory-service per recuperare i prodotti.
Non accede direttamente al DB: tutto passa via HTTP inter-servizio.
"""
import logging

from fastapi import FastAPI

from .aiagents import (
    create_categorization_products_agent,
    create_receipe_agent,
    get_response_chat,
)
from . import schemas
from .services.product_client import ProductServiceClient

# Logging strutturato
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s – %(message)s",
)
logger = logging.getLogger("ai-service")

app = FastAPI(
    title="Pantryly AI Service",
    version="1.0.0",
)

# Client condiviso (stateless, può essere singleton)
product_client = ProductServiceClient()


@app.get("/", tags=["Health"])
def health_check():
    """Endpoint di health-check."""
    return {"status": "ok"}


@app.get("/get_receipe_from_product", tags=["Recipes"])
async def get_recipes():
    """
    Genera ricette usando i prodotti presenti in inventario.
    Chiama l'inventory-service per ottenere la lista prodotti,
    poi delega all'agente AI.
    """
    products = await product_client.get_all_products()
    logger.info("Prodotti recuperati per ricette: %d", len(products))
    return await create_receipe_agent(products)


@app.get("/get_categorized_product", tags=["Categorization"])
async def get_categorized_products():
    """
    Categorizza i prodotti usando l'AI.
    Ogni prodotto riceve una categoria semantica (es. "latticini", "frutta").
    """
    products = await product_client.get_all_products()
    logger.info("Prodotti recuperati per categorizzazione: %d", len(products))
    return await create_categorization_products_agent(products)


@app.post("/chat", response_model=schemas.AIChatResponse, tags=["Chat"])
async def chat(req: schemas.AIChatRequest):
    """Chat libera con l'assistente AI."""
    return await get_response_chat(req.request)

