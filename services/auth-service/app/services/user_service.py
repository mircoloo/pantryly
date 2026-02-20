"""
Logica di business per la gestione utenti.

Questo servizio orchestra repository, hashing e JWT
senza contenere logica di accesso diretto al DB.
"""
import logging

from fastapi import HTTPException, status

from app.core.authHandler import AuthHandler
from app.core.hashHelper import HashHelper
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import (
    UserCreate,
    UserHashedCreate,
    UserLogin,
    UserWithToken,
)

logger = logging.getLogger(__name__)


class UserService:
    """Servizio applicativo per operazioni CRUD e login utenti."""

    def __init__(self, repo: UserRepository):
        self.repo = repo

    # ── Creazione utente ─────────────────────────────────────────────
    def create_user(self, user_data: UserCreate) -> User:
        """Registra un nuovo utente dopo aver verificato che lo username sia unico."""
        existing = self.repo.get_by_username(user_data.username)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists",
            )

        hashed_password = HashHelper.get_password_hash(user_data.password)
        user_hashed = UserHashedCreate(
            username=user_data.username,
            hashed_password=hashed_password,
        )
        return self.repo.create(user_hashed)

    # ── Query utenti ─────────────────────────────────────────────────
    def get_all_users(self) -> list[User]:
        """Restituisce tutti gli utenti."""
        return self.repo.get_all()

    def get_user_by_id(self, id: int) -> User | None:
        """Restituisce un utente per id, o None."""
        return self.repo.get_by_id(id)

    def get_user_by_username(self, username: str) -> User | None:
        """Restituisce un utente per username, o None."""
        return self.repo.get_by_username(username)

    # ── Login ────────────────────────────────────────────────────────
    def login(self, user_login: UserLogin) -> UserWithToken:
        """
        Verifica le credenziali e restituisce un JWT.

        Nota: NON logghiamo password/hash per motivi di sicurezza.
        """
        user = self.repo.get_by_username(user_login.username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        if not HashHelper.verify_password(user_login.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Check your credentials",
            )

        token = AuthHandler.sign_jwt(user.id)
        if not token:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to process request",
            )
        # Formato OAuth2 standard: access_token + token_type
        return UserWithToken(access_token=token, token_type="bearer")