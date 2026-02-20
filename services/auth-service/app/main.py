from fastapi import FastAPI
from app.core.database import create_db_and_tables
from .api.v1 import user, auth
from app.core.logger import setup_logging
setup_logging()
import logging

logger = logging.getLogger(__name__)
logger.info("Application started")

create_db_and_tables()

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)

