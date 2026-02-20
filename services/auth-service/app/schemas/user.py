from pydantic import BaseModel, SecretStr, EmailStr

class UserCreate(BaseModel):
    username: str
    password: str
    
class UserHashedCreate(BaseModel):
    username: str
    hashed_password: str
    
class UserResponse(BaseModel):
    id: int
    username: str
    class Config:
        from_attributes = True
        
class UserUpdate(BaseModel):
    id: int 
    username: str | None = None
    password: str | None = None

class UserLogin(BaseModel):
    username: str
    password: str
    
class UserWithToken(BaseModel):
    token : str