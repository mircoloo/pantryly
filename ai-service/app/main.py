from fastapi import FastAPI
from .aiagents.test_agent import process_request
from . import schemas
import httpx
app = FastAPI()


@app.get("/")
def test_endpoint():
    return "OK"

@app.post("/chat")
async def chat_request(request: schemas.AIChatRequest):
    return await process_request(request)
