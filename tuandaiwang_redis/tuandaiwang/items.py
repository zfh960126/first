# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import sys
import os
import scrapy
from scrapy import Item,Field
from tuandaiwang.settings import TABLE_NAME

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class TWDItem(Item):
        table_name = TABLE_NAME
        id  =  Field()
        title =  Field()
        amount = Field()
        rate = Field()
        period = Field()
        progress = Field()
        repay_way = Field()
        url = Field()
        compile_day = Field()
        auther = Field()
        inverestments = Field()
