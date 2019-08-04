# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import copy
import json

import jieba

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from os import path


class BossJobPipeline(object):
    def __init__(self):
        self.job_items = []

    def process_item(self, item, spider):
        self.job_items.append(copy.deepcopy(dict(item)))
        return item

    def close_spider(self, spider):
        with open('job.json', 'w', encoding='utf-8') as file_pipeline:
            json.dump(self.job_items, file_pipeline, ensure_ascii=False)


class BossJobDetailPipeline:
    def __init__(self):
        self.job_items = []

    def process_item(self, item, spider):
        self.job_items.append(copy.deepcopy(item['job_detail']))
        return item

    def close_spider(self, spider):
        job_details = ''.join(self.job_items)
        self.generate_word_count(job_details)

    def generate_word_count(self, job_details: str):
        # job_details = jieba.cut(job_details)
        self.generate_image(job_details)

    @staticmethod
    def generate_image(job_details):
        d = path.dirname(__file__)
        backgroud_Image = np.array(Image.open("111.jpg"))
        # 绘制词云图
        #             mask=backgroud_Image,  # 设置背景图片
        wc = WordCloud(
            font_path='font.ttf',  # 显示中文，可以更换字体
            background_color='white',  # 背景色
            width=1200,
            height=800
            # max_words=30,  # 最大显示单词数
            # max_font_size=60  # 频率最大单词字体大小
        ).generate(job_details)
        # 传入需画词云图的文本
        image = wc.to_image()
        image.show()

