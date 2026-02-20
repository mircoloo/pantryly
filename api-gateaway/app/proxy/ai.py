"""
Proxy per l'ai-service.

Tutte le rotte richiedono autenticazione JWT.
Il Gateway valida il token e propaga l'identità dell'utente all'ai-service
tramite l'header interno `x-user-id`.

Nota: il timeout è più generoso (60 s) perché le chiamate AI
(generazione ricette, categorizzazione) possono richiedere più tempo.
"""
import logging
from typing import Optional

import httpx
from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel

from app.core.config import settings
from app.core.security import get_current_user
from app import schemas

logger = logging.getLogger("gateway.ai")

router = APIRouter(prefix="/ai", tags=["AI"])


# ── Helper interno ───────────────────────────────────────────────────
async def _forward_to_ai(
    method: str,
    path: str,
    user: dict,
    body: Optional[BaseModel] = None,
) -> Response:
    """
    Inoltra la richiesta all'ai-service.

    - Aggiunge l'header x-user-id con l'id dell'utente autenticato.
    - Se `body` è un modello Pydantic, lo serializza in JSON.
    - Timeout più alto (60 s) per le risposte AI.
    """
    url = f"{settings.AI_SERVICE_URL}{path}"
    content = body.model_dump_json().encode() if body else b""
    headers = {
        "Content-Type": "application/json",
        "x-user-id": str(user.get("sub", "")),
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.request(
            method=method,
            url=url,
            content=content,
            headers=headers,
        )

    logger.info("ai-service %s %s → %s", method, path, response.status_code)

    return Response(
        content=response.content,
        status_code=response.status_code,
        media_type=response.headers.get("content-type"),
    )


# ── Rotte protette ──────────────────────────────────────────────────
@router.get("/recipes", response_model=schemas.ReceipesResponse)
async def get_recipes(user: dict = Depends(get_current_user)):
    """Genera ricette a partire dai prodotti in inventario."""
    return await _forward_to_ai("GET", "/get_receipe_from_product", user)


@router.get("/categorize", response_model=schemas.CategorizedProductsResponse)
async def categorize_products(user: dict = Depends(get_current_user)):
    """Categorizza i prodotti usando l'AI."""
    return await _forward_to_ai("GET", "/get_categorized_product", user)


@router.post("/chat", response_model=schemas.AIChatResponse)
async def ai_chat(
    body: schemas.AIChatRequest,
    user: dict = Depends(get_current_user),
):
    """Chat libera con l'assistente AI."""
    return await _forward_to_ai("POST", "/chat", user, body)
