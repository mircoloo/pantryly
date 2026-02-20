"""
Agente AI per la chat libera.

Riceve un messaggio di testo e restituisce la risposta del modello Gemini.
"""
from .. import schemas
from .agent_utils import gemini_client


async def get_response_chat(request_text: str) -> schemas.AIChatResponse:
    """
    Chat generica con l'assistente AI.
    Usa response_format per ottenere una risposta strutturata.
    """
    messages = [{"role": "user", "content": request_text}]

    response = gemini_client.chat.completions.parse(
        model="gemini-3-flash-preview",
        messages=messages,
        response_format=schemas.AIChatResponse,
    )
    return response.choices[0].message.parsed

