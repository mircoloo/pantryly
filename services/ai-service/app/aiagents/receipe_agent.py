"""
Agente AI per la generazione di ricette.

Riceve la lista di prodotti/ingredienti dall'inventario
e genera suggerimenti di ricette usando Gemini.
"""
import json
from typing import List

from .. import schemas
from .agent_utils import gemini_client


async def create_receipe_agent(
    products: List[dict],
) -> schemas.ReceipesResponse:
    """
    Genera ricette basate sugli ingredienti disponibili.

    Il prompt specifica che non tutti gli ingredienti devono essere usati,
    e che la risposta deve essere in italiano.
    """
    query = f"""
        Dati i seguenti ingredienti:
        {json.dumps(products, indent=2)}

        Suggerisci una o più ricette gustose e ben bilanciate.
        Non è necessario utilizzare tutti gli ingredienti, ma la ricetta
        deve essere coerente e sensata.
        Rispondi esclusivamente in lingua italiana.
        Se non ci sono ingredienti, rispondi che non ci sono ingredienti
        per cucinare.
    """
    messages = [{"role": "user", "content": query}]

    response = gemini_client.chat.completions.parse(
        model="gemini-3-flash-preview",
        messages=messages,
        response_format=schemas.ReceipesResponse,
    )
    return response.choices[0].message.parsed
