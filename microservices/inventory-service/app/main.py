from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.v1 import products
from app.core.database import create_db_and_tables

import httpx
import requests

BASE_DIR = Path(__file__).resolve().parent

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

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get("/products/{user_id}", response_class=HTMLResponse)
async def read_posts(request: Request, user_id: int):
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://localhost:8000/v1/products?user_id={user_id}")
        posts = response.json()
        
    return templates.TemplateResponse(
        request=request, name="item.html", context={"posts": posts}
    )

@app.get("/", status_code=status.HTTP_200_OK, tags=["Health"])
async def health_check():
    return {"status": "UP"}


app.include_router(products.router)