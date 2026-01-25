from fastapi import FastAPI
from .aiagents.test_agent import process_request
from . import schemas
import httpx
from .services.product_client import ProductServiceClient
app = FastAPI()

product_service_client = ProductServiceClient()

@app.get("/")
def test_endpoint():
    return "OK"

@app.post("/chat")
async def chat_request(request: schemas.AIChatRequest):
    products = await product_service_client.get_all_products()
    print(products)
    return await process_request(request, products)
