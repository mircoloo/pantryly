"""
Endpoint di autenticazione (login).

Questo modulo espone le rotte per l'autenticazione degli utenti.
La registrazione avviene tramite il modulo user.py (POST /v1/users).
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import UserLogin
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.core.database import get_db

router = APIRouter(
    prefix="/v1/auth",  # FIX: rimosso il doppio slash
    tags=["Auth"],
)


def get_user_service(db: Session = Depends(get_db)):
    """Factory dependency: crea UserService con il repository iniettato."""
    repo = UserRepository(db)
    return UserService(repo)


@router.post("/login")
def login(user: UserLogin, service: UserService = Depends(get_user_service)):
    """
    Effettua il login e restituisce un JWT.

    Body: { "username": "...", "password": "..." }
    Risposta: { "token": "<jwt>" }
    """
    return service.login(user)
