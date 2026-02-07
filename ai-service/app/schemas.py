from pydantic import BaseModel, Field
from datetime import date
from typing import List


class Product(BaseModel):
    name: str
    expiration_date: date
    barcode: str = Field(description="Il codice a barre del prodotto")
class Receipe(BaseModel):
    name: str = Field(description="Il nome della ricetta")
    dish_type: str = Field(description="Il tipo di piatto, se primo piatto dolce o altro")
    ingredients: List[Product] = Field(description="La lista degli ingredienti per la ricetta")
    receipe: str = Field(description="The various step to complete the receipe")
    
class ReceipesResponse(BaseModel):
    receipes: List[Receipe]

class AIChatRequest(BaseModel):
    request: str
    
class AIChatResponse(BaseModel):
    response: str

class CategorizedProduct(Product):
    category: str

class CategorizedProductsResponse(BaseModel):
    products: List[CategorizedProduct]
    

