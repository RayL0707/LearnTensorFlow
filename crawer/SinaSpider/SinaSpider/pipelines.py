# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time

class SinaspiderPipeline(object):
    def __init__(self):
        self.start = time.time()
    def process_item(self, item, spider):
        return item

    def open_spider(self, spider):
        print("==================开启爬虫 \""+spider.name+"\" ==================")

    def close_spider(self, spider):
        print("==================关闭爬虫 \""+spider.name+"\" ==================")
