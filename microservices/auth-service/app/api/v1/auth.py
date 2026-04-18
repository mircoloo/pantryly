from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserLogin
from app.services.user_service import UserService, IncorrectCredentials
from fastapi import HTTPException, status

router = APIRouter(
    prefix="/v1/auth",
    tags=["Auth"],
)

def _to_http_exception(exc: Exception):
    if isinstance(exc, IncorrectCredentials):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Internal server error"
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
    try:
        return service.login(user)
    except Exception as exc:
        raise _to_http_exception(exc) from exc

