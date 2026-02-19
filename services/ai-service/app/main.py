from fastapi import FastAPI
from .aiagents import create_receipe_agent, create_categorization_products_agent, get_response_chat
from . import schemas
from .services.product_client import ProductServiceClient
app = FastAPI()

product_service_client = ProductServiceClient()

@app.get("/")
def test_endpoint():
    return "OK"

@app.get("/get_receipe_from_product")
async def get_receipe_from_products():
    # Retrieve products from the db
    products = await product_service_client.get_all_products()
    print(products)
    return await create_receipe_agent(products)

@app.get("/get_categorized_product")
async def get_categorized_products():
    products = await product_service_client.get_all_products()

    return await create_categorization_products_agent(products)

@app.post("/chat", response_model=schemas.AIChatResponse)
async def chat(req: schemas.AIChatRequest):
    return await get_response_chat(req.request)
