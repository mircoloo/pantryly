from pydantic import BaseModel, SecretStr

class UserCreate(BaseModel):
    username: str
    password: SecretStr
    
