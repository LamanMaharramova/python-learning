import json

def load_recipes():
    try:
        with open("recipes.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    


def save_recipes(recipes):
    with open("recipes.json", "w") as file:
        json.dump(recipes, file, indent=2)
    print("recipe is saved succesfully")
