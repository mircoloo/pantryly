from sqlalchemy.orm import Session
from app.models.user import User
from app.core.logger import logging


class UserRepository:
    def __init__(self, db: Session):
        self.db: Session = db

    def get_by_id(self, id: int) -> User | None:
        return self.db.query(User).filter(User.id == id).first()

    def get_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def get_all(self) -> list[User]:
        return self.db.query(User).all()
    
    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
