from fastapi import FastAPI
from .aiagents.test_agent import process_request, process_get_categorized_products
from . import schemas
import httpx
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
    return await process_request(products)

@app.get("/get_categorized_product")
async def get_categorized_products():
    products = await product_service_client.get_all_products()
    return await process_get_categorized_products(products)