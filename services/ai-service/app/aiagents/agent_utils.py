"""
Utility condivise dagli agenti AI.

Configura il client OpenAI SDK puntando alle API di Google Gemini
(compatibilità OpenAI).

La chiave API viene caricata dalla variabile d'ambiente GOOGLE_API_KEY.
"""
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Chiave API per Google Gemini (via OpenAI-compatible endpoint)
google_api_key = os.getenv("GOOGLE_API_KEY", "")

# Client configurato per usare le API Gemini con l'SDK OpenAI
gemini_client = OpenAI(
    api_key=google_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
