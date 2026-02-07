from .agent_utils import gemini_client
from typing import List
from .. import schemas
import json


async def create_receipe_agent(products : List[schemas.Product]):
    query: str = f"""
                Dati i seguenti ingredienti:
                {json.dumps(products, indent=2)}

                Suggerisci una o più ricette gustose e ben bilanciate.
                Non è necessario utilizzare tutti gli ingredienti, ma la ricetta deve essere coerente e sensata.
                Rispondi esclusivamente in lingua italiana.
                Se non ci sono ingredienti rispondere che non ci sono ingredienti per cucinare.
                """
    messages = [{"role": "user", "content": query}]
    response = gemini_client.chat.completions.parse(
        model="gemini-3-flash-preview",
        messages=messages,
        response_format=schemas.ReceipesResponse
    )
    return response.choices[0].message.parsed