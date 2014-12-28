#!/usr/bin/python
# book_reader.py
# Reads the books.template file and replaces the 
# all-capitals placeholders with the data from
# the books.txt file and a modal if there is 
# a corresponding review for this book

import sys

BOOK_LIST = 'books.txt'
TEMPLATE = 'templates/books.template'

# Used to encase each book title/author
OPEN = '<a href="#" class="list-group-item text-center" data-toggle="modal" data-target="#ofMiceAndMen">'
CLOSE = '</a>'

# Used to offset the author with smaller text
SM_OPEN = '<small>'
SM_CLOSE = '</small>'

# Finds heading in template and replaces it with the sublist
def replace(heading, sublist, template):

    # Build the string from the sublist that we want to use
    # to replace the heading in the template
    strlist = ''
    for pair in sublist:
        book, author = tuple(pair.split(", "))
        strlist += OPEN + book + " " + SM_OPEN + author + SM_CLOSE + CLOSE + '\n'


    # Replace the heading in the template with our list of book/auth elements
    i = template.index(heading)
    template[i] = strlist


def make_books():

    # Read in the book list and the template files
    with open(BOOK_LIST) as f:
        book_list = [x.strip() for x in f.readlines()]
    with open(TEMPLATE) as f:
        template = [x.strip() for x in f.readlines()]


    # Find each heading in the book list and its associated books
    # and substitute them into the template
    while len(book_list) > 0:

        i = 0
        heading = book_list[i].upper()

        # Get all the books fall under this heading as a sublist
        while i < len(book_list) and book_list[i] != '':
            i += 1

        sublist = book_list[1:i]
        replace(heading, sublist, template)

        book_list = book_list[i+1:]

    # Add the newlines back to the template file
    template = [x + '\n' for x in template]

    # Write the completed template to a file
    fo = open('books.gen.html', 'w+')
    fo.writelines(template)
    fo.close()

if __name__ == '__main__':
    make_books()
