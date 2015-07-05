#!/usr/bin/python
# recipe_page_maker.py
# Make the index.html page containing
# the list of recipes

from os import listdir

# Make sure to run this script from the base directory
# /Users/Mike/workspace/mike so the relative path below works
PATH = "recipes"

# Write out to the index.html file of the recipes directory
OUT_FILE = PATH + "/index.html"

# Each line of the file is a link to the recipe
LINK_LINE = '<a href="{}"> {} </a><br>'

# Open the file we are writing to, then make the link html
fo = open(OUT_FILE, "w+")
recipes = listdir(PATH)
links = [LINK_LINE.format(recipe, recipe) + '\n' for recipe in recipes]

# Write to and close the file
fo.writelines(links)
fo.close()
