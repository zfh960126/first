# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy import Request
from dongfangcaifu.items import DongfangcaifuItem_yuyueshijian
from time import sleep


class EastmoneySpider(scrapy.Spider):
    name = 'eastmoney-4'
    allowed_domains = ['eastmoney.com']
    start_urls = ['http://eastmoney.com/']






    def start_requests(self):
        for i in range(0,5):
            list_url =  'http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get?type=NBJB_YYSJ_N&token=70f12f2f4f091e459a279469fe49eca5&st=FRDATE&sr=1&p='+str(i)+'&ps=50&js=var%20buvpoDBy={pages:(tp),data:%20(x)}&filter=(REPORTDATE=^2017-12-31^)&rt=50688989'
            yield Request(list_url, callback=self.parse_index,dont_filter=True)

    def parse_index(self, response):
            print(response.text)
            compile = '{"SECUCODE":"(.*?)","SECUNAME":"(.*?)","FRDATE":"(.*?)","FCDATE":"(.*?)","SCDATE":"(.*?)","TCDATE":"(.*?)","RADATE":"(.*?)","REPORTDATE":"(.*?)","STAT":"(.*?)"}'
            s = re.findall(compile,response.text)
            dongfang_item = DongfangcaifuItem_yuyueshijian()
            for i in s:

                dongfang_item['股票代码'] = i[0]
                dongfang_item['股票简称'] = i[1]
                dongfang_item['首次预约时间'] = i[2]
                dongfang_item['一次变更日期'] = i[3]
                dongfang_item['二次变更日期'] = i[4]
                dongfang_item['三次变更日期'] = i[5]
                dongfang_item['实际披露时间'] = i[6]


                yield dongfang_item