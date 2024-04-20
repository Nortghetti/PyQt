import sys
import json
from urllib.parse import urlparse
from collections import namedtuple
import re
import requests
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap


class Recipe:
    def __init__(self, name, description, image, recipeYield, cookTime, prepTime, ingredients):
        self.name = name

        cook_match = re.match(r'PT(\d+)M', cookTime)
        if cook_match:
            self.cookTime = int(cook_match.group(1))
        else:
            self.cookTime = 0

        prep_match = re.match(r'PT(\d+)M', prepTime)
        if prep_match:
            self.prepTime = int(prep_match.group(1))
        else:
            self.prepTime = 0

        self.recipeYield = recipeYield
        self.ingredients = ingredients
        self.description = description
        self.image_file = image

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
    
class RecipeUi(QDialog):
    def __init__(self, height, width, recipes):
        super().__init__()
        self.height = height
        self.width = width
        self.recipes = recipes
        self.page = 0
        self.per_page = 4
        self.setup_window()

    def setup_window(self):
        self.setWindowTitle("Recipes")
        self.setFixedSize(QSize(self.width, self.height))
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.layout_ui()

    def layout_ui(self):
        start_index = self.page * self.per_page
        end_index = min((self.page + 1) * self.per_page, len(self.recipes))

        for i, recipe_index in enumerate(range(start_index, end_index)):
            recipe = self.recipes[recipe_index]
            group_box = QGroupBox()
            group_box.setFixedSize(QSize(int(self.width/2), int(self.height/2)))
            group_layout = QVBoxLayout(group_box)
            number_label = QLabel(f"Recipe #: {recipe_index}")
            name_label = QLabel(f"Name: {recipe.get_name()}")
            cook_label = QLabel(f"Cook Time: {recipe.get_cook_time()}")
            prep_label = QLabel(f"Prep Time: {recipe.get_prep_time()}")

            view_button = QPushButton("View Recipe")
            #view_button.clicked.connect() #show the recipe

            #donwload images
            recipe.set_image(recipe.get_image())

            image_label = QLabel()
            pixmap = QPixmap(recipe.get_image())
            image_label.setPixmap(pixmap.scaledToWidth(int(self.width/2)))

            group_layout.addWidget(image_label)

            group_layout.addWidget(number_label)
            group_layout.addWidget(name_label)
            group_layout.addWidget(cook_label)
            group_layout.addWidget(prep_label)
            group_layout.addWidget(view_button)
            self.layout.addWidget(group_box, i//2, i%2)

    def next():
        ###called when the user clicks the next button. This method should get the next set of recipes in the list and update the UI with new information
        ()
    def previous():
        ###called when the user clicks the previous button. This method should get the previous set of recipes in the list and update the UI with new information
        ()
    def first():
        ### jumps to the beginning of the list of recipes and shows the first set in the UI based on the selected numberper page value
        ()
    def last():
         ###jumps to the end of the list of recipes and shows the last set in the UI based on the selected number per page value
        ()
    def search(recipe_keywords):
        ###searches the recipe list for recipes whose name, ingredients, or description contains the user-supplied string. The next, previous, first, and last buttons should also be used to navigate the search results when the user submits a search query.
        ()
    def reset():
        ###clears the search results and returns to normal pagination of the list of recipes
        ()
    



def main():
    processor = RecipeProcessor()
    processor.load_recipes('recipes.json')

    app = QApplication(sys.argv)
    recipes = processor.get_recipes()
    window = RecipeUi(400, 600, recipes)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
