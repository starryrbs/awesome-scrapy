# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from boss_job.items import BossJobItem


class JobInfoSpider(scrapy.Spider):
    name = 'job_info'
    allowed_domains = ['zhipin.com']
    zhilian_link = 'https://www.zhipin.com'

    custom_settings = {
        'ITEM_PIPELINES': {
            'boss_job.pipelines.BossJobPipeline': 300,
        }
    }

    def start_requests(self):
        keyword = '机器学习'
        query_job_url = "https://www.zhipin.com/c101020100/?query={keyword}&page={page}&ka=page-{page}"
        for i in range(1, 10):
            url = query_job_url.format(keyword=keyword, page=i)
            yield Request(url=url)

    def parse(self, response):
        jobs = response.xpath('//div[@class="job-list"]/ul/li')
        for job in jobs:
            item = BossJobItem()
            company_name = job.xpath('div/div[@class="info-company"]/div/h3/a/text()').get()
            job_detail_detail_url = job.xpath('div/div[@class="info-primary"]/h3/a/@href').get()
            item['company_name'] = company_name
            item['job_detail_detail_url'] = self.zhilian_link + job_detail_detail_url
            yield item
