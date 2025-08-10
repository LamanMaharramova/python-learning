from pydantic import BaseModel

class Recipes(BaseModel):
    name: str
    ingredients: list[str]

class Message(BaseModel):
    message: str