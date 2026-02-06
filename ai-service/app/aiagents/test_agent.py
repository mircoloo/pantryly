from dotenv import load_dotenv
load_dotenv()
from agents import Runner, Agent, function_tool
from .. import schemas
import httpx
import json
from typing import List
from openai import OpenAI
import os

google_api_key = os.getenv('GOOGLE_API_KEY')

gemini = OpenAI(api_key=google_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")



# chat_agent = Agent(name="Chef Assistant", 
#                    instructions="You are a helpful assistant which receives a list of products from the pantry and have to suggest  \
#                    some receipe to the user, your language is Italian you must answer in this language. Use ONLY the products provided \
#                        Do not ask to the user if has other ingredients. just use the one in the provided,. Furthermore ask product based on the expiration date\
#                            so if they are almost to the deadline use those first ingredient. Devi ritornare gli ingredienti da utilizzare, e la ricetta. Inoltre il nome della ricetta e il tipo di piatto (se dolce, primo piatto etc \
#                             Puoi ritornare anche una lista di ricette se ti va in modo da dare più idee se le hai", 
#                    model="gpt-4o-mini",
#                    output_type=List[schemas.Receipe]
#                    )

# categorization_product = Agent(name="Categorizzatore di prodotti", 
#                    instructions="Sei un agente che deve categorizzare i vari prodotti in modo che siano ben organizzati da mostrare all'utente in maniera chiara. \
#                        Per esempio prodotti per la colazione, per il bagno, per i primi piatti etc", 
#                    model="gpt-4o-mini",
#                    output_type=List[schemas.CategorizedProduct]
#                    )


async def process_get_categorized_products(products: List[schemas.Product]):
    query: str = f"Given the ingredients given here: {json.dumps(products, indent=2)} give a category at each product and return the same but with the category"
    messages = [{"role": "user", "content": query}]
    
    response = gemini.chat.completions.parse(
        model="gemini-3-flash-preview",
        messages=messages,
        response_format=schemas.CategorizedProductsResponse
    )
    # If using response_format, the returned object is already your model
    return response.choices[0].message.parsed
    return result.final_output

async def process_request(products : List[schemas.Product]):
    query: str = f"Given the ingredients given here: {json.dumps(products, indent=2)} suggest a nice and delicious receipe, is not necessary to use all the ingredients, the receipe has to have some sense. Respond in language Italian."
    messages = [{"role": "user", "content": query}]
    response = gemini.chat.completions.parse(
        model="gemini-3-flash-preview",
        messages=messages,
        response_format=schemas.ReceipesResponse
    )
    # If using response_format, the returned object is already your model
    return response.choices[0].message.parsed

async def get_response_chat(request_text: str):
    print(request_text)
    messages = [{"role": "user", "content": request_text}]
    response = gemini.chat.completions.parse(
        model="gemini-3-flash-preview",
        messages=messages,
        response_format=schemas.AIChatResponse
    )
    # If using response_format, the returned object is already your model
    return response.choices[0].message.parsed
    
