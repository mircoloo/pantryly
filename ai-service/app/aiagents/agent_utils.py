from dotenv import load_dotenv
load_dotenv()
from agents import Runner, Agent, function_tool
import httpx
import json
from typing import List
from openai import OpenAI
import os

google_api_key = os.getenv('GOOGLE_API_KEY')

gemini_client = OpenAI(api_key=google_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")