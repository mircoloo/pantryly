from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserAlreadyExistsError, UserService
from app.core.auth_handler import AuthHandler
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

router = APIRouter(
    prefix="/v1/users",
    tags=["Users"],
)


def get_user_service(db: Session = Depends(get_db)):
    repo = UserRepository(db)
    return UserService(repo)


def _to_http_exception(exc: Exception) -> HTTPException:
    if isinstance(exc, UserAlreadyExistsError):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Unexpected server error",
    )


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    try:
        return service.create_user(user)
    except UserAlreadyExistsError as exc:
        raise _to_http_exception(exc) from exc

@router.get("/me", response_model=UserResponse)
def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    service: UserService = Depends(get_user_service),
):
    """Return the currently authenticated user based on JWT token."""
    try:
        user_id: int | None = int(AuthHandler.decode_jwt(token).get("user_id"))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user

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


    
