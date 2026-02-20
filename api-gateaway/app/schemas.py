"""
Schemi Pydantic del Gateway.

Questi schemi replicano i contratti dei microservizi downstream
per due motivi:
  1. Documentazione OpenAPI/Swagger: il client vede body e response tipizzati.
  2. Validazione anticipata: il gateway rifiuta subito una request malformata
     invece di inoltrare dati invalidi al servizio interno.

NOTA: se un servizio aggiunge campi, basta aggiornare lo schema
corrispondente qui per mantenere la doc in sync.
"""
from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field


# ── Auth ────────────────────────────────────────────────────────────
class UserCreate(BaseModel):
    """Body per la registrazione di un nuovo utente."""
    username: str
    password: str


class UserLogin(BaseModel):
    """Body per il login."""
    username: str
    password: str


class UserResponse(BaseModel):
    """Risposta con i dati pubblici dell'utente (senza password)."""
    id: int
    username: str


class TokenResponse(BaseModel):
    """Risposta OAuth2-compatibile del login."""
    access_token: str
    token_type: str = "bearer"


# ── Products ────────────────────────────────────────────────────────
class ProductCreate(BaseModel):
    """Body per la creazione di un prodotto."""
    name: str
    barcode: str
    expiration_date: Optional[date] = None


class ProductShow(BaseModel):
    """Rappresentazione di un prodotto restituito dall'inventario."""
    id: int
    user_id: int
    name: str
    barcode: str
    expiration_date: Optional[date] = None


# ── AI ──────────────────────────────────────────────────────────────
class AIChatRequest(BaseModel):
    """Body per la chat libera con l'AI."""
    request: str


class AIChatResponse(BaseModel):
    """Risposta della chat AI."""
    response: str


class Product(BaseModel):
    """Prodotto usato dentro le ricette AI."""
    name: str
    expiration_date: date
    barcode: str = Field(description="Il codice a barre del prodotto")


class CategorizedProduct(Product):
    """Prodotto con categoria assegnata dall'AI."""
    category: str


class CategorizedProductsResponse(BaseModel):
    """Risposta dell'endpoint di categorizzazione AI."""
    products: List[CategorizedProduct]


class Receipe(BaseModel):
    """Singola ricetta generata dall'AI."""
    name: str = Field(description="Il nome della ricetta")
    dish_type: str = Field(description="Tipo di piatto (primo, dolce, ecc.)")
    ingredients: List[Product] = Field(description="Ingredienti necessari")
    receipe: str = Field(description="Passaggi per preparare la ricetta")


class ReceipesResponse(BaseModel):
    """Risposta dell'endpoint di generazione ricette."""
    receipes: List[Receipe]
