from pydantic import BaseModel, Field
from datetime import date
from typing import List
class Receipe(BaseModel):
    name: str = Field(description="The name of the receipe")
    dish_type: str = Field(description="Type of dish, if is a dessert or a first course etc")
    ingredients: List[str] = Field(description="A list of ingredients for the given receipe")
    receipe: str = Field(description="The various step to complete the receipe")




class AIChatRequest(BaseModel):
    request: str
    
class AIChatResponse(BaseModel):
    response: str
    
class Product(BaseModel):
    name: str
    expiration_date: date
    
class CategorizedProduct(Product):
    category: str