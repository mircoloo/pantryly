"""
API Gateway – Punto di ingresso unico per tutti i microservizi Pantryly.

Architettura:
  ┌─────────┐     ┌──────────────────┐     ┌────────────────┐
  │ Client  │────▶│  API Gateway     │────▶│ auth-service   │
  └─────────┘     │  (questo file)   │────▶│ inventory-svc  │
                  │  JWT validation  │────▶│ ai-service     │
                  └──────────────────┘     └────────────────┘

Flusso:
  1. Il client chiama il Gateway.
  2. Per le rotte protette il Gateway valida il JWT (vedi core/security.py).
  3. Se valido, inoltra la richiesta al microservizio corretto
     aggiungendo l'header x-user-id.
  4. Restituisce al client la risposta originale del servizio.

Rotte pubbliche (senza JWT): /auth/login, /auth/register
Rotte protette (con JWT):    /products/*, /ai/*
"""
import logging

from fastapi import FastAPI

from app.proxy import auth, product, ai

# ── Logging strutturato ──────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s – %(message)s",
)
logger = logging.getLogger("gateway")

# ── Applicazione FastAPI ─────────────────────────────────────────────
app = FastAPI(
    title="Pantryly API Gateway",
    description="Punto di ingresso unico per i microservizi Pantryly",
    version="1.0.0",
)

# ── Registrazione dei router proxy ───────────────────────────────────
# Auth: /auth/*       (pubbliche – login e registrazione)
app.include_router(auth.router)
# Products: /products/* (protette – richiedono JWT)
app.include_router(product.router)
# AI: /ai/*           (protette – richiedono JWT)
app.include_router(ai.router)

logger.info("Gateway avviato – rotte registrate")


@app.get("/health", tags=["Health"])
async def health_check():
    """Endpoint di health-check usato da Docker / load-balancer."""
    return {"status": "ok"}

