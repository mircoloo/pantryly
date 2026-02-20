"""
Agente AI per la categorizzazione dei prodotti.

Riceve una lista di prodotti e chiede al modello Gemini
di assegnare una categoria semantica a ciascuno.
"""
import json
from typing import List

from .. import schemas
from .agent_utils import gemini_client


async def create_categorization_products_agent(
    products: List[dict],
) -> schemas.CategorizedProductsResponse:
    """
    Categorizza i prodotti usando Gemini.

    Usa il response_format di OpenAI SDK per ottenere una risposta
    strutturata e validata dallo schema Pydantic.
    """
    query = (
        f"Given the ingredients given here: {json.dumps(products, indent=2)} "
        "give a category at each product and return the same but with the category"
    )
    messages = [{"role": "user", "content": query}]

    response = gemini_client.chat.completions.parse(
        model="gemini-3-flash-preview",
        messages=messages,
        response_format=schemas.CategorizedProductsResponse,
    )
    return response.choices[0].message.parsed
