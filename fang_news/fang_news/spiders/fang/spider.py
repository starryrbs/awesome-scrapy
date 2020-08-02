from itemadapter import ItemAdapter
from scrapy import Spider
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst
from scrapy.utils.url import add_http_if_no_scheme

from fang_news.items import NewsItem, CityItem, DetailItem

DEFAULT_REQUEST_HEADERS = {
    'authority': 'sh.news.fang.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'zh-CN,zh;q=0.9',
}

DEFAULT_SPIDER_SETTINGS = {
    'DEFAULT_REQUEST_HEADERS': DEFAULT_REQUEST_HEADERS
}


class FangCitySpider(Spider):
    name = "fang_city_spider"

    start_urls = ['https://www.fang.com/SoufunFamily.htm']

    custom_settings = DEFAULT_SPIDER_SETTINGS

    def parse(self, response):
        cities_element = response.xpath('//table[@id="senfe1"]//td/a')
        for city_element in cities_element:
            loader = ItemLoader(item=CityItem(), selector=city_element)
            loader.add_xpath('city', './text()', TakeFirst())
            loader.add_xpath('domain', './@href', re=r'://(.+?)\.')
            item = loader.load_item()
            print(item)


class FangListSpider(Spider):
    name = "fang_list_spider"

    start_urls = []

    custom_settings = DEFAULT_SPIDER_SETTINGS

    new_page_url_template = 'https://{domain}news.fang.com/gdxw.html'

    def __init__(self, **kwargs):
        super(FangListSpider, self).__init__(**kwargs)
        self.domain = kwargs['domain']
        # 北京做特殊处理
        self.start_urls = [self.new_page_url_template.format(domain='' if self.domain == 'bj' else self.domain + '.')]

    def parse(self, response):
        news_container_element = response.xpath('//div[@class="infoBox-item clearfix"]')
        for news_element in news_container_element:
            loader = ItemLoader(item=NewsItem(), selector=news_element)
            loader.add_xpath('release_time', './/div[@class="comment clearfix"]/span[2]/text()')
            loader.add_xpath('title', './/h3/a')
            loader.add_xpath('thumbnail', './/img/@src')
            href = news_element.xpath('.//h3/a/@href').get()
            loader.add_value('url', href, MapCompose(add_http_if_no_scheme))
            item = loader.load_item()
            res = ItemAdapter(item).asdict()
            print(res)


class FangDetailSpider(Spider):
    name = 'fang_detail_spider'

    custom_settings = DEFAULT_SPIDER_SETTINGS

    def __init__(self, **kwargs):
        super(FangDetailSpider, self).__init__(**kwargs)
        self.start_urls = kwargs['start_urls']

    def parse(self, response):
        loader = ItemLoader(item=DetailItem(), selector=response)
        loader.add_value('url', response.request.url)
        loader.add_xpath('content', '//div[@class="news-text"]')
        loader.add_xpath('keywords', '//div[@class="tagBox clearfix"]/a[position()>1]')
        item = loader.load_item()
        res = ItemAdapter(item).asdict()

