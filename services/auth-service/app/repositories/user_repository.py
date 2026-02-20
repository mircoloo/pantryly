from sqlalchemy.orm import Session
from app.models.user import User
from app.core.logger import logging
from app.schemas.user import UserHashedCreate

class UserRepository:
    def __init__(self, db: Session):
        self.db: Session = db

    def create(self, user: UserHashedCreate) -> User:
        print(user)
        new_user = User(**user.model_dump(exclude_none=True))
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
    
    def get_by_id(self, id: int) -> User | None:
        return self.db.query(User).filter(User.id == id).first()

    def get_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def get_all(self) -> list[User]:
        return self.db.query(User).all()
    
    
