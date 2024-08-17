from models import Author, Quote

def search_quotes_by_author(author_name):
    author = Author.objects(fullname=author_name).first()
    if author:
        quotes = Quote.objects(author=author)
        return quotes
    return []

def search_quotes_by_tag(tag):
    quotes = Quote.objects(tags=tag)
    return quotes

def search_quotes_by_tags(tags):
    tags_list = tags.split(',')
    quotes = Quote.objects(tags__in=tags_list)
    return quotes

def main():
    while True:
        command = input("Enter command: ").strip()
        if command.startswith("name: "):
            author_name = command.split("name: ")[1].strip()
            quotes = search_quotes_by_author(author_name)
            for quote in quotes:
                print(quote.quote)
        elif command.startswith("tag: "):
            tag = command.split("tag: ")[1].strip()
            quotes = search_quotes_by_tag(tag)
            for quote in quotes:
                print(quote.quote)
        elif command.startswith("tags: "):
            tags = command.split("tags: ")[1].strip()
            quotes = search_quotes_by_tags(tags)
            for quote in quotes:
                print(quote.quote)
        elif command == "exit":
            break

if __name__ == "__main__":
    main()