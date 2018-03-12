# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy import Request
from dongfangcaifu.items import DongfangcaifuItem_yejiyugao
from time import sleep


class EastmoneySpider(scrapy.Spider):
    name = 'eastmoney-3'
    allowed_domains = ['eastmoney.com']
    start_urls = ['http://eastmoney.com/']






    def start_requests(self):
        for i in range(0,100):
            list_url =  'http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get?type=NBJB_YJYB_N&token=70f12f2f4f091e459a279469fe49eca5&st=RANGEAVG&sr=-1&p='+str(i)+'&ps=50&js=var%20XjVsjmIv={pages:(tp),data:%20(x)}&filter=(REPORTDATE=^2017-12-31^)&rt=50688865'
            yield Request(list_url, callback=self.parse_index,dont_filter=True)

    def parse_index(self, response):
            print(response.text)
            compile = '{"SECUCODE":"(.*?)","SECUNAME":"(.*?)","REPORTDATE":"(.*?)","CONTENT":"(.*?)","RANGE":"(.*?)","FORCASTTYPE":"(.*?)","NETPPROFIT":(.*?),"NOTICEDATE":"(.*?)","MARKS":"(.*?)","(.*?)":"(.*?)","RANGEAVG":(.*?)}'
            s = re.findall(compile,response.text)
            dongfang_item = DongfangcaifuItem_yejiyugao()
            for i in s:

                dongfang_item['股票代码'] = i[0]
                dongfang_item['股票简称'] = i[1]
                dongfang_item['业绩变动'] = i[3]
                dongfang_item['业绩变动幅度'] = i[4]
                dongfang_item['预告类型'] = i[5]
                dongfang_item['上年同期净利润'] = i[6]
                dongfang_item['公告日期'] = i[7]


                yield dongfang_item