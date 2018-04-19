# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy import Request
from dongfangcaifu.items import DongfangcaifuItem
from time import sleep


class EastmoneySpider(scrapy.Spider):
    name = 'eastmoney-2'
    allowed_domains = ['eastmoney.com']
    start_urls = ['http://eastmoney.com/']

    def start_requests(self):
        for i in range(0,5):
            list_url =  'http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get?type=NBJB_YJKB_N&token=70f12f2f4f091e459a279469fe49eca5&filter=(REPORTDATE=^2017-12-31^)&st=NOTICEDATE&sr=-1&p='+str(i)+'&ps=50&js=var%20ccZdvBSI={pages:(tp),data:%20(x)}&rt=50687018'
            yield Request(list_url, callback=self.parse_index,dont_filter=True)

    def parse_index(self, response):
            print(response.text)
            compile = '{"SECUCODE":"(.*?)","SECUNAME":"(.*?)","EPSJB":(.*?),"EPSKCJB":(.*?),"YS":(.*?),"YSTZ":(.*?),"YSHZ":(.*?),"SJL":(.*?),"SJLTZ":(.*?),"SJLHZ":(.*?),"BPS":(.*?),"ROEPJ":(.*?),"MGXJJE":(.*?),"XSMLL":(.*?),"LRFP":"(.*?)","GXL":(.*?),"NOTICEDATE":"(.*?)","REPORTDATE":"(.*?)","TYPE":"(.*?)","COMPANYCODE":"(.*?)"}'
            s = re.findall(compile,response.text)
            dongfang_item = DongfangcaifuItem()
            for i in s:
                print(i)
                dongfang_item['股票代码'] = i[0]
                dongfang_item['股票简称'] = i[1]
                dongfang_item['每股收益'] = i[2]
                dongfang_item['营业收入'] = i[4]
                dongfang_item['营业收入_同比增长'] = i[5]
                dongfang_item['营业收入_季度环比增长'] = i[6]
                dongfang_item['净利润'] = i[7]
                dongfang_item['净利润_同比增长'] = i[8]
                dongfang_item['净利润_季度环比增长'] = i[9]
                dongfang_item['每股净资产'] = i[10]
                dongfang_item['净资产收益率'] = i[11]
                dongfang_item['每股经营现金流量'] = i[12]
                dongfang_item['销售毛利率'] = i[13]
                dongfang_item['利润分配'] = i[14]
                dongfang_item['公告日期'] = i[16]

                yield dongfang_item