import os
import pandas as pd
from rasa_sdk import Action

# Define the dataset file path
FILE_PATH = os.path.join(os.path.dirname(__file__), "../data/cleaned_indian_recipes.csv")

class ActionListIngredients(Action):
    def name(self):
        return "action_list_ingredients"

    def run(self, dispatcher, tracker, domain):
        user_message = tracker.latest_message.get("text").lower()
        
        if not os.path.exists(FILE_PATH):
            dispatcher.utter_message(text="Error: Recipe dataset not found.")
            return []

        df = pd.read_csv(FILE_PATH)

        for _, row in df.iterrows():
            if row["dish_name"].lower() in user_message:
                ingredients = row["ingredients"].replace("\n", ", ")
                response = f"The ingredients for {row['dish_name']} are: {ingredients}"
                dispatcher.utter_message(text=response)
                return []

        dispatcher.utter_message(text="I couldn't find that recipe.")
        return []

class ActionListInstructions(Action):
    def name(self):
        return "action_list_instructions"

    def run(self, dispatcher, tracker, domain):
        user_message = tracker.latest_message.get("text").lower()

        if not os.path.exists(FILE_PATH):
            dispatcher.utter_message(text="Error: Recipe dataset not found.")
            return []

        df = pd.read_csv(FILE_PATH)

        for _, row in df.iterrows():
            if row["dish_name"].lower() in user_message:
                instructions = row["instructions"].replace("\n", " ")
                response = f"Here are the instructions to make {row['dish_name']}: {instructions}"
                dispatcher.utter_message(text=response)
                return []

        dispatcher.utter_message(text="I couldn't find that recipe.")
        return []