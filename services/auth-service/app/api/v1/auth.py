from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserLogin
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.core.database import get_db
import logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/v1//auth",
    tags=["Auth"]
)

def get_user_service(db: Session = Depends(get_db)):
    repo = UserRepository(db)
    return UserService(repo)


@router.post("/login")
def login(user: UserLogin, service: UserService = Depends(get_user_service)):
    try:
        return service.login(user)
    except Exception as error:
        raise error
