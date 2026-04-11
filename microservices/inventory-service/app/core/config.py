from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

WORK_DIR = Path(__file__).parent.parent.parent / ".env"
class Config(BaseSettings):
    DATABASE_URL: str = ""

    model_config = SettingsConfigDict(env_file=WORK_DIR)



config = Config()
