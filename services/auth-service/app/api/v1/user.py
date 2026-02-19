from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

def get_user_service(db: Session = Depends(get_db)):
    repo = UserRepository(db)
    return UserService(repo)

@router.post("", response_model=UserResponse)
def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    try:
        return service.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{id}", response_model=UserResponse)
async def get_user_by_id(id: int, service: UserService = Depends(get_user_service)):
    user = service.get_user_by_id(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.get("/", response_model=list[UserResponse])
async def read_users(service: UserService = Depends(get_user_service)):
    return service.get_all_users()


# @router.get("/users", response_model=UserResponse)
# async def get_user_by_username(username: str, service: UserService = Depends(get_user_service)):
#     return service.get_user_by_username(username)

