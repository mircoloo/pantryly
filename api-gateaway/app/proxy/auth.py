"""
Proxy per l'auth-service.

Inoltra le richieste di registrazione e login al microservizio di autenticazione.
Queste rotte sono PUBBLICHE: non richiedono JWT perché il token
non esiste ancora al momento del login/registrazione.

Flusso tipico:
  Client ──POST /auth/login──▶ Gateway ──POST /v1/auth/login──▶ auth-service
                                 ◀── { token: "..." } ◀──────────────────────
"""
import logging
from typing import Optional

import httpx
from fastapi import APIRouter, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from pydantic import BaseModel

from app.core.config import settings
from app import schemas

logger = logging.getLogger("gateway.auth")

router = APIRouter(prefix="/auth", tags=["Auth"])


# ── Helper interno ───────────────────────────────────────────────────
async def _forward_to_auth(
    method: str,
    path: str,
    body: Optional[BaseModel] = None,
) -> Response:
    """
    Inoltra una richiesta al servizio di autenticazione.

    Se `body` è un modello Pydantic, lo serializza in JSON.
    Preserva status-code e content-type della risposta originale,
    così il client riceve errori significativi (400, 404, …) e non
    un generico 500 dal gateway.
    """
    url = f"{settings.AUTH_SERVICE_URL}{path}"
    content = body.model_dump_json().encode() if body else b""

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.request(
            method=method,
            url=url,
            content=content,
            headers={"Content-Type": "application/json"},
        )

    logger.info("auth-service %s %s → %s", method, path, response.status_code)

    # Restituiamo la risposta così com'è (status + body + content-type)
    return Response(
        content=response.content,
        status_code=response.status_code,
        media_type=response.headers.get("content-type"),
    )


# ── Rotte pubbliche ────────────────────────────────────────────────
@router.post("/register", response_model=schemas.UserResponse)
async def register(body: schemas.UserCreate):
    """
    Registrazione di un nuovo utente.
    Proxy verso: POST /v1/users (auth-service).
    """
    return await _forward_to_auth("POST", "/v1/users", body)


@router.post("/login", response_model=schemas.TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login e generazione JWT (OAuth2-compatibile).

    Swagger invia i campi come form-data (username + password).
    Il gateway li converte in JSON e inoltra all'auth-service.
    Proxy verso: POST /v1/auth/login (auth-service).
    """
    # Converte i campi del form OAuth2 in un modello JSON per l'auth-service
    body = schemas.UserLogin(
        username=form_data.username,
        password=form_data.password,
    )
    return await _forward_to_auth("POST", "/v1/auth/login", body)
