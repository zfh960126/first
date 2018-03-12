# -*- coding: utf-8 -*-

import sys
import os
import scrapy
from scrapy import Request
import re
from tuandaiwang.items import TWDItem
from settings import MAX_PAGE
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from scrapy_redis.spiders import RedisCrawlSpider


sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class TdwSpider(RedisCrawlSpider):
    name = 'tdw'
    allowed_domains = ['tdw.com']
    redis_key = "tdw:start_urls"
    max_page = MAX_PAGE


    def start_requests(self):
        for i in range(1,self.max_page):
            list_url =  'https://www.tuandai.com/pages/zSharePlan/getZXList?RepaymentTypeId=0&beginRate=0&endDeadLine=0&endRate=0&orderby=0&pageindex='+str(i)+'&pagesize=5&rate=0&startDeadLine=0&status=2&strkey=&type=1&unitEnd=0&unitStart=0'

            yield Request(list_url, callback=self.parse_index)

    def parse_index(self, response):

            reg = re.compile(r'detail.aspx\?id=(.*?)\\')
            urls = reg.findall(response.text,re.S)
            for url in urls:
                id = url
                url = 'https://www.tuandai.com/pages/invest/zx_detail.aspx?id='+str(id)
                yield Request(url, callback=self.parse_detail)


    def parse_detail(self,response):

        url = response.url
        id= re.search('.*?zx_detail.aspx\?id=(.*?)$', response.url).group(1)#$
        title = response.xpath('//a[@style="text-decoration: none;"]//text()').extract_first()
        amount = response.xpath('//body/div[3]/div[1]/div/div[3]/div[3]/span/text()').extract_first()
        rate = response.xpath('//body/div[3]/div[1]/div/div[3]/div[1]/span/text()').extract_first()
        period = response.xpath('//div[@class="bid_inf_rate c_484848"]//span[@class="c-666 f36"]//text()').extract_first()
        progress = response.xpath('//dl[@class="bid_progress_bar inline-block-debug"]//dt//text()').extract_first()
        repay_way = response.xpath('/html/body/div[3]/div[1]/div/ul/li[3]').extract_first()
        # compile_day = re.search('.*?完成时间：</span>(.*?)<br.*?', response.text,re.S).group(1)#$
        compile_day = response.xpath('/html/body/div[3]/div[2]/div/p[2]').re_first(r"(\d{4}-\d{1,2}-\d{1,2})")
        auther_id = re.search('var borrowUserId = "(.*?)"', response.text).group(1)#$
        auther_url = 'https://www.tuandai.com/pages/invest/getBorrowUserNickName?borrowUserId='+ auther_id
        auther_html = requests.get(auther_url)
        auther = re.search('"NickName":"(.*?)"}', auther_html.text).group(1)#$
        inventor_url = 'https://www.tuandai.com/pages/invest/getSubscribePageListZX?pageIndex=1&pageSize=1000&projectId='+str(id)
        yield Request(inventor_url, callback=self.parse_inventor,
                      meta={'key1':id,'key2':url,'key3':amount,'key4':title,'key5':rate,'key6':period,'key7':progress,'key8':
                      repay_way, 'key9': compile_day, 'key10': auther,})
    def parse_inventor(self, response):
            inverestments = re.findall(r'{"NickName":"(.*?)"}', response.text)
            print()
            twd_item = TWDItem()
            twd_item['id'] = response.meta['key1']
            twd_item['url'] = response.meta['key2']
            twd_item['amount'] = response.meta['key3']
            twd_item['title'] = response.meta['key4']
            twd_item['rate'] = response.meta['key5']
            twd_item['period'] = response.meta['key6']
            twd_item['progress'] = response.meta['key7']
            twd_item['repay_way'] = response.meta['key8']
            twd_item['compile_day'] = response.meta['key9']
            twd_item['auther'] = response.meta['key10']
            twd_item['inverestments'] = inverestments
            yield twd_item
