from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserLogin
from app.services.user_service import UserService

router = APIRouter(
    prefix="/v1/auth",  # FIX: rimosso il doppio slash
    tags=["Auth"],
)


def get_user_service(db: Session = Depends(get_db)):
    """Factory dependency: crea UserService con il repository iniettato."""
    repo = UserRepository(db)
    return UserService(repo)

# TO add the auth service different form user service
# def get_auth_service(db: Session = Depends(get_db)):
#     repo = UserRepository(db)
#     return UserService(repo)


@router.post("/login")
def login(user: UserLogin, service: UserService = Depends(get_user_service)):
    """
    Login the user and response with JWT token

    Body: { "username": "...", "password": "..." }
    Response: { "token": "<jwt>" }
    """
    return service.login(user)
