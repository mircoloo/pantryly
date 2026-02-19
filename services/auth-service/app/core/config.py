from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Config(BaseSettings):
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_NAME: str = "test.db"
    DB_URL: str = "sqlite:///./auth_service.db"
    
config = Config()
    
    
print(config.DB_URL)