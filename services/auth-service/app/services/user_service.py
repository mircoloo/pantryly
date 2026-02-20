from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.schemas.user import UserCreate, UserHashedCreate, UserLogin, UserWithToken
from app.core.hashHelper import HashHelper
from app.core.authHandler import AuthHandler
from fastapi import HTTPException, status
import logging
logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_user(self, user_data: UserCreate) -> User:
        existing = self.repo.get_by_username(user_data.username)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Username already exists")

        hashed_password = HashHelper.get_password_hash(user_data.password)
        user_hashed = UserHashedCreate(username=user_data.username, hashed_password=hashed_password)
        
        return self.repo.create(user_hashed)
    
    def get_all_users(self) -> list[User]:
        return self.repo.get_all()
    
    def get_user_by_id(self, id:int) -> User | None:
        return self.repo.get_by_id(id)
    
    def get_user_by_username(self, username: str) -> User | None:
        res = self.repo.get_by_username(username)
        return res
    
    def login(self, user_login: UserLogin) -> UserWithToken:
        user = self.repo.get_by_username(user_login.username)
        if not user: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found")
        logger.info(f"{user.username=}  {user.hashed_password=} {HashHelper.get_password_hash(user_login.password)=}")
        if HashHelper.verify_password(user_login.password, user.hashed_password):
            token = AuthHandler.sign_jwt(user.id)
            if token:
                return UserWithToken(token = token)
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Unable to process request")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Check your credentials")