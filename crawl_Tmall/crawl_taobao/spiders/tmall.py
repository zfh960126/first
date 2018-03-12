# -*- coding: utf-8 -*-
import scrapy
from crawl_taobao.items import CrawlTaobaoItem
import re
MAX_PAGE = 2
class TmallSpider(scrapy.Spider):
    name = 'tmall'
    count = 0
    start_urls = ['https://list.tmall.com/']

    def start_requests(self):
        for i in range(1,MAX_PAGE):
            list_url ='https://list.tmall.com/search_product.htm?&cat=50025135&s='+str(60*i)+'&industryCatId=50025135'

            yield scrapy.Request(list_url, callback=self.parse,dont_filter=True)



    def parse(self, response):

        TmallSpider.count+=1
        divs=response.xpath('//div[@class="view  "]/div[@class="product  "]/div[@class="product-iWrap"]')
        if not divs:
            self.log("List Page error--%s" %response.url)

        for div in divs:
            item=CrawlTaobaoItem()
            item['GOODS_PRICE']=div.xpath('p[@class="productPrice"]/em/@title').extract_first()
            item['GOODS_NAME']=div.xpath("p[@class='productTitle']/a/@title").extract_first()
            pre_goods_url=div.xpath("p[@class='productTitle']/a/@href").extract_first()

            item['GOODS_URL'] = pre_goods_url if "https:" in pre_goods_url else("https:"+pre_goods_url)


            item['GOODS_PIC_URL'] ="https:"+re.findall('<img data-ks-lazyload="(.*?)"',div.extract(),re.S)[0]


            yield scrapy.Request(url=item['GOODS_URL'],meta={'item':item},dont_filter=True,callback=self.parse_detail,)

    def parse_detail(self,response):
                item  = response.meta['item']

                item['SHOP_NAME'] = re.findall('<input type="hidden" name="seller_nickname" value="(.*?)"',response.text,re.S)[0]
                item['SHOP_URL'] ="https:"+re.findall('<a class="slogo-shopname" href="(.*?)"',response.text,re.S)[0]
                item['COMPANY_ADRESS'] = re.findall('<input type="hidden" name="region" value="(.*?)"',response.text,re.S)[0]

                yield item



