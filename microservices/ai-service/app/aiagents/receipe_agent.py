"""
Agente AI per la generazione di ricette.

Riceve la lista di prodotti/ingredienti dall'inventario
e genera suggerimenti di ricette usando Gemini.
"""

import json

import openai
from app import schemas


async def create_receipe_agent(
    products: list[schemas.Product],
    client: openai.OpenAI,
) -> schemas.ReceipesResponse:
    products_json = json.dumps([p.model_dump(mode="json") for p in products])
    query: str = f"""
        Dati i seguenti ingredienti:
        {products_json}
        
        Suggerisci una o più ricette gustose e ben bilanciate.
        Non è necessario utilizzare tutti gli ingredienti, ma la ricetta
        deve essere coerente e sensata.
        Rispondi esclusivamente in lingua italiana.
        Se non ci sono ingredienti, rispondi che non ci sono ingredienti
        per cucinare.
    """
    messages = [{"role": "user", "content": query}]

    response = client.chat.completions.parse(
        model="gemini-3-flash-preview",
        messages=messages,
        response_format=schemas.ReceipesResponse,
    )
    return response.choices[0].message.parsed
