from functools import lru_cache

from openai import OpenAI

from app.core.config import settings


API_KEY = settings.GOOGLE_API_KEY


@lru_cache(maxsize=1)
def get_agent_client() -> OpenAI:
    return OpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
