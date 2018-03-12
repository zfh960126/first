# -*- coding: utf-8 -*-
import scrapy


class DoubanBookItem(scrapy.Item):
    table_name = 'book'
    name = scrapy.Field()            # 书名
    price = scrapy.Field()           # 价格
    edition_year = scrapy.Field()    # 出版年份
    publisher = scrapy.Field()       # 出版社
    ratings = scrapy.Field()         # 评分
    author = scrapy.Field()          # 作者
    content = scrapy.Field()
    url = scrapy.Field()

class DoubanMailItem(scrapy.Item):
    table_name = 'mail'
    sender_time = scrapy.Field()     # 发送时间
    sender_from = scrapy.Field()     # 发送人
    url = scrapy.Field()             # 豆邮详细地址
    title = scrapy.Field()           # 豆邮标题

class DoubanMovieCommentItem(scrapy.Item):
    table_name = 'book_comment'
    useful_num = scrapy.Field()      # 多少人评论有用
    no_help_num = scrapy.Field()     # 多少人评论无用
    people = scrapy.Field()          # 评论者
    people_url = scrapy.Field()      # 评论者页面
    star = scrapy.Field()            # 评分
    comment = scrapy.Field()         # 评论
    title = scrapy.Field()           # 标题
    url = scrapy.Field()# 当前页