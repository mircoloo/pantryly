"""
Repository per la tabella 'users'.

Accesso diretto al DB – nessuna logica di business qui.
La logica di business sta in UserService.
"""
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserHashedCreate


class UserRepository:
    """Pattern Repository: incapsula tutte le query sulla tabella users."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, user: UserHashedCreate) -> User:
        """Inserisce un nuovo utente e restituisce l'entità con l'id generato."""
        new_user = User(**user.model_dump(exclude_none=True))
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def get_by_id(self, id: int) -> User | None:
        """Cerca un utente per id."""
        return self.db.query(User).filter(User.id == id).first()

    def get_by_username(self, username: str) -> User | None:
        """Cerca un utente per username."""
        return self.db.query(User).filter(User.username == username).first()

    def get_all(self) -> list[User]:
        """Restituisce tutti gli utenti."""
        return self.db.query(User).all()

