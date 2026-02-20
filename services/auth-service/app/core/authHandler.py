from jose import ExpiredSignatureError
from passlib.exc import InvalidTokenError
from jose import jwt
from app.core.config import config
from datetime import datetime, timedelta, timezone

JWT_SECRET = config.JWT_SECRET
JWT_ALGORITHM = config.JWT_ALGORITHM
JWT_EXPIRATION_TIME = config.JWT_EXPIRATION_TIME 

class AuthHandler(object):

    @staticmethod
    def sign_jwt(user_id: int) -> str:
        expiration = datetime.now(timezone.utc) + timedelta(
            minutes=JWT_EXPIRATION_TIME
        )
        payload = {
            "user_id": user_id,
            "exp": expiration 
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return token
    
    @staticmethod
    def decode_jwt(token: str) -> dict:
        try:
            decoded_token = jwt.decode(
                token,
                JWT_SECRET,
                algorithms=[JWT_ALGORITHM]
            )
            return decoded_token

        except ExpiredSignatureError:
            return {"error": "Token has expired"}

        except InvalidTokenError:
            return {"error": "Invalid token"} 
        