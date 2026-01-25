from pydantic import BaseModel
from datetime import date



class AIChatRequest(BaseModel):
    request: str
    
class Product(BaseModel):
    name: str
    expiration_date: date