# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QutoutiaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # table_name = 'news'
    table_name = 'post'
    title = scrapy.Field()
    content = scrapy.Field()
    publish_at = scrapy.Field()
    url = scrapy.Field()
    channel = scrapy.Field()
    author = scrapy.Field()
    created_at = scrapy.Field()
    img_url = scrapy.Field()
    source = scrapy.Field()
    img_count = scrapy.Field()
    state = scrapy.Field()
    time_gap = scrapy.Field()
    read_count = scrapy.Field()
    comment_count = scrapy.Field()
    hash = scrapy.Field()




