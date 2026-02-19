from fastapi import APIRouter, Depends
from app.services.user_service import UserService
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.schema import get_db

router = APIRouter(prefix="/v1", tags=["Users"])

user_service = UserService()

@router.get("/users")
async def read_users(db: AsyncSession = Depends(get_db)):
    return user_service.get_users(db)




