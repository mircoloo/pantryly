from sqlalchemy.orm import Session
from ..models import User
from sqlalchemy.ext.asyncio import AsyncSession

class UserService:
    def __init__(self):
        pass

    def get_users(self, db: AsyncSession):
        return db.query(User).all()
    
    def get_user(self, id: int, db: AsyncSession):
        return db.query(User).filter(User.id)
    
    def create_user(self, username: str, password: str, db: AsyncSession):
        new_user = User()
