# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy import Request
from wangyixinwen_app.items import *


class WangyiSpider(scrapy.Spider):
    name = 'wangyi'
    allowed_domains = ['163.com']
    start_urls = ['http://163.com/']


    def start_requests(self):

        url_list = [

            "http://c.m.163.com/dlist/article/dynamic?from=T1348648517839&offset=0&size=10&fn=1&LastStdTime=0&passport=&devId=Vg8bLbvy6oEHRRfKFG9BTpY0BxtRaCKaXjTsQUxCAF419v5906mDnEPZxOZtoKWIIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=&lon=&version=34.1&net=wifi&ts=1522312714&sign=sIP%2BjAuEyek4857cccm4Bqoy0h7Ce3VNMbNBctG%2BYPJ48ErR02zJ6%2FKXOnxX046I&encryption=1&canal=huawei_news&mac=racUMC0A9havm%2BHe6jH3YAvVdjgSXYDtwEDZ03eH1l8%3D&open=&openpath=",
            "http://c.m.163.com/dlist/article/dynamic?from=T1348649079062&offset=0&size=10&fn=1&LastStdTime=0&passport=&devId=Vg8bLbvy6oEHRRfKFG9BTpY0BxtRaCKaXjTsQUxCAF419v5906mDnEPZxOZtoKWIIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=&lon=&version=34.1&net=wifi&ts=1522316043&sign=Q3enlB58tnCcJT1qSaqDb5%2BvXin73x7lUUn5hdJ0r1N48ErR02zJ6%2FKXOnxX046I&encryption=1&canal=huawei_news&mac=racUMC0A9havm%2BHe6jH3YAvVdjgSXYDtwEDZ03eH1l8%3D&open=&openpath=",
            "http://c.m.163.com/dlist/article/dynamic?from=T1348648756099&offset=0&size=10&fn=1&LastStdTime=0&passport=&devId=Vg8bLbvy6oEHRRfKFG9BTpY0BxtRaCKaXjTsQUxCAF419v5906mDnEPZxOZtoKWIIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=&lon=&version=34.1&net=wifi&ts=1522316911&sign=7aC505uIKt%2FPwH7gsP4nSOioejGcjmUPlScE8y8P6%2Bd48ErR02zJ6%2FKXOnxX046I&encryption=1&canal=huawei_news&mac=racUMC0A9havm%2BHe6jH3YAvVdjgSXYDtwEDZ03eH1l8%3D&open=&openpath=",
            "http://c.m.163.com/dlist/article/dynamic?from=T1348649580692&offset=0&size=10&fn=1&LastStdTime=0&passport=&devId=Vg8bLbvy6oEHRRfKFG9BTpY0BxtRaCKaXjTsQUxCAF419v5906mDnEPZxOZtoKWIIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=&lon=&version=34.1&net=wifi&ts=1522317115&sign=wGiS0NsoXRPwejk5JMo77hLu5sOVWCQGVT1rmLXSYJ948ErR02zJ6%2FKXOnxX046I&encryption=1&canal=huawei_news&mac=racUMC0A9havm%2BHe6jH3YAvVdjgSXYDtwEDZ03eH1l8%3D&open=&openpath=",
            "http://c.m.163.com/nc/auto/districtcode/list/110000/0-20.html",
            "http://c.m.163.com/dlist/article/dynamic?from=T1348648141035&offset=0&size=10&fn=1&LastStdTime=0&passport=&devId=Vg8bLbvy6oEHRRfKFG9BTpY0BxtRaCKaXjTsQUxCAF419v5906mDnEPZxOZtoKWIIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=&lon=&version=34.1&net=wifi&ts=1522317489&sign=SgZbiPGReOgU75UnGnDmykv3F54ViUbKO8sy%2B3XRuBZ48ErR02zJ6%2FKXOnxX046I&encryption=1&canal=huawei_news&mac=racUMC0A9havm%2BHe6jH3YAvVdjgSXYDtwEDZ03eH1l8%3D&open=&openpath=",
            "http://c.m.163.com/recommend/getSubDocPic?size=10&offset=0&fn=1&LastStdTime=0&passport=&devId=Vg8bLbvy6oEHRRfKFG9BTpY0BxtRaCKaXjTsQUxCAF419v5906mDnEPZxOZtoKWIIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=&lon=&version=34.2&net=wifi&ts=1522754593&sign=Rdqexf7E7fHX4oVewGCzVuvYJlr3RcnO55oBdGSKuoR48ErR02zJ6%2FKXOnxX046I&encryption=1&canal=huawei_news&mac=racUMC0A9havm%2BHe6jH3YAvVdjgSXYDtwEDZ03eH1l8%3D&open=&openpath=",
            "http://c.m.163.com/dlist/article/dynamic?from=T1414389941036&offset=0&size=10&fn=1&LastStdTime=0&passport=&devId=Vg8bLbvy6oEHRRfKFG9BTpY0BxtRaCKaXjTsQUxCAF419v5906mDnEPZxOZtoKWIIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=&lon=&version=34.2&net=wifi&ts=1522754665&sign=bFn0nYT8xXNEVWVhEOBiv2Ghk15O1zVDEcxycBg0bxd48ErR02zJ6%2FKXOnxX046I&encryption=1&canal=huawei_news&mac=racUMC0A9havm%2BHe6jH3YAvVdjgSXYDtwEDZ03eH1l8%3D&open=&openpath=",
            "http://c.m.163.com/nc/household/city/110000/0-20.html",
            "http://c.m.163.com/dlist/article/dynamic?from=T1348650839000&offset=0&size=10&fn=2&LastStdTime=0&passport=&devId=Vg8bLbvy6oEHRRfKFG9BTpY0BxtRaCKaXjTsQUxCAF419v5906mDnEPZxOZtoKWIIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=&lon=&version=34.2&net=wifi&ts=1522755274&sign=8kmmBt6F7OB8HGvYRDA25F6QSMB61cOmTEQzHry0p6d48ErR02zJ6%2FKXOnxX046I&encryption=1&canal=huawei_news&mac=racUMC0A9havm%2BHe6jH3YAvVdjgSXYDtwEDZ03eH1l8%3D&open=&openpath=",
            "http://c.m.163.com/dlist/article/dynamic?from=T1502955728035&offset=0&size=10&fn=2&LastStdTime=0&passport=&devId=Vg8bLbvy6oEHRRfKFG9BTpY0BxtRaCKaXjTsQUxCAF419v5906mDnEPZxOZtoKWIIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=&lon=&version=34.2&net=wifi&ts=1522755313&sign=IwbXkxklYn3bQmQd37AdAq10nkhZUG4PI1o4ERidE2h48ErR02zJ6%2FKXOnxX046I&encryption=1&canal=huawei_news&mac=racUMC0A9havm%2BHe6jH3YAvVdjgSXYDtwEDZ03eH1l8%3D&open=&openpath=",
            "http://c.m.163.com/nc/article/list/T1385429690972/0-20.html",
            "http://c.m.163.com/dlist/article/dynamic?from=T1348650593803&offset=0&size=10&fn=2&LastStdTime=0&passport=&devId=Vg8bLbvy6oEHRRfKFG9BTpY0BxtRaCKaXjTsQUxCAF419v5906mDnEPZxOZtoKWIIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=&lon=&version=34.2&net=wifi&ts=1522755412&sign=Po%2Ffhl1rulfnvKZjBeat7dFNr7wHq%2B1mI7ePqnkuqSV48ErR02zJ6%2FKXOnxX046I&encryption=1&canal=huawei_news&mac=racUMC0A9havm%2BHe6jH3YAvVdjgSXYDtwEDZ03eH1l8%3D&open=&openpath=",
            "http://c.m.163.com/dlist/article/dynamic?from=T1348654204705&offset=0&size=10&fn=2&LastStdTime=0&passport=&devId=Vg8bLbvy6oEHRRfKFG9BTpY0BxtRaCKaXjTsQUxCAF419v5906mDnEPZxOZtoKWIIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=&lon=&version=34.2&net=wifi&ts=1522755494&sign=Gox12uCPpofOYr8d9FT%2BhaBqlHdn%2B7ynLWbiObNf4p148ErR02zJ6%2FKXOnxX046I&encryption=1&canal=huawei_news&mac=racUMC0A9havm%2BHe6jH3YAvVdjgSXYDtwEDZ03eH1l8%3D&open=&openpath=",
            "http://c.m.163.com/nc/article/list/T1368497029546/0-20.html",
            "http://c.m.163.com/dlist/article/dynamic?from=T1348654151579&offset=0&size=10&fn=2&LastStdTime=0&passport=&devId=Vg8bLbvy6oEHRRfKFG9BTpY0BxtRaCKaXjTsQUxCAF419v5906mDnEPZxOZtoKWIIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=&lon=&version=34.2&net=wifi&ts=1522755662&sign=T%2BJJzg05qPzA4%2F9%2F5KE2zmV7F9gJxCyZ4CSEj3cQOs948ErR02zJ6%2FKXOnxX046I&encryption=1&canal=huawei_news&mac=racUMC0A9havm%2BHe6jH3YAvVdjgSXYDtwEDZ03eH1l8%3D&open=&openpath=",

        ]

        for url in url_list:
            if url == "http://c.m.163.com/dlist/article/dynamic?from=T1348648517839&offset=0&size=10&fn=1&LastStdTime=0&passport=&devId=Vg8bLbvy6oEHRRfKFG9BTpY0BxtRaCKaXjTsQUxCAF419v5906mDnEPZxOZtoKWIIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=&lon=&version=34.1&net=wifi&ts=1522312714&sign=sIP%2BjAuEyek4857cccm4Bqoy0h7Ce3VNMbNBctG%2BYPJ48ErR02zJ6%2FKXOnxX046I&encryption=1&canal=huawei_news&mac=racUMC0A9havm%2BHe6jH3YAvVdjgSXYDtwEDZ03eH1l8%3D&open=&openpath=" :
                #娱乐
                type = 2
            if url == "http://c.m.163.com/dlist/article/dynamic?from=T1348649079062&offset=0&size=10&fn=1&LastStdTime=0&passport=&devId=Vg8bLbvy6oEHRRfKFG9BTpY0BxtRaCKaXjTsQUxCAF419v5906mDnEPZxOZtoKWIIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=&lon=&version=34.1&net=wifi&ts=1522316043&sign=Q3enlB58tnCcJT1qSaqDb5%2BvXin73x7lUUn5hdJ0r1N48ErR02zJ6%2FKXOnxX046I&encryption=1&canal=huawei_news&mac=racUMC0A9havm%2BHe6jH3YAvVdjgSXYDtwEDZ03eH1l8%3D&open=&openpath=" :
                #体育
                type = 18
            if url == "http://c.m.163.com/dlist/article/dynamic?from=T1348648756099&offset=0&size=10&fn=1&LastStdTime=0&passport=&devId=Vg8bLbvy6oEHRRfKFG9BTpY0BxtRaCKaXjTsQUxCAF419v5906mDnEPZxOZtoKWIIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=&lon=&version=34.1&net=wifi&ts=1522316911&sign=7aC505uIKt%2FPwH7gsP4nSOioejGcjmUPlScE8y8P6%2Bd48ErR02zJ6%2FKXOnxX046I&encryption=1&canal=huawei_news&mac=racUMC0A9havm%2BHe6jH3YAvVdjgSXYDtwEDZ03eH1l8%3D&open=&openpath=" :
                #财经
                # type = 10
                pass
            if url == "http://c.m.163.com/dlist/article/dynamic?from=T1348649580692&offset=0&size=10&fn=1&LastStdTime=0&passport=&devId=Vg8bLbvy6oEHRRfKFG9BTpY0BxtRaCKaXjTsQUxCAF419v5906mDnEPZxOZtoKWIIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=&lon=&version=34.1&net=wifi&ts=1522317115&sign=wGiS0NsoXRPwejk5JMo77hLu5sOVWCQGVT1rmLXSYJ948ErR02zJ6%2FKXOnxX046I&encryption=1&canal=huawei_news&mac=racUMC0A9havm%2BHe6jH3YAvVdjgSXYDtwEDZ03eH1l8%3D&open=&openpath=":
                #科技
                type = 8
            if url == "http://c.m.163.com/nc/auto/districtcode/list/110000/0-20.html":
                # 汽车
                type = 11
            if url == "http://c.m.163.com/dlist/article/dynamic?from=T1348648141035&offset=0&size=10&fn=1&LastStdTime=0&passport=&devId=Vg8bLbvy6oEHRRfKFG9BTpY0BxtRaCKaXjTsQUxCAF419v5906mDnEPZxOZtoKWIIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=&lon=&version=34.1&net=wifi&ts=1522317489&sign=SgZbiPGReOgU75UnGnDmykv3F54ViUbKO8sy%2B3XRuBZ48ErR02zJ6%2FKXOnxX046I&encryption=1&canal=huawei_news&mac=racUMC0A9havm%2BHe6jH3YAvVdjgSXYDtwEDZ03eH1l8%3D&open=&openpath=":
                # 军事
                type = 19
                # return None
            if url == "http://c.m.163.com/recommend/getSubDocPic?size=10&offset=0&fn=1&LastStdTime=0&passport=&devId=Vg8bLbvy6oEHRRfKFG9BTpY0BxtRaCKaXjTsQUxCAF419v5906mDnEPZxOZtoKWIIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=&lon=&version=34.2&net=wifi&ts=1522754593&sign=Rdqexf7E7fHX4oVewGCzVuvYJlr3RcnO55oBdGSKuoR48ErR02zJ6%2FKXOnxX046I&encryption=1&canal=huawei_news&mac=racUMC0A9havm%2BHe6jH3YAvVdjgSXYDtwEDZ03eH1l8%3D&open=&openpath=":
                # 热点
                type = 1
            if url == "http://c.m.163.com/dlist/article/dynamic?from=T1414389941036&offset=0&size=10&fn=1&LastStdTime=0&passport=&devId=Vg8bLbvy6oEHRRfKFG9BTpY0BxtRaCKaXjTsQUxCAF419v5906mDnEPZxOZtoKWIIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=&lon=&version=34.2&net=wifi&ts=1522754665&sign=bFn0nYT8xXNEVWVhEOBiv2Ghk15O1zVDEcxycBg0bxd48ErR02zJ6%2FKXOnxX046I&encryption=1&canal=huawei_news&mac=racUMC0A9havm%2BHe6jH3YAvVdjgSXYDtwEDZ03eH1l8%3D&open=&openpath=":
                # 健康
                type = 3
            if url == "http://c.m.163.com/nc/household/city/110000/0-20.html":
                # 生活
                type = 9
            if url == "http://c.m.163.com/dlist/article/dynamic?from=T1348650839000&offset=0&size=10&fn=2&LastStdTime=0&passport=&devId=Vg8bLbvy6oEHRRfKFG9BTpY0BxtRaCKaXjTsQUxCAF419v5906mDnEPZxOZtoKWIIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=&lon=&version=34.2&net=wifi&ts=1522755274&sign=8kmmBt6F7OB8HGvYRDA25F6QSMB61cOmTEQzHry0p6d48ErR02zJ6%2FKXOnxX046I&encryption=1&canal=huawei_news&mac=racUMC0A9havm%2BHe6jH3YAvVdjgSXYDtwEDZ03eH1l8%3D&open=&openpath=":
                # 情感
                type = 12
            if url == "http://c.m.163.com/dlist/article/dynamic?from=T1502955728035&offset=0&size=10&fn=2&LastStdTime=0&passport=&devId=Vg8bLbvy6oEHRRfKFG9BTpY0BxtRaCKaXjTsQUxCAF419v5906mDnEPZxOZtoKWIIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=&lon=&version=34.2&net=wifi&ts=1522755313&sign=IwbXkxklYn3bQmQd37AdAq10nkhZUG4PI1o4ERidE2h48ErR02zJ6%2FKXOnxX046I&encryption=1&canal=huawei_news&mac=racUMC0A9havm%2BHe6jH3YAvVdjgSXYDtwEDZ03eH1l8%3D&open=&openpath=":
                # 星座
                type = 13
            if url == "http://c.m.163.com/nc/article/list/T1385429690972/0-20.html":
                # 美食
                type = 14
            if url == "http://c.m.163.com/dlist/article/dynamic?from=T1348650593803&offset=0&size=10&fn=2&LastStdTime=0&passport=&devId=Vg8bLbvy6oEHRRfKFG9BTpY0BxtRaCKaXjTsQUxCAF419v5906mDnEPZxOZtoKWIIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=&lon=&version=34.2&net=wifi&ts=1522755412&sign=Po%2Ffhl1rulfnvKZjBeat7dFNr7wHq%2B1mI7ePqnkuqSV48ErR02zJ6%2FKXOnxX046I&encryption=1&canal=huawei_news&mac=racUMC0A9havm%2BHe6jH3YAvVdjgSXYDtwEDZ03eH1l8%3D&open=&openpath=":
                # 时尚
                type = 15
            if url == "http://c.m.163.com/dlist/article/dynamic?from=T1348654204705&offset=0&size=10&fn=2&LastStdTime=0&passport=&devId=Vg8bLbvy6oEHRRfKFG9BTpY0BxtRaCKaXjTsQUxCAF419v5906mDnEPZxOZtoKWIIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=&lon=&version=34.2&net=wifi&ts=1522755494&sign=Gox12uCPpofOYr8d9FT%2BhaBqlHdn%2B7ynLWbiObNf4p148ErR02zJ6%2FKXOnxX046I&encryption=1&canal=huawei_news&mac=racUMC0A9havm%2BHe6jH3YAvVdjgSXYDtwEDZ03eH1l8%3D&open=&openpath=":
                # 旅游
                type = 16
            if url == "http://c.m.163.com/nc/article/list/T1368497029546/0-20.html":
                # 历史
                type = 20
            if url == "http://c.m.163.com/dlist/article/dynamic?from=T1348654151579&offset=0&size=10&fn=2&LastStdTime=0&passport=&devId=Vg8bLbvy6oEHRRfKFG9BTpY0BxtRaCKaXjTsQUxCAF419v5906mDnEPZxOZtoKWIIIGNeE0nI41SFrBIaL1THA%3D%3D&lat=&lon=&version=34.2&net=wifi&ts=1522755662&sign=T%2BJJzg05qPzA4%2F9%2F5KE2zmV7F9gJxCyZ4CSEj3cQOs948ErR02zJ6%2FKXOnxX046I&encryption=1&canal=huawei_news&mac=racUMC0A9havm%2BHe6jH3YAvVdjgSXYDtwEDZ03eH1l8%3D&open=&openpath=":
                # 游戏
                type = 23




            yield Request(url, callback=self.parse_index, meta={'type': type}, dont_filter=True)

    def parse_index(self, response):
        type = response.meta['type']
        items = WangyixinwenAppItem()
        reg = re.compile(r'"votecount":(.*?),".*?"url_3w":"(.*?)"')
        urls = reg.findall(response.text, re.S)
        for comment_count,url in urls:
            if url:

                yield Request(url, callback=self.parse_detail, meta={'type': type, 'comment_count': comment_count}, dont_filter=True)

    def parse_detail(self, response):

        items = WangyixinwenAppItem()
        items['url'] = response.url
        items['title'] = response.xpath('//div[@id="epContentLeft"]/h1/text()').extract_first()
        items['content'] = response.xpath('//div[@id="endText"]').extract_first()
        items['date'] = response.xpath('//div[@class="post_time_source"]/text()').extract_first()
        items['type'] = response.meta['type']
        items['publisher'] = response.xpath('//a[@id="ne_article_source"]/text()').extract_first()
        items['comment_count'] = response.meta['comment_count']
        yield items

