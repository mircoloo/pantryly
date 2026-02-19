from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

router = APIRouter()

def get_user_service(db: Session = Depends(get_db)):
    repo = UserRepository(db)
    return UserService(repo)

@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    try:
        return service.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))




@router.get("/users/{id}", response_model=UserResponse)
async def get_user_by_id(id: int, service: UserService = Depends(get_user_service)):
    return service.get_user_by_id(id)

@router.get("/users", response_model=list[UserResponse])
async def read_users(service: UserService = Depends(get_user_service)):
    return service.get_all_users()


# @router.get("/users", response_model=UserResponse)
# async def get_user_by_username(username: str, service: UserService = Depends(get_user_service)):
#     return service.get_user_by_username(username)

