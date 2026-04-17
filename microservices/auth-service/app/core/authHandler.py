
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, TypedDict
from jose import ExpiredSignatureError, JWTError, jwt

from app.core.config import settings


JWT_SECRET = settings.JWT_SECRET
JWT_ALGORITHM = settings.JWT_ALGORITHM
JWT_EXPIRATION_TIME = settings.JWT_EXPIRATION_MINUTES  


class AuthHandler:
    """Utility stateless per la gestione dei token JWT."""

    @staticmethod
    def sign_jwt(user_id: int) -> str:
        """
        Generate a JWT token with the subject (sub) = user_id
        """
        expiration = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRATION_TIME)
        payload: Dict[str, Any] = {
            "sub": str(user_id),
            "exp": expiration,
        }
        return jwt.encode(
            claims=payload, 
            key=JWT_SECRET.get_secret_value(), 
            algorithm=JWT_ALGORITHM)

    @staticmethod
    def decode_jwt(token: str) -> dict:
        try:
            return jwt.decode(
                token,
                JWT_SECRET.get_secret_value(),
                algorithms=[JWT_ALGORITHM],
            )
        except ExpiredSignatureError:
            return {"error": "Token has expired"}
        except JWTError:
            return {"error": "Invalid token"}
