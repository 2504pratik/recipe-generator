import os
import pandas as pd
from rasa_sdk import Action

# Define the correct path to the CSV file
FILE_PATH = os.path.join(os.path.dirname(__file__), "../data/cleaned_indian_recipes.csv")

class ActionFindRecipe(Action):
    def name(self):
        return "action_find_recipe"

    def run(self, dispatcher, tracker, domain):
        user_message = tracker.latest_message.get("text").lower()

        # Ensure file exists
        if not os.path.exists(FILE_PATH):
            dispatcher.utter_message(text="Error: Recipe dataset not found.")
            return []

        # Load the CSV
        df = pd.read_csv(FILE_PATH)

        # Find matching recipes based on ingredients mentioned
        found_recipes = []
        for _, row in df.iterrows():
            ingredients = str(row["ingredients"]).lower()
            if any(word in user_message for word in ingredients.split()):
                found_recipes.append(row["dish_name"])

        # Create response message
        if found_recipes:
            response = f"Here are some recipes you might like: {', '.join(found_recipes)}"
        else:
            response = "Sorry, I couldn't find a recipe with those ingredients."

        dispatcher.utter_message(text=response)
        return []

class ActionListIngredients(Action):
    def name(self):
        return "action_list_ingredients"

    def run(self, dispatcher, tracker, domain):
        user_message = tracker.latest_message.get("text").lower()

        # Ensure file exists
        if not os.path.exists(FILE_PATH):
            dispatcher.utter_message(text="Error: Recipe dataset not found.")
            return []

        # Load the CSV
        df = pd.read_csv(FILE_PATH)

        # Search for the recipe by name
        for _, row in df.iterrows():
            if row["dish_name"].lower() in user_message:
                ingredients = row["ingredients"].replace("\n", ", ")
                response = f"The ingredients for {row['dish_name']} are: {ingredients}"
                dispatcher.utter_message(text=response)
                return []

        dispatcher.utter_message(text="I couldn't find that recipe.")
        return []