# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from test_spyder.items import AuthorItem, QuoteItem

class QuotesScraperPipeline:
    def open_spider(self, spider):
        self.quotes_file = open('quotes.json', 'w', encoding='utf-8')
        self.authors_file = open('authors.json', 'w', encoding='utf-8')
        self.quotes_file.write('[\n')
        self.authors_file.write('[\n')
        self.first_quote = True
        self.first_author = True
        self.authors_set = set()

    def close_spider(self, spider):
        self.quotes_file.write('\n]')
        self.authors_file.write('\n]')
        self.quotes_file.close()
        self.authors_file.close()

    def process_item(self, item, spider):
        if isinstance(item, QuoteItem):
            if not self.first_quote:
                self.quotes_file.write(',\n')
            json.dump(dict(item), self.quotes_file, ensure_ascii=False, indent=2)
            self.first_quote = False
        elif isinstance(item, AuthorItem):
            if item['fullname'] not in self.authors_set:
                self.authors_set.add(item['fullname'])
                if not self.first_author:
                    self.authors_file.write(',\n')
                json.dump(dict(item), self.authors_file, ensure_ascii=False, indent=2)
                self.first_author = False
        return item