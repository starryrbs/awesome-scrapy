# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class BossJobItem(scrapy.Item):
    company_name = Field()
    job_detail_detail_url = Field()


class BossJobDetailItem(scrapy.Item):
    company_name = Field()
    job_detail = Field()
