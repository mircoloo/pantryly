from dotenv import load_dotenv
load_dotenv()
from agents import Runner, Agent, function_tool
from .. import schemas
import httpx
import json
from typing import List

chat_agent = Agent(name="Chef Assistant", 
                   instructions="You are a helpful assistant which receives a list of products from the pantry and have to suggest  \
                   some receipe to the user, your language is Italian you must answer in this language. Use ONLY the products provided \
                       Do not ask to the user if has other ingredients. just use the one in the provided,. Furthermore ask product based on the expiration date\
                           so if they are almost to the deadline use those first ingredient", 
                   model="gpt-4o-mini",
                   )

async def process_request(request: schemas.AIChatRequest, products: List[schemas.Product]):

    
    products_data = [p.model_dump() for p in products]
    prompt_content = f"Domanda dell'utente: Creami una ricetta con i prodotti elencati: \n\n Ecco la lista dei prodotti disponibili in formato JSON:\n {json.dumps(products_data, indent=2)}"
    
    
    result = await Runner.run(
        chat_agent, 
        input=[
            {
                "role": "user",
                "content": prompt_content 
            }
        ]
    )
    
    return result.final_output