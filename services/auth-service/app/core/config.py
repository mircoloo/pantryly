from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Config(BaseSettings):
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_NAME: str = ""
    DB_URL: str = ""
    
    JWT_SECRET: str = ''
    JWT_ALGORITHM: str = 'HS256'
    JWT_EXPIRATION_TIME: int = 15
    
    
config = Config()

    
