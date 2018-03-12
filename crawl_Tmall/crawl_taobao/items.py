# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from crawl_taobao.settings import TABLE_NAME

class CrawlTaobaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    table_name = TABLE_NAME
    GOODS_PRICE=scrapy.Field()
    GOODS_URL = scrapy.Field()
    GOODS_NAME = scrapy.Field()
    SHOP_NAME = scrapy.Field()
    SHOP_URL = scrapy.Field()
    COMPANY_ADRESS = scrapy.Field()
    GOODS_PIC_URL = scrapy.Field()
