from file_handler import save_recipes, load_recipes
recipes = []  # This will store all recipes

def show_menu():
    print("\n📖 Recipe Manager")
    print("1. Add a recipe")
    print("2. View all recipes")
    print("3. Exit")
    print("4. Delete")
    print("5. Search recipes")

recipes = load_recipes()

def add_recipe(recipes):
    name = input("Enter recipe name: ")
    ingredients = input("Enter ingredients (comma-separated): ")
    ingredients_list = [item.strip() for item in ingredients.split(",")]

    recipe = {
        "name": name,
        "ingredients": ingredients_list
    }

    recipes.append(recipe)
    save_recipes(recipes)
    print(f"✅ '{name}' added!\n")
    return recipes

def show_recipes(recipes):
    if len(recipes) == 0:
        print("⚠️ No recipes yet.")
    else:
        for idx, recipe in enumerate(recipes, start=1):
            print(f"\n{idx}. {recipe['name']}")
            print("   Ingredients:")
            for ing in recipe["ingredients"]:
                print(f"     - {ing}")
    return recipes

def delete_recipe(recipes_list):
    for index, rec in enumerate(recipes_list, start =1):
        print(f"{index}. {rec['name']}")
    idx_to_delete = int(input("Which recipe number would you like to delete? "))
    if (len(recipes_list) < idx_to_delete):
        idx_to_delete = input("Please choose a valid number")
    recipes_list.pop(idx_to_delete-1)
    save_recipes(recipes_list)
    print(f" The recipe {idx_to_delete} was deleted succesfully")
    print(f"\n {recipes_list}")

def search_recipes(recipes):
    search = input("Enter search terms: ")
    matched_recipes =  [recipe for recipe in recipes if search.lower() in recipe["name"].lower()]
    if not matched_recipes:
        print("No recipes found")
        return
    for recipe in matched_recipes:
        print(f"{recipe['name']}")
        print( " Ingredients: ")
        for i in recipe["ingredients"]:
            print(i)

while True:
    show_menu()
    choice = input("Choose an option (1–4): ")

    if choice == "1":
        add_recipe(recipes)
        
    elif choice == "2":
        show_recipes(recipes)
        
    elif choice == "4":
        delete_recipe(recipes)

    elif choice == "5":
        search_recipes(recipes)
        
    elif choice == "3":
        print("👋 Goodbye!")
        break
    else:
        print("❌ Invalid choice. Try again.")
