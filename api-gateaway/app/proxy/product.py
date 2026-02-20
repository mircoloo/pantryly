"""
Proxy per l'inventory-service.

Tutte le rotte richiedono autenticazione: il Gateway valida il JWT
e inoltra l'header x-user-id al servizio downstream, così da poter
associare i prodotti all'utente (multi-tenancy futura).

Vantaggi rispetto al catch-all generico `/{path:path}`:
  - Ogni endpoint è documentato in OpenAPI/Swagger.
  - Validazione esplicita dei parametri (es. product_id: int).
  - Più facile aggiungere rate-limiting o cache per singola rotta.
"""
import logging
from typing import List, Optional

import httpx
from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel

from app.core.config import settings
from app.core.security import get_current_user
from app import schemas

logger = logging.getLogger("gateway.products")

router = APIRouter(prefix="/products", tags=["Products"])


# ── Helper interno ───────────────────────────────────────────────────
async def _forward_to_inventory(
    method: str,
    path: str,
    user: dict,
    body: Optional[BaseModel] = None,
) -> Response:
    """
    Inoltra la richiesta all'inventory-service.

    - Aggiunge l'header `x-user-id` con l'id dell'utente autenticato.
    - Se `body` è un modello Pydantic, lo serializza in JSON.
    - Preserva status-code, body e content-type originali.
    """
    url = f"{settings.PRODUCT_SERVICE_URL}{path}"
    content = body.model_dump_json().encode() if body else b""
    headers = {
        "Content-Type": "application/json",
        "x-user-id": str(user.get("sub", "")),
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.request(
            method=method,
            url=url,
            content=content,
            headers=headers,
        )

    logger.info("inventory-service %s %s → %s", method, path, response.status_code)

    return Response(
        content=response.content,
        status_code=response.status_code,
        media_type=response.headers.get("content-type"),
    )


# ── Rotte protette ──────────────────────────────────────────────────
@router.get("", response_model=List[schemas.ProductShow])
async def list_products(user: dict = Depends(get_current_user)):
    """Elenca tutti i prodotti."""
    return await _forward_to_inventory("GET", "/v1/products", user)


@router.post("", response_model=schemas.ProductShow, status_code=status.HTTP_201_CREATED)
async def create_product(
    body: schemas.ProductCreate,
    user: dict = Depends(get_current_user),
):
    """Crea un nuovo prodotto."""
    return await _forward_to_inventory("POST", "/v1/products", user, body)


@router.get("/{product_id}", response_model=schemas.ProductShow)
async def get_product(product_id: int, user: dict = Depends(get_current_user)):
    """Recupera un prodotto per id."""
    return await _forward_to_inventory("GET", f"/v1/products/{product_id}", user)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, user: dict = Depends(get_current_user)):
    """Elimina un prodotto per id."""
    return await _forward_to_inventory("DELETE", f"/v1/products/{product_id}", user)
