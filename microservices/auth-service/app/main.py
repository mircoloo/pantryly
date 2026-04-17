import logging

from fastapi import FastAPI

from app.api.v1 import auth, user
from app.core.database import create_db_and_tables
from app.core.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

create_db_and_tables()

app = FastAPI(
    title="Pantryly Auth Service",
    version="1.0.0",
)

# Registrazione router
app.include_router(user.router, prefix="/api")
app.include_router(auth.router, prefix="/api")

logger.info("Auth service avviato")
