"""
Configurazione centralizzata dell'auth-service.

Le variabili vengono caricate automaticamente dal file .env tramite pydantic-settings.
Il JWT_SECRET DEVE essere lo stesso valore usato nel Gateway.
"""
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """Impostazioni del servizio di autenticazione."""

    # ── Database ─────────────────────────────────────────────────────
    DB_URL: str = "sqlite:///./auth_service.db"

    # ── JWT ───────────────────────────────────────────────────────────
    JWT_SECRET: str = ""          # OBBLIGATORIO: impostare nel .env
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_TIME: int = 15  # minuti

    class Config:
        env_file = ".env"


# Istanza singleton importata da tutti i moduli
config = Config()

