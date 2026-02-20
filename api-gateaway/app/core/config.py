"""
Configurazione centralizzata del Gateway.

Usa pydantic-settings per caricare le variabili d'ambiente dal file .env.
Ogni variabile ha un default sicuro; in produzione va sovrascritta via env
o tramite il file .env nella root del servizio.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Impostazioni caricate automaticamente dalle variabili d'ambiente."""

    # ── URL interni dei microservizi (risolti via Docker network) ────
    AUTH_SERVICE_URL: str = "http://auth-service:8000"
    PRODUCT_SERVICE_URL: str = "http://inventory-service:8000"
    AI_SERVICE_URL: str = "http://ai-service:8000"

    # ── JWT – DEVE corrispondere al segreto usato dall'auth-service ──
    JWT_SECRET: str = ""
    JWT_ALGORITHM: str = "HS256"

    class Config:
        # Cerca il .env nella directory di lavoro (root del servizio)
        env_file = ".env"


# Istanza singleton importata da tutti i moduli del gateway
settings = Settings()

