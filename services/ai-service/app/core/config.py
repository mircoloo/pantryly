from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """Impostazioni del servizio di autenticazione."""

    # ── Database ─────────────────────────────────────────────────────
    DATABASE_URL: str = ""
    PRODUCT_SERVICE_URL:str = ""
    GOOGLE_API_KEY: str = ""
    class Config:
        env_file = ".env"


# Istanza singleton importata da tutti i moduli
config = Config()

