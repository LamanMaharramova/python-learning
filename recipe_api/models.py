from pydantic import BaseModel

class Recipe(BaseModel):
    name: str
    ingredients: list[str]

class Message(BaseModel):
    message: str