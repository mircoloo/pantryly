"""
Auth Service – Microservizio di autenticazione Pantryly.

Gestisce:
  - Registrazione utenti (POST /v1/users)
  - Login e generazione JWT (POST /v1/auth/login)
  - Query utenti (GET /v1/users, GET /v1/users/{id})
"""
import logging

from fastapi import FastAPI

from app.core.database import create_db_and_tables
from app.core.logger import setup_logging
from app.api.v1 import auth, user

# Configurazione logging prima di qualsiasi altra operazione
setup_logging()
logger = logging.getLogger(__name__)

# Creazione tabelle al primo avvio (SQLite / dev)
create_db_and_tables()

app = FastAPI(
    title="Pantryly Auth Service",
    version="1.0.0",
)

# Registrazione router
app.include_router(user.router)
app.include_router(auth.router)

logger.info("Auth service avviato")

