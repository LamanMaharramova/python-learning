import json
from typing import List, Dict

FILEPATH = "recipes.json"

def load_recipes() -> List[Dict]:
    try:
        with open(FILEPATH, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    
def save_recipes(recipes: List[Dict]):
    with open(FILEPATH, "w") as file:
        json.dump(recipes, file, indent=4)
