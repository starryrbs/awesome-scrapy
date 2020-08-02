import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose
from w3lib.html import strip_html5_whitespace, remove_tags, replace_entities, remove_comments, replace_escape_chars

from fang_news.item_loaders import format_date, filter_invalid_url


class CityItem(scrapy.Item):
    city = scrapy.Field(
        output_processor=TakeFirst(),
    )
    domain = scrapy.Field(
        output_processor=TakeFirst(),
    )


class NewsItem(scrapy.Item):
    release_time = scrapy.Field(
        input_processor=MapCompose(format_date),
        output_processor=TakeFirst(),
    )
    title = scrapy.Field(
        input_processor=MapCompose(remove_tags, strip_html5_whitespace, replace_entities),
        output_processor=TakeFirst(),
    )
    url = scrapy.Field(
        output_processor=TakeFirst(),
    )
    thumbnail = scrapy.Field(
        input_processor=MapCompose(filter_invalid_url)
    )


class DetailItem(scrapy.Item):
    url = scrapy.Field(
        output_processor=TakeFirst(),
    )

    content = scrapy.Field(
        input_processor=MapCompose(replace_escape_chars, strip_html5_whitespace, replace_entities, remove_comments),
        output_processor=TakeFirst(),
    )

    keywords = scrapy.Field(
        input_processor=MapCompose(remove_tags, strip_html5_whitespace, replace_entities),
    )


