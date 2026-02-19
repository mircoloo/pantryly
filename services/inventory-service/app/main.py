from dotenv import load_dotenv
load_dotenv()
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import schemas
from . import database
from . import models
from . import repository
from .database import get_db, create_db_and_tables
from .routes import products
from . import logging as log

create_db_and_tables()
app = FastAPI()

log.logger.error("Stay calm!")

@app.get("/",  status_code=status.HTTP_200_OK)
def check_online():
    return {"status": "ok"}

app.include_router(products.router)