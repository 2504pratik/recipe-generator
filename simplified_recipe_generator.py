import spacy
import json
import re
from typing import List, Dict, Any
from pathlib import Path

class SimpleRecipeGenerator:
    def __init__(self, recipe_data_path: str):
        """
        Initialize the Recipe Generator with recipe data and SpaCy model
        
        Args:
            recipe_data_path: Path to the recipe JSON data
        """
        # Load recipe data
        self.recipes = self._load_recipe_data(recipe_data_path)
        
        # Load SpaCy NLP model
        print("Loading SpaCy model...")
        try:
            self.nlp = spacy.load("en_core_web_md")
        except OSError:
            print("Downloading SpaCy model...")
            spacy.cli.download("en_core_web_md")
            self.nlp = spacy.load("en_core_web_md")
        
        # Create a list of all known ingredients
        self.all_ingredients = set()
        for recipe in self.recipes:
            for ingredient in recipe.get('ingredients', []):
                self.all_ingredients.add(ingredient['name'].lower())
    
    def _load_recipe_data(self, file_path: str) -> List[Dict[str, Any]]:
        """Load recipe data from JSON file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def extract_ingredients(self, query: str) -> List[str]:
        """Extract ingredients from user query"""
        query = query.lower()
        found_ingredients = []
        
        # Process with SpaCy
        doc = self.nlp(query)
        
        # Try to find ingredients from our known list
        for ingredient in self.all_ingredients:
            # Check for whole ingredient names
            if ingredient in query:
                found_ingredients.append(ingredient)
                continue
            
            # Check for ingredient words
            ingredient_words = ingredient.split()
            if len(ingredient_words) > 1:
                for word in ingredient_words:
                    if len(word) > 3 and word in query:  # Only consider significant words
                        found_ingredients.append(ingredient)
                        break
        
        # If no ingredients found, extract nouns as potential ingredients
        if not found_ingredients:
            for token in doc:
                if token.pos_ in ["NOUN", "PROPN"] and len(token.text) > 3:
                    found_ingredients.append(token.text)
        
        return list(set(found_ingredients))  # Remove duplicates
    
    def find_recipes_by_ingredients(self, ingredients: List[str], limit: int = 3) -> List[Dict[str, Any]]:
        """Find recipes that match the given ingredients"""
        matching_recipes = []
        
        # Convert ingredients to lowercase for case-insensitive matching
        ingredients = [ing.lower() for ing in ingredients]
        
        for recipe in self.recipes:
            # Get recipe ingredients
            recipe_ingredients = [ing['name'].lower() for ing in recipe.get('ingredients', [])]
            
            # Calculate matches
            matches = 0
            for ing in ingredients:
                # Check if the ingredient matches exactly or is contained within recipe ingredients
                for recipe_ing in recipe_ingredients:
                    if ing == recipe_ing or ing in recipe_ing or recipe_ing in ing:
                        matches += 1
                        break
            
            if matches > 0:
                matching_recipes.append({
                    'recipe': recipe,
                    'score': matches / len(ingredients)
                })
        
        # Sort by score (highest first) and return the recipes
        matching_recipes.sort(key=lambda x: x['score'], reverse=True)
        return [item['recipe'] for item in matching_recipes[:limit]]
    
    def generate_recipe(self, query: str) -> Dict[str, Any]:
        """Generate a recipe based on user query"""
        try:
            # Extract ingredients from query
            ingredients = self.extract_ingredients(query)
            
            if ingredients:
                recipes = self.find_recipes_by_ingredients(ingredients)
                if recipes:
                    return {'status': 'success', 'recipes': recipes}
                else:
                    return {'status': 'error', 'message': f"No recipes found with: {', '.join(ingredients)}"}
            else:
                return {'status': 'error', 'message': "No ingredients detected in your query"}
                
        except Exception as e:
            return {'status': 'error', 'message': f"Error generating recipe: {str(e)}"}