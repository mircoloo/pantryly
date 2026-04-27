from typing import Annotated

from fastapi import APIRouter, Depends
from openai import OpenAI

from app import schemas
from app.aiagents import create_receipe_agent
from app.aiagents.agent_utils import get_agent_client

router = APIRouter(
    prefix="/v1/ai",
    tags=["AI"],
)

@router.post("/suggest-receipe")
async def suggest_receipe(
    products: list[schemas.Product],
    client: Annotated[OpenAI, Depends(get_agent_client)],
):  
    return await create_receipe_agent(products, client)
    