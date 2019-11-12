#!/usr/bin/env python3
# recipe_page_maker.py
# Make the index.html page containing
# the list of recipes

from os import listdir

# Make sure to run this script from the base directory
# /Users/Mike/workspace/mike so the relative path below works

RECIPE_PATH = "recipes"
TEMPLATE = "templates/recipes.template"
OUT_FILE = "recipes/recipes.gen.html"
START_FLAG = "RECIPES"

# Each line of the file is a link to the recipe
LINK_LINE = '<li class="recipe"> <a href="{}"> {} </a> </li>'

# Build the links using the .rtf resource names in the /recipes/
# directory since the .rtf extension indicates a recipe
recipes = listdir(RECIPE_PATH)
links = sorted([LINK_LINE.format(x, x) for x in recipes
                if x.endswith('rtf') or x.endswith('txt')])

# Open and read the template file
with open(TEMPLATE) as f:
    template = [x.strip() for x in f.readlines()]

# Replace the recipe flag in the template with our recipe content
i = template.index(START_FLAG)
template.pop(i)
template[i:i] = links

for x in template:
    print(x)
# Add the newlines back to the template file
template = [x + '\n' for x in template]

# Open and write to the output file
fo = open(OUT_FILE, "w+")
fo.writelines(template)
fo.close()
