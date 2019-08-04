from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from boss_job.spiders.job_detail import JobDetailSpider

process = CrawlerProcess(settings=get_project_settings())
process.crawl(JobDetailSpider)
process.start()
