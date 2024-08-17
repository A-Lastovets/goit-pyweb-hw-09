"""
This module performs operations related to JSON processing.

It includes reading, writing, and manipulating JSON data.
"""

import json
from mongoengine import connect
from models import Author, Quote

# Підключення до бази даних
connect(host='mongodb+srv://alastovets:8yqcQPghSOJWSYWo@clustera.jq75x.mongodb.net/')

# Завантаження авторів
def load_authors() -> None:
    """Loads author data from a JSON file and stores it in the database.

    This function reads the 'authors.json' file, checks if each author already
    exists in the database, and if not, creates a new record for the author
    with the provided details (full name, birth date, birth location, and
    description).

    Raises:
        FileNotFoundError: If the 'authors.json' file is not found.
        json.JSONDecodeError: If the JSON file contains invalid JSON.
    """

    with open('A:/Home_work/goit-pyweb-hw-09/test_spyder/authors.json', 'r', encoding='utf-8') as f:
        authors = json.load(f)
        for author in authors:
            if not Author.objects(fullname=author['fullname']).first():
                new_author = Author(
                    fullname=author['fullname'],
                    born_date=author.get('born_date', ''),
                    born_location=author.get('born_location', ''),
                    description=author.get('description', '')
                )
                new_author.save()
                print(f'Author: {new_author.fullname} created.')
            else:
                print(f'Author already exists: {author["fullname"]}')
# Завантаження цитат
def load_quotes() -> None:
    """Loads quote data from a JSON file and stores it in the database.

    This function reads the 'quotes.json' file, checks if the author of each
    quote exists in the database, and if so, creates a new record for the quote,
    associating it with the corresponding author.

    Raises:
        FileNotFoundError: If the 'quotes.json' file is not found.
        json.JSONDecodeError: If the JSON file contains invalid JSON.
        Exception: If an author is not found for a given quote.
    """
    with open('A:/Home_work/goit-pyweb-hw-09/test_spyder/quotes.json', 'r', encoding='utf-8') as f:
        quotes = json.load(f)
        for quote in quotes:
            author = Author.objects(fullname=quote['author']).first()
            if author:
                new_quote = Quote(
                    tags=quote.get('tags', []),
                    author=author,
                    quote=quote['quote']
                )
                new_quote.save()
                print(f'Quote: "{new_quote.quote}" by {new_quote.author.fullname} created.')
            else:
                print(f'Author not found for quote: "{quote["quote"]}"')

if __name__ == '__main__':
    load_authors()
    load_quotes()
