# -*- coding: utf-8 -*-
import re
from scrapy import Request
from qutoutiao.items import *


class ToutiaoSpider(scrapy.Spider):
    name = 'toutiao'
    allowed_domains = ["qktoutiao.com"]
    start_urls = ['http://qutoutiao/']

    def start_requests(self):
            url_list = [

                    "http://api.1sapp.com/content/outList?cid=27&tn=1&page=1&limit=100",
                    "http://api.1sapp.com/content/outList?cid=13&tn=1&page=1&limit=100",
                    "http://api.1sapp.com/content/outList?cid=42&tn=1&page=1&limit=100",
                    "http://api.1sapp.com/content/outList?cid=5&tn=1&page=1&limit=100",
                    "http://api.1sapp.com/content/outList?cid=15&tn=1&page=1&limit=100",
                    "http://api.1sapp.com/content/outList?cid=4&tn=1&page=1&limit=100",
                    "http://api.1sapp.com/content/outList?cid=23&tn=1&page=1&limit=100",
                    "http://api.1sapp.com/content/outList?cid=3&tn=1&page=1&limit=100",
                    "http://api.1sapp.com/content/outList?cid=6&tn=1&page=1&limit=100",
                    "http://api.1sapp.com/content/outList?cid=11&tn=1&page=1&limit=100",
                    "http://api.1sapp.com/content/outList?cid=2&tn=1&page=1&limit=100",
                    "http://api.1sapp.com/content/outList?cid=29&tn=1&page=1&limit=100",
                    "http://api.1sapp.com/content/outList?cid=16&tn=1&page=1&limit=100",
                    "http://api.1sapp.com/content/outList?cid=14&tn=1&page=1&limit=100",
                    "http://api.1sapp.com/content/outList?cid=18&tn=1&page=1&limit=100",
                    "http://api.1sapp.com/content/outList?cid=9&tn=1&page=1&limit=100",
                    "http://api.1sapp.com/content/outList?cid=19&tn=1&page=1&limit=100",
                    "http://api.1sapp.com/content/outList?cid=1&tn=1&page=1&limit=100",
                    "http://api.1sapp.com/content/outList?cid=8&tn=1&page=1&limit=100",
                    "http://api.1sapp.com/content/outList?cid=7&tn=1&page=1&limit=100",
                    "http://api.1sapp.com/content/outList?cid=12&tn=1&page=1&limit=100",
                    "http://api.1sapp.com/content/outList?cid=17&tn=1&page=1&limit=100",
                    "http://api.1sapp.com/content/outList?cid=10&tn=1&page=1&limit=100",

            ]
            channel = 0
            for url in url_list:
                if url == "http://api.1sapp.com/content/outList?cid=27&tn=1&page=1&limit=100":
                    #sannong
                    channel = 21
                if url == "http://api.1sapp.com/content/outList?cid=13&tn=1&page=1&limit=100":
                    #tiyu
                    channel = 18
                if url == "http://api.1sapp.com/content/outList?cid=42&tn=1&page=1&limit=100":
                    #jinakang
                    channel = 3
                if url == "http://api.1sapp.com/content/outList?cid=5&tn=1&page=1&limit=100":
                    #yangsheng
                    channel = 4
                if url == "http://api.1sapp.com/content/outList?cid=15&tn=1&page=1&limit=100":
                    #junshi
                    channel = 19
                if url == "http://api.1sapp.com/content/outList?cid=4&tn=1&page=1&limit=100":
                    #lizhi
                    channel = 7
                if url == "http://api.1sapp.com/content/outList?cid=23&tn=1&page=1&limit=100":
                    #lishi
                    channel = 20
                if url == "http://api.1sapp.com/content/outList?cid=3&tn=1&page=1&limit=100":
                    #qiwen
                    channel = 6
                if url == "http://api.1sapp.com/content/outList?cid=6&tn=1&page=1&limit=100":
                    #yule
                    channel = 2
                if url == "http://api.1sapp.com/content/outList?cid=11&tn=1&page=1&limit=100":
                    #qinggan
                    channel = 12
                if url == "http://api.1sapp.com/content/outList?cid=2&tn=1&page=1&limit=100":
                    #gaoxiao
                    channel = 5
                if url == "http://api.1sapp.com/content/outList?cid=29&tn=1&page=1&limit=100":
                    #lvxing
                    channel = 22
                if url == "http://api.1sapp.com/content/outList?cid=16&tn=1&page=1&limit=100":
                    #sannong
                    channel = 16
                if url == "http://api.1sapp.com/content/outList?cid=14&tn=1&page=1&limit=100":
                    #shishang
                    channel = 15
                if url == "http://api.1sapp.com/content/outList?cid=18&tn=1&page=1&limit=100":
                    #xingzuo
                    channel = 13
                if url == "http://api.1sapp.com/content/outList?cid=9&tn=1&page=1&limit=100":
                    #qiche
                    channel = 11
                if url == "http://api.1sapp.com/content/outList?cid=19&tn=1&page=1&limit=100":
                    #youxi
                    channel = 23
                if url == "http://api.1sapp.com/content/outList?cid=1&tn=1&page=1&limit=100":
                    #redian
                    channel = 1
                if url == "http://api.1sapp.com/content/outList?cid=8&tn=1&page=1&limit=100":
                    #shenghuo
                    channel = 9
                if url == "http://api.1sapp.com/content/outList?cid=7&tn=1&page=1&limit=100":
                    #keji
                    channel = 8
                if url == "http://api.1sapp.com/content/outList?cid=12&tn=1&page=1&limit=100":
                    #meishi
                    channel = 14
                if url ==  "http://api.1sapp.com/content/outList?cid=17&tn=1&page=1&limit=100":
                    #yuer
                    channel = 17
                if url == "http://api.1sapp.com/content/outList?cid=10&tn=1&page=1&limit=100":
                    #caijin
                    channel = 10

                yield Request(url, callback=self.parse_index, meta={'channel': channel}, dont_filter=False)

    def parse_index(self, response):
            channel = response.meta['channel']
            reg = re.compile(r'"url":"(.*?)"')
            urls = reg.findall(response.text, re.S)
            for key in urls:
                url = key.replace('\\', '')
                url = re.sub(r"key=.*", '', url)
                yield Request(url, meta={'channel': channel}, callback=self.parse_detail, dont_filter=False)

    def parse_detail(self, response):
            items = QutoutiaoItem()
            items['url'] = response.url
            items['title'] = response.xpath('//div[@class="article"]/h1/text()').extract_first()
            items['content'] = response.xpath('//div[@class="content"]').extract_first()
            items['publish_at'] = response.xpath('//div[@class="article"]/div/text()').extract_first()
            items['channel'] = response.meta['channel']
            items['author'] = items['publish_at']

            yield items
