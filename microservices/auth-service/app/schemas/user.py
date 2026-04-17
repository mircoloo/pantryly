from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=8)
    password: str = Field(min_length=8)


class UserHashedCreate(BaseModel):
    username: str
    hashed_password: str


class UserResponse(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    id: int
    username: str | None = None
    password: str | None = None


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
