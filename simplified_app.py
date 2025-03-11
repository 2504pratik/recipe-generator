from simplified_recipe_generator import SimpleRecipeGenerator
import os

# Check if data directory exists, create if not
os.makedirs("data", exist_ok=True)

# Initialize the generator
generator = SimpleRecipeGenerator(recipe_data_path='data/recipes.json')

# Test the generator
print("\nRecipe Generator is ready!")
print("You can ask for recipes like:")
print("- 'What can I make with chicken?'")
print("- 'I have mushrooms and rice, what can I cook?'")
print("- 'Give me a recipe with salmon'")

while True:
    query = input("\nWhat would you like to cook? (or 'exit' to quit): ")
    if query.lower() == 'exit':
        break
        
    result = generator.generate_recipe(query)

    # Display results
    if result['status'] == 'success':
        for recipe in result['recipes']:
            print(f"\nRecipe: {recipe['name']}")
            print("Ingredients:")
            for ing in recipe['ingredients']:
                print(f"- {ing['amount']} {ing['name']}")
            print("\nInstructions:")
            for i, step in enumerate(recipe['instructions'], 1):
                print(f"{i}. {step}")
    else:
        print(f"Error: {result['message']}")