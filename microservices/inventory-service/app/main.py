from contextlib import asynccontextmanager
from fastapi import FastAPI




from fastapi import status

from app.core.database import create_db_and_tables
from app.api.v1 import products


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    # e.g. close connections, cleanup


app = FastAPI(
    title="Pantryly Inventory Service",
    version="0.0.0",
    lifespan=lifespan,
)

@app.get("/", status_code=status.HTTP_200_OK, tags=["Health"])
async def health_check():
    return {"status": "UP"}


app.include_router(products.router)