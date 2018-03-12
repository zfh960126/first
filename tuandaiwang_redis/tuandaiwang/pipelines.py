# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
import os
from tuandaiwang.items import TWDItem
import re
import pymongo
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class TuandaiwangPipeline(object):


    def process_item(self, item, spider):
        if isinstance(item, TWDItem):
            if item.get('repay_way'):
                #去掉所有<>形式的
                item['repay_way'] = re.split(r'<.*?>',item.get('repay_way'))
                repay_way  = ''
                for s in item['repay_way']:
                    if s=='\n' or s =='\s' or s =='结清方式：':
                        pass
                    else:
                        repay_way+=s
                item['repay_way'] =repay_way
                investor_list = []
            if item.get('inverestments'):
                    for investor in item.get('inverestments'):
                        investor ='\"investor\":'+ investor
                        investor = re.sub(r'\"TenderMode\":(.*?),\"AddDate\"','"day"',investor)
                        investor_list.append(investor)
                    item['inverestments'] = investor_list

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
        self.db[item.table_name].update({'id': item.get('id')}, {'$set': dict(item)}, True)
        return item
