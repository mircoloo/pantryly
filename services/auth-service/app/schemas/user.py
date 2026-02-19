from pydantic import BaseModel, SecretStr, EmailStr

class UserCreate(BaseModel):
    username: str
    password: str
    
class UserResponse(BaseModel):
    id: int
    username: str
    hashed_password: str

    class Config:
        from_attributes = True
