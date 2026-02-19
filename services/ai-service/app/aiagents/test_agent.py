from dotenv import load_dotenv
load_dotenv()
from agents import Runner, Agent, function_tool
from .. import schemas
import httpx
import json
from typing import List
from openai import OpenAI
import os
from .agent_utils import gemini_client

async def get_response_chat(request_text: str):
    messages = [{"role": "user", "content": request_text}]
    response = gemini_client.chat.completions.parse(
        model="gemini-3-flash-preview",
        messages=messages,
        response_format=schemas.AIChatResponse
    )
    return response.choices[0].message.parsed
    
