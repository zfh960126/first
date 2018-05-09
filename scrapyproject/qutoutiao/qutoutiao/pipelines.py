# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
import re
import pymongo
import simhash
from simhash import Simhash

class QutoutiaoPipeline(object):
    def process_item(self, item, spider):
        if item.get('content') and item.get('publish_at'):
            item['content'] = re.sub(r'</?[^/?(img)(/p)][^><]*>', "", item.get('content'))
            # item['content'] = item['content'].replace("</p>", "\n")
            item['content'] = re.sub(r'<img data-src', "<img src", item['content'])
            item['content'] = re.sub(r'<p.*?>', "<p>", item['content'])
            item['content'] = item['content'].replace("<p></p>", "")
            # item['content'] = item['content'].replace("<p>", "")

            simhash_content = re.sub(r'<.*?>', "", item['content'])
            hash = Simhash(simhash_content).value
            item['hash'] = str(hash)

            item['author'] = item.get('publish_at').split(" ")[2]
            item['publish_at'] = " ".join(item.get('publish_at').split(" ")[0:2])
            item['publish_at'] = ":".join(item['publish_at'].split(":")[0:2])
            item['publish_at'] = datetime.datetime.strptime(item['publish_at'], "%Y-%m-%d %H:%M") - \
                                 datetime.timedelta(hours=8)

            # item['created_at'] = time.strftime("%Y-%m-%d %H:%M:%S")
            item['created_at'] = datetime.datetime.utcnow()

            content = re.sub(r'<img data-src', "<img src", item.get('content'))
            # item['img_url'] = re.findall('<img data-src="(.*?)"',item.get('content'))
            item['img_url'] = re.findall('<img src="(.*?)"', content)
            item['img_url'] = item['img_url'][0:3]

            item['source'] = "趣头条"
            item['state'] = 0
            item['read_count'] = ""
            item['comment_count'] = ""

            time_gap = item['created_at'] - item['publish_at']
            if time_gap.days != 0:
                item['time_gap'].days = str(time_gap.day) + "天"
            if time_gap.seconds > 3600:
                hours = int(time_gap.seconds / 3600)
                min = int(time_gap.seconds % 3600 / 60)
                item['time_gap'] = str(hours) + "小时" + str(min) + "分钟"
            if time_gap.seconds <= 3600:
                item['time_gap'] = str(int(time_gap.seconds / 60)) + "分钟"

            if len(item['img_url']) == 0:
                item['img_count'] = 0
            if len(item['img_url']) == 1:
                item['img_count'] = 1
            if len(item['img_url']) == 2:
                item['img_count'] = 1
                item['img_url'] = item['img_url'][0]
            if len(item['img_url']) == 3:
                item['img_count'] = 3

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
        self.db["post_id"].update({'id': "post_id"}, {'$inc': {'post_id': 1}}, True)
        post_id = self.db["post_id"].find_one()['post_id']

        hashs = self.db[item.table_name].find({},{"hash" : 1,"_id":0})

        for hash in list(hashs):

            if distance_(int(item.get('hash')),int(hash['hash'])) <10:

                print(item.get('title'))
                return item

        data = dict(item)
        data['post_id'] = post_id
        self.db[item.table_name].update({'title': data['title'], 'source': item.get('source')}, {'$set': data},
                                        True)
        return item





def distance_(t1, t2):
    n = t1^ t2
    i = 0
    while n:
        n &= (n - 1)
        i += 1
    return i