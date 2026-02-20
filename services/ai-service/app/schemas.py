"""
Schemi Pydantic per l'ai-service.

Definiscono la struttura dei dati in ingresso/uscita degli endpoint AI.
Usati anche come `response_format` per le risposte strutturate di Gemini.
"""
from datetime import date
from typing import List

from pydantic import BaseModel, Field


# ── Prodotti ─────────────────────────────────────────────────────
class Product(BaseModel):
    """Prodotto base (ricevuto dall'inventory-service)."""
    name: str
    expiration_date: date
    barcode: str = Field(description="Il codice a barre del prodotto")


class CategorizedProduct(Product):
    """Prodotto con categoria assegnata dall'AI."""
    category: str


class CategorizedProductsResponse(BaseModel):
    """Risposta dell'endpoint di categorizzazione."""
    products: List[CategorizedProduct]


# ── Ricette ──────────────────────────────────────────────────────
class Receipe(BaseModel):
    """Singola ricetta generata dall'AI."""
    name: str = Field(description="Il nome della ricetta")
    dish_type: str = Field(description="Il tipo di piatto (primo, dolce, ecc.)")
    ingredients: List[Product] = Field(description="Ingredienti necessari")
    receipe: str = Field(description="I passaggi per preparare la ricetta")


class ReceipesResponse(BaseModel):
    """Risposta dell'endpoint di generazione ricette."""
    receipes: List[Receipe]


# ── Chat ─────────────────────────────────────────────────────────
class AIChatRequest(BaseModel):
    """Richiesta per la chat libera."""
    request: str


class AIChatResponse(BaseModel):
    """Risposta della chat libera."""
    response: str

