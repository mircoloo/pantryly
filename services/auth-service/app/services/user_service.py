from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.schemas.user import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_user(self, user_data: UserCreate) -> User:
        existing = self.repo.get_by_username(user_data.username)
        if existing:
            raise ValueError("Email già registrata")

        # Logica applicativa
        hashed_password = pwd_context.hash(user_data.password)

        user = User(
            username=user_data.username,
            hashed_password=hashed_password
        )
        return self.repo.create(user)
    
    def get_all_users(self) -> list[User]:
        return self.repo.get_all()
    
    def get_user_by_id(self, id:int) -> User | None:
        return self.repo.get_by_id(id)
    
    def get_user_by_username(self, username: str) -> User | None:
        return self.repo.get_by_username(username) 
