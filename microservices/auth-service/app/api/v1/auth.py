from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.auth import Token
from app.schemas.user import UserLogin
from app.services.user_service import UserService, IncorrectCredentials
from fastapi.security import OAuth2PasswordRequestForm

from fastapi import HTTPException, status

router = APIRouter(
    prefix="/v1/auth",
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


from fastapi.security import OAuth2PasswordRequestForm

@router.post("/token", response_model=Token)
def get_jwt_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: UserService = Depends(get_user_service),
):
    """
    Authenticate user and return a JWT token.

    Expects form data:
    - username: str
    - password: str

    Returns:
    - access_token: str
    - token_type: "bearer"
    """
    try:
        user = UserLogin(
            username=form_data.username,
            password=form_data.password,
        )
        return service.login(user)

    except Exception as exc:
        raise _to_http_exception(exc) from exc

def _to_http_exception(exc: Exception):
    if isinstance(exc, IncorrectCredentials):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Internal server error",
    )
