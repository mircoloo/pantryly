import httpx
import os 
from .. import schemas
from typing import List

base_url = os.environ.get("PRODUCT_SERVICE_URL")

class ProductServiceClient:
    def __init__(self):
        self.base_url = base_url
    async def get_all_products(self) -> List[schemas.Product]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.base_url}/v1/products")
                response.raise_for_status() 
                # Trasforma il JSON in oggetti Pydantic (validazione automatica)
                pydantic_products = [schemas.Product(**item) for item in response.json()]
                return [item for item in response.json()]
                    
            except httpx.RequestError as exc:
                print(f"Errore di rete: {exc}")
                return []
            except httpx.HTTPStatusError as exc:
                print(f"Il servizio prodotti ha risposto con errore: {exc.response.status_code}")
                return []