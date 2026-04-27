from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Impostazioni del servizio di autenticazione."""

    # ── Database ─────────────────────────────────────────────────────
    DATABASE_URL: str = ""
    PRODUCT_SERVICE_URL: str = ""
    GOOGLE_API_KEY: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# Istanza singleton importata da tutti i moduli
settings = Settings()
