from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings class for all the auth and user microservice variables"""

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8"
    )

    # ── Database ─────────────────────────────────────────────────────
    DATABASE_URL: str = ""

    # ── JWT ───────────────────────────────────────────────────────────
    JWT_SECRET: SecretStr
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 30 # minutes


settings = Settings() # type: ignore[call-arg] # Loaded from .env file
