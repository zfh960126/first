# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
import os
from crawl_taobao.items import CrawlTaobaoItem
import re
import pymongo
from scrapy import Request
from scrapy.exceptions import DropItem
import requests


class CrawlTaobaoPipeline(object):
    def process_item(self, item, spider):
        return item



class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[item.table_name].update({'id': item.get('GOODS_URL')}, {'$set': dict(item)}, True)
        return item

class XiazaitupianPipeline(object):
    def process_item(self, item, spider):
        GOODS_PIC_URL = item['GOODS_PIC_URL']
        name=item['GOODS_NAME']
        path = 'C:\\Users\\WE\\Desktop\\github\\crawl_taobao\\crawl_taobao\\picture\\' + str(name) + '.jpg'#图片存储位置
        image = requests.get(GOODS_PIC_URL)
        f = open(path, 'wb')
        f.write(image.content)
        f.close()
        print(u'正在保存图片：', GOODS_PIC_URL)

        return item