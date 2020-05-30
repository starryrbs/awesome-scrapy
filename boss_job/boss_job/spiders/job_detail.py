# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy.http import Request

from boss_job.items import BossJobDetailItem


class JobDetailSpider(scrapy.Spider):
    name = 'job_detail'
    allowed_domains = ['zhipin.com']
    start_urls = ['http://zhipin.com/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'boss_job.pipelines.BossJobDetailPipeline': 300,
        }
    }

    def start_requests(self):
        jobs = self.get_job_url()
        for job in jobs:
            yield Request(job['job_detail_detail_url'])

    @staticmethod
    def get_job_url():
        with open('job.json', 'r', encoding='utf-8') as file_pipeline:
            return json.load(file_pipeline)

    def parse(self, response):
        item = BossJobDetailItem()
        job_detail = response.xpath('string(//div[@class="detail-content"]//div[@class="text"])').get(
            default='').replace('\n', '').replace(' ', '')
        company_name = response.xpath('//div[@class="job-sec"]/div[@class="name"]/text()').get(default='')
        item['job_detail'] = job_detail
        item['company_name'] = company_name
        yield item
