"""
Endpoint CRUD per gli utenti.

La registrazione (POST /v1/users) è esposta anche dal Gateway
tramite il proxy /auth/register.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService

router = APIRouter(
    prefix="/v1/users",
    tags=["Users"],
)


def get_user_service(db: Session = Depends(get_db)):
    """Factory dependency: crea UserService con il repository iniettato."""
    repo = UserRepository(db)
    return UserService(repo)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    """Registra un nuovo utente."""
    return service.create_user(user)


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, service: UserService = Depends(get_user_service)):
    """Recupera un utente per id."""
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.get("", response_model=list[UserResponse])
def list_users(service: UserService = Depends(get_user_service)):
    """Elenca tutti gli utenti."""
    return service.get_all_users()

