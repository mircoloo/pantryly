

import logging

from fastapi import HTTPException, status

from app.core.auth_handler import AuthHandler
from app.core.hash_helper import get_password_hash, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import (UserCreate, UserHashedCreate, UserLogin,
                              Token)

logger = logging.getLogger(__name__)

class UserAlreadyExistsError(Exception):
    def __init__(self, username: str):
        self.username = username
        super().__init__(username)
        
class IncorrectCredentials(Exception):
    pass
class UserService:

    def __init__(self, repo: UserRepository):
        self.repo = repo

    # ── Creazione utente ─────────────────────────────────────────────
    def create_user(self, user_data: UserCreate) -> User:
        """Registra un nuovo utente dopo aver verificato che lo username sia unico."""
        existing = self.repo.get_by_username(user_data.username)
        if existing:
            raise UserAlreadyExistsError(username=user_data.username)
        hashed_password = get_password_hash(user_data.password)
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

    # ── Login ──────────────────────────────────────────────────────── # TO MODIFY THE ERORS
    def login(self, user_login: UserLogin) -> Token:
        """
        Verify the token and resturn the payload

        """
        user = self.repo.get_by_username(user_login.username)
        

        if not user or not verify_password(user_login.password, user.hashed_password):
            raise IncorrectCredentials
        
        to_sign = {
            "user_id":user.id,
                   }
        
        token = AuthHandler.sign_jwt(to_sign)
        print(AuthHandler.decode_jwt(token))
        if not token:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to process request",
            )
        # Formato OAuth2 standard: access_token + token_type
        return Token(access_token=token, token_type="bearer")
