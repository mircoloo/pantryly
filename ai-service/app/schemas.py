from pydantic import BaseModel



class AIChatRequest(BaseModel):
    request: str