#!/usr/bin/python
# book_reader.py
# Reads the books.template file and replaces the 
# all-capitals placeholders with the data from
# the books.txt file and a modal if there is 
# a corresponding review for this book which
# can be found in reviews.txt

''' books.txt file format
Header                  - The first line gets turned into a top level accordion tab
Reviewed, Title, Author - Subsequent lines are interpreted as CSV
Reviewed, Title, Author - Reviewed is boolean, "N" or "Y" if book was reviewed
Reviewed, Title, Author - Title is the title of the book
Reviewed, Title, Author - Author is the author of the book
                        - An empty line indicating the end of this accordion tab 
(Repeat as for all accordion tabs)
'''

''' reviews.txt file format
Title, Author           - The title and the author of the book being reviewed
RTitle                  - The title of the review
Review                  - All of the text of the review
                        - An empty line indicating the end of this review
(Repeat for all reviews)
'''

import sys

BOOK_LIST = 'books.txt'
BOOK_REVIEWS = 'reviews.txt'
TEMPLATE = 'templates/books.template'

# For books with a review, use modal 
HAS_REVIEW_OPEN = '<a href="#" class="list-group-item text-center" data-toggle="modal" data-target="#{}">'
HAS_REVIEW_CLOSE = '</a>'

# For books without a review, don't use modal
NO_REVIEW_OPEN = '<div class="list-group-item text-center">'
NO_REVIEW_CLOSE = '</div>'

# Used to offset the author with smaller text
SM_OPEN = '<small>'
SM_CLOSE = '</small>'

# Finds heading in template and replaces it with the sublist
# Retuns a list of books that have reviews 
def replace_accordion(heading, sublist, template):

    # Build the string from the sublist that we want to use
    # to replace the heading in the template
    strlist = ''

    for item in sublist:

        read, title, author = tuple(item.split(", "))

        # If the book has no review, don't link to a modal
        if read == 'N':
            strlist += NO_REVIEW_OPEN
        else:
            # Strip strings of whitespace to match modal
            # for use as modal identifiers, for example
            # Of Mice And Men -----> OfMiceAndMen
            title_target = "".join(title.split())
            strlist += HAS_REVIEW_OPEN.format(title_target)

        strlist += title + " " + SM_OPEN + author + SM_CLOSE 

        # If the book has no review, don't link to a modal
        if read == 'N':
            strlist += NO_REVIEW_CLOSE
        else:
            strlist += HAS_REVIEW_CLOSE

    # Replace the heading in the template with our list of book/auth elements
    i = template.index(heading)
    template[i] = strlist

# Go through the list of books that have reviews
# and extract their reviews from reviews.txt
# and place them in their modals
def replace_reviews(template):

    with open(BOOK_REVIEWS) as f:
        reviews = [x.strip() for x in f.readlines()]

    # Substitute each review into its appropriate place in the modal 
    while len(reviews) > 0:

        book_title, author = tuple(reviews[0].split(", "))

        review_title = reviews[1]

        # Get the review body which is of arbitrary length
        i = 2
        body = ""
        while i < len(reviews) and reviews[i] != '':
            body += reviews[i]
            i += 1

        # Update reviews so on the next iteration we
        # are looking at the next book review entry
        reviews = reviews[i+1:]

        # The key into the template is the 
        # full capitalizion of the 
        # book title, for example
        # Of Mice and Men -----> OF MICE AND MEN
        key = book_title.upper()

        # Replace the modal title with the review title
        i = template.index(key)
        template[i] = review_title

        # Replace the modal body with the review content
        i = template.index(key)
        template[i] = body

        # Replace the modal footer with the title, author
        i = template.index(key)
        template[i] = book_title + " " + SM_OPEN + author + SM_CLOSE


def make_book_page():

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
        replace_accordion(heading, sublist, template)

        book_list = book_list[i+1:]

    # Add the book review text into their modals
    replace_reviews(template)

    # Add the newlines back to the template file
    template = [x + '\n' for x in template]

    # Write the completed template to a file
    fo = open('books.gen.html', 'w+')
    fo.writelines(template)
    fo.close()

if __name__ == '__main__':
    make_book_page()
