# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import pymongo
import datetime


class WangyixinwenAppPipeline(object):
    def process_item(self, item, spider):
        # if isinstance(item, QutoutiaoItem):
            if not item.get('content'):
                return None
            if item.get('content'):
                item['content'] = re.sub(r'</?[^/?(img)(/p)][^><]*>', "", item.get('content'))
                item['content'] = re.sub(r'<p.*?>', "", item['content'])
                # item['content'] = item['content'].replace("</p>", "\n").strip()
                item['content'] = re.sub(r'</p>', "\n", item['content']).strip()
                # item['content'] = re.sub(r'\s', "", item['content'])
                item['date'] = item.get('date').replace("\u3000来源:","")
                item['date'] = " ".join(item['date'].strip().split(" ")[0:2])
                item['date'] = datetime.datetime.strptime(item['date'], "%Y-%m-%d %H:%M:%S")
                item['now_time'] = datetime.datetime.now()
                item['img_url'] = re.findall('src="(.*?)"', item.get('content'))
                item['img_url'] = item['img_url'][0:3]
                item['source'] = "网易新闻_app"
                item['statue'] = 0
                item['read_count'] = 10
                article = re.sub(r'<.*?>', "", item['content']).strip()
                print(re.sub(r'\s', "", article))
                item['news_count'] =len(re.sub(r'\s', "", article))
                if len(item['img_url']) == 0:
                    item['img_url_num'] = 0
                if len(item['img_url']) == 1:
                    item['img_url_num'] = 1
                if len(item['img_url']) == 2:
                    item['img_url_num'] = 1
                    item['img_url'] = item['img_url'][0]
                if len(item['img_url']) == 3:
                     item['img_url_num'] = 3

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
        # self.db.my_collection.create_index("title")


    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # m = hashlib.md5()
        # m.update(item.get('url').encode("utf-8"))
        # id = m.hexdigest()
        self.db.my_collection.create_index("title")
        self.db["news_id"].update({'id': "news_id"}, {'$inc': {'news_id': 1}}, True)
        news_id = self.db["news_id"].find_one()['news_id']
        dic_item = dict(item)
        dic_item['news_id'] = news_id
        self.db[item.table_name].update({'title':item.get('title')},{'$set': dic_item}, True)
        return item