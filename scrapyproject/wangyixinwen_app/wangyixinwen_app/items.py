# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WangyixinwenAppItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    table_name = 'wangyi'
    title = scrapy.Field()
    content = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()
    type = scrapy.Field()
    publisher = scrapy.Field()
    comment_count = scrapy.Field()
    type = scrapy.Field()
    now_time = scrapy.Field()
    img_url = scrapy.Field()
    source = scrapy.Field()
    img_url_num = scrapy.Field()
    news_count = scrapy.Field()
    statue = scrapy.Field()
    read_count = scrapy.Field()