"""
Define here the models for your scraped items

See documentation in:
https://docs.scrapy.org/en/latest/topics/items.html
"""
import scrapy

from test_spyder.items import QuoteItem, AuthorItem

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        for quote in response.css("div.quote"):
            quote_text = quote.css("span.text::text").get().strip()
            author_name = quote.css("small.author::text").get().strip()
            tags = quote.css("div.tags a.tag::text").getall()

            # Yield quote data
            yield QuoteItem(
                quote=quote_text,
                author=author_name,
                tags=tags
            )

            # Follow link to author page
            author_page = quote.css("span a::attr(href)").get()
            if author_page:
                yield response.follow(author_page, callback=self.parse_author)

        # Follow pagination link
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_author(self, response):
        name = response.css("h3.author-title::text").get().strip()
        born_date = response.css("span.author-born-date::text").get().strip()
        born_location = response.css("span.author-born-location::text").get().strip()
        description = response.css("div.author-description::text").get().strip()

        yield AuthorItem(
            fullname=name,
            born_date=born_date,
            born_location=born_location,
            description=description
        )
