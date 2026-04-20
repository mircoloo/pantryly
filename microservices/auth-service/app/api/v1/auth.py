from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated

from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import Token, UserLogin
from app.services.user_service import UserService, IncorrectCredentials
from app.core.auth_handler import AuthHandler

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

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


@router.post("/login")
def login(user: UserLogin, 
          service: Annotated[UserService, Depends(get_user_service)]) -> Token:
    """
    Login the user and response with JWT token

    Body: { "username": "...", "password": "..." }
    Response: { "token": "<jwt>" }
    """
    try:
        return service.login(user)
    except Exception as exc:
        raise _to_http_exception(exc) from exc


@router.post("/verify_token")
def verify_token(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    payload = AuthHandler.decode_jwt(token=token)
    if payload is None:
        raise HTTPException(
            detail="Not valid token",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    return payload


@router.get("/introspect", status_code=status.HTTP_204_NO_CONTENT)
def introspect_token(
    token: Annotated[str, Depends(oauth2_scheme)],
    service: Annotated[UserService, Depends(get_user_service)],
) -> Response:
    payload = AuthHandler.decode_jwt(token=token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    user = service.get_user_by_id(int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT, headers={"X-User-Id": str(user.id)})

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
