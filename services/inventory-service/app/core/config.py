from pydantic_settings import BaseSettings


class Config(BaseSettings):

    # ── Database ─────────────────────────────────────────────────────
    DATABASE_URL: str = ""

    class ConfigDict:
        env_file = ".env"


# Istanza singleton importata da tutti i moduli
config = Config()

