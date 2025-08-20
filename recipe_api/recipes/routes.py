from typing import List
from fastapi import APIRouter, HTTPException, Path, Query, status
from ..models import Recipe, Message
from ..data_handler import load_recipes, save_recipes

router = APIRouter()
recipes = load_recipes()

# -------------------- GET ALL RECIPES --------------------
@router.get("/recipes", response_model=List[Recipe], status_code=status.HTTP_200_OK)
def get_recipes():
    return recipes

# -------------------- ADD NEW RECIPE --------------------
@router.post("/recipes", response_model=Message, status_code=status.HTTP_201_CREATED)
def add_recipe(recipe: Recipe):
    if any(r["name"].lower() == recipe.name.lower() for r in recipes):
        raise HTTPException(status_code=400, detail="Recipe already exists")
    recipes.append(recipe.model_dump())
    save_recipes(recipes)
    return {"message": "Recipe added successfully"}

# -------------------- SEARCH RECIPES --------------------
@router.get("/recipes/search", response_model=List[Recipe], status_code=status.HTTP_200_OK)
def search_recipes(term: str = Query(..., description="Search by name", min_length=3)):
    matches = [recipe for recipe in recipes if term.lower() in recipe["name"].lower()]
    if not matches:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return matches

# -------------------- GET RECIPE BY NAME --------------------
@router.get("/recipes/{name}", response_model=Recipe, status_code=status.HTTP_200_OK)
def get_recipe(name: str = Path(..., min_length=3, max_length=50, description="Name of recipe")):
    name_lower = name.lower()
    for recipe in recipes:
        if recipe["name"].lower() == name_lower:
            return recipe
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")

# -------------------- DELETE RECIPE --------------------
@router.delete("/recipes/{name}", response_model=Message, status_code=status.HTTP_200_OK)
def delete_recipe(name: str = Path(..., min_length=3, max_length=50, description="Name of recipe")):
    name_lower = name.lower()
    for idx, recipe in enumerate(recipes):
        if recipe["name"].lower() == name_lower:
            recipes.pop(idx)
            save_recipes(recipes)
            return {"message": f"Deleted recipe '{name}'"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such recipe found")

# -------------------- UPDATE RECIPE --------------------
@router.put("/recipes/{name}", response_model=Message, status_code=status.HTTP_200_OK)
def update_recipe(name: str = Path(..., min_length=3, max_length=50, description="Name of recipe"),
                  updated_recipe: Recipe = ...):
    name_lower = name.lower()
    for idx, recipe in enumerate(recipes):
        if recipe["name"].lower() == name_lower:
            recipes[idx] = updated_recipe.model_dump()
            save_recipes(recipes)
            return {"message": f"Recipe '{name}' updated successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Recipe '{name}' not found")

@router.get("/recipes/filter", response_model=List[Recipe])
def filter_recipes(
    term: str = Query(..., min_length=3, description="Search term"),
    min_ingredients: int = Query(0, ge=0, description="Minimum number of ingredients")):
    filtered = [r for r in recipes 
                if term.lower() in r["name"].lower() or len(r["ingredients"]) >= min_ingredients
                ]
    if not filtered:
        raise HTTPException(status_code=404, detail="No recipes found")
    return filtered

