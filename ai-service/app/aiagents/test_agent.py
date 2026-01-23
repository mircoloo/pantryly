from dotenv import load_dotenv
load_dotenv()
from agents import Runner, Agent, function_tool
from .. import schemas
import httpx
import json

chat_agent = Agent(name="Chef Assistant", 
                   instructions="You are a helpful assistant which receives a list of products from the pantry and have to suggest  \
                   some receipe to the user, your language is Italian you must answer in this language. Use ONLY the products provided \
                       Do not ask to the user if has other ingredients. just use the one in the provided,. Furthermore ask product based on the expiration date\
                           so if they are almost to the deadline use those first ingredient", 
                   model="gpt-4o-mini",
                   )

products = [
                {"name":"nutella","barcode":"3017620422003","expiration_date":"2026-01-22"},
                {"name":"tonno rio mare","barcode":"8004030103818","expiration_date":"2026-01-23"},
                {"name":"pasta barilla","barcode":"076808280081","expiration_date":"2026-01-23"},
                {"name":"avocado coop","barcode":"8001120737335","expiration_date":"2026-01-23"},
            ]

async def process_request(request: schemas.AIChatRequest):
    result = await Runner.run(chat_agent, 
                              input=[
                                        {
                                            "role": "user",
                                            "content": [
                                                {
                                                    "type": "input_text",
                                                    "text": json.dumps(products, indent=2)
                                                }]
                                        }
                                    ]
                            )
    return result.final_output
