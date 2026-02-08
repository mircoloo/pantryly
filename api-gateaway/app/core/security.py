# core/security.py
from jose import jwt, JWTError
from fastapi import HTTPException
from ..config import SECRET_KEY, ALGORITHM

def verify_jwt(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
