from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from boss_job.spiders.job_info import JobInfoSpider

process = CrawlerProcess(settings=get_project_settings())  # 括号中可以添加参数
process.crawl(JobInfoSpider)
process.start()
