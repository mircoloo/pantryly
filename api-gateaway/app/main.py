from fastapi import FastAPI
from .proxy import product, ai

app = FastAPI(title="API Gateway")

app.include_router(product.router)
app.include_router(ai.router)
