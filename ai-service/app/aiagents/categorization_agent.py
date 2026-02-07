from .agent_utils import gemini_client
from typing import List
from .. import schemas
import json

async def create_categorization_products_agent(products: List[schemas.Product]):
    query: str = f"Given the ingredients given here: {json.dumps(products, indent=2)} give a category at each product and return the same but with the category"
    messages = [{"role": "user", "content": query}]
    
    response = gemini_client.chat.completions.parse(
        model="gemini-3-flash-preview",
        messages=messages,
        response_format=schemas.CategorizedProductsResponse
    )
    # If using response_format, the returned object is already your model
    return response.choices[0].message.parsed