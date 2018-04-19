# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item,Field


class DongfangcaifuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    table_name = '业绩快报'
    股票代码 = Field()
    股票简称 = Field()
    每股收益 = Field()
    营业收入 = Field()
    营业收入_同比增长 = Field()
    营业收入_季度环比增长 = Field()
    净利润 = Field()
    净利润_同比增长 = Field()
    净利润_季度环比增长 = Field()
    每股净资产 = Field()
    净资产收益率 = Field()
    每股经营现金流量 = Field()
    销售毛利率 = Field()
    利润分配 = Field()
    公告日期 = Field()

class DongfangcaifuItem_yejiyugao(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    table_name = '业绩预告'
    股票代码 = Field()
    股票简称 = Field()
    业绩变动 = Field()
    业绩变动幅度 = Field()
    预告类型 = Field()
    上年同期净利润 = Field()
    公告日期  = Field()

class DongfangcaifuItem_yuyueshijian(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    table_name = '预约披露时间'
    股票代码 = Field()
    股票简称 = Field()
    首次预约时间 = Field()
    一次变更日期 = Field()
    二次变更日期 = Field()
    三次变更日期 = Field()
    实际披露时间  = Field()