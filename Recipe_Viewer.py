import sys
import json
from urllib.parse import urlparse
import requests
from collections import namedtuple


class Recipe:
    def __init__(self, name, cookTime, prepTime, recipeYield, ingredients, description, image_url):
        self.name = name
        self.cookTime = cookTime
        self.prepTime = prepTime
        self.recipeYield = recipeYield
        self.ingredients = ingredients
        self.description = description
        self.image_url = image_url
        self.image_file = None

    # Get name of recipe
    def get_name(self):
        return self.name

    # Get and return cookTime for recipe in HH:MM format with leading zeros
    def get_cook_time(self):
        return self.format_time(self.cookTime)

    # Get and return prepTime for recipe in HH:MM format with leading zeros
    def get_prep_time(self):
        return self.format_time(self.prepTime)

    # Get and return recipeYield for a given recipe
    def get_recipe_yield(self):
        return self.recipeYield

    # Download image from web and display in the UI. An ACII-based progress bar must be displayed in the command line
    # as images are downloaded. This should include the index of the image downloaded (Ex: Downloading image 10 of xxx)
    def set_image(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                self.image_file = urlparse(url).path.split('/')[-1]
                with open(self.image_file, 'wb') as f:
                    f.write(response.content)
        except Exception as e:
            print("Error while downloading image", e)

    # Returns name of an image file for saving or displaying (saved images must have same name as url)
    def get_image(self):
        return self.image_file

    # Formats time to HH:MM
    def format_time(self, time):
        hours, minutes = divmod(time, 60)
        return f"{hours:02d}:{minutes:02d}"


class RecipeProcessor:
    def __init__(self):
        self.recipes = []
    def load_recipes(self, json_file):
        with open(json_file, encoding='utf-8') as f:
            data = json.load(f)
            for recipe_data in data:
                try:
                    recipe = Recipe(recipe_data['name'], recipe_data['description'], recipe_data['image'],
                                    recipe_data['recipeYield'], recipe_data['cookTime'], recipe_data['prepTime'],
                                    recipe_data['ingredients'])
                    self.recipes.append(recipe)
                except Exception as e:
                    print(f"Error loading recipe: {e}")

    def get_recipes(self):
        return self.recipes


def main():
    processor = RecipeProcessor()
    processor.load_recipes('recipes.json')


if __name__ == '__main__':
    main()
