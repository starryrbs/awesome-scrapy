import json
from datetime import datetime

from scrapy import Spider, Request
from scrapy.loader import ItemLoader
from scrapy.utils.project import get_project_settings
from w3lib.url import add_or_replace_parameters, url_query_parameter

from fang_news.items import NewsItem

PAGE_KEY = 'page'
TYPE_KEY = 'type'

NEWS_LIST_URL = 'https://sh.news.anjuke.com/toutiao/ajax/toutiaoajax/'

settings = get_project_settings()


class AnJuKeListSpider(Spider):
    name = "anjuke_list_spider"

    start_urls = [add_or_replace_parameters(NEWS_LIST_URL, {PAGE_KEY: 1, TYPE_KEY: 2})]

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'authority': 'sh.news.anjuke.com',
            'accept': '*/*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://sh.news.anjuke.com/?from=navigation',
            'accept-language': 'zh-CN,zh;q=0.9',
        },
        'DOWNLOAD_DELAY': 2
    }

    def parse(self, response):

        result = json.loads(response.text)
        news_list = result['list']
        release_time = None
        if news_list:
            for news_item in news_list:
                loader = ItemLoader(item=NewsItem())
                loader.add_value('release_time', news_item['time'])
                loader.add_value('title', news_item['title'])
                loader.add_value('url', news_item['url'])
                loader.add_value('thumbnail', news_item['image_url'])
                item = loader.load_item()
                release_time = item['release_time']
                print(item)
            else:
                if isinstance(release_time, datetime) \
                        and (datetime.now() - release_time).days < settings['MAX_CRAWLED_DAYS']:
                    page = url_query_parameter(response.url, PAGE_KEY)
                    page = int(page) + 1
                    next_page_url = add_or_replace_parameters(response.url, {PAGE_KEY: page})
                    # yield Request(url=next_page_url, callback=self.parse)
