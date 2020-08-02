from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from twisted.internet import defer

from fang_news.spiders.anjuke.pider import AnJuKeListSpider
from fang_news.spiders.fang.spider import FangListSpider, FangCitySpider, FangDetailSpider

process = CrawlerProcess(get_project_settings())


@defer.inlineCallbacks
def crawl_anjuke():
    yield process.crawl(AnJuKeListSpider)
    yield process.crawl(FangListSpider)


@defer.inlineCallbacks
def crawl_fang():
    # yield process.crawl(FangCitySpider)
    # for domain in ['sh',]:
    #     yield process.crawl(FangListSpider, **{'domain': domain})
    yield process.crawl(FangDetailSpider, **{
        'start_urls': ['https://sh.news.fang.com/open/36844181.html']
    })


if __name__ == '__main__':
    # crawl_anjuke()
    crawl_fang()
    process.start()
