from datetime import datetime, timedelta, timezone, UTC
from typing import Dict, Any, Mapping, TypedDict
from jose import ExpiredSignatureError, JWTError, jwt

from app.core.config import settings

JWT_SECRET = settings.JWT_SECRET
JWT_ALGORITHM = settings.JWT_ALGORITHM
JWT_EXPIRATION_MINUTES = settings.JWT_EXPIRATION_MINUTES


class AuthHandler:
    """Stateless class for JWT handling."""

    @staticmethod
    def sign_jwt(data: dict, expires_delta: timedelta | None = None) -> str:
        """
        Generate and sign a JSON Web Token (JWT) from the provided payload.

        The function creates a copy of the input data, adds an expiration claim
        ("exp"), and signs the token using the configured secret key and algorithm.

        Args:
            data (dict): The payload to include in the JWT. Must be JSON-serializable.
            expires_delta (timedelta): Time interval after which the token will expire.

        Returns:
            str: Encoded JWT as a string.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else:
            expire = datetime.now(UTC) + timedelta(
                minutes=settings.JWT_EXPIRATION_MINUTES
            )

        to_encode.update({"exp": expire})

        return jwt.encode(
            claims=to_encode, key=JWT_SECRET.get_secret_value(), algorithm=JWT_ALGORITHM
        )

    @staticmethod
    def decode_jwt(token: str) -> dict[str, Any] | None:
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
