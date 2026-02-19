from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Config(BaseSettings):
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_NAME: str = ""
    DB_URL: str = ""
    
    SECRET_KEY: str = ''
    ALGORITHM: str = 'HS256'
    
    
config = Config()

    
