from typing import List
from fastapi import APIRouter, HTTPException, Query, status
from ..models import Recipes, Message
from ..data_handler import load_recipes, save_recipes

router = APIRouter()
recipes = load_recipes()

@router.get("/recipes", response_model = List[Recipes])
def get_recipes():
    return  recipes

@router.post("/recipes",  response_model = Recipes, status_code=status.HTTP_201_CREATED)
def add_recipes(recipe: Recipes):
    recipes.append(recipe.model_dump())
    save_recipes(recipes)
    return recipe

@router.get("/recipes/search")
def search_recipes(term: str = Query(..., description="Search by name", min_length=3)):
    matches = [recipe for recipe in recipes if term.lower() in recipe["name"].lower()]
    return {"results": matches} if matches else {"message": "No matching recipe found"}

@router.delete("/recipes/{name}", response_model=Message, status_code=status.HTTP_200_OK)
def delete_recipe(name: str):
    for idx, recipe in enumerate(recipes):
        if recipe["name"].lower() == name:
            recipes.pop(idx)
            save_recipes(recipes)
            return {"message": f"Delete recipe for {name}"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such recipe found")

@router.put("/recipes/{name}", response_model=Message)
def update_recipe(name: str, updated_recipe: Recipes):
    for idx, recipe in enumerate(recipes):
        if recipe["name"].lower() == name.lower():
            recipes[idx] = updated_recipe.model_dump()
            save_recipes(recipes)
            return {"message": f"Recipe for {name} was updated succesfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Recipe {name} not found")
